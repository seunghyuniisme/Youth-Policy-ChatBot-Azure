from flask import Flask, request, jsonify, send_file, render_template, send_from_directory
from flask_cors import CORS
from openai import AzureOpenAI
import requests
import os
import logging
app = Flask(__name__)
CORS(app)
speaker_profile_id = None
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Azure OpenAI 설정
azure_oai_endpoint = 'https://hani-openai.openai.azure.com/'
azure_oai_key = '7a810a8e3cae4362810d8bb19f8e9324'
azure_oai_deployment = 'gpt-4o'

# Azure OpenAI 클라이언트 초기화
client = AzureOpenAI(
    azure_endpoint=azure_oai_endpoint,
    api_key=azure_oai_key,
    api_version="2024-02-15-preview"
)

# 시스템 메시지 로드 함수
def load_system_message(character):
    file_name = f"system_message_{character}.txt"
    file_path = os.path.join('prompts', file_name)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            system_message = file.read()
            print(f"Loaded system message for {character}: {system_message}")
            return system_message
    except FileNotFoundError:
        print(f"System message file not found for character: {character}")
        return "기본 시스템 메시지"


# 네아버 블로그 API 
def search_naver_blog(query):
    client_id = 'vTwwnYEG531P5MTPVUcv'
    client_secret = 'zpC7PzW6ms'
    url = "https://openapi.naver.com/v1/search/blog"
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    params = {
        'query': query,
        'display': 5,
        'start': 1
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        results = []
        for index, item in enumerate(data['items'], start=1):
            # HTML 형식으로 링크 생성
            link = f"{index}. <a href='{item['link']}' target='_blank'>{item['title']}</a>"
            results.append(link)
        # HTML 형식으로 결과를 반환
        return "<br>".join(results)
    else:
        return f"Error with Naver API: {response.status_code}"




# 대화 내역을 저장하기 위한 전역 변수
message_array = []

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# 기본 라우트
@app.route('/')
def index():
    return render_template('main.html')

# select.html 라우트 추가
@app.route('/select.html')
def select():
    return render_template('select.html')

# index.html 경로를 처리하는 라우트
@app.route('/index.html')
def index_html():
    return render_template('index.html')

# 정적 파일 경로 제공
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# 이미지 파일 경로 제공
@app.route('/image/<path:filename>')
def send_image(filename):
    return send_from_directory('static/image', filename)





#채팅
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('prompt')
        selected_character = request.json.get('character')

        if not user_input or not selected_character:
            return jsonify({"error": "No prompt or character provided"}), 400

        # 새로운 캐릭터 선택 시 시스템 메시지를 추가하되, 대화 내역은 유지
        system_message = load_system_message(selected_character)
        if message_array and message_array[0]["role"] == "system":
            message_array[0]["content"] = system_message  # 기존 시스템 메시지를 교체
        else:
            message_array.insert(0, {"role": "system", "content": system_message})  # 새로운 시스템 메시지를 추가

        # 리뷰 관련 입력 처리
        if '리뷰' in user_input:
            review_index = user_input.find('리뷰')
            search_query = user_input[:review_index].strip()

            if search_query:
                search_query += ' 청년'
            else:
                search_query = '청년 리뷰'

            naver_search_result = search_naver_blog(search_query)

            review_guide = ("아래는 네이버 블로그 검색🔍 기반의 리뷰 정보입니다.\n"
                            "링크를 클릭👆하면 관련 리뷰를 확인👀할 수 있습니다.\n\n")
            full_response = review_guide + naver_search_result

            # 리뷰 결과를 사용자에게 바로 전송
            return jsonify({"response": full_response})

        # Add user input to the message array
        message_array.append({"role": "user", "content": user_input})

        # Generate response from Azure OpenAI
        response = client.chat.completions.create(
            model=azure_oai_deployment,
            temperature=0.7,
            max_tokens=1200,
            messages=message_array
        )

        generated_text = response.choices[0].message.content

        # Add the AI response to the message array to keep the conversation going
        message_array.append({"role": "assistant", "content": generated_text})

        # Return the generated response as JSON
        return jsonify({"response": generated_text})

    except Exception as ex:
        # Check if the error is related to content filtering
        if 'content_filter_result' in str(ex):
            return jsonify({"error": "The content was filtered due to Azure OpenAI's content management policy."}), 400
        else:
            print(f"Exception occurred: {ex}")
            return jsonify({"error": str(ex)}), 500
        

        
#가장최근파일 출력하는 함수
@app.route('/latest-audio-file', methods=['GET'])
def latest_audio_file():
    try:
        file_name = get_latest_audio_file()
        if file_name:
            file_path = os.path.join('static', 'audio', file_name)
            if os.path.exists(file_path):
                logger.info(f"Streaming the latest audio file: {file_name}")
                return send_file(file_path, as_attachment=False)
            else:
                logger.error(f"Audio file not found: {file_name}")
                return jsonify({"error": "Audio file not found"}), 404
        else:
            return jsonify({"error": "No audio files found or an error occurred."}), 404
    except Exception as e:
        logger.error(f"Error processing request for latest audio file: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# 텍스트 오디오 기능전환
@app.route('/audio/convert', methods=['POST'])
def convert_audio():
    try:
        # 최신 텍스트 가져오기
        if not message_array or message_array[-1]["role"] != "assistant":
            return jsonify({"error": "No latest assistant message found"}), 400
        
        latest_text = message_array[-1]["content"]
        
        # 오디오 파일 생성
        audio_file_path = generate_audio(latest_text)
        if audio_file_path:
            # send_file 함수에서 attachment_filename을 download_name으로 변경
            return send_file(audio_file_path, mimetype='audio/wav', as_attachment=True, download_name='generated_audio.wav')
        else:
            return jsonify({"error": "Failed to generate audio"}), 500

    except Exception as ex:
        print(f"Error in convert_audio: {ex}")
        return jsonify({"error": str(ex)}), 500

# 텍스트를 받아 오디오 파일로 변환하는 함수
def generate_audio(text: str) -> str:
    global speaker_profile_id  # 전역 변수 사용
    try:
        if not speaker_profile_id:
            raise ValueError("Speaker profile ID is not set. Please create a personal voice first.")
        # Log speakerProfileId
        print(f'Using speaker profile ID: {speaker_profile_id}')
        
        # 텍스트를 음성으로 변환하여 파일 저장
        output_file_path = request_tts(text, speaker_profile_id)
        if output_file_path:
            return output_file_path
        else:
            raise Exception("Failed to generate audio using Azure TTS API.")
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None


#가장 최근 오디오파일 불러옴
def get_latest_audio_file(directory='static/audio/'):
    try:
        # 'static/audio/' 디렉토리에서 .wav 확장자를 가진 파일 목록을 가져옵니다.
        audio_files = [f for f in os.listdir(directory) if f.endswith('.wav')]
        if not audio_files:
            logger.error("No audio files found in the specified directory.")
            return None

        # 파일을 생성 시간 기준으로 정렬하고 가장 최근 파일을 선택합니다.
        latest_file = max(audio_files, key=lambda f: os.path.getctime(os.path.join(directory, f)))
        
        logger.info(f"Latest audio file found: {latest_file}")
        return latest_file
    except Exception as e:
        logger.error(f"Error getting latest audio file: {e}", exc_info=True)
        return None















##########################여기서부터 음성#######################################
#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.

import json
import requests
from time import sleep
import os
import logging
try:
    import customvoice
except ImportError:
    print('Pleae copy folder https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/custom-voice/python/customvoice and keep the same folder structure as github.' )
    quit()
import azure.cognitiveservices.speech as speechsdk

def speech_synthesis_to_wave_file(text: str, output_file_path: str, speaker_profile_id: str = None):
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=config.key, region=config.region)
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)
    file_config = speechsdk.audio.AudioOutputConfig(filename=output_file_path)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

    if speaker_profile_id:
        # speaker_profile_id가 있는 경우 해당 ID를 사용하는 SSML 생성
        ssml = (
            "<speak version='1.0' xml:lang='ko-KR' xmlns='http://www.w3.org/2001/10/synthesis' "
            "xmlns:mstts='http://www.w3.org/2001/mstts'>"
            "<voice name='DragonLatestNeural'>"
            f"<mstts:ttsembedding speakerProfileId='{speaker_profile_id}'/>"
            "<mstts:express-as style='Prompt'>"
            f"<lang xml:lang='ko-KR'>{text}</lang>"
            "</mstts:express-as>"
            "</voice></speak>"
        )
    else:
        # speaker_profile_id가 없는 경우 기본 목소리를 사용하는 SSML 생성
        ssml = (
            "<speak version='1.0' xml:lang='ko-KR'>"
            "<voice xml:lang='ko-KR' xml:gender='Female' name='ko-KR-JiMinNeural'>"
            f"{text}"
            "</voice></speak>"
        )

    def word_boundary(evt):
        print(f"Word Boundary: Text='{evt.text}', Audio offset={evt.audio_offset / 10000}ms, Duration={evt.duration / 10000}ms, text={evt.text}")

    speech_synthesizer.synthesis_word_boundary.connect(word_boundary)
    result = speech_synthesizer.speak_ssml_async(ssml).get()

    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized for text [{text}], and the audio was saved to [{output_file_path}]")
        print(f"result id: {result.result_id}")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
        print(f"result id: {result.result_id}")
#유효서검사
def retrieve_existing_speaker_profile_id(project_id: str, personal_voice_id: str) -> str:
    """
    이 함수는 기존의 personal voice ID를 사용하여 기존 speaker profile ID를 검색하고 반환합니다.
    """
    try:
        # 여기에 실제로 기존 speaker profile ID를 검색하는 로직을 추가하십시오.
        # 예시로, 프로젝트의 상태를 조회하거나 특정 API를 호출하여 값을 가져옵니다.
        # 아래의 코드는 예시이며 실제 구현에 맞게 수정해야 합니다.
        response = customvoice.PersonalVoice.get(config, personal_voice_id)
        if response and response.speaker_profile_id:
            return response.speaker_profile_id
        else:
            print("No existing speaker profile ID found.")
            return None
    except Exception as e:
        print(f"Error retrieving existing speaker profile ID: {e}")
        return None

#speaker_profile_id생성을 도와주는 함수
def create_personal_voice(project_id: str,
                          consent_id: str, consent_file_path: str, voice_talent_name: str, company_name: str,
                          personal_voice_id: str, audio_folder: str):
    try:
        # Create project
        project = customvoice.Project.create(config, project_id, customvoice.ProjectKind.PersonalVoice)
        print(f'Project created. project id: {project.id}')

        # Upload consent
        consent = customvoice.Consent.create(config, project_id, consent_id, voice_talent_name, company_name, consent_file_path, 'ko-KR')
        if consent.status == customvoice.Status.Failed:
            print(f'Create consent failed. consent id: {consent.id}')
            raise Exception
        elif consent.status == customvoice.Status.Succeeded:
            print(f'Create consent succeeded. consent id: {consent.id}')

        # Create personal voice
        personal_voice = customvoice.PersonalVoice.create(config, project_id, personal_voice_id, consent_id, audio_folder)
        if personal_voice.status == customvoice.Status.Failed:
            print(f'Create personal voice failed. personal voice id: {personal_voice.id}')
            raise Exception
        elif personal_voice.status == customvoice.Status.Succeeded:
            print(f'Create personal voice succeeded. personal voice id: {personal_voice.id}, speaker profile id: {personal_voice.speaker_profile_id}')

        # Check and log speaker profile ID
        if personal_voice.speaker_profile_id:
            print(f'Speaker Profile ID: {personal_voice.speaker_profile_id}')
        else:
            print('Speaker Profile ID not found.')
            raise ValueError("Speaker Profile ID was not created properly.")

        return personal_voice.speaker_profile_id

    except Exception as e:
        if "Resource Id already exists" in str(e):
            print("Resource already exists. Retrieving existing speaker profile ID...")
            # Implement logic to retrieve the existing speaker profile ID
            existing_speaker_profile_id = retrieve_existing_speaker_profile_id(project_id, personal_voice_id)
            if existing_speaker_profile_id:
                print(f'Retrieved existing speaker profile ID: {existing_speaker_profile_id}')
                return existing_speaker_profile_id
            else:
                raise ValueError("Failed to retrieve existing speaker profile ID.")
        else:
            raise e




def clean_up(project_id: str, consent_id: str, personal_voice_id: str):
    customvoice.PersonalVoice.delete(config, personal_voice_id)
    customvoice.Consent.delete(config, consent_id)
    customvoice.Project.delete(config, project_id)


region = 'eastus' # eastus, westeurope, southeastasia
key = '303e8feb39e949be9df0929bc0c93390'


logging.basicConfig(filename="customvoice.log",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

config = customvoice.Config(key, region, logger)


# project_id = 'personal-voice-project-1'
# consent_id = 'personal-voice-consent-1'
# personal_voice_id  = 'personal-voice-1'
project_id = 'test1'
consent_id = 'test1'
personal_voice_id  = 'test-speaker'

try:
    # step 1: create personal voice
    # Need consent file and audio file to create personal vocie.
    # This is consent file template.
    # I [voice talent name] am aware that recordings of my voice will be used by [company name] to create and use a synthetic version of my voice.
    # You can find sample consent file here
    # https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/CustomVoice/Sample%20Data/Individual%20utterances%20%2B%20matching%20script/VoiceTalentVerbalStatement.wav
    consent_file_path = r'TestData/agreement.wav'
    voice_talent_name = '서예건'
    company_name = '하니바람'

    # Need 5 - 90 seconds audio file.
    # You can find sample audio file here.
    # https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/CustomVoice/Sample%20Data/Individual%20utterances%20%2B%20matching%20script/SampleAudios.zip
    audio_folder = r'TestData/voice/'
    speaker_profile_id = create_personal_voice(project_id, 
                                            consent_id, consent_file_path, voice_talent_name, company_name,
                                            personal_voice_id, audio_folder)

    # step 2: synthesis wave
    text = '안녕하세요? 상쾌한 수요일 아침입니다.'
    output_wave_file_path = 'output_sdk.wav'
    speech_synthesis_to_wave_file(text, output_wave_file_path, speaker_profile_id)
except Exception as e:
    print(e)
    
    

# finally:
#     # Optional step 3: clean up, if you don't need this voice to synthesis more content.
#     clean_up(project_id, consent_id, personal_voice_id)
###############################################################ai speech가져오는부분 함수########################
import requests

# Azure Speech API 인증 정보
subscription_key = "303e8feb39e949be9df0929bc0c93390"
endpoint_id = "b134f8d5-2716-4f2e-abfe-62b1705deaf9"
region = "eastus"


# Azure Speech API 토큰을 얻는 함수
def get_token():
    endpoint = f"https://{region}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
    }

    response = requests.post(endpoint, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        return ''

def request_tts(text, speaker_profile_id):
    endpoint = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
    access_token = get_token()

    if not access_token:
        print("Failed to obtain access token.")
        return None

    headers = {
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
        "Authorization": f"Bearer {access_token}"
    }

    # SSML (Speech Synthesis Markup Language) 포맷
    ssml = (
        "<speak version='1.0' xml:lang='ko-KR' xmlns='http://www.w3.org/2001/10/synthesis' "
        "xmlns:mstts='http://www.w3.org/2001/mstts'>"
        f"<voice name='DragonLatestNeural'>"
        f"<mstts:ttsembedding speakerProfileId='{speaker_profile_id}'/>"
        "<mstts:express-as style='Prompt'>"
        f"<lang xml:lang='ko-KR'>{text}</lang>"
        "</mstts:express-as>"
        "</voice></speak>"
    )

    # 데이터를 UTF-8로 인코딩합니다.
    response = requests.post(endpoint, headers=headers, data=ssml.encode('utf-8'))

    if response.status_code == 200:
        file_name = 'static/audio/generated_audio.wav'
        with open(file_name, "wb") as audio_file:
            audio_file.write(response.content)
        return file_name
    else:
        print(f"Error during TTS request: {response.status_code}, {response.text}")
        return None


if __name__ == '__main__':
    if speaker_profile_id is None:
        speaker_profile_id = create_personal_voice(project_id, consent_id, consent_file_path, voice_talent_name, company_name, personal_voice_id, audio_folder)
    
    app.run(debug=True)
