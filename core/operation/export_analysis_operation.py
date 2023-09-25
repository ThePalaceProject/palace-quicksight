import json
import os
from typing import List

from core.operation.baseoperation import (
    DATA_SET_DIR,
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
            self._log.error(
                f"Unexpected response from describe_analysis request: {https_status}"
            )
            return

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
        definition_json_str = json.dumps(map_to_save, indent=4)
        template_file_path = self._resolve_path(
            self._output_dir, TEMPLATE_DIR, self._template_definition["Name"] + ".json"
        )
        with open(template_file_path, "w") as template_file:
            template_file.write(definition_json_str)

        files_to_update.append(template_file_path)

        # for each dataset declaration identifiers
        for di in data_set_identifier_declarations:
            # save to json file
            ds_file = self._save_dataset_to_file(di=di)
            files_to_update.append(ds_file)

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
        return self._create_or_update_template(template_data=params)

    def _save_dataset_to_file(self, di) -> str:
        """

        :param di: dataset map
        :return: The path of the dataset file
        """
        identifier = di["Identifier"]
        arn = di["DataSetArn"]
        dataset_id = arn.split("dataset/", 1)[1]
        ds_def_elements_to_save = self._describe_data_set(dataset_id)
        # remove the following fields from the response before saving it.
        for i in ["Arn", "DataSetId", "CreatedTime", "LastUpdatedTime"]:
            ds_def_elements_to_save.pop(i)

        # align the data set name with the identifier
        ds_def_elements_to_save["Name"] = identifier
        # remove the datasource arn since this will need to be overridden
        recursively_replace_value(ds_def_elements_to_save, "DataSourceArn", "")
        # save what is left to disk
        ds_def_str = json.dumps(ds_def_elements_to_save, indent=4)
        dataset_file_path = self._resolve_path(
            self._output_dir, DATA_SET_DIR, identifier + ".json"
        )

        with open(dataset_file_path, "w") as dataset_file:
            dataset_file.write(ds_def_str)

        return dataset_file_path
