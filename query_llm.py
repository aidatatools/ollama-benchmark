import requests

headers = {
    'Content-Type': 'application/json',
}
#"model" : "phi"
#"model" : "llma2"
#"model" : "mistral"

data = '{\n  "model": "phi",\n  "prompt": "Why is the sky blue?",\n  "stream": false\n}'

response = requests.post('http://localhost:11434/api/generate', headers=headers, data=data)
jsonResponse = response.json()
print("Print each key-value pair from JSON response")
for key, value in jsonResponse.items():
    if not ((key=="response") or (key=="context")):
        print(f"{key} : {value}")
