"""

 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: MIT-0
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this
 * software and associated documentation files (the "Software"), to deal in the Software
 * without restriction, including without limitation the rights to use, copy, modify,
 * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
"""

import json
import boto3
import os

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
    table = dynamodb.Table(os.environ['DynamoDb_Table'])
    step = boto3.client("stepfunctions")

    responseupdate = table.update_item(
                       Key={
                            'Id': "1"
                       },
                       UpdateExpression="SET #ttlexpired=:newValue, #stepalreadydone=:newAlready, #productlive=:newOnline",
                       ExpressionAttributeNames={
                            '#ttlexpired': 'ttlexpired',
                            '#stepalreadydone': 'stepalreadydone',
                            '#productlive': 'productlive'
                       },
                       ExpressionAttributeValues={
                            ':newValue': "0",
                            ':newAlready': "0",
                            ':newOnline': "0"
                       },
                       ReturnValues="UPDATED_NEW"
                    )
    return {
        'statusCode': 200,
        'body': json.dumps('Processed')
    }
