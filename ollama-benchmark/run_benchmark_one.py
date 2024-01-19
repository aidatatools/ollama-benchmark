import argparse
import yaml
import subprocess
import re

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

if __name__ == "__main__": 
    args = parser.parse_args()
    #print(f"args.verbose value：{args.verbose}")
    if (args.models is not None):
        #print(f"args.models file path：{args.models}")
        models_dict = parse_yaml(args.models)
        first_model_name = models_dict['models'][0]['model']
        print(first_model_name)
        result = subprocess.run(['ollama', 'run', first_model_name,f'"Why is the sky blue?"','--verbose','|','grep','eval'], stdout=subprocess.PIPE)
        out = result.stdout

        with open("tmp_out.txt", "wb") as binary_file:
            # Write bytes to file
            binary_file.write(out)
        
    