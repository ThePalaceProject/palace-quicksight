import os
import tempfile

from botocore.config import Config
from botocore.session import Session
from botocore.stub import Stubber

from core.operation.export_analysis_operation import ExportAnalysisOperation
from tests.core.operation.analysis_test_responses import (
    create_template_response,
    describe_data_set_1_response,
    describe_data_set_2_response,
    describe_refresh_props_response,
    describe_template_definition_response,
    get_analysis_definition_response,
    get_analysis_description_response,
    list_refresh_schedules_response,
)


class TestExportAnalysisOperation:
    def test(self):
        analysis_id = "my-quicksight-analysis-id"
        output_dir = tempfile.NamedTemporaryFile().name
        account = "012345678910"

        boto_config = Config(
            region_name="us-east-1",
        )

        sess = Session()
        qs_client = sess.create_client("quicksight", config=boto_config)

        with Stubber(qs_client) as stub:
            analysis_description_params = {
                "AwsAccountId": account,
                "AnalysisId": analysis_id,
            }

            stub.add_response(
                "describe_analysis",
                service_response=get_analysis_description_response(analysis_id),
                expected_params=analysis_description_params,
            )

            stub.add_response(
                "describe_analysis_definition",
                service_response=get_analysis_definition_response(),
                expected_params=analysis_description_params,
            )

            create_template_params = {
                "AwsAccountId": account,
                "TemplateId": "library-template",
                "Name": "library",
                "SourceEntity": {
                    "SourceAnalysis": {
                        "Arn": "arn",
                        "DataSetReferences": [
                            {
                                "DataSetPlaceholder": "circulation_view",
                                "DataSetArn": "arn:aws:quicksight:us-west-2:128682227026:dataset/e9e15c78-0193-4e4c-9a49-ed005569297d",
                            },
                            {
                                "DataSetPlaceholder": "patron_events",
                                "DataSetArn": "arn:aws:quicksight:us-west-2:128682227026:dataset/86eb4ca5-9552-4ba6-8b1b-7ef1b9b40f78",
                            },
                        ],
                    }
                },
            }

            stub.add_response(
                "delete_template",
                service_response={},
                expected_params={
                    "TemplateId": "library-template",
                    "AwsAccountId": account,
                },
            )

            stub.add_response(
                "create_template",
                service_response=create_template_response(),
                expected_params=create_template_params,
            )

            stub.add_response(
                "describe_template_definition",
                service_response=describe_template_definition_response(),
                expected_params={
                    "AwsAccountId": account,
                    "TemplateId": "library-template",
                    "AliasName": "$LATEST",
                },
            )

            stub.add_response(
                "describe_data_set",
                service_response=describe_data_set_1_response(),
                expected_params={
                    "AwsAccountId": account,
                    "DataSetId": "e9e15c78-0193-4e4c-9a49-ed005569297d",
                },
            )

            stub.add_response(
                "describe_data_set_refresh_properties",
                service_response=describe_refresh_props_response(),
                expected_params={
                    "AwsAccountId": account,
                    "DataSetId": "e9e15c78-0193-4e4c-9a49-ed005569297d",
                },
            )

            stub.add_response(
                "list_refresh_schedules",
                service_response=list_refresh_schedules_response(),
                expected_params={
                    "AwsAccountId": account,
                    "DataSetId": "e9e15c78-0193-4e4c-9a49-ed005569297d",
                },
            )

            stub.add_response(
                "describe_data_set",
                service_response=describe_data_set_2_response(),
                expected_params={
                    "AwsAccountId": account,
                    "DataSetId": "86eb4ca5-9552-4ba6-8b1b-7ef1b9b40f78",
                },
            )

            # if the refresh properties don't exist, an InvalidParameterException is thrown FWIW.
            stub.add_client_error(
                "describe_data_set_refresh_properties",
                service_error_code="InvalidParameterException",
                expected_params={
                    "AwsAccountId": account,
                    "DataSetId": "86eb4ca5-9552-4ba6-8b1b-7ef1b9b40f78",
                },
            )

            op = ExportAnalysisOperation(
                qs_client=qs_client,
                analysis_id=analysis_id,
                output_dir=output_dir,
                aws_account_id=account,
            )

            results = op.execute()

        assert results["status"] == "success"

        assets_dir = os.path.join(output_dir, "assets")
        data_sets_dir = os.path.join(assets_dir, "data-sets")
        templates_dir = os.path.join(assets_dir, "templates")
        template_file = os.path.join(templates_dir, "library.json")
        patron_events_file = os.path.join(data_sets_dir, "patron_events.json")
        circulation_events_file = os.path.join(data_sets_dir, "circulation_view.json")
        circulation_events_refresh_schedule_file = os.path.join(
            data_sets_dir, "circulation_view-data-set-refresh-schedules.json"
        )
        for p in [
            assets_dir,
            data_sets_dir,
            templates_dir,
            template_file,
            patron_events_file,
            circulation_events_file,
            circulation_events_refresh_schedule_file,
        ]:
            assert os.path.exists(p)
