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
    bucket_name = 'awenaife-llm-infer-prompt'
    file_key = 'prompt.txt'

    try:
        s3_response = s3.get_object(Bucket=bucket_name, Key=file_key)
        prompt = s3_response['Body'].read().decode('utf-8')
        

        parsed_body = json.loads(event['body'])
        input_value = parsed_body['input']

        teste = event['body']['input']
        print('event ---------> ', teste)
        
        input_text = prompt + input_value
        #body = "{\"inputText\":\"" + input_text + "\",\"textGenerationConfig\":{\"maxTokenCount\":8192,\"stopSequences\":[],\"temperature\":0,\"topP\":1}}"
        
        print('Prompt S3 ---------> ', prompt)
        print('input_value ---------> ', input_value)

        body = json.dumps({
            "inputText": input_text,
            "textGenerationConfig": {
                "maxTokenCount": 8192,
                "stopSequences": [],
                "temperature": 0,
                "topP": 1
            }
        })


        response = bedrock_runtime.invoke_model(
            body=body,
            modelId='amazon.titan-text-express-v1',
            accept='application/json',
            contentType='application/json'
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
