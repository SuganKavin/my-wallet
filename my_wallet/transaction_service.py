from aws_cdk import (core,
                     aws_apigateway as apigateway,
                     aws_dynamodb as dynamodb,
                     aws_lambda as lambda_)


class TransactionService(core.Construct):
    def __init__(self, scope: core.Construct, id: str):
        super().__init__(scope, id)


        '''wallet_table = dynamodb.table('WalletDetail')
        transaction_table = dynamodb.table('TransactionDetail')'''

        create_trx_handler = lambda_.Function("Transaction", "TrxCreateHandler",
                                              function_name="TransactionCreate",
                                              runtime=lambda_.Runtime.PYTHON_3_7,
                                              code=lambda_.Code.asset("resources"),
                                              handler="create.handler",
                                              environment=dict(
                                                  WALLET_TABLE="WalletDetail",
                                                  TRANSACTION_TABLE="TransactionDetail" )
                                              )

        '''transaction_table.grant_read_write_data(create_trx_handler)
        wallet_table.grant_read_write_data(create_trx_handler)'''


        api = apigateway.RestApi(self, "Transaction-api",
                                 rest_api_name="Wallet Service",
                                 description="This service serves Wallets.")

        post_integration = apigateway.LambdaIntegration(create_trx_handler,
                                                        request_templates={
                                                            "application/json": '{ "statusCode": "200" }'})

        api.root.add_method("POST",post_integration)

