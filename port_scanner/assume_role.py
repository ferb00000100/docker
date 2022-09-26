import os
import boto3
from boto3.session import Session


def iso_security_enforce(account):
    AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_SESSION = os.environ['AWS_SESSION_TOKEN']

    session = Session(aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_ACCESS,
                      aws_session_token=AWS_SESSION)

    sts_client = session.client('sts')

    assumed_role_object = sts_client.assume_role(
        RoleArn='arn:aws:iam::' + account + ':role/ISOSecurityEnforce',
        RoleSessionName='AssumeRoleISOAuditSession',
        DurationSeconds=3600
    )

    credentials = assumed_role_object['Credentials']
    print('got seciso', credentials)
    return credentials


def iso_enforce(account, AWS_ACCESS_KEY, AWS_SECRET_ACCESS, AWS_SESSION):

    session = Session(aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_ACCESS,
                      aws_session_token=AWS_SESSION)

    sts_client = session.client('sts')

    assumed_role_object = sts_client.assume_role(
        RoleArn='arn:aws:iam::' + account + ':role/ISOEnforce',
        RoleSessionName='AssumeRoleISOAuditSession',
        DurationSeconds=3600
    )

    credentials = assumed_role_object['Credentials']
    print('got iso enforce', credentials)
    return credentials
