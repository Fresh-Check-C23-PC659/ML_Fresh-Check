import requests
resp = requests.post("http://127.0.0.1:5000", files={'file': open('stale_banana.png', 'rb')})
# resp = requests.post("https://predictfruit-73izf5446q-as.a.run.app", files={'file': open('stale_orange.png', 'rb')})

if resp.status_code == 200:
    try:
        response_data = resp.json()
        print(response_data)
    except requests.exceptions.JSONDecodeError as e:
        print("Error decoding JSON response:", e)
else:
    print("Error:", resp.status_code, resp.text)

