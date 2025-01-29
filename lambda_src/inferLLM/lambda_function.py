import json
import boto3

bedrock = boto3.client(
    service_name='bedrock',
    region_name='us-east-1'
)

bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = 'awenaife-llm-config'
    prompt_file_key = 'prompt.txt'
    config_file_key = 'config.json'

    try:
        s3_response_p = s3.get_object(Bucket=bucket_name, Key=prompt_file_key)
        prompt = s3_response_p['Body'].read().decode('utf-8')
        s3_response_c = s3.get_object(Bucket=bucket_name, Key=config_file_key)
        config = s3_response_c['Body'].read().decode('utf-8')
        config_dict = json.loads(config)
        model_id = config_dict["modelId"]
        max_token_count = config_dict["maxTokenCount"]
        stop_sequences = config_dict["stopSequences"]
        temperature = config_dict["temperature"]
        top_p = config_dict["topP"]
        accept = config_dict["accept"]
        content_type = config_dict["contentType"]

        parsed_body = json.loads(event['body'])
        input_value = parsed_body['input']
        input_text = prompt + input_value

        body = json.dumps({
            "inputText": input_text,
            "textGenerationConfig": {
                "maxTokenCount": max_token_count,
                "stopSequences": stop_sequences,
                "temperature": temperature,
                "topP": top_p
            }
        })

        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=model_id,
            accept=accept,
            contentType=content_type
        )

        response_body = json.loads(response.get('body').read())

        return {
            'statusCode': 200,
            'body': json.dumps({"Answer": response_body})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({"Error": str(e)})
        }
