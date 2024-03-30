import requests,json

remote_server = "llm.aidatatools.com"

data = {}
data["uuid"]= f"d0a9ec51-60a1-5a2b-9a2b-4bcac27e0a95"
data["src_str"]= f"macOS|Apple M1|Apple M1|16.00"
data["encode"]= f"ZDBhOWVjNTEtNjBhMS01YTJiLTlhMmItNGJjYWMyN2UwYTk2"

json_object = json.dumps(data, indent = 4)

print(json_object)
print('-'*10)

url = f'http://{remote_server}/receiver.php'

x = requests.post(url, data = json_object)

print(x.text) 
