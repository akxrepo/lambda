import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('People')  # Create People table in DynamoDB with PersonID as partitionkey
    try:
        # TODO: write code...
        response = table.put_item(
          Item=event)
        return "Done"
    except:
        raise


################
Data Sample
################
{
  "PersonID": 007,
  "Address": "UK",
  "FirstName": "James",
  "LastName": "Bond",
  "Phone": "007-007-007"
}
    
