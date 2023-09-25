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


def create_quicksight_client(aws_profile: str):
    boto3.setup_default_session(profile_name=aws_profile)
    return boto3.client("quicksight")


@click.group()
def cli():
    pass


@click.command()
@click.option("--aws-profile", required=True, help="The AWS account profile")
@click.option("--aws-account-id", required=True, help="The ID of the AWS account")
@click.option(
    "--analysis-id", required=True, help="The ID of the Analysis to be exported"
)
@click.option(
    "--output-dir",
    required=True,
    help="The path to the output directory to which resources will be exported",
)
def export_analysis(
    aws_profile: str, aws_account_id: str, analysis_id: str, output_dir: str
):
    """
    Exports a template and dependent data sets based on the specified analysis to JSON files.
    """
    log.info(f"Create version")
    log.info(f"aws_profile = {aws_profile}")
    log.info(f"analysis_id= {analysis_id}")
    log.info(f"aws_account_id={aws_account_id}")
    log.info(f"output_dir={output_dir}")
    result = ExportAnalysisOperation(
        qs_client=create_quicksight_client(aws_profile=aws_profile),
        aws_account_id=aws_account_id,
        analysis_id=analysis_id,
        output_dir=output_dir,
    ).execute()
    log.info(result)


cli.add_command(export_analysis)


@click.command
@click.option("--aws-profile", required=True, help="The AWS account profile")
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
    aws_profile: str,
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
    log.info(f"aws_profile = {aws_profile}")
    log.info(f"aws_account_id = {aws_account_id}")
    log.info(f"template_name = {template_name}")
    log.info(f"data_source_arn = {data_source_arn}")
    log.info(f"input_dir= {input_dir}")

    result = ImportFromJsonOperation(
        qs_client=create_quicksight_client(aws_profile),
        aws_account_id=aws_account_id,
        template_name=template_name,
        target_namespace=target_namespace,
        data_source_arn=data_source_arn,
        input_dir=input_dir,
    ).execute()
    log.info(result)


cli.add_command(import_template)


@click.command
@click.option("--aws-profile", required=True, help="The AWS account profile")
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
def publish_dashboard(
    aws_profile: str,
    aws_account_id: str,
    template_id: str,
    target_namespace: str,
    group_name: str,
):
    """
    Create/Update a dashboard from a template
    """

    log.info(f"publish dashboard from template")
    log.info(f"aws_profile = {aws_profile}")
    log.info(f"aws_account_id = {aws_account_id}")
    log.info(f"template_id = {template_id}")
    log.info(f"group_name = {group_name}")
    result = PublishDashboardFromTemplateOperation(
        qs_client=create_quicksight_client(aws_profile),
        aws_account_id=aws_account_id,
        template_id=template_id,
        target_namespace=target_namespace,
        group_name=group_name,
    ).execute()
    log.info(result)


cli.add_command(publish_dashboard)
