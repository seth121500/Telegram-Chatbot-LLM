import json
import requests
import os

import datetime
import pytz

filename = "history.json"
if os.path.exists(filename):
    with open(filename, 'r') as file:
        history_data = json.load(file)
else:
    history_data = {'internal': [], 'visible': []}

history = {'internal': history_data['internal'], 'visible': history_data['visible']}


f = open('Coraline_Model.json')
data = json.load(f)

HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/chat'

# For reverse-proxied streaming, the remote will likely host with ssl - https://
# URI = 'https://your-uri-here.trycloudflare.com/api/v1/chat'




#current_date = datetime.datetime.now().strftime('%Y-%m-%d')
#context_with_current_date = context.replace('<Time>', current_date)
#print(context_with_current_date)


# Replace <message> with a history message
#history_message = "Nice to see you"
#context = context.replace("<message>", history_message)

#history = {'internal': [], 'visible': []}
def run(user_input, context):

    user_name = "Name"
    data['user_input'] = user_input
    data['history'] = history
    data['context'] = context
    data['your_name'] = user_name
    request = data


    response = requests.post(URI, json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['history']
        response_message = result['visible'][-1][1]

        user_message = f"{user_name}: {user_input}"
        response_entry = f"Coraline: {response_message}"

        history['internal'].append([user_message, response_entry])
        history['visible'].append([user_message, response_entry])

        with open(filename, 'w') as file:
            json.dump({'internal': history['internal'], 'visible': history['visible']}, file, indent=4)
            print(f"Message appended to {filename}.")

        print(context)
        return response_message







