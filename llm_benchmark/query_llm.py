import requests

headers = {
    'Content-Type': 'application/json',
}
#"model" : "phi"
#"model" : "llama2"
#"model" : "mistral"

data = '{\n  "model": "llama2:7b",\n  "prompt": "Why is the sky blue? Is it related to sunshine?",\n  "stream": false\n}'

response = requests.post('http://localhost:11434/api/generate', headers=headers, data=data)
jsonResponse = response.json()

model = ""
total_duration = 0.0
load_duration = 0.0
prompt_eval_count = 0
prompt_eval_duration = 0.0
eval_count = 0
eval_duration = 0.0
for key, value in jsonResponse.items():
    if (key=="response"):
        pass
    elif (key=="context"):
        pass
    elif (key=="model"):
        model = value
    elif (key=="total_duration"):
        total_duration = float(value)/(10**6)
    elif (key=="load_duration"):
        load_duration = float(value)/(10**6)
    elif (key=="prompt_eval_count"):
        prompt_eval_count=int(value)
    elif (key=="prompt_eval_duration"):
        prompt_eval_duration=float(value)/(10**6)
    elif (key=="eval_count"):
        eval_count=int(value)
    elif (key=="eval_duration"):
        eval_duration=float(value)/(10**6)

print(f"model = {model}")

print(f"{'total_duration time': >20} = {total_duration:10.2f} ms")
print(f"{'load_duration time': >20} = {load_duration:10.2f} ms")

print(f"{'prompt eval time ': >20} = {prompt_eval_duration:10.2f} ms / {prompt_eval_count:>6} tokens")    
print(f"{'eval time ': >20} = {eval_duration:10.2f} ms / {eval_count:>6} tokens ")
print(f"Performance: {eval_count/eval_duration*1000:10.2f}(tokens/s)")    
         
