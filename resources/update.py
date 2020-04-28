import json
import logging
import os
import uuid
import boto3
import decimal

from botocore.exceptions import ClientError
from datetime import datetime

dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    data = json.loads(event['body'])

    id  = event['pathParameters']['id']

    if not id:
        logging.error("Validation Failed. Missing id")
        raise Exception("Couldn't update the wallet.")

    table = dynamodb.Table(os.environ['WALLET_TABLE'])

    try:
        # update the account in the database
        result = table.update_item(
            Key={
                'id': event['pathParameters']['id']
            },
            ExpressionAttributeValues={
                ':cb': data['CurrentBalance'],
                ':updatedAt': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            },
            UpdateExpression='SET CurrentBalance = :cb, updatedAt = :updatedAt',
            ReturnValues='ALL_NEW',
        )

        replace_decimals(result)
        # create a response
        response = {
            "statusCode": 200,
            "body": json.dumps(result['Attributes'])
        }
    except ClientError as ex:
        response = {
            "statusCode": 400,
            "body": json.dumps(ex.response['Error']['Message'])
        }

    return response

def replace_decimals(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = replace_decimals(v)
        return obj
    elif isinstance(obj, set):
        return set(replace_decimals(i) for i in obj)
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj
