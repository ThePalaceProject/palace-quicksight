from datetime import datetime

from dateutil.tz import tzlocal


def get_analysis_description_response(analysis_id):
    return {
        'ResponseMetadata': {'RequestId': 'aca2b75d-503b-48c4-b66c-273eafe97a33',
                             'HTTPStatusCode': 200,
                             'HTTPHeaders': {'date': 'Tue, 05 Sep 2023 19:29:21 GMT',
                                             'content-type': 'application/json',
                                             'content-length': '1495',
                                             'connection': 'keep-alive',
                                             'x-amzn-requestid': 'aca2b75d-503b-48c4-b66c-273eafe97a33'},
                             'RetryAttempts': 0}, 'Status': 200,
        'Analysis': {'AnalysisId': analysis_id,
                     'Arn': 'arn',
                     'Name': 'library', 'Status': 'CREATION_SUCCESSFUL', 'DataSetArns': [
                'arn:aws:quicksight:us-west-2:128682227026:dataset/e9e15c78-0193-4e4c-9a49-ed005569297d',
                'arn:aws:quicksight:us-west-2:128682227026:dataset/86eb4ca5-9552-4ba6-8b1b-7ef1b9b40f78', ],
                     'ThemeArn': 'theme-arn',
                     'CreatedTime': datetime(2023, 9, 1, 10, 6, 19, 376000, tzinfo=tzlocal()),
                     'LastUpdatedTime': datetime(2023, 9, 1, 10, 6, 19, 376000, tzinfo=tzlocal()),
                     'Sheets': [
                         {'SheetId': '9f2df4a8-21e2-4aa4-adcd-3fb32e86c4ba',
                          'Name': 'Circulation Summary'},
                         {'SheetId': '341952d3-ece8-4a4b-924c-2d16c905e486',
                          'Name': 'Circulation over Time'},
                         {'SheetId': '8e9ca074-e043-4e02-be63-649e1ded32e6',
                          'Name': 'Loaned Title Use'}]},
        'RequestId': 'aca2b75d-503b-48c4-b66c-273eafe97a33'}


def get_analysis_definition_response():
    return {
        'ResponseMetadata': {'RequestId': 'dac531e6-fc4f-41a5-986e-4212c79e9c6c', 'HTTPStatusCode': 200,
                             'HTTPHeaders': {'date': 'Tue, 05 Sep 2023 19:47:04 GMT',
                                             'content-type': 'application/json', 'content-length': '172259',
                                             'connection': 'keep-alive',
                                             'x-amzn-requestid': 'dac531e6-fc4f-41a5-986e-4212c79e9c6c'},
                             'RetryAttempts': 0}, 'Status': 200,
        'AnalysisId': 'd954330e-7b80-4a4a-ab64-47f53d8eea38', 'Name': 'library',
        'ResourceStatus': 'CREATION_SUCCESSFUL',
        'ThemeArn': 'theme-arn',
        'Definition': {'DataSetIdentifierDeclarations': [{'Identifier': 'circulation_view',
                                                          'DataSetArn': 'arn:aws:quicksight:us-west-2:128682227026:dataset/e9e15c78-0193-4e4c-9a49-ed005569297d'},
                                                         {'Identifier': 'patron_events',
                                                          'DataSetArn': 'arn:aws:quicksight:us-west-2:128682227026:dataset/86eb4ca5-9552-4ba6-8b1b-7ef1b9b40f78'}],
                       'Sheets': [],
                       'ColumnConfigurations': [],
                       'AnalysisDefaults': {'DefaultNewSheetConfiguration': {
                           'InteractiveLayoutConfiguration': {'Grid': {'CanvasSizeOptions': {
                               'ScreenCanvasSizeOptions': {'ResizeOption': 'FIXED',
                                                           'OptimizedViewPortWidth': '1600px'}}}},
                           'SheetContentType': 'INTERACTIVE'}}}, 'RequestId': 'dac531e6-fc4f-41a5-986e-4212c79e9c6c'}


def create_template_response():
    return {'ResponseMetadata': {'RequestId': '55aba51c-0052-4311-8fb3-b9433f0041da', 'HTTPStatusCode': 202,
                                 'HTTPHeaders': {'date': 'Tue, 05 Sep 2023 21:52:26 GMT',
                                                 'content-type': 'application/json', 'content-length': '293',
                                                 'connection': 'keep-alive',
                                                 'x-amzn-requestid': '55aba51c-0052-4311-8fb3-b9433f0041da'},
                                 'RetryAttempts': 0}, 'Status': 202, 'TemplateId': 'library-template',
            'Arn': 'arn:aws:quicksight:us-west-2:128682227026:template/library-template',
            'VersionArn': 'arn:aws:quicksight:us-west-2:128682227026:template/library-template/version/9',
            'CreationStatus': 'CREATION_IN_PROGRESS', 'RequestId': '55aba51c-0052-4311-8fb3-b9433f0041da'}


def create_template_parameters(aws_account_id: str):
    {'AwsAccountId': aws_account_id, 'TemplateId': 'library-template', 'Name': 'library', 'SourceEntity': {
        'SourceAnalysis': {
            'Arn': 'arn:aws:quicksight:us-west-2:128682227026:analysis/d954330e-7b80-4a4a-ab64-47f53d8eea38',
            'DataSetReferences': [{'DataSetPlaceholder': 'circulation_view',
                                   'DataSetArn': 'arn:aws:quicksight:us-west-2:128682227026:dataset/e9e15c78-0193-4e4c-9a49-ed005569297d'},
                                  {'DataSetPlaceholder': 'patron_events',
                                   'DataSetArn': 'ds_2_arn'}]}}}


def describe_template_definition_response():
    return {'ResponseMetadata': {'RequestId': 'c9ebc247-e7f7-4140-913c-2a1288ff43f6', 'HTTPStatusCode': 200,
                                 'HTTPHeaders': {'date': 'Tue, 05 Sep 2023 21:59:51 GMT',
                                                 'content-type': 'application/json', 'content-length': '173310',
                                                 'connection': 'keep-alive',
                                                 'x-amzn-requestid': 'c9ebc247-e7f7-4140-913c-2a1288ff43f6'},
                                 'RetryAttempts': 0}, 'Status': 200, 'Name': 'library',
            'TemplateId': 'library-template',
            'ResourceStatus': 'CREATION_SUCCESSFUL',
            'ThemeArn': 'arn:aws:quicksight:us-west-2:128682227026:theme/5f5e7417-a800-4812-9e59-dc44e0580412',
            'Definition': {'DataSetConfigurations': [{'Placeholder': 'circulation_view', 'DataSetSchema': {
                'ColumnSchemaList': [{'Name': 'fiction', 'DataType': 'INTEGER'},
                                     {'Name': 'location', 'DataType': 'STRING'},
                                     {'Name': 'event_type', 'DataType': 'STRING'},
                                     {'Name': 'audience', 'DataType': 'STRING'},
                                     {'Name': 'medium', 'DataType': 'STRING'},
                                     {'Name': 'time_stamp', 'DataType': 'DATETIME'},
                                     {'Name': 'distributor', 'DataType': 'STRING'},
                                     {'Name': 'author', 'DataType': 'STRING'},
                                     {'Name': 'libary_short_name', 'DataType': 'STRING'},
                                     {'Name': 'title', 'DataType': 'STRING'},
                                     {'Name': 'open_access', 'DataType': 'INTEGER'},
                                     {'Name': 'collection_name', 'DataType': 'STRING'},
                                     {'Name': 'genre', 'DataType': 'STRING'},
                                     {'Name': 'library_name', 'DataType': 'STRING'}]}, 'ColumnGroupSchemaList': []},
                                                     {'Placeholder': 'patron_events', 'DataSetSchema': {
                                                         'ColumnSchemaList': [
                                                             {'Name': 'location', 'DataType': 'STRING'},
                                                             {'Name': 'event_type', 'DataType': 'STRING'},
                                                             {'Name': 'time_stamp',
                                                              'DataType': 'DATETIME'},
                                                             {'Name': 'library_name',
                                                              'DataType': 'STRING'}]},
                                                      'ColumnGroupSchemaList': []}], },
            }


def describe_data_set_1_response():
    return {'ResponseMetadata': {'RequestId': '5c7285af-6ea4-4192-af69-8f8093785112', 'HTTPStatusCode': 200,
                                 'HTTPHeaders': {'date': 'Wed, 06 Sep 2023 00:02:50 GMT',
                                                 'content-type': 'application/json', 'content-length': '4642',
                                                 'connection': 'keep-alive',
                                                 'x-amzn-requestid': '5c7285af-6ea4-4192-af69-8f8093785112'},
                                 'RetryAttempts': 0}, 'Status': 200,
            'DataSet': {'Arn': 'arn:aws:quicksight:us-west-2:128682227026:dataset/e9e15c78-0193-4e4c-9a49-ed005569297d',
                        'DataSetId': 'e9e15c78-0193-4e4c-9a49-ed005569297d', 'Name': 'circulation_events_view',
                        'CreatedTime': datetime(2023, 2, 28, 13, 39, 33, 923000, tzinfo=tzlocal()),
                        'LastUpdatedTime': datetime(2023, 6, 7, 10, 5, 32, 640000, tzinfo=tzlocal()),
                        'PhysicalTableMap': {'25046cd8-e08f-41e0-8af8-5259b64499fd': {'CustomSql': {
                            'DataSourceArn': 'arn:aws:quicksight:us-west-2:128682227026:datasource/a4e44abb-c1fd-4b5a-be3f-daca72d50e0a',
                            'Name': 'circulation_events_view',
                            'SqlQuery': 'select \n    ce.time_stamp, \n    l.short_name as libary_short_name, \n    l.name as library_name,\n    l.location as location,\n    et.name as event_type, \n    i.identifier,\n    it.name as identifier_type,\n    c.name as collection_name, \n    ce.title, \n    ce.author,\n    ce.audience,\n    ce.publisher,\n    ce.language,\n    ce.genre,\n    ce.open_access,\n    ce.fiction,\n    ce.distributor,\n    ce.medium\nfrom \n    circulation_events ce,\n    libraries l,\n    collections c,\n    circulation_event_types et,\n    identifiers i,\n    identifier_types it\nwhere \n    ce.library_id = l.id and\n    ce.event_type_id = et.id and\n    ce.collection_id = c.id and\n    ce.identifier_id = i.id and \n    i.identifier_type_id = it.id',
                            'Columns': [{'Name': 'time_stamp', 'Type': 'DATETIME'},
                                        {'Name': 'libary_short_name', 'Type': 'STRING'},
                                        {'Name': 'library_name', 'Type': 'STRING'},
                                        {'Name': 'location', 'Type': 'STRING'},
                                        {'Name': 'event_type', 'Type': 'STRING'},
                                        {'Name': 'identifier', 'Type': 'STRING'},
                                        {'Name': 'identifier_type', 'Type': 'STRING'},
                                        {'Name': 'collection_name', 'Type': 'STRING'},
                                        {'Name': 'title', 'Type': 'STRING'}, {'Name': 'author', 'Type': 'STRING'},
                                        {'Name': 'audience', 'Type': 'STRING'}, {'Name': 'publisher', 'Type': 'STRING'},
                                        {'Name': 'language', 'Type': 'STRING'}, {'Name': 'genre', 'Type': 'STRING'},
                                        {'Name': 'open_access', 'Type': 'BIT'}, {'Name': 'fiction', 'Type': 'BIT'},
                                        {'Name': 'distributor', 'Type': 'STRING'},
                                        {'Name': 'medium', 'Type': 'STRING'}]}}}, 'LogicalTableMap': {
                    '6c80275e-d03d-417c-a8cd-57d93e58129b': {'Alias': 'circulation_events_view', 'DataTransforms': [{
                        'ProjectOperation': {
                            'ProjectedColumns': [
                                'time_stamp',
                                'libary_short_name',
                                'library_name',
                                'location',
                                'event_type',
                                'identifier',
                                'identifier_type',
                                'collection_name',
                                'title',
                                'author',
                                'audience',
                                'publisher',
                                'language',
                                'genre',
                                'open_access',
                                'fiction',
                                'distributor',
                                'medium']}}],
                                                             'Source': {
                                                                 'PhysicalTableId': '25046cd8-e08f-41e0-8af8-5259b64499fd'}}},
                        'OutputColumns': [{'Name': 'time_stamp', 'Type': 'DATETIME'},
                                          {'Name': 'libary_short_name', 'Type': 'STRING'},
                                          {'Name': 'library_name', 'Type': 'STRING'},
                                          {'Name': 'location', 'Type': 'STRING'},
                                          {'Name': 'event_type', 'Type': 'STRING'},
                                          {'Name': 'identifier', 'Type': 'STRING'},
                                          {'Name': 'identifier_type', 'Type': 'STRING'},
                                          {'Name': 'collection_name', 'Type': 'STRING'},
                                          {'Name': 'title', 'Type': 'STRING'}, {'Name': 'author', 'Type': 'STRING'},
                                          {'Name': 'audience', 'Type': 'STRING'},
                                          {'Name': 'publisher', 'Type': 'STRING'},
                                          {'Name': 'language', 'Type': 'STRING'}, {'Name': 'genre', 'Type': 'STRING'},
                                          {'Name': 'open_access', 'Type': 'INTEGER'},
                                          {'Name': 'fiction', 'Type': 'INTEGER'},
                                          {'Name': 'distributor', 'Type': 'STRING'},
                                          {'Name': 'medium', 'Type': 'STRING'}], 'ImportMode': 'DIRECT_QUERY',
                        'ConsumedSpiceCapacityInBytes': 0, 'FieldFolders': {},
                        'DataSetUsageConfiguration': {'DisableUseAsDirectQuerySource': False,
                                                      'DisableUseAsImportedSource': False}},
            'RequestId': '5c7285af-6ea4-4192-af69-8f8093785112'}


def describe_data_set_2_response():
    return {'ResponseMetadata': {'RequestId': '3e6ad967-c44d-4a86-8391-be51ebf978c5', 'HTTPStatusCode': 200,
                                 'HTTPHeaders': {'date': 'Wed, 06 Sep 2023 00:07:58 GMT',
                                                 'content-type': 'application/json', 'content-length': '2564',
                                                 'connection': 'keep-alive',
                                                 'x-amzn-requestid': '3e6ad967-c44d-4a86-8391-be51ebf978c5'},
                                 'RetryAttempts': 0}, 'Status': 200,
            'DataSet': {'Arn': 'arn:aws:quicksight:us-west-2:128682227026:dataset/86eb4ca5-9552-4ba6-8b1b-7ef1b9b40f78',
                        'DataSetId': '86eb4ca5-9552-4ba6-8b1b-7ef1b9b40f78', 'Name': 'patron_events',
                        'CreatedTime': datetime(2023, 2, 28, 16, 8, 15, 620000, tzinfo=tzlocal()),
                        'LastUpdatedTime': datetime(2023, 3, 1, 8, 28, 1, 477000, tzinfo=tzlocal()),
                        'PhysicalTableMap': {'50873ea6-0c3a-4989-97e1-eb740e8a3348': {'CustomSql': {
                            'DataSourceArn': 'arn:aws:quicksight:us-west-2:128682227026:datasource/a4e44abb-c1fd-4b5a-be3f-daca72d50e0a',
                            'Name': 'patron_events',
                            'SqlQuery': 'select \n    pe.time_stamp, \n    l.short_name as library_short_name, \n    l.name as library_name, \n    l.location,  \n    l.state, \n    ev.name as event_type \nfrom  \n    patron_events pe, \n    libraries l, \n    circulation_event_types ev \nwhere \n    pe.library_id = l.id and \n    pe.event_type_id = ev.id',
                            'Columns': [{'Name': 'time_stamp', 'Type': 'DATETIME'},
                                        {'Name': 'library_short_name', 'Type': 'STRING'},
                                        {'Name': 'library_name', 'Type': 'STRING'},
                                        {'Name': 'location', 'Type': 'STRING'}, {'Name': 'state', 'Type': 'STRING'},
                                        {'Name': 'event_type', 'Type': 'STRING'}]}}}, 'LogicalTableMap': {
                    '4dc4e51c-76b2-4595-8b3b-1759f76a05c4': {'Alias': 'patron_events', 'DataTransforms': [{
                                                                                                              'ProjectOperation': {
                                                                                                                  'ProjectedColumns': [
                                                                                                                      'time_stamp',
                                                                                                                      'library_short_name',
                                                                                                                      'library_name',
                                                                                                                      'location',
                                                                                                                      'state',
                                                                                                                      'event_type']}}],
                                                             'Source': {
                                                                 'PhysicalTableId': '50873ea6-0c3a-4989-97e1-eb740e8a3348'}}},
                        'OutputColumns': [{'Name': 'time_stamp', 'Type': 'DATETIME'},
                                          {'Name': 'library_short_name', 'Type': 'STRING'},
                                          {'Name': 'library_name', 'Type': 'STRING'},
                                          {'Name': 'location', 'Type': 'STRING'}, {'Name': 'state', 'Type': 'STRING'},
                                          {'Name': 'event_type', 'Type': 'STRING'}], 'ImportMode': 'DIRECT_QUERY',
                        'ConsumedSpiceCapacityInBytes': 0, 'FieldFolders': {},
                        'DataSetUsageConfiguration': {'DisableUseAsDirectQuerySource': False,
                                                      'DisableUseAsImportedSource': False}},
            'RequestId': '3e6ad967-c44d-4a86-8391-be51ebf978c5'}
