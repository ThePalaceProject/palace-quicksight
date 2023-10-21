import json
import logging
import os
import time
from abc import abstractmethod
from dataclasses import dataclass

ASSET_DIR = "assets"
TEMPLATE_DIR = os.path.join(ASSET_DIR, "templates")
DATA_SET_DIR = os.path.join(ASSET_DIR, "data-sets")


@dataclass
class TemplateResponse:
    arn: str
    version_arn: str
    template_id: str


class BaseOperation:
    """
    A base class for AWS based operations.
    """

    def __init__(self, qs_client, s3_client, aws_account_id: str):
        self._aws_account_id = aws_account_id
        self._qs_client = qs_client
        self._s3_client = s3_client
        self._log = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def execute(self) -> dict:
        pass

    def _create_or_update_template(self, template_data: dict) -> TemplateResponse:
        """
        Creates new or updates existing template.
        :param template_data:
        :return: Template ARN, Template Version ARN, and the Template ID
        """

        template_id = template_data["TemplateId"]
        try:
            self._log.info(f"ready to delete template ({template_id}) if exists.")

            self._qs_client.delete_template(
                **{
                    "TemplateId": template_id,
                    "AwsAccountId": template_data["AwsAccountId"],
                }
            )

            # there can be some latency between the completion of the deletion command
            # and the complete backend deletion operation.
            time.sleep(3)
            self._log.info(f"template ({template_id}) deletion complete.")

        except self._qs_client.exceptions.ResourceNotFoundException as e:
            self._log.info(f"template ({template_id}) not found: no deletion needed.")

        response = self._qs_client.create_template(**template_data)

        http_status = response["ResponseMetadata"]["HTTPStatusCode"]
        if http_status != 202:
            self._log.error(
                f"Unexpected response from create_template request: "
                f"template_id = {template_id}, http_status = {http_status}"
            )
            raise Exception(
                f"Unexpected response from trying to create/update template : {json.dumps(response, indent=4)} "
            )
        else:
            self._log.info(
                f"Template ({template_id}) created successfully: http_status = {http_status}"
            )
            return TemplateResponse(
                response["Arn"], response["VersionArn"], response["TemplateId"]
            )

    def _create_or_update_template_from_template_definition(
        self, template_definition: dict
    ) -> TemplateResponse:
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
