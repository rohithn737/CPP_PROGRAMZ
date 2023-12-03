from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
import boto3
import json
from botocore.exceptions import ClientError
 
 
 
def get_secret():
 
    secret_name = "db_secret"
    region_name = "us-east-1"
 
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
 
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        secret_string = get_secret_value_response['SecretString']
 
        if secret_string:
            secret = json.loads(secret_string)
            print(secret)
            return secret
        else:
            raise ImproperlyConfigured(f"Secret '{secret_name}' does not contain a 'SecretString'.")
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e