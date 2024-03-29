import argparse
import yaml
import subprocess
import ollama

parser = argparse.ArgumentParser(
    prog="python3 check_models.py",
    description="Before running check_models.py, please make sure you installed ollama successfully \
        on macOS, Linux, or WSL2 on Windows. You can check the website: https://ollama.ai",
    epilog="Author: Jason Chuang")

parser.add_argument("-v",
                    "--verbose",
                    action="store_true",
                    help="this program helps you check whether you have ollama benchmark models installed")

parser.add_argument("-m",
                    "--models",
                    type=str,
                    help="provide benchmark models YAML file path. ex. ../data/benchmark_models.yml")

def parse_yaml(yaml_file_path):
    with open(yaml_file_path, 'r') as stream:
        try:
            data=yaml.safe_load(stream)
            #print(d)
        except yaml.YAMLError as e:
            print(e)
    return data

def pull_models(models_file_path):
    print(f"LLM models file path：{models_file_path}")
    print(f"Checking and pulling the following LLM models")
    models_dict = parse_yaml(models_file_path)
    for x in models_dict['models']:
        model_name = x['model']
        print(model_name)
        ollama.pull(model_name)

if __name__ == "__main__": 
    args = parser.parse_args()
    #print(f"args.verbose value：{args.verbose}")
    if (args.models is not None):
        print(f"args.models file path：{args.models}")
        models_dict = parse_yaml(args.models)
        for x in models_dict['models']:
            model_name = x['model']
            print(model_name)
            result = subprocess.run(['ollama', 'pull', model_name], stdout=subprocess.PIPE)
            result.stdout
    