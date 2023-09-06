import json

from core.operation.baseoperation import (DATA_SET_DIR, TEMPLATE_DIR,
                                          BaseOperation)
from core.util import recursively_replace_value


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

    def execute(self):
        # Read template file into dictionary
        template_data = None
        template_file = self._resolve_path(
            self._intput_dir, TEMPLATE_DIR, self._template_name + ".json"
        )
        with open(template_file) as template_file:
            template_data = json.loads(template_file.read())

        # create namespace if not exists
        # try:
        #     self._qs_client.create_namespace(AwsAccountId=self._aws_account_id, Namespace=self._target_namespace,
        #                                      IdentityStore="QUICKSIGHT")
        # except self._qs_client.exceptions.ConflictException as e:
        #     self._log.info(f"Namespace {self._target_namespace} already exists: ignoring.")
        #
        # namespace = self._qs_client.describe_namespace(AwsAccountId=self._aws_account_id,
        #                                                Namespace=self._target_namespace)

        # create name template in namespace
        template_data["Name"] = self._target_namespace + "-" + self._template_name
        template_data["TemplateId"] = template_data["Name"]
        (
            arn,
            version_arn,
            template_id,
        ) = self._create_or_update_template_from_template_definition(
            template_definition=template_data
        )

        # for each data set id associated with the template
        dataset_configurations = template_data["Definition"]["DataSetConfigurations"]
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
            arn, data_set_id = self._create_or_update_data_set(
                dataset_definition=dataset
            )

    def _create_or_update_data_set(self, dataset_definition: dict):
        """
        Create new or updates existing DataSet
        :param dataset_definition:
        :return: DataSet ARN and DataSet Id
        """
        try:
            response = self._qs_client.create_data_set(**dataset_definition)
        except self._qs_client.exceptions.ResourceExistsException as e:
            response = self._qs_client.update_data_set(**dataset_definition)
        httpStatus = response["ResponseMetadata"]["HTTPStatusCode"]
        if httpStatus != 201 and httpStatus != 200:
            self._log.error(
                f"Unexpected response from create_dataset request: {httpStatus} "
            )
            raise Exception(
                f"Unexpected response from trying to create/update dataset : {json.dumps(response, indent=4)} "
            )
        else:
            return response["Arn"], response["DataSetId"]
