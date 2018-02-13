#!/usr/bin/env python
# vim: set fileencoding=utf8 :

import logging
import pprint

import click
import boto3
from retrying import retry

athena = boto3.client('athena')
s3 = boto3.resource('s3')

AMC_URL_TEMPLATE = 'https://{region_name}.console.aws.amazon.com/athena/home?region={region_name}#query/history/{query_id}'

REGION_NAME = boto3.session.Session().region_name

@retry(stop_max_attempt_number = 10,
       wait_exponential_multiplier = 30 * 1000,
       wait_exponential_max = 10 * 60 * 1000)
def poll_status(_id):
    '''
    poll query status
    '''
    result = athena.get_query_execution(
        QueryExecutionId = _id
    )

    logging.info(pprint.pformat(result['QueryExecution']))
    state = result['QueryExecution']['Status']['State']
    if state == 'SUCCEEDED':
        return result
    elif state == 'FAILED':
        return result
    else:
        raise Exception

def query_to_athena(s3bucket, database, save_result, sqlfile):
    logging.info("sqlfile:" + sqlfile)
    sql = open(sqlfile, 'r').read()
    logging.info("SQL:" + sql)
    result = athena.start_query_execution(
        QueryString = sql,
        QueryExecutionContext = {
            'Database': database
        },
        ResultConfiguration = {
            'OutputLocation': 's3://' + s3bucket,
        }
    )

    logging.info(pprint.pformat(result))

    QueryExecutionId = result['QueryExecutionId']
    result = poll_status(QueryExecutionId)

    # save API response
    with open(sqlfile + '.log', 'w') as f:
        f.write(pprint.pformat(result, indent = 4))

    # save query result from S3
    if result['QueryExecution']['Status']['State'] == 'SUCCEEDED':
        if save_result:
            s3_key = QueryExecutionId + '.csv'
            query_result = sqlfile + '.csv'
            s3.Bucket(s3bucket).download_file(s3_key, query_result)
            logging.info("saved query result {} to : {}".format(
              result['QueryExecution']['ResultConfiguration']['OutputLocation'], query_result))
    else:
        click.echo('Query Execution Failed', err=True)

    amc_url = AMC_URL_TEMPLATE.format(region_name = REGION_NAME, query_id = QueryExecutionId)
    logging.info('AMC URL : {}s'.format(amc_url))
    click.echo('AMC URL : {}s'.format(amc_url))

    logging.info('FINISHED')
    return QueryExecutionId
