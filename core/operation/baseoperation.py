import json
import logging
import os
from abc import abstractmethod

ASSET_DIR = "assets"
TEMPLATE_DIR = os.path.join(ASSET_DIR, "templates")
DATA_SET_DIR = os.path.join(ASSET_DIR, "data-sets")


class BaseOperation:

    """
    A base class for AWS based operations.
    """

    def __init__(self, qs_client, aws_account_id: str):
        self._aws_account_id = aws_account_id
        self._qs_client = qs_client
        self._log = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def execute(self):
        pass

    def _create_or_update_template(self, template_data: dict) -> tuple[str, str, str]:
        """
        Creates new or updates existing template.
        :param template_data:
        :return: Template ARN, Template Version ARN, and the Template ID
        """
        try:
            response = self._qs_client.create_template(**template_data)
        except self._qs_client.exceptions.ResourceExistsException as e:
            response = self._qs_client.update_template(**template_data)
        httpStatus = response["ResponseMetadata"]["HTTPStatusCode"]
        if httpStatus != 202:
            self._log.error(
                f"Unexpected response from create_template request: {httpStatus} "
            )
            raise Exception(
                f"Unexpected response from trying to create/update template : {json.dumps(response, indent=4)} "
            )
        else:
            return response["Arn"], response["VersionArn"], response["TemplateId"]

    def _create_or_update_template_from_template_definition(
        self, template_definition: dict
    ):
        template_definition["AwsAccountId"] = self._aws_account_id
        return self._create_or_update_template(template_data=template_definition)

    def _resolve_data_set_id_from_placeholder(
        self, namespace: str, placeholder: str
    ) -> str:
        return namespace + "-" + placeholder

    def _get_template_definition(self, template_id):
        return self._qs_client.describe_template_definition(
            AwsAccountId=self._aws_account_id,
            TemplateId=template_id,
            AliasName="$LATEST",
        )

    def _describe_data_set(self, data_set_id):
        response = self._qs_client.describe_data_set(
            AwsAccountId=self._aws_account_id, DataSetId=data_set_id
        )
        return response["DataSet"]

    def _resolve_path(self, *paths):
        return os.path.join(*paths)
