import json
from lambda_function import lambda_handler

with open("/Users/jean/github/awenaife_backend/lambda_src/inferLLM/event.json", "r") as f:
    event = json.load(f)

response = lambda_handler(event, None)

print(json.dumps(response, indent=4))