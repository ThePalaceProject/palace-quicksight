import json
import os
from typing import List

from botocore.exceptions import ClientError

from core.operation.baseoperation import (
    DATA_SET_DIR,
    DATA_SET_REFRESH_PROPS_SUFFIX,
    TEMPLATE_DIR,
    BaseOperation,
    TemplateResponse,
)
from core.util import recursively_replace_value, retry


class ExportAnalysisOperation(BaseOperation):
    """
    Exports a Quicksight Analysis and all it's dependencies to json files on disk
    """

    def __init__(self, analysis_id: str, output_dir: str, *args, **kwargs):
        self._analysis_id = analysis_id
        self._output_dir = output_dir
        super().__init__(*args, **kwargs)

    def execute(self) -> dict:
        os.makedirs(self._resolve_path(self._output_dir, TEMPLATE_DIR), exist_ok=True)
        os.makedirs(self._resolve_path(self._output_dir, DATA_SET_DIR), exist_ok=True)

        # retrieve description
        analysis_description = self._qs_client.describe_analysis(
            AwsAccountId=self._aws_account_id, AnalysisId=self._analysis_id
        )
        # check that analysis exists
        https_status = analysis_description["ResponseMetadata"]["HTTPStatusCode"]

        if https_status != 200:
            message = (
                f"Unexpected response from describe_analysis request: {https_status}"
            )
            self._log.error(message)
            raise Exception(message)

        # retrieve definition
        analysis_definition = self._qs_client.describe_analysis_definition(
            AwsAccountId=self._aws_account_id, AnalysisId=self._analysis_id
        )

        # extract DataSet references
        analysis = analysis_description["Analysis"]
        data_set_identifier_declarations = analysis_definition["Definition"][
            "DataSetIdentifierDeclarations"
        ]

        data_set_references = []
        for did in data_set_identifier_declarations:
            data_set_references.append(
                {
                    "DataSetPlaceholder": did["Identifier"],
                    "DataSetArn": did["DataSetArn"],
                }
            )

        # create a template from the analysis
        template_response = self._create_or_update_template_from_analysis(
            analysis=analysis, data_set_references=data_set_references
        )

        def verify_success() -> bool:
            self._template_definition = self._get_template_definition(
                template_id=template_response.template_id
            )

            return "SUCCESSFUL" in self._template_definition["ResourceStatus"]

        retry(verify_success)

        # get the newly created template definition
        self._log.info(f"Writing template definition response to disk")
        files_to_update = []
        map_to_save = {}
        # retain only the fields we will need to restore the state.
        for i in ["Name", "Definition", "TemplateId"]:
            map_to_save[i] = self._template_definition[i]

        # save the template as json file
        definition_json_str = json.dumps(map_to_save, indent=4, default=str)
        template_file_path = self._resolve_path(
            self._output_dir, TEMPLATE_DIR, self._template_definition["Name"] + ".json"
        )
        with open(template_file_path, "w") as template_file:
            template_file.write(definition_json_str)

        files_to_update.append(template_file_path)

        # for each dataset declaration identifiers
        for di in data_set_identifier_declarations:
            identifier = di["Identifier"]
            arn = di["DataSetArn"]
            data_set_id = arn.split("dataset/", 1)[1]
            # save data set definition to json file
            ds_file = self._save_dataset_to_file(data_set_id, identifier)
            files_to_update.append(ds_file)
            ds_refresh_props_file = self._save_dataset_refresh_props_to_file(
                data_set_id, identifier
            )
            if ds_refresh_props_file:
                files_to_update.append(ds_refresh_props_file)
                ds_refresh_schedules_file = (
                    self._save_dataset_refresh_schedules_to_file(
                        data_set_id, identifier
                    )
                )
                if ds_refresh_schedules_file:
                    files_to_update.append(ds_refresh_props_file)

        return {"status": "success", "files_exported": files_to_update}

    def _create_or_update_template_from_analysis(
        self, analysis, data_set_references: List
    ) -> TemplateResponse:
        template_name = analysis["Name"]
        params = {
            "AwsAccountId": self._aws_account_id,
            "TemplateId": template_name + "-template",
            "Name": analysis["Name"],
            "SourceEntity": {
                "SourceAnalysis": {
                    "Arn": analysis["Arn"],
                    "DataSetReferences": data_set_references,
                },
            },
        }
        return self._recreate_template(template_data=params)

    def _save_dataset_to_file(
        self, data_set_id: str, logical_data_set_name: str
    ) -> str:
        """
        :return: The path of the dataset file
        """

        ds_def_elements_to_save = self._describe_data_set(data_set_id)
        # remove the following fields from the response before saving it.
        for i in ["Arn", "DataSetId", "CreatedTime", "LastUpdatedTime"]:
            ds_def_elements_to_save.pop(i)

        # align the data set name with the identifier
        ds_def_elements_to_save["Name"] = logical_data_set_name
        # remove the datasource arn since this will need to be overridden
        recursively_replace_value(ds_def_elements_to_save, "DataSourceArn", "")
        # save what is left to disk
        ds_def_str = json.dumps(ds_def_elements_to_save, indent=4)
        dataset_file_path = self._resolve_path(
            self._output_dir, DATA_SET_DIR, logical_data_set_name + ".json"
        )

        with open(dataset_file_path, "w") as dataset_file:
            dataset_file.write(ds_def_str)

        return dataset_file_path

    def _save_dataset_refresh_props_to_file(
        self, data_set_id: str, logical_data_set_name: str
    ) -> str | None:
        # get data set refresh props
        try:
            response = self._qs_client.describe_data_set_refresh_properties(
                AwsAccountId=self._aws_account_id, DataSetId=data_set_id
            )
            data_set_refresh_props = response["DataSetRefreshProperties"]
            data_set_refresh_props_str = json.dumps(data_set_refresh_props, indent=4)
            file_path = self._resolve_path(
                self._output_dir,
                DATA_SET_DIR,
                logical_data_set_name + DATA_SET_REFRESH_PROPS_SUFFIX + ".json",
            )

            with open(file_path, "w") as props_file:
                props_file.write(data_set_refresh_props_str)

            return file_path
        except ClientError as e:
            # If the refresh properties don't exist an InvalidParameterException is thrown
            # rather than ResourceNotFoundException as I would have expected. Having a generic catch all here is
            # probably sufficient.
            return None

    def _save_dataset_refresh_schedules_to_file(
        self, data_set_id: str, logical_data_set_name: str
    ) -> str | None:
        try:
            response = self._qs_client.list_refresh_schedules(
                AwsAccountId=self._aws_account_id, DataSetId=data_set_id
            )
            refresh_schedules = response["RefreshSchedules"]
            # remove account specific info
            for schedule in refresh_schedules:
                for prop in ["ScheduleId", "StartAfterDateTime", "Arn"]:
                    del schedule[prop]

            data_set_refresh_schedules = {"RefreshSchedules": refresh_schedules}

            file_path = self._resolve_path(
                self._output_dir,
                DATA_SET_DIR,
                self._resolve_schedules_filename(logical_data_set_name),
            )

            with open(file_path, "w") as schedules_file:
                data_set_refresh_schedules_str = json.dumps(
                    data_set_refresh_schedules, indent=4, default=str
                )
                schedules_file.write(data_set_refresh_schedules_str)
            return file_path

        except self._qs_client.exceptions.ResourceNotFoundException as e:
            return None
