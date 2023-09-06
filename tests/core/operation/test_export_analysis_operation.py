import os

import botocore
from botocore.stub import Stubber

from core.operation.export_analysis_operation import ExportAnalysisOperation
from tests.core.operation.analysis_test_responses import (
    create_template_response, describe_data_set_1_response,
    describe_data_set_2_response, describe_template_definition_response,
    get_analysis_definition_response, get_analysis_description_response)


class TestExportAnalysisOperation:
    def test(self):
        analysis_id = "my-quicksight-analysis-id"
        output_dir = "/tmp/test-output"
        account = "012345678910"

        qs_client = botocore.session.get_session().create_client("quicksight")
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
                "describe_data_set",
                service_response=describe_data_set_2_response(),
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

            op.execute()

        assets_dir = os.path.join(output_dir, "assets")
        data_sets_dir = os.path.join(assets_dir, "data-sets")
        templates_dir = os.path.join(assets_dir, "templates")
        template_file = os.path.join(templates_dir, "library.json")
        patron_events_file = os.path.join(data_sets_dir, "patron_events.json")
        circulation_events_file = os.path.join(data_sets_dir, "circulation_view.json")
        for p in [
            assets_dir,
            data_sets_dir,
            templates_dir,
            template_file,
            patron_events_file,
            circulation_events_file,
        ]:
            assert os.path.exists(p)
