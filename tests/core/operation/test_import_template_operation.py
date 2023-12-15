import datetime
from unittest.mock import patch

from botocore.config import Config
from botocore.session import Session
from botocore.stub import Stubber

from core.operation.import_from_json_operation import ImportFromJsonOperation


def create_data_set_response(target_namespace, data_set_name):
    response = {
        "ResponseMetadata": {
            "RequestId": "3aecd4ed-9a15-408a-a251-532718e574bd",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "date": "Tue, 19 Sep 2023 17:54:43 GMT",
                "content-type": "application/json",
                "content-length": "215",
                "connection": "keep-alive",
                "x-amzn-requestid": "3aecd4ed-9a15-408a-a251-532718e574bd",
            },
            "RetryAttempts": 0,
        },
        "Status": 200,
        "Arn": f"arn:aws:quicksight:us-west-2:128682227026:dataset/{data_set_name}",
        "DataSetId": data_set_name,
        "RequestId": "3aecd4ed-9a15-408a-a251-532718e574bd",
    }
    return response


def create_data_set_params1(target_namespace, data_source_arn, aws_account_id):
    data_set_params = {
        "Name": "circulation_view",
        "PhysicalTableMap": {
            "25046cd8-e08f-41e0-8af8-5259b64499fd": {
                "CustomSql": {
                    "DataSourceArn": data_source_arn,
                    "Name": "circulation_view",
                    "SqlQuery": "sql query",
                    "Columns": [{"Name": "time_stamp", "Type": "DATETIME"}],
                }
            }
        },
        "LogicalTableMap": {
            "6c80275e-d03d-417c-a8cd-57d93e58129b": {
                "Alias": "circulation_view",
                "DataTransforms": [
                    {"ProjectOperation": {"ProjectedColumns": ["time_stamp"]}}
                ],
                "Source": {"PhysicalTableId": "25046cd8-e08f-41e0-8af8-5259b64499fd"},
            }
        },
        "ImportMode": "DIRECT_QUERY",
        "FieldFolders": {},
        "DataSetUsageConfiguration": {
            "DisableUseAsDirectQuerySource": False,
            "DisableUseAsImportedSource": False,
        },
        "AwsAccountId": aws_account_id,
        "DataSetId": f"{target_namespace}-circulation_view",
    }
    return data_set_params


def create_data_set_params2(target_namespace, data_source_arn, aws_account_id):
    data_set_params = {
        "Name": "patron_events",
        "PhysicalTableMap": {
            "50873ea6-0c3a-4989-97e1-eb740e8a3348": {
                "CustomSql": {
                    "DataSourceArn": data_source_arn,
                    "Name": "patron_events",
                    "SqlQuery": "sql query",
                    "Columns": [{"Name": "time_stamp", "Type": "DATETIME"}],
                }
            }
        },
        "LogicalTableMap": {
            "4dc4e51c-76b2-4595-8b3b-1759f76a05c4": {
                "Alias": "patron_events",
                "DataTransforms": [
                    {"ProjectOperation": {"ProjectedColumns": ["time_stamp"]}}
                ],
                "Source": {"PhysicalTableId": "50873ea6-0c3a-4989-97e1-eb740e8a3348"},
            }
        },
        "ImportMode": "DIRECT_QUERY",
        "FieldFolders": {},
        "DataSetUsageConfiguration": {
            "DisableUseAsDirectQuerySource": False,
            "DisableUseAsImportedSource": False,
        },
        "AwsAccountId": aws_account_id,
        "DataSetId": f"{target_namespace}-patron_events",
    }
    return data_set_params


def create_data_set_refresh_properties_params(data_set_id, aws_account_id):
    return {
        "AwsAccountId": aws_account_id,
        "DataSetId": data_set_id,
        "DataSetRefreshProperties": {
            "RefreshConfiguration": {
                "IncrementalRefresh": {
                    "LookbackWindow": {
                        "ColumnName": "time_stamp",
                        "Size": 1,
                        "SizeUnit": "DAY",
                    }
                }
            }
        },
    }


def create_refresh_schedule_params(data_set_id, aws_account_id):
    return {
        "AwsAccountId": aws_account_id,
        "DataSetId": data_set_id,
        "Schedule": {
            "ScheduleFrequency": {
                "Interval": "DAILY",
                "Timezone": "America/New_York",
                "TimeOfTheDay": "23:59",
            },
            "StartAfterDateTime": "2023-09-29 16:59:00-07:00",
            "RefreshType": "INCREMENTAL_REFRESH",
        },
    }


def create_template_params(target_namespace, aws_account_id):
    return {
        "Name": f"{target_namespace}-library",
        "TemplateId": f"{target_namespace}-library",
        "AwsAccountId": aws_account_id,
        "Definition": {
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
            "Sheets": [],
            "AnalysisDefaults": {
                "DefaultNewSheetConfiguration": {
                    "InteractiveLayoutConfiguration": {
                        "Grid": {
                            "CanvasSizeOptions": {
                                "ScreenCanvasSizeOptions": {
                                    "ResizeOption": "FIXED",
                                    "OptimizedViewPortWidth": "1600px",
                                }
                            }
                        }
                    },
                    "SheetContentType": "INTERACTIVE",
                }
            },
        },
    }

    return


def create_template_response(new_template_name):
    return {
        "ResponseMetadata": {
            "RequestId": "09f0120c-92c9-4f16-8044-dc44b715f6db",
            "HTTPStatusCode": 202,
            "HTTPHeaders": {
                "date": "Tue, 19 Sep 2023 17:32:44 GMT",
                "content-type": "application/json",
                "content-length": "293",
                "connection": "keep-alive",
                "x-amzn-requestid": "09f0120c-92c9-4f16-8044-dc44b715f6db",
            },
            "RetryAttempts": 0,
        },
        "Status": 202,
        "TemplateId": new_template_name,
        "Arn": f"arn:aws:quicksight:us-west-2:128682227026:template/{new_template_name}",
        "VersionArn": f"arn:aws:quicksight:us-west-2:128682227026:template/{new_template_name}/version/4",
        "CreationStatus": "CREATION_IN_PROGRESS",
        "RequestId": "09f0120c-92c9-4f16-8044-dc44b715f6db",
    }


def create_new_dataset_name(target_namespace: str, data_set_name: str) -> str:
    return f"{target_namespace}-{data_set_name}"


class TestImportTemplateOperation:
    def test(self):
        template_name = "library"
        input_dir = "tests/core/operation/resources"
        account = "012345678910"
        target_namespace = "my_env"
        data_source_arn = "my_data_source_arn"

        boto_config = Config(
            region_name="us-east-1",
        )

        new_template_name = target_namespace + "-" + template_name

        sess = Session()
        qs_client = sess.create_client("quicksight", config=boto_config)

        this_time_tomorrow = datetime.datetime.now()
        with Stubber(qs_client) as stub, patch(
            "core.operation.import_from_json_operation.ImportFromJsonOperation._get_tomorrow"
        ) as dt:

            dt.return_value = this_time_tomorrow
            stub.add_response(
                "delete_template",
                service_response={},
                expected_params={
                    "TemplateId": new_template_name,
                    "AwsAccountId": account,
                },
            )

            stub.add_response(
                "create_template",
                service_response=create_template_response(new_template_name),
                expected_params=create_template_params(target_namespace, account),
            )

            ds1_name = create_new_dataset_name(
                target_namespace=target_namespace, data_set_name="circulation_view"
            )

            stub.add_client_error(
                "delete_data_set_refresh_properties",
                service_error_code="InvalidParameterException",
                expected_params={
                    "DataSetId": ds1_name,
                    "AwsAccountId": account,
                },
            )

            schedule_id = "my_schedule_id"
            stub.add_response(
                "list_refresh_schedules",
                service_response={
                    "RefreshSchedules": [
                        {
                            "ScheduleId": schedule_id,
                            "RefreshType": "INCREMENTAL_REFRESH",
                            "ScheduleFrequency": {
                                "Interval": "DAILY",
                                "Timezone": "America/New_York",
                                "TimeOfTheDay": "23:59",
                            },
                        }
                    ]
                },
                expected_params={
                    "DataSetId": ds1_name,
                    "AwsAccountId": account,
                },
            )

            stub.add_response(
                "delete_refresh_schedule",
                service_response={},
                expected_params={
                    "DataSetId": ds1_name,
                    "AwsAccountId": account,
                    "ScheduleId": schedule_id,
                },
            )

            stub.add_response(
                "delete_data_set",
                service_response={},
                expected_params={
                    "DataSetId": ds1_name,
                    "AwsAccountId": account,
                },
            )

            stub.add_response(
                "create_data_set",
                service_response=create_data_set_response(target_namespace, ds1_name),
                expected_params=create_data_set_params1(
                    target_namespace=target_namespace,
                    data_source_arn=data_source_arn,
                    aws_account_id=account,
                ),
            )

            stub.add_response(
                "put_data_set_refresh_properties",
                service_response={},
                expected_params=create_data_set_refresh_properties_params(
                    ds1_name, account
                ),
            )

            stub.add_response(
                "create_refresh_schedule",
                service_response={},
                expected_params={
                    "DataSetId": ds1_name,
                    "AwsAccountId": account,
                    "Schedule": {
                        "ScheduleId": ds1_name + "-0",
                        "ScheduleFrequency": {
                            "Interval": "DAILY",
                            "Timezone": "UTC",
                            "TimeOfTheDay": "07:00",
                        },
                        "StartAfterDateTime": this_time_tomorrow,
                        "RefreshType": "INCREMENTAL_REFRESH",
                    },
                },
            )

            ds2_name = create_new_dataset_name(
                target_namespace=target_namespace, data_set_name="patron_events"
            )

            stub.add_client_error(
                "delete_data_set_refresh_properties",
                service_error_code="InvalidParameterException",
                expected_params={
                    "DataSetId": ds2_name,
                    "AwsAccountId": account,
                },
            )

            stub.add_response(
                "list_refresh_schedules",
                service_response={"RefreshSchedules": []},
                expected_params={
                    "DataSetId": ds2_name,
                    "AwsAccountId": account,
                },
            )

            stub.add_response(
                "delete_data_set",
                service_response={},
                expected_params={
                    "DataSetId": ds2_name,
                    "AwsAccountId": account,
                },
            )

            stub.add_response(
                "create_data_set",
                service_response=create_data_set_response(target_namespace, ds2_name),
                expected_params=create_data_set_params2(
                    target_namespace=target_namespace,
                    data_source_arn=data_source_arn,
                    aws_account_id=account,
                ),
            )

            op = ImportFromJsonOperation(
                qs_client=qs_client,
                template_name=template_name,
                target_namespace=target_namespace,
                input_dir=input_dir,
                aws_account_id=account,
                data_source_arn=data_source_arn,
            )

            result = op.execute()
            assert result["status"] == "success"
