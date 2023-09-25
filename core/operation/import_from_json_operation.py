import json
import time
from dataclasses import dataclass

from core.operation.baseoperation import DATA_SET_DIR, TEMPLATE_DIR, BaseOperation
from core.util import recursively_replace_value


@dataclass
class DataSetResponse:
    arn: str
    data_set_id: str


class ImportFromJsonOperation(BaseOperation):
    """
    Imports a Quicksight template and all it's dependencies into Quicksight.
    """

    def __init__(
        self,
        template_name: str,
        target_namespace: str,
        data_source_arn: str,
        input_dir: str,
        *args,
        **kwargs,
    ):
        self._template_name = template_name
        self._target_namespace = target_namespace
        self._data_source_arn = data_source_arn
        self._intput_dir = input_dir
        super().__init__(*args, **kwargs)

    def execute(self) -> dict:
        # Read template file into dictionary
        template_data = None
        template_file = self._resolve_path(
            self._intput_dir, TEMPLATE_DIR, self._template_name + ".json"
        )
        with open(template_file) as template_file:
            template_data = json.loads(template_file.read())

        # create name template in namespace
        template_data["Name"] = self._target_namespace + "-" + self._template_name
        template_data["TemplateId"] = template_data["Name"]
        template_response = self._create_or_update_template_from_template_definition(
            template_definition=template_data
        )

        # for each data set id associated with the template
        dataset_configurations = template_data["Definition"]["DataSetConfigurations"]
        data_sets_created = []
        for di in dataset_configurations:
            # Read data set into dictionary
            dataset = None
            placeholder = di["Placeholder"]
            dataset_filename = self._resolve_path(
                self._intput_dir, DATA_SET_DIR, placeholder + ".json"
            )
            with open(dataset_filename) as dataset_file:
                dataset = json.loads(dataset_file.read())

            # replace the blank datasource arn value in the data set dictionaries
            recursively_replace_value(dataset, "DataSourceArn", self._data_source_arn)
            # Remove fields that are not allowed
            for i in ["OutputColumns", "ConsumedSpiceCapacityInBytes"]:
                dataset.pop(i)

            # Add required fields
            dataset["AwsAccountId"] = self._aws_account_id
            dataset["DataSetId"] = self._resolve_data_set_id_from_placeholder(
                placeholder=placeholder, namespace=self._target_namespace
            )
            dataset["Name"] = dataset["Name"]
            ds_response = self._create_or_update_data_set(dataset_definition=dataset)

            data_sets_created.append(
                {
                    "id": ds_response.data_set_id,
                    "arn": ds_response.arn,
                }
            )

        return {
            "status": "success",
            "data_sets": data_sets_created,
            "template": {
                "id": template_response.template_id,
                "arn": template_response.arn,
                "version_arn": template_response.version_arn,
            },
        }

    def _create_or_update_data_set(self, dataset_definition: dict):
        """
        Create new or updates existing DataSet
        :param dataset_definition:
        :return: DataSet ARN and DataSet Id
        """

        try:
            self._qs_client.delete_data_set(
                **{
                    "DataSetId": dataset_definition["DataSetId"],
                    "AwsAccountId": dataset_definition["AwsAccountId"],
                }
            )

            # there can be some latency between the completion of the deletion command
            # and the complete backend deletion operation.
            time.sleep(3)

        except self._qs_client.exceptions.ResourceNotFoundException as e:
            pass

        response = self._qs_client.create_data_set(**dataset_definition)
        http_status = response["ResponseMetadata"]["HTTPStatusCode"]
        if http_status != 201 and http_status != 200:
            self._log.error(
                f"Unexpected response from create_dataset request: {http_status} "
            )
            raise Exception(
                f"Unexpected response from trying to create/update dataset : {json.dumps(response, indent=4)} "
            )
        else:
            return DataSetResponse(response["Arn"], response["DataSetId"])
