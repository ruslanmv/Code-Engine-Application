# Import necessary libraries
import streamlit as st
import ibm_boto3
from ibm_botocore.client import Config, ClientError
from io import BytesIO
import os
from dotenv import load_dotenv
from cloudfunction.watsonx import main as watsonx

# Constants for IBM COS values
load_dotenv()
credentials = {
        "COS_ENDPOINT": os.environ.get("COS_ENDPOINT", None),
        "COS_API_KEY_ID": os.environ.get("COS_API_KEY_ID", None),
        "COS_INSTANCE_CRN": os.environ.get("COS_INSTANCE_CRN", None),
        "COS_BUCKET": os.environ.get("COS_BUCKET", None),
        }

# Create IBM COS client
cos = ibm_boto3.client(
    "s3",
    ibm_api_key_id=credentials['COS_API_KEY_ID'],
    ibm_service_instance_id=credentials['COS_INSTANCE_CRN'],
    config=Config(signature_version="oauth"),
    endpoint_url=credentials['COS_ENDPOINT']
)

# Function to upload file to IBM COS
def FileUpload(bucket_name, item_name, file_obj):
    print("Creating new item: {0}".format(item_name))
    try:
        cos.upload_fileobj(
            Fileobj=file_obj,
            Bucket=bucket_name,
            Key=item_name
        )
        print("Item: {0} created!".format(item_name))
        return True
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
        return False
    except Exception as e:
        print("Unable to create text file: {0}".format(e))
        return False

# Streamlit App
def main():
    st.title("Questions Solver with IBM WatsonX")
    # File Upload
    uploaded_file = st.file_uploader("Choose a file to upload")
    if uploaded_file is not None:
        file_name = uploaded_file.name
        file_contents = uploaded_file.read()
        file_obj = BytesIO(file_contents)
        if FileUpload(credentials['COS_BUCKET'], file_name, file_obj):
            st.success(f"File '{file_name}' uploaded successfully!")
            # Process uploaded file
            payload = {
            "bucket_name": credentials['COS_BUCKET'],
            "object_name": file_name      
            }
            print("Payload", payload)
            response = watsonx(payload)
            st.success(f"Summary: '{response['body']}'")
        else:
            st.error(f"Failed to upload file '{file_name}'")

# Entry point for the application
if __name__ == "__main__":
    main()

