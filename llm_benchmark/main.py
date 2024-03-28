import typer
from llm_benchmark import check_models
from systeminfo import main

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name}!")
    

@app.command()
def run(sendinfo: bool = False):
    print(f"Total memory size : {main.get_total_memory_size():.2f} GB")
    print(f"Get extra , os_version: {main.get_extra()['os_version']}")
    ft_mem_size = float(f"{main.get_total_memory_size():.2f}")
    models_file_path='data/benchmark_models_16gb_ram.yml'
    if(ft_mem_size>3.5 and ft_mem_size <7.5):
        models_file_path ='data/benchmark_models_4gb_ram.yml'
    elif(ft_mem_size>7.5 and ft_mem_size <15.5):
        models_file_path = 'data/benchmark_models_8gb_ram.yml'

    check_models.pull_models(models_file_path)



@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
