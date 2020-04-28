import json
import logging
import os
import time
import uuid
import logging
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    data = json.loads(event['body'])

    timestamp = str(time.time())

    table = dynamodb.Table(os.environ['WALLET_TABLE'])

    wallet_bwal ={
        'WalletCurrency': data['WalletCurrency'],
        'AccountId': data['AccountId'],
        'CurrentReservedBalance': 0,
        'WalletType': 'BWAL',
        'CurrentBalance': 0,
        'id': str(uuid.uuid1()),
        'createdAt': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'updatedAt': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    wallet_pwal ={
        'WalletCurrency': data['WalletCurrency'],
        'AccountId': data['AccountId'],
        'CurrentReservedBalance': 0,
        'WalletType': 'PWAL',
        'CurrentBalance': 0,
        'id': str(uuid.uuid1()),
        'createdAt': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'updatedAt': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    logging.info(wallet_bwal)
    logging.info(wallet_pwal)
    with table.batch_writer() as batch:
        batch.put_item(
            Item= wallet_bwal)
        batch.put_item(
            Item= wallet_pwal)



    # create a response
    response = {
        "statusCode": 200
    }

    return response
