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
from urllib.parse import urlparse 
 
def lambda_handler(event, context):
    rekognition = boto3.client("rekognition")
    metadata_insert = boto3.client("ivs")
    dynamodb = boto3.client("dynamodb")    
    dynamodbresource = boto3.resource("dynamodb", region_name="eu-west-1")
    table = dynamodbresource.Table(os.environ['DynamoDb_Table'])

    step = boto3.client("stepfunctions")
    file_obj = event["Records"][0]
    bucket_name = str(file_obj["s3"]["bucket"]["name"])
    file_name = str(file_obj["s3"]["object"]["key"])

    s3_url = "s3://"+bucket_name+"/"+file_name
    rekognition_arn = os.environ['Rekognition_Arn']
    response = rekognition.detect_custom_labels(
        ProjectVersionArn=rekognition_arn,
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': file_name
            }
        },
        MaxResults=10,
        MinConfidence=5
    )
    object= response["CustomLabels"][0]["Name"]

    if object == os.environ['Product1'] :
      response_dynamodb = dynamodb.scan(
            TableName=os.environ['DynamoDb_Table']

      )
      statusobject=response_dynamodb['Items'][1]['productlive']['S']
      statusobjectother=response_dynamodb['Items'][0]['productlive']['S']
      alreadyobject=response_dynamodb['Items'][1]['stepalreadydone']['S']
      alreadyobjectother=response_dynamodb['Items'][0]['stepalreadydone']['S']
      ttlexpiredobject=response_dynamodb['Items'][1]['ttlexpired']['S']
      ttlexpiredobjectother=response_dynamodb['Items'][0]['ttlexpired']['S']
      if alreadyobjectother == "0":
          if ttlexpiredobject == "0":
                if statusobject == "0":
                    parts_channel= urlparse(file_name)
                    channel_arn = parts_channel.path.strip('/').split('/')
                    channel_arn = os.environ['Ivs_arn']+channel_arn[3] 
                    metadata_response = metadata_insert.put_metadata(
                        channelArn=channel_arn,
                        metadata='{\"type\": \"product\",\"image\": \"https://aws.amazon.com/?nc2=h_lg\",\"qr\": \"https://d2xbxlm8rp3jp3.cloudfront.net/qr-awscode.jpg\","title\": \"Aws Cloud privider\",\"description\": \"Look at news \",\"price\": \"Pay as you go\"}'
                    )
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
                                            ':newValue': "1",
                                            ':newAlready': "1",
                                            ':newOnline': "1"
                                        },
                                        ReturnValues="UPDATED_NEW"
                    )
                    response = step.start_execution(
                        stateMachineArn=os.environ['StateMachine_object1'],
                                input="{\"status\" : \"active\"}"
                    )
          elif ttlexpiredobject ==1:
                            print("TTl not expired")

    if object == os.environ['Product2'] :
      response_dynamodb = dynamodb.scan(
            TableName=os.environ['DynamoDb_Table']

      )

      statusobject=response_dynamodb['Items'][0]['productlive']['S']
      statusobjectother=response_dynamodb['Items'][1]['productlive']['S']
      alreadyobject=response_dynamodb['Items'][0]['stepalreadydone']['S']
      alreadyobjectother=response_dynamodb['Items'][1]['stepalreadydone']['S']
      ttlexpiredobject=response_dynamodb['Items'][0]['ttlexpired']['S']
      ttlexpiredobjectother=response_dynamodb['Items'][1]['ttlexpired']['S']
      if alreadyobjectother == "0":
            if ttlexpiredobject == "0":
                if statusobject == "0":
                    parts_channel= urlparse(file_name)
                    channel_arn = parts_channel.path.strip('/').split('/')
                    print(channel_arn[3])
                    channel_arn = os.environ['Ivs_arn']+channel_arn[3] 
                    print(channel_arn)
                    metadata_response = metadata_insert.put_metadata(
                      channelArn=channel_arn,
                      metadata='{\"type\": \"product\",\"image\": \"https://blog.twitch.tv/assets/uploads/01-twitch-logo.jpg\",\"qr\": \"https://d2xbxlm8rp3jp3.cloudfront.net/qr-twitchcode.jpg\","title\": \"Social Network\",\"description\": \"Description \",\"price\": \"Free\"}'
                    )
                    responseupdate = table.update_item(
                        Key={
                           'Id': '2'
                        },
                        UpdateExpression='SET #ttlexpired=:newValue, #stepalreadydone=:newAlready, #productlive=:newOnline',
                        ExpressionAttributeNames={
                            '#ttlexpired': 'ttlexpired',
                            '#stepalreadydone': 'stepalreadydone',
                            '#productlive': 'productlive'
                        },
                        ExpressionAttributeValues={
                            ':newValue': "1",
                            ':newAlready': "1",
                            ':newOnline': "1"
                        },
                        ReturnValues="UPDATED_NEW"
                    )
                    response = step.start_execution(
                        stateMachineArn=os.environ['StateMachine_object2'],
                                input="{\"status\" : \"active\"}"
                    )
            elif ttlexpiredobject ==1:
                            print("TTl not expired")

        
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Processed')
    }
