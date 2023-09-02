import click

import logging

from core.operation.export_analysis_operation import ExportAnalysisOperation
from core.operation.import_from_json_operation import ImportFromJsonOperation
from core.operation.publish_dashboard_from_template import PublishDashboardFromTemplateOperation

log = logging.getLogger("core.cli")


@click.group()
def cli():
    pass


@click.command()
@click.option('--aws-profile', required=True, help='The AWS account profile')
@click.option('--aws-account-id', required=True, help='The ID of the AWS account')
@click.option('--analysis-id', required=True, help='The ID of the Analysis to be exported')
@click.option('--output-dir', required=True,
              help='The path to the output directory to which resources will be exported')
def export_analysis(aws_profile: str, aws_account_id: str, analysis_id: str, output_dir: str):
    """
    Creates a template from  the analysis and exports at and the dataset(s) to json.
    """
    click.echo(f"Create version")
    click.echo(f"aws_profile = {aws_profile}")
    click.echo(f"analysis_id= {analysis_id}")
    click.echo(f"aws_account_id= {aws_account_id}")
    click.echo(f"output_dir= {output_dir}")
    ExportAnalysisOperation(aws_profile=aws_profile, aws_account_id=aws_account_id, analysis_id=analysis_id,
                            output_dir=output_dir).execute()


cli.add_command(export_analysis)


@click.command
@click.option('--aws-profile', required=True, help='The AWS account profile')
@click.option('--aws-account-id', required=True, help='The ID of the AWS account')
@click.option('--template-name', required=True, help='The name of the template to be restored')
@click.option('--data-source-arn', required=True,
              help='The ARN of the data source you want to associate with the data sets')
@click.option('--target-namespace', required=True,
              help='The namespace you wish to target (e.g. tpp-prod, tpp-dev, tpp-staging).')
@click.option('--input-dir', required=True,
              help='The path to the input directory from which resources will be imported')
def import_template(aws_profile: str, aws_account_id: str, template_name: str, data_source_arn: str,
                     target_namespace: str, input_dir: str):
    """
    Import template and datasource files from json
    """

    click.echo(f"import_from_json")
    click.echo(f"aws_profile = {aws_profile}")
    click.echo(f"aws_account_id = {aws_account_id}")
    click.echo(f"template_name = {template_name}")
    click.echo(f"data_source_arn = {data_source_arn}")
    click.echo(f"input_dir= {input_dir}")

    ImportFromJsonOperation(aws_profile=aws_profile, aws_account_id=aws_account_id, template_name=template_name,
                            target_namespace=target_namespace, data_source_arn=data_source_arn,
                            input_dir=input_dir).execute()


cli.add_command(import_template)


@click.command
@click.option('--aws-profile', required=True, help='The AWS account profile')
@click.option('--aws-account-id', required=True, help='The ID of the AWS account')
@click.option('--template-id', required=True, help='The ID of the template to be restored')
@click.option('--target-namespace', required=True,
              help='The namespace you wish to target (e.g. tpp-prod, tpp-dev, tpp-staging).')
@click.option('--group-name', required=True, help='Name of the Quicksight User Group')
def publish_dashboard(aws_profile: str, aws_account_id: str, template_id: str, target_namespace: str,
                                    group_name: str):
    """
    Create/Update a dashboard from a template
    """

    click.echo(f"publish dashboard from template")
    click.echo(f"aws_profile = {aws_profile}")
    click.echo(f"aws_account_id = {aws_account_id}")
    click.echo(f"template_id = {template_id}")
    click.echo(f"group_name = {group_name}")
    PublishDashboardFromTemplateOperation(aws_profile=aws_profile,
                                          aws_account_id=aws_account_id,
                                          template_id=template_id,
                                          target_namespace=target_namespace,
                                          group_name=group_name).execute()


cli.add_command(publish_dashboard)
