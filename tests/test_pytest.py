import requests
# test_typer.py
from typer.testing import CliRunner
from llm_benchmark.main import app

#"model" : "gemma:2b"
#"model" : "gemma:7b"

def test_localhost_ollama():
    # This test is preventing WSL2 to connect to Windows version of Ollama
    url = "http://127.0.0.1:11434/"
    response = requests.get(url)
    rtext = response.text
    assert rtext.strip() == "Ollama is running"

def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(app, ['hello','World'])
    assert result.exit_code == 0
    assert 'Hello World!' in result.output

