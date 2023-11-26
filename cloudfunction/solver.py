import os
from dotenv import load_dotenv
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
import requests


parameters = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 1000
}
load_dotenv()
project_id = os.getenv("PROJECT_ID", None)
credentials = {
        #"url": "https://us-south.ml.cloud.ibm.com",
        "url":  "https://eu-de.ml.cloud.ibm.com",
        "apikey": os.getenv("API_KEY", None)
        }    
#this cell should never fail, and will produce no output
import requests

def getBearer(apikey):
    form = {'apikey': apikey, 'grant_type': "urn:ibm:params:oauth:grant-type:apikey"}
    print("About to create bearer")
#    print(form)
    response = requests.post("https://iam.cloud.ibm.com/oidc/token", data = form)
    if response.status_code != 200:
        print("Bad response code retrieving token")
        raise Exception("Failed to get token, invalid status")
    json = response.json()
    if not json:
        print("Invalid/no JSON retrieving token")
        raise Exception("Failed to get token, invalid response")
    print("Bearer retrieved")
    return json.get("access_token")

credentials["token"] = getBearer(credentials["apikey"])
from ibm_watson_machine_learning.foundation_models import Model
def call_model(text):
    model_id = ModelTypes.LLAMA_2_70B_CHAT
    # Initialize the Watsonx foundation model
    llm_model = Model(
        model_id=model_id, 
        params=parameters, 
        credentials=credentials,
        project_id=project_id)
    print("OK")
    prompt = f"""<s>[INST] <<SYS>> You have been given a text containing several questions from a test or exam. Your task is to create a document where each question is followed by its answer, provided by you (the AI). Use your knowledge to answer the questions as accurately as possible. For each question, print the question and write the answer below it, starting with "Answer:". The given text is as follows: {text} <</SYS>>[/INST]
    """
    result=llm_model.generate(prompt)['results'][0]['generated_text']
    return result

testing=False

if testing:
    text='''
    1. What ancient civilization is considered the birthplace of Western culture and is known for its contributions to philosophy, democracy, and the arts?
    2. Who was the famous conqueror who created one of the largest empires in history, stretching from Greece to Egypt and into present-day India?
    '''

    result=call_model(text)
    print(result)

