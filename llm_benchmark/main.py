import typer
from systeminfo.main import get_total_memory_size


app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name}!")
    print(f"Total memory_size:{get_total_memory_size():.2f}GB")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
