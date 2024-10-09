import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set parameters for Azure OpenAI Service Whisper
openai.api_type = os.getenv("OPENAI_API_TYPE", "azure")
openai.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_version = os.getenv("OPENAI_API_VERSION")
deployment_id = os.getenv("AZURE_DEPLOYMENT_ID")

# Streamlit UI
st.title("Audio/Video Transcription using Whisper")

# File uploader for audio/video files
uploaded_file = st.file_uploader("Upload an audio or video file", type=["mp3", "wav", "m4a", "mp4"])

if uploaded_file is not None:
    # Define the path where the file will be saved
    audio_file_path = f"C:\\whisper\\{uploaded_file.name}"
    
    # Save uploaded file to the specified directory
    os.makedirs(os.path.dirname(audio_file_path), exist_ok=True)  # Ensure the directory exists
    with open(audio_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Read and transcribe the audio file
    with open(audio_file_path, "rb") as audio_file:
        try:
            transcript = openai.audio.transcriptions.create(
                model=deployment_id,
                file=audio_file
            )
            # Check if the response has a 'text' attribute
            if hasattr(transcript, 'text'):
                # Display transcription results
                st.subheader("Transcription:")
                st.write(transcript.text)
            else:
                st.error("Transcription text not found in the response.")
        except Exception as e:
            st.error(f"Error during transcription: {e}")
