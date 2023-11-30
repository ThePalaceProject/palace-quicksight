import logging

import boto3
import click

from core.operation.export_analysis_operation import ExportAnalysisOperation
from core.operation.import_from_json_operation import ImportFromJsonOperation
from core.operation.publish_dashboard_from_template import (
    PublishDashboardFromTemplateOperation,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("palace-quicksight.log"), logging.StreamHandler()],
)


log = logging.getLogger("core.cli")

boto3.setup_default_session()


def create_quicksight_client():
    return boto3.client("quicksight")


def create_s3_client():
    return boto3.client("s3")


@click.group()
def cli():
    pass


@click.command()
@click.option("--aws-account-id", required=True, help="The ID of the AWS account")
@click.option(
    "--analysis-id", required=True, help="The ID of the Analysis to be exported"
)
@click.option(
    "--output-dir",
    required=True,
    help="The path to the output directory to which resources will be exported",
)
def export_analysis(aws_account_id: str, analysis_id: str, output_dir: str):
    """
    Exports a template and dependent data sets based on the specified analysis to JSON files.
    """
    log.info(f"Create version")
    log.info(f"analysis_id= {analysis_id}")
    log.info(f"aws_account_id={aws_account_id}")
    log.info(f"output_dir={output_dir}")
    result = ExportAnalysisOperation(
        qs_client=create_quicksight_client(),
        aws_account_id=aws_account_id,
        analysis_id=analysis_id,
        output_dir=output_dir,
    ).execute()
    log.info(result)


cli.add_command(export_analysis)


@click.command
@click.option("--aws-account-id", required=True, help="The ID of the AWS account")
@click.option(
    "--template-name", required=True, help="The name of the template to be restored"
)
@click.option(
    "--data-source-arn",
    required=True,
    help="The ARN of the data source you want to associate with the data sets",
)
@click.option(
    "--target-namespace",
    required=True,
    help="The namespace you wish to target (e.g. tpp-prod, tpp-dev, tpp-staging).",
)
@click.option(
    "--input-dir",
    required=True,
    help="The path to the input directory from which resources will be imported",
)
def import_template(
    aws_account_id: str,
    template_name: str,
    data_source_arn: str,
    target_namespace: str,
    input_dir: str,
):
    """
    Import template and datasource files from json
    """

    log.info(f"import_from_json")
    log.info(f"aws_account_id = {aws_account_id}")
    log.info(f"template_name = {template_name}")
    log.info(f"data_source_arn = {data_source_arn}")
    log.info(f"input_dir= {input_dir}")

    result = ImportFromJsonOperation(
        qs_client=create_quicksight_client(),
        aws_account_id=aws_account_id,
        template_name=template_name,
        target_namespace=target_namespace,
        data_source_arn=data_source_arn,
        input_dir=input_dir,
    ).execute()
    log.info(result)


cli.add_command(import_template)


@click.command
@click.option("--aws-account-id", required=True, help="The ID of the AWS account")
@click.option(
    "--template-id", required=True, help="The ID of the template to be restored"
)
@click.option(
    "--target-namespace",
    required=True,
    help="The namespace you wish to target (e.g. tpp-prod, tpp-dev, tpp-staging).",
)
@click.option("--group-name", required=True, help="Name of the Quicksight User Group")
@click.option(
    "--output-json",
    required=False,
    help="The file path to which operation output should be written as json",
)
@click.option(
    "--result-bucket",
    required=False,
    help="An S3 bucket to save the results to. If specified, you must also specify a result-key",
)
@click.option(
    "--result-key",
    required=False,
    help="An S3 object key to save the results to. If used, result-bucket must be specified.",
)
def publish_dashboard(
    aws_account_id: str,
    template_id: str,
    target_namespace: str,
    group_name: str,
    output_json: str,
    result_bucket: str,
    result_key: str,
):
    """
    Create/Update a dashboard from a template
    """

    log.info(f"publish dashboard from template")
    log.info(f"aws_account_id = {aws_account_id}")
    log.info(f"template_id = {template_id}")
    log.info(f"group_name = {group_name}")
    result = PublishDashboardFromTemplateOperation(
        qs_client=create_quicksight_client(),
        s3_client=create_s3_client(),
        aws_account_id=aws_account_id,
        template_id=template_id,
        target_namespace=target_namespace,
        group_name=group_name,
        output_json=output_json,
        result_bucket=result_bucket,
        result_key=result_key,
    ).execute()
    log.info(result)


cli.add_command(publish_dashboard)


@click.command
@click.option("--aws-account-id", required=True, help="The ID of the AWS account")
@click.option(
    "--template-name", required=True, help="The name of the template to be restored"
)
@click.option(
    "--data-source-arn",
    required=True,
    help="The ARN of the data source you want to associate with the data sets",
)
@click.option(
    "--target-namespace",
    required=True,
    help="The namespace you wish to target (e.g. tpp-prod, tpp-dev, tpp-staging).",
)
@click.option(
    "--input-dir",
    required=True,
    help="The path to the input directory from which resources will be imported",
)
@click.option("--group-name", required=True, help="Name of the Quicksight User Group")
@click.option(
    "--result-bucket",
    required=False,
    help="An S3 bucket to save the results to. If specified, you must also specify a result-key",
)
@click.option(
    "--result-key",
    required=False,
    help="An S3 object key to save the results to. If used, result-bucket must be specified.",
)
@click.option(
    "--output-json",
    required=False,
    help="(Optional) The file path to which operation output should be written as json",
)
def import_and_publish(
    aws_account_id: str,
    template_name: str,
    data_source_arn: str,
    target_namespace: str,
    input_dir: str,
    group_name: str,
    result_bucket: str,
    result_key: str,
    output_json: str = None,
):

    log.info(f"import_and_publish")
    log.info(f"aws_account_id = {aws_account_id}")
    log.info(f"template_name = {template_name}")
    log.info(f"data_source_arn = {data_source_arn}")
    log.info(f"input_dir= {input_dir}")
    log.info(f"group_name = {group_name}")
    log.info(f"result_bucket = {result_bucket}")
    log.info(f"result_key = {result_key}")
    log.info(f"output_json = {output_json}")

    log.info(f"Importing {template_name}")
    result = ImportFromJsonOperation(
        qs_client=create_quicksight_client(),
        aws_account_id=aws_account_id,
        template_name=template_name,
        target_namespace=target_namespace,
        data_source_arn=data_source_arn,
        input_dir=input_dir,
    ).execute()
    log.info(f"Import result: {result}")
    template_id: str = result["template"]["id"]
    log.info(
        f"Publishing template {template_id} as dashboard using datasource {data_source_arn}"
    )

    result = PublishDashboardFromTemplateOperation(
        qs_client=create_quicksight_client(),
        s3_client=create_s3_client(),
        aws_account_id=aws_account_id,
        dashboard_alias=template_name,
        template_id=template_id,
        target_namespace=target_namespace,
        group_name=group_name,
        result_bucket=result_bucket,
        result_key=result_key,
        output_json=output_json,
    ).execute()
    log.info(f"publish result = {result}")


cli.add_command(import_and_publish)
