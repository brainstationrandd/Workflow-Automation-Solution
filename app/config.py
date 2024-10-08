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
l2_model_arn = config['l2_model_arn']
l2_bucket_name = config['l2_bucket_name']
local_pdf_directory = "data/uploaded_pdfs"
sub_category_threshold = 0.3
sns_topic_subscription_arn = config['sns_topic_subscription_arn']
sns_topic_arn = config['sns_topic_arn']
region_name = config['region_name']
MAILGUN_API_KEY = config['MAILGUN_API_KEY']
MAILGUN_DOMAIN = config['MAILGUN_DOMAIN']