# Import required libraries
import streamlit as st
import ibm_boto3
from ibm_botocore.client import Config, ClientError
from io import BytesIO
import os
from dotenv import load_dotenv
from cloudfunction.watsonx import main as watsonx

# Load environment variables
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

# Function to upload a file to the specified IBM COS bucket
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

# Main function for the Streamlit app
def main():
    # Set page configuration
    st.set_page_config(
        page_title="Questions Solver with IBM WatsonX",
        page_icon=":question:",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    # Add custom CSS
    st.markdown(
        """
        <style>
            .menu {
                background-color: black;
                padding: 10px 20px;
                border-radius: 5px;
            }
            .menu h1 {
                color: white;
                margin: 0;
                padding: 0;
                font-size: 24px;
                font-weight: bold;
            }
            .title {
                font-size: 36px;
                font-weight: bold;
                color: #0f62fe;
            }
            .response-container {
                padding: 10px;
                background-color: white;
                border-radius: 5px;
            }
            body {
                background-color: #f0f0f0;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display title and menu
    st.markdown('<div class="menu"><h1>Questions Solver with IBM WatsonX</h1></div>', unsafe_allow_html=True)

    # File uploader
    uploaded_file = st.file_uploader("Choose a file to upload", type=["txt"], help="Upload a text")
    if uploaded_file is not None:
        file_name = uploaded_file.name
        file_contents = uploaded_file.read()
        file_obj = BytesIO(file_contents)
        
        # Upload the file and process the response
        if FileUpload(credentials['COS_BUCKET'], file_name, file_obj):
            st.markdown(f"<div style='color:#0f62fe'><strong>File '{file_name}' uploaded successfully!</strong></div>", unsafe_allow_html=True)
            payload = {
                "bucket_name": credentials['COS_BUCKET'],
                "object_name": file_name
            }
            print("Payload", payload)
            response = watsonx(payload)
            st.markdown(f"<div class='response-container'><strong>Response:</strong> <pre>{response['body']}</pre></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color:#da1e28'><strong>Failed to upload file '{file_name}'</strong></div>", unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()
