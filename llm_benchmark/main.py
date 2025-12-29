import typer, base64
from llm_benchmark import check_models
from llm_benchmark import check_ollama
from llm_benchmark import run_benchmark

from .systeminfo import sysmain

from .security_connection import connection

from importlib.resources import files


app = typer.Typer()

@app.command()
def hello(name: str):
    print(f"Hello {name}!")
    

@app.command()
def run(
    ollamabin: str = typer.Option('ollama', "--ollamabin"),
    sendinfo: bool = typer.Option(True, "--sendinfo/--no-sendinfo"),
    custombenchmark: str = typer.Option(None, "--custombenchmark")
):
    sys_info = sysmain.get_extra()
    print(f"Total memory size : {sys_info['memory']:.2f} GB") 
    print(f"cpu_info: {sys_info['cpu']}")
    print(f"gpu_info: {sys_info['gpu']}")
    print(f"os_version: {sys_info['os_version']}")

    ollama_version = check_ollama.check_ollama_version(ollamabin)
    print(f"ollama_version: {ollama_version}")
    print('-'*10)

    ft_mem_size = float(f"{sys_info['memory']:.2f}")

    if custombenchmark:
        models_file_path = custombenchmark
        sendinfo = False
        print(f"running custom benchmark from models_file_path: {models_file_path}")
        print(f"Disabling sendinfo for custom benchmark")
    else:
        models_file_path = str(files('llm_benchmark').joinpath('data/benchmark_models_32gb_ram.yml'))
        if(ft_mem_size>=1 and ft_mem_size <2):
            models_file_path = str(files('llm_benchmark').joinpath('data/benchmark_models_2gb_ram.yml'))
        elif(ft_mem_size>=2 and ft_mem_size <4):
            models_file_path = str(files('llm_benchmark').joinpath('data/benchmark_models_3gb_ram.yml'))
        elif(ft_mem_size>=4 and ft_mem_size <7):
            models_file_path = str(files('llm_benchmark').joinpath('data/benchmark_models_4gb_ram.yml'))
        elif(ft_mem_size>=7 and ft_mem_size <15):
            models_file_path = str(files('llm_benchmark').joinpath('data/benchmark_models_8gb_ram.yml'))
        elif(ft_mem_size>=15 and ft_mem_size <31):
            models_file_path = str(files('llm_benchmark').joinpath('data/benchmark_models_16gb_ram.yml'))

    check_models.pull_models(models_file_path)
    print('-'*10)

    benchmark_file_path = str(files('llm_benchmark').joinpath('data/benchmark2.yml'))

    bench_results_info = {}
    is_simulation = False
    if custombenchmark:
        result0 = run_benchmark.run_benchmark(models_file_path,benchmark_file_path, 'custom-model', ollamabin)
        bench_results_info.update(result0)
    elif is_simulation==False :
        result1 = run_benchmark.run_benchmark(models_file_path,benchmark_file_path, 'instruct', ollamabin)
        bench_results_info.update(result1)
        result2 = run_benchmark.run_benchmark(models_file_path,benchmark_file_path, 'question-answer', ollamabin)
        bench_results_info.update(result2)
        result3 = run_benchmark.run_benchmark(models_file_path,benchmark_file_path, 'vision-image', ollamabin)
        bench_results_info.update(result3)
        result4 = run_benchmark.run_benchmark(models_file_path,benchmark_file_path, 'instruction-question-answer-code-generation', ollamabin)
        bench_results_info.update(result4)
    else:
        bench_results_info.update({"llama2:7b":7.65})
        bench_results_info.update({"gemma2:7b":17.77})

    if (sendinfo==True):
        print(f"Sending the following data to a remote server")
        print(f"Your machine UUID : {sysmain.get_uuid()}")
        #print(f"{bench_results_info.items()}")
        x = connection.send_benchmark(sysmain.get_uuid(),ollama_version,bench_results_info)
        #print(x)
        print('=='*10)
        #print(f"{sys_info.items()}")
        sys_info = sysmain.get_extra()
        sys_info['uuid']=f"{sysmain.get_uuid()}"
        x = connection.send_sysinfo(sys_info)
        #print(x)


@app.command()
def goodbye(name: str, formal: bool = typer.Option(False, "--formal")):
    if formal:
        print(f"Goodbye Mr.(Ms.) {name}. Have a good day.")
    else:
        print(f"Bye {name}!")

@app.command()
def sysinfo(formal: bool = typer.Option(True, "--formal")):
    if formal:
        sys_info = sysmain.get_extra()
        sys_info['uuid'] = f"{sysmain.get_uuid()}"
        #print(sys_info.items())
        print(f"memory : {sys_info['memory']:.2f} GB") 
        print(f"cpu_info: {sys_info['cpu']}")
        print(f"gpu_info: {sys_info['gpu']}")
        print(f"os_version: {sys_info['os_version']}")
        print(f"Your machine UUID : {sys_info['uuid']}")

        x = connection.send_sysinfo(sys_info)
        print(x)
    else:
        print(f"No print!")


if __name__ == "__main__":
    app()
