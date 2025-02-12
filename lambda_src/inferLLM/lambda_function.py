import json
import boto3
import os
import urllib.request

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = os.environ.get("BUCKET_NAME") 
    prompt_file_key = os.environ.get("PROMPT_FILE") 
    apikey_file_key  = os.environ.get("APIKEY_FILE")
    apiurl = os.environ.get("API_URL")

    s3_response_p = s3.get_object(Bucket=bucket_name, Key=prompt_file_key)
    prompt = s3_response_p['Body'].read().decode('utf-8')

    s3_response_a = s3.get_object(Bucket=bucket_name, Key=apikey_file_key)
    apikey = s3_response_a['Body'].read().decode('utf-8')

    parsed_body = json.loads(event['body'])
    input_value = parsed_body['input']

    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json"
    }
        
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_value}
        ],
        "temperature": 0.7
    }
        
    json_data = json.dumps(data).encode("utf-8")
    request = urllib.request.Request(
        apiurl,
        data=json_data,
        headers={
            "Authorization": f"Bearer {apikey}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(request) as response:
            response_data = response.read()
            result = json.loads(response_data)
            response_text = result["choices"][0]["message"]["content"]

        return {
            'statusCode': 200,
            'body': json.dumps({"Answer": response_text})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({"Error": str(e)})
        }
