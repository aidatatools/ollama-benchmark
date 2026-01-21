import argparse
import yaml
import subprocess
import datetime
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

parser.add_argument("--host",
                    type=str,
                    help="optional ollama http host, ex. http://127.0.0.1:11434")

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
        client = ollama.Client(host=args.host) if args.host else None

        loc_dt = datetime.datetime.today()
        # Writing to file
        with open(f'log_{loc_dt.strftime("%Y-%m-%d-%H%M%S")}.log', "w") as file1:
            for onemodel in models_dict['models']:
                model_name = onemodel['model']
                print(f'model_name =    {model_name}')
                file1.write(f'\nmodel_name =    {model_name}\n')

                if client:
                    response = client.generate(
                        model=model_name,
                        prompt="Why is the sky blue?",
                        stream=False
                    )
                    file1.write(str(response))
                    eval_count = response.get('eval_count')
                    eval_duration = response.get('eval_duration')
                    if eval_count and eval_duration:
                        rate = (eval_count * 1_000_000_000) / eval_duration
                        print(f"eval rate: {rate:.2f} tokens/s")
                        print(rate)
                else:
                    result = subprocess.run(['ollama', 'run', model_name,f'"Why is the sky blue?"','--verbose'], capture_output=True, text=True, check=True)
                    std_err = result.stderr
                    #print(result.stderr)
                    file1.write(std_err)

                    for line in std_err.split('\n'):
                        if ('eval rate' in line) and ('prompt' not in line):
                            print(line)
                            number = float(line[-20:-8])
                            print(number)


                print("-"*40)
                file1.write("\n"+"-"*40)
