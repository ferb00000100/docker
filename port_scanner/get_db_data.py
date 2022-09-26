import json
import boto3
import botocore.exceptions


def get_data(data):
    try:
        secret_name = "Sec_Compl_Postgres_Log_in"
        region_name = "us-east-1"

        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        response = client.get_secret_value(
            SecretId=secret_name
        )

        secret = response['SecretString']
        formatSecret = json.loads(secret)
        if data == 'user':
            key = formatSecret['username']
            return key
        if data == 'pwd':
            key = formatSecret['password']
            return key
        if data == 'host':
            key = formatSecret['host']
            return key
        if data == 'name':
            key = formatSecret['dbname']
            return key
        if data == 'port':
            key = formatSecret['port']
            return key
    except botocore.exceptions.NoCredentialsError as error:
        print('Error Getting Data', error)


def get_dev_sec_prod_acct():
    try:
        secret_name = "devsec_prod_account"
        region_name = "us-east-1"

        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        response = client.get_secret_value(
            SecretId=secret_name
        )

        secret = response['SecretString']
        formatSecret = json.loads(secret)
        key = formatSecret['account']
        return key
    except botocore.exceptions.NoCredentialsError as error:
        print('Error Getting DevSecPord Account ', error)
