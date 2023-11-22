import json
import time

from core.operation.baseoperation import BaseOperation


class PublishDashboardFromTemplateOperation(BaseOperation):
    """
    Publishes Dashboard based on template
    """

    def __init__(
        self,
        template_id: str,
        target_namespace: str,
        group_name: str,
        output_json: str,
        result_bucket: str,
        result_key: str,
        s3_client,
        *args,
        **kwargs,
    ):
        self._template_id = template_id
        self._target_namespace = target_namespace
        self._group_name = group_name
        self._output_json = output_json
        self._result_bucket = result_bucket
        self._result_key = result_key
        self._s3_client = s3_client
        super().__init__(*args, **kwargs)

    def execute(self) -> dict:
        desc_template_params = {
            "AwsAccountId": self._aws_account_id,
            "TemplateId": self._template_id,
        }
        template = self._qs_client.describe_template(**desc_template_params)["Template"]

        namespace_params = {
            "AwsAccountId": self._aws_account_id,
            "Namespace": "default",
        }
        namespace_arn = self._qs_client.describe_namespace(**namespace_params)[
            "Namespace"
        ]["Arn"]

        # extract the data source placeholders
        dashboard_id = self._template_id
        parameters: dict = {
            "AwsAccountId": self._aws_account_id,
            "Name": dashboard_id,
            "DashboardId": dashboard_id,
            "SourceEntity": {
                "SourceTemplate": {"DataSetReferences": [], "Arn": template["Arn"]}
            },
        }

        ds_references = parameters["SourceEntity"]["SourceTemplate"][
            "DataSetReferences"
        ]

        # for each data set config
        for dsr in template["Version"]["DataSetConfigurations"]:
            # resolve the dataset arn
            placeholder = dsr["Placeholder"]
            data_set_id = self._resolve_data_set_id_from_placeholder(
                placeholder=placeholder, namespace=self._target_namespace
            )
            data_set = self._describe_data_set(data_set_id=data_set_id)
            arn = data_set["Arn"]
            # associate arn with placeholder key and add to references array
            ds_references.append(
                {
                    "DataSetPlaceholder": placeholder,
                    "DataSetArn": arn,
                }
            )

        # publish dashboard
        dashboard_arn, dashboard_id = self._recreate_dashboard(
            dashboard_params=parameters
        )

        # pause for a moment to allow the updates to be processed.
        time.sleep(3)

        # Grant permissions
        # resolve readers group
        readers_group_arn = self._qs_client.describe_group(
            AwsAccountId=self._aws_account_id,
            Namespace="default",
            GroupName=self._group_name,
        )["Group"]["Arn"]

        qs_actions = [
            "quicksight:DescribeDashboard",
            "quicksight:ListDashboardVersions",
            "quicksight:QueryDashboard",
        ]
        permissions_params = {
            "AwsAccountId": self._aws_account_id,
            "DashboardId": self._template_id,
            "GrantPermissions": [
                {
                    "Actions": qs_actions,
                    "Principal": namespace_arn,
                },
                {
                    "Actions": qs_actions,
                    "Principal": readers_group_arn,
                },
            ],
        }

        response = self._qs_client.update_dashboard_permissions(**permissions_params)
        http_status = response["ResponseMetadata"]["HTTPStatusCode"]
        if http_status != 202 and http_status != 200:
            self._log.error(
                f"Unexpected response from update_dashboard_permissions request: {http_status} "
            )
            raise Exception(
                f"Unexpected response from trying to update_dashboard_permissions : {json.dumps(response, indent=4)} "
            )

        result = {
            "status": "success",
            "dashboard_info": {self._template_id: [dashboard_arn]},
        }

        if self._output_json:
            with open(self._output_json, "w") as output:
                output.write(json.dumps(result))
                self._log.info(f"Output written to {self._output_json}")

        if self._result_bucket and self._result_key:
            self._s3_client.put_object(
                Bucket=self._result_bucket,
                Key=self._result_key,
                Body=json.dumps(result["dashboard_info"]),
            )

        return result

    def _recreate_dashboard(self, dashboard_params: dict) -> tuple[str, str]:
        """
        Creates new or recreates existing template.
        :param dashboard_params:
        :return: Dashboard ARN, Dashboard ID
        """
        try:
            response = self._qs_client.delete_dashboard(
                AwsAccountId=dashboard_params["AwsAccountId"],
                DashboardId=dashboard_params["DashboardId"],
            )
        except self._qs_client.exceptions.ResourceNotFoundException as e:
            pass

        try:
            response = self._qs_client.create_dashboard(**dashboard_params)
        except self._qs_client.exceptions.ResourceExistsException as e:
            response = self._qs_client.update_dashboard(**dashboard_params)
        http_status = response["ResponseMetadata"]["HTTPStatusCode"]
        if http_status != 202 and http_status != 200:
            self._log.error(
                f"Unexpected response from create_template request: {http_status} "
            )
            raise Exception(
                f"Unexpected response from trying to create/update template : {json.dumps(response, indent=4)} "
            )
        else:
            return response["Arn"], response["DashboardId"]
