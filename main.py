import json
import os
import requests
import settings


def text_to_speech(text='Привет друг!'):
    headers = {
        "Authorization": f"Bearer {settings.KEY}"}
    url = "https://api.edenai.run/v2/audio/text_to_speech"

    payload = {
        'providers': 'lovoai',
        'language': 'ru-RU',
        'option': 'FEMALE',
        'lovoai': 'ru-RU_Anna Kravchuk',
        'text': f'{text}'
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)

    with open(f'response.json', 'w') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    audio_url = result.get('lovoai').get('audio_resource_url')
    r = requests.get(audio_url)

    with open('speech.wav', 'wb') as file:
        file.write(r.content)


if __name__ == '__main__':
    text_to_speech()
