import json
import boto3
import requests
from decimal import *
from datetime import datetime

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb',region_name='us-east-1') 
    table = dynamodb.Table('Visitors')

    headers = event["headers"]
    ip_address = headers["X-Forwarded-For"]
    ip_array = ip_address.split(',')
    ip_address = ip_array[0]

    req = requests.get(f'http://ip-api.com/json/{ip_address}')
    location_data = req.json()

    now = datetime.now()
    time_stamp = now.strftime("%m/%d/%Y %H:%M:%S")
    
    table.put_item(Item={'IpAddress': ip_address, 'City': location_data["city"], 'Region': location_data["regionName"],"Lat": Decimal(str(location_data["lat"])), "Lon": Decimal(str(location_data["lon"])), "Time": time_stamp})
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "success"
        }),
    }
