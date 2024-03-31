import requests,json


remote_server = "http://llm.aidatatools.com"
#emote_server = "http://localhost:5000"

def send_sysinfo(data_dict):
    
    json_object = json.dumps(data_dict, indent = 4)
    print(json_object)
    print('-'*10)

    url = f'{remote_server}/api/receiver.php'

    x = requests.post(url, data = json_object)

    return x.text 

def send_benchmark(uuid, ollama_version,data_dict):
    data_dict.update({"uuid":f"{uuid}"})
    data_dict.update({"ollama_version":f"{ollama_version}"})
    json_object = json.dumps(data_dict, indent = 4)
    print(json_object)
    print('-'*10)

    url = f'{remote_server}/api/receiver_benchmark.php'

    x = requests.post(url, data = json_object)

    return x.text 