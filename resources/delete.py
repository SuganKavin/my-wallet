import os
import boto3

dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    table = dynamodb.Table(os.environ['WALLET_TABLE'])

    table.delete_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200
    }

    return response


'''
1. hard/soft delete
  soft delete then we can add additional field to mark as N
'''