from dotenv import dotenv_values
config = dotenv_values(".env")
openai_api_key = config['OPENAI_API_KEY'] 
key = config['key']
secret = config['secret']
session_token = config['session_token']
comprehendAITeam = config['comprehendAITeam']
l1_model_arn = config['l1_model_arn']
l1_bucket_name = config['l1_bucket_name']
account_id = config['account_id']