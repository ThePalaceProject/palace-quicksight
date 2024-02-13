import json
import os.path
import tempfile

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
        result_bucket = "result-bucket"
        result_key = "result-key"
        output_json = tempfile.NamedTemporaryFile()

        boto_config = Config(
            region_name="us-east-1",
        )

        qs_client = botocore.session.get_session().create_client(
            "quicksight", config=boto_config
        )

        s3_client = botocore.session.get_session().create_client(
            "s3", config=boto_config
        )

        dashboard_arn = (
            "arn:aws:quicksight:us-west-2:128682227026:dashboard/tpp-prod-library"
        )
        describe_template_definition_params = {
            "AwsAccountId": account,
            "TemplateId": template_id,
            "AliasName": "$LATEST",
        }
        with Stubber(qs_client) as qs_stub, Stubber(s3_client) as s3_stub:
            template_arn = f"arn:aws:quicksight:::template/{target_namespace}-library"
            qs_stub.add_response(
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

            qs_stub.add_response(
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

            qs_stub.add_response(
                "describe_data_set",
                service_response={"DataSet": {"Arn": ds1_arn}},
                expected_params={
                    "AwsAccountId": account,
                    "DataSetId": f"{target_namespace}-circulation_view",
                },
            )
            qs_stub.add_response(
                "describe_data_set",
                service_response={"DataSet": {"Arn": ds2_arn}},
                expected_params={
                    "AwsAccountId": account,
                    "DataSetId": f"{target_namespace}-patron_events",
                },
            )

            qs_stub.add_response(
                "delete_dashboard",
                service_response={},
                expected_params={
                    "AwsAccountId": account,
                    "DashboardId": template_id,
                },
            )

            qs_stub.add_response(
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
                    "Arn": dashboard_arn,
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
            qs_stub.add_response(
                "describe_group",
                service_response={"Group": {"Arn": group_arn}},
                expected_params={
                    "AwsAccountId": account,
                    "Namespace": "default",
                    "GroupName": group_name,
                },
            )

            qs_stub.add_response(
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

            s3_stub.add_response(
                "put_object",
                service_response={},
                expected_params={
                    "Bucket": result_bucket,
                    "Key": result_key,
                    "ContentType": "application/json",
                    "Body": json.dumps({template_id: [dashboard_arn]}),
                },
            )

            op = PublishDashboardFromTemplateOperation(
                qs_client=qs_client,
                s3_client=s3_client,
                template_id=template_id,
                target_namespace=target_namespace,
                aws_account_id=account,
                group_name=group_name,
                output_json=output_json.name,
                result_bucket=result_bucket,
                result_key=result_key,
            )

            result = op.execute()

            assert result["status"] == "success"
            assert result["dashboard_info"] == {template_id: [dashboard_arn]}
            assert os.path.exists(output_json.name)

            with open(output_json.name) as file:
                result_from_file = json.loads(file.read())
                assert result_from_file["dashboard_info"] == {
                    template_id: [dashboard_arn]
                }
