import argparse
import yaml
import subprocess
import datetime
import pkg_resources

parser = argparse.ArgumentParser(
    prog="python3 check_models.py",
    description="Before running check_models.py, please make sure you installed ollama successfully \
        on macOS, Linux, or WSL2 on Windows. You can check the website: https://ollama.com",
    epilog="Author: Jason Chuang")

parser.add_argument("-v",
                    "--verbose",
                    action="store_true",
                    help="this program helps you check whether you have ollama benchmark models installed")

parser.add_argument("-m",
                    "--models",
                    type=str,
                    help="provide benchmark models YAML file path. ex. ../data/benchmark_models.yml")

parser.add_argument("-b",
                    "--benchmark",
                    type=str,
                    help="provide benchmark YAML file path. ex. ../data/benchmark1.yml")

parser.add_argument("-t",
                    "--type",
                    type=str,
                    help="provide benchmark model type. ex, instruct")


def parse_yaml(yaml_file_path):
    with open(yaml_file_path, 'r') as stream:
        try:
            data=yaml.safe_load(stream)
            #print(d)
        except yaml.YAMLError as e:
            print(e)
    return data

def run_benchmark(models_file_path, benchmark_file_path, type, ollamabin):
    
    models_dict = parse_yaml(models_file_path)
    benchmark_dict = parse_yaml(benchmark_file_path)
    model_type = type
    allowed_models = {e['model'] for e in models_dict['models']}
    #print(allowed_models)
    ans={}
    # Writing to file        
    for one_model_type in benchmark_dict['modeltypes']:
        #print(one_model_type)
        if (one_model_type['type']==model_type):
            #print(one_model_type['models'])
            #print(one_model_type['prompts'])
            for onemodel in one_model_type['models']:
                if (onemodel['model'] in allowed_models ):
                    loc_dt = datetime.datetime.today()
                    with open(f'log_{loc_dt.strftime("%Y-%m-%d-%H%M%S")}.log', "w", encoding='utf-8') as file1:
                        #print(onemodel)
                        stored_nums=[]
                        model_name = onemodel['model']
                        print(f'model_name =    {model_name}')
                        file1.write(f'\nmodel_name =    {model_name}\n')
                        
                        if model_name.startswith('llava'):
                            for one_prompt in one_model_type['prompts']:
                                img_file_names = one_prompt['keywords'].split(',')
                                for img in img_file_names:
                                    img_file_path = pkg_resources.resource_filename('llm_benchmark',f'data/img/{img}')
                                    prompt = f"{one_prompt['prompt']} {img_file_path}"
                                    print(f"prompt = {prompt}")
                                    result = subprocess.run([ollamabin, 'run', model_name, one_prompt['prompt'],'--verbose'], capture_output=True, text=True, check=True, encoding='utf-8')
                                    std_err = result.stderr
                                    #print(result.stderr)
                                    file1.write(std_err)
                                    
                                    for line in std_err.split('\n'):
                                        if ('eval rate' in line) and ('prompt' not in line):
                                            print(line)
                                            number = float(line[-20:-8])
                                            stored_nums.append(number)
                                            #print(number)
                        else:
                            for one_prompt in one_model_type['prompts']:
                                print(f"prompt = {one_prompt['prompt']}")
                                result = subprocess.run([ollamabin, 'run', model_name, one_prompt['prompt'],'--verbose'], capture_output=True, text=True, check=True, encoding='utf-8')
                                std_err = result.stderr
                                #print(result.stderr)                                   
                                file1.write(std_err)                                    
                                
                                for line in std_err.split('\n'):
                                    if ('eval rate' in line) and ('prompt' not in line):
                                        print(line)
                                        number = float(line[-20:-8])
                                        stored_nums.append(number)
                                        #print(number)

                        print("-"*20) 
                        if(len(stored_nums)!=0):       
                            average = sum(stored_nums)/len(stored_nums)
                            print("Average of eval rate: ", round(average,3), " tokens/s")
                            ans[f"{model_name}"]=f"{round(average,3):.2f}"

                        print("-"*40)
                        file1.write("\n"+"-"*40)
                    file1.close()
                    
    return ans

if __name__ == "__main__": 
    args = parser.parse_args()
    #print(f"args.verbose value：{args.verbose}")
    if (args.models is not None) and (args.benchmark is not None) and (args.type is not None):
        run_benchmark(args.models, args.benchmark, args.type)
        print('-'*40)
        
        