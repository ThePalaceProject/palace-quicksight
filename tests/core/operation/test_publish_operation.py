import botocore
from botocore.config import Config
from botocore.stub import Stubber

from core.operation.publish_dashboard_from_template import (
    PublishDashboardFromTemplateOperation,
)


class TestPublishDashboardFromTemplateOperation:
    def test(self):
        target_namespace = "my_env"
        template_id = f"{target_namespace}-library"
        account = "012345678910"
        group_name = "my_group"

        boto_config = Config(
            region_name="us-east-1",
        )

        qs_client = botocore.session.get_session().create_client(
            "quicksight", config=boto_config
        )

        describe_template_definition_params = {
            "AwsAccountId": account,
            "TemplateId": template_id,
            "AliasName": "$LATEST",
        }
        with Stubber(qs_client) as stub:
            template_arn = f"arn:aws:quicksight:::template/{target_namespace}-library"
            stub.add_response(
                "describe_template",
                service_response={
                    "Template": {
                        "Arn": template_arn,
                        "Version": {
                            "VersionNumber": 5,
                            "Status": "CREATION_SUCCESSFUL",
                            "DataSetConfigurations": [
                                {
                                    "Placeholder": "circulation_view",
                                    "DataSetSchema": {"ColumnSchemaList": []},
                                    "ColumnGroupSchemaList": [],
                                },
                                {
                                    "Placeholder": "patron_events",
                                    "DataSetSchema": {"ColumnSchemaList": []},
                                    "ColumnGroupSchemaList": [],
                                },
                            ],
                        },
                    }
                },
                expected_params={"AwsAccountId": account, "TemplateId": template_id},
            )

            namespace_arn = "arn:quicksight:::namespace/default"

            stub.add_response(
                "describe_namespace",
                service_response={"Namespace": {"Arn": namespace_arn}},
                expected_params={
                    "AwsAccountId": account,
                    "Namespace": "default",
                },
            )

            ds1_arn = (
                f"arn:aws:quicksight:::dataset/{target_namespace}-circulation_view"
            )
            ds2_arn = f"arn:aws:quicksight:::dataset/{target_namespace}-patron_events"

            stub.add_response(
                "describe_data_set",
                service_response={"DataSet": {"Arn": ds1_arn}},
                expected_params={
                    "AwsAccountId": account,
                    "DataSetId": f"{target_namespace}-circulation_view",
                },
            )
            stub.add_response(
                "describe_data_set",
                service_response={"DataSet": {"Arn": ds2_arn}},
                expected_params={
                    "AwsAccountId": account,
                    "DataSetId": f"{target_namespace}-patron_events",
                },
            )

            stub.add_response(
                "create_dashboard",
                service_response={
                    "ResponseMetadata": {
                        "RequestId": "7d276ede-baa4-4662-abb1-a917489c9e96",
                        "HTTPStatusCode": 200,
                        "HTTPHeaders": {
                            "date": "Tue, 19 Sep 2023 21:49:00 GMT",
                            "content-type": "application/json",
                            "content-length": "309",
                            "connection": "keep-alive",
                            "x-amzn-requestid": "7d276ede-baa4-4662-abb1-a917489c9e96",
                        },
                        "RetryAttempts": 0,
                    },
                    "Arn": "arn:aws:quicksight:us-west-2:128682227026:dashboard/tpp-prod-library",
                    "VersionArn": f"arn:aws:quicksight:::dashboard/{target_namespace}-library/version/6",
                    "DashboardId": f"{target_namespace}-library",
                    "CreationStatus": "CREATION_IN_PROGRESS",
                    "Status": 202,
                    "RequestId": "7d276ede-baa4-4662-abb1-a917489c9e96",
                },
                expected_params={
                    "AwsAccountId": account,
                    "Name": template_id,
                    "DashboardId": template_id,
                    "SourceEntity": {
                        "SourceTemplate": {
                            "DataSetReferences": [
                                {
                                    "DataSetPlaceholder": "circulation_view",
                                    f"DataSetArn": ds1_arn,
                                },
                                {
                                    "DataSetPlaceholder": "patron_events",
                                    "DataSetArn": ds2_arn,
                                },
                            ],
                            "Arn": template_arn,
                        }
                    },
                },
            )
            group_arn = f"arn:aws:quicksight:::group/{group_name}"
            stub.add_response(
                "describe_group",
                service_response={"Group": {"Arn": group_arn}},
                expected_params={
                    "AwsAccountId": account,
                    "Namespace": "default",
                    "GroupName": group_name,
                },
            )

            stub.add_response(
                "update_dashboard_permissions",
                service_response={
                    "ResponseMetadata": {
                        "RequestId": "14cfee14-421d-4ce1-91ea-e5aef9a0c0ca",
                        "HTTPStatusCode": 200,
                        "HTTPHeaders": {
                            "date": "Tue, 19 Sep 2023 21:32:57 GMT",
                            "content-type": "application/json",
                            "content-length": "633",
                            "connection": "keep-alive",
                            "x-amzn-requestid": "14cfee14-421d-4ce1-91ea-e5aef9a0c0ca",
                        },
                        "RetryAttempts": 0,
                    },
                    "Status": 200,
                },
                expected_params={
                    "AwsAccountId": account,
                    "DashboardId": template_id,
                    "GrantPermissions": [
                        {
                            "Actions": [
                                "quicksight:DescribeDashboard",
                                "quicksight:ListDashboardVersions",
                                "quicksight:QueryDashboard",
                            ],
                            "Principal": namespace_arn,
                        },
                        {
                            "Actions": [
                                "quicksight:DescribeDashboard",
                                "quicksight:ListDashboardVersions",
                                "quicksight:QueryDashboard",
                            ],
                            "Principal": group_arn,
                        },
                    ],
                },
            )
            op = PublishDashboardFromTemplateOperation(
                qs_client=qs_client,
                template_id=template_id,
                target_namespace=target_namespace,
                aws_account_id=account,
                group_name=group_name,
            )

            result = op.execute()

            assert result["status"] == "success"
            assert result["dashboard_id"] == template_id
