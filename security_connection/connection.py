import requests,json


remote_server = "https://llm.aidatatools.com"
#remote_server = "http://localhost:5000"

def send_sysinfo(data_dict):
    
    json_object = json.dumps(data_dict, indent = 4)
    print(json_object)
    print('-'*10)

    url = f'{remote_server}/api/receiver.php'

    x = requests.post(url, data = json_object)

    return x.text 
