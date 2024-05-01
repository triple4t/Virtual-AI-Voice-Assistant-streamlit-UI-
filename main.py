import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai
import base64


def setup_openai_config(api_key) :
    return openai.OpenAI(api_key= api_key)


def transcribe_audio(client, audio_path) :
    
    with open(audio_path, "rb") as audio_file :
        transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
        )
        return transcript.text
    

def fetch_ai_response (client, input_text) :
    messages = [{"role" : "user", "content" : input_text}]
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages = messages
    )

    return response.choices[0].message.content

def texttoaudio(client, input_text, audio_path) :
    response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input= input_text
    )
    response.stream_to_file(audio_path)



def main():

    st.sidebar.title("API Key Configuration :")

    api_key = st.sidebar.text_input("Enter your OpenAI API Key ", type= "password")

    st.title("AKIS Voice Assistant :")
    st.write("Hi there! click on the voice recorder to interact with me. How can I assist you?")
    # print(api_key)


    if api_key:
        client = setup_openai_config(api_key)
        recorded_audio = audio_recorder()
   

        if recorded_audio :

            audio_file = "audio.mp3"
            with open(audio_file, "wb") as f:
                f.write(recorded_audio)

            transcribe_text = transcribe_audio(client, audio_file)
            
            st.write("Transcribed text : ", transcribe_text)

            ans =  fetch_ai_response(client,transcribe_text)


            audiofile = "response.mp3"
            texttoaudio(client, ans, audiofile)
            st.audio(audiofile)
            st.write(ans)

            


if __name__ == "__main__":
    main()