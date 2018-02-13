#!/usr/bin/env python
# vim: set fileencoding=utf8 :

import logging

import click
import athena_batch_query

logging.basicConfig(filename = 'athena.log',
                    filemode = 'a',
                    level = logging.INFO,
                    format = '%(levelname)s:%(asctime)s:%(message)s'
                    )

@click.command()
@click.option('--s3bucket', help='athena log bucket', required=True)
@click.option('--database', help='athena database name', required=True)
@click.option('--save/--no-save', default=False)
@click.argument('args', nargs=-1)
def cli(s3bucket, database, save, args):
    logging.info("s3bucket:" + s3bucket)
    logging.info("database:" + database)
    for arg in args:
        try:
            click.echo('filename: %s' % click.format_filename(arg))
            query_id = athena_batch_query.query_to_athena(s3bucket, database, save, arg)
        except Exception, err:
            click.echo('Start Query Execution Failed', err=True)
            logging.error(err, exc_info=True)
