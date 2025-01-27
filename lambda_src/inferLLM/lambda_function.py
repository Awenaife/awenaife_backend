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

def lambda_handler(event, context):
    try:
        # Retrieve the raw body from the event
        raw_body = event.get('body', '')

        # Ensure the body is not empty
        if not raw_body:
            raise ValueError("Request body is empty.")

        # Parse the JSON body
        try:
            json_body = json.loads(raw_body)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON in the request body.")

        # Ensure the 'input' key exists
        input_value = json_body.get('input')
        if input_value is None:
            raise ValueError("The 'input' field is missing in the JSON body.")

        # Construct the body for Bedrock model invocation
        body = json.dumps({
            "inputText": input_value,
            "textGenerationConfig": {
                "maxTokenCount": 8192,
                "stopSequences": [],
                "temperature": 0,
                "topP": 1
            }
        })

        # Invoke the model
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId='amazon.titan-text-express-v1',
            accept='application/json',
            contentType='application/json'
        )

        # Parse the response body from Bedrock
        response_body = json.loads(response.get('body').read())

        # Return the response
        return {
            'statusCode': 200,
            'body': json.dumps({"Answer": response_body})
        }

    except Exception as e:
        # Handle any errors and return an appropriate response
        print(f"Error: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({"error": str(e)})
        }