import json
import boto3
#teste 1
bedrock = boto3.client(
    service_name='bedrock',
    region_name='us-east-1'
)

bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

def lambda_handler(event, context):
    raw_body = event.get('body', '')
    json_body = json.loads(raw_body)
    input_value = json_body['input']
    body = "{\"inputText\":\"" + input_value + "\",\"textGenerationConfig\":{\"maxTokenCount\":8192,\"stopSequences\":[],\"temperature\":0,\"topP\":1}}"

    response = bedrock_runtime.invoke_model(
        body=body,
        modelId='amazon.titan-text-express-v1',
        accept='application/json',
        contentType='application/json'
    )

    response_body = json.loads(response.get('body').read())

    print(response_body)
    return {
        'statusCode': 200,
        'body': json.dumps({"Answer": response_body})
    }
