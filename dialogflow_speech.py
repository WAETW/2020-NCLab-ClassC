import dialogflow_v2 as dialogflow
import pyaudio
import random
from mailing import *
'''開啟麥克風並透過Dialogflow內建的語音辨識功能來辨識'''
def detect_intent_stream():
    session = random.randint(0,10)
    project_id = '' # 你的dialogflow projectid
    session_id = str(session)
    language_code = 'zh-TW'
    session_client = dialogflow.SessionsClient()
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 44000
    session_path = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session_path))

    def request_generator(audio_config):
        query_input = dialogflow.types.QueryInput(audio_config=audio_config)
        query_params = dialogflow.types.QueryParameters(reset_contexts=True)
        yield dialogflow.types.StreamingDetectIntentRequest(
            session=session_path, query_params=query_params,query_input=query_input,single_utterance = True)

        audio = pyaudio.PyAudio()
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44000
        CHUNK = 4096
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        print("嗨")


        while True:
            chunk = stream.read(CHUNK,exception_on_overflow = False)
            if not chunk:
                break
            yield dialogflow.types.StreamingDetectIntentRequest(
                input_audio=chunk,single_utterance = True)
        stream.stop_stream()
        stream.close()
        audio.terminate()
    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)

    requests = request_generator(audio_config)
    responses = session_client.streaming_detect_intent(requests)

    print('=' * 20)
    for response in responses:
        print('Intermediate transcript: "{}".'.format(
                response.recognition_result.transcript))

    query_result = response.query_result

    print('=' * 20)
    print('語音辨識結果: {}'.format(query_result.query_text))
    print('動作: {} (confidence: {})\n'.format(
        query_result.intent.display_name,
        query_result.intent_detection_confidence))
    return response
def action_detection(response):
    action = response.query_result.action
    if action == 'help':
        print(1)
    else:
        print(0)
if __name__ == '__main__':
    response = detect_intent_stream()
    action_detection(response)
