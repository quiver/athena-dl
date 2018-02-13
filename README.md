# athena-dl

This package provides a command line interface to query SQL to Amazon Athena and save its results in a batch.

The package works on Python versions:

- 2.7.x and greater

# Installation

## install via pip
```
$ pip install athena-dl
```
## install from GitHub

```
$ git clone https://github.com/quiver/athena-dl.git
$ cd athena-dl
$ pip install --editable .
```

# Getting Started

First create SQL files to query against Amazon athena.

```
$ cat foo.sql
SELECT count(*)
FROM elb_logs

$ cat bar.sql
SELECT user_agent
      ,count(*)
FROM elb_logs
GROUP BY user_agent
```
Then pass 
- S3 bucket for Athena (Athena uses `aws-athena-query-results-<AWS-ACCOUNT_ID>-<REGION>` as its default S3 bucket name)
- database name
- SQL files
```
$ athena-dl --help
Usage: athena-dl [OPTIONS] [ARGS]...

Options:
  --s3bucket TEXT  athena log bucket  [required]
  --database TEXT  athena database name  [required]
  --save / --no-save
  --help           Show this message and exit.

$ athena-dl \
  --s3bucket aws-athena-query-results-123456789012-us-west-1 \
  --database ec-prd \
  foo.sql bar.sql

filename: foo.sql
AMC URL : https://us-west-1.console.aws.amazon.com/athena/home?region=ap-northeast-1#query/history/1234-5678-...
filename: bar.sql
AMC URL : https://us-west-1.console.aws.amazon.com/athena/home?region=ap-northeast-1#query/history/8765-4321-...
```
Check its results
```
$ ls -1
athena.log    # application log
bar.sql       # sql file
bar.sql.log   # AWS API response for bar.sql
...
```

By accessing AMC URLs, you can also check query results through AWS Web console.

To save query results loccaly, pass `--save` switch:

```
$ athena-dl \
  --s3bucket aws-athena-query-results-123456789012-us-west-1 \
  --save \
  --database ec-prd \
  foo.sql bar.sql
```
Check its results
```
$ ls -1
athena.log    # application log
bar.sql       # sql file
bar.sql.csv   # query result for bar.sql
bar.sql.log   # AWS API response for bar.sql
...
$ cat bar.sql.csv
"foo","_col1"
"xxx","1"
"yyy","4"
...
```
