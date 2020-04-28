import os
import json
import boto3
import decimal

dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    table = dynamodb.Table(os.environ['WALLET_TABLE'])

    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    replace_decimals(result)

    if 'Item' in result:
        # create a response
        response = {
            "statusCode": 200,
            "body": json.dumps(result['Item'])
        }
    else:
        response = {
            "statusCode": 400,
            "body": json.dumps("Wallet is not available")
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

'''
1. based on id
2. based on id and no of transaction 
3. based on id and date range
'''