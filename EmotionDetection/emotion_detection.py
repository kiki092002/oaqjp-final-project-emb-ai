import requests,json
def emotion_detector(text_to_analyze):
    
    url= 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header= {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj= { "raw_document": { "text": text_to_analyze } }
    response = requests.post(url, json = myobj, headers=header)
    formatted_response = json.loads(response.text)
    emotion = formatted_response['emotionPredictions'][0]['emotion']
    dominant_emotion = max(emotion,key=emotion.get)
    return dominant_emotion