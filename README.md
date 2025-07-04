# llm-benchmark (ollama-benchmark)

LLM Benchmark for Throughput via Ollama (Local LLMs)

Measure how fast your local LLMs *really* are—with a simple, cross-platform CLI tool that tells you the tokens-per-second truth.

## Installation prerequisites

Working [Ollama](https://ollama.com) installation.

## Installation Steps

Depending on your python setup either

```bash
pip install llm-benchmark
```

or

```bash
pipx install llm-benchmark
```

## Usage for general users directly

```bash
llm_benchmark run
```

## Installation and Usage in Video format

![llm-benchmark](https://github.com/aidatatools/ollama-benchmark/blob/main/llm-benchmark.gif)

It's tested on Python 3.9 and above.

## ollama installation with the following models installed

7B model can be run on machines with 8GB of RAM

13B model can be run on machines with 16GB of RAM

## Usage explaination

On Windows, Linux, and macOS, it will detect memory RAM size to first download required LLM models.

When memory RAM size is greater than or equal to 4GB, but less than 7GB, it will check if gemma:2b exist. The program implicitly pull the model.

```bash
ollama pull deepseek-r1:1.5b
ollama pull gemma:2b
ollama pull phi:2.7b
ollama pull phi3:3.8b
```

When memory RAM size is greater than 7GB, but less than 15GB, it will check if these models exist. The program implicitly pull these models

```bash
ollama pull phi3:3.8b
ollama pull gemma2:9b
ollama pull mistral:7b
ollama pull llama3.1:8b
ollama pull deepseek-r1:8b
ollama pull llava:7b
```

When memory RAM size is greater than 15GB, but less than 31GB, it will check if these models exist. The program implicitly pull these models

```bash
ollama pull gemma2:9b
ollama pull mistral:7b
ollama pull phi4:14b
ollama pull deepseek-r1:8b
ollama pull deepseek-r1:14b
ollama pull llava:7b
ollama pull llava:13b
```

When memory RAM size is greater than 31GB, it will check if these models exist. The program implicitly pull these models

```bash
ollama pull phi4:14b
ollama pull deepseek-r1:14b
ollama pull deepseek-r1:32b
```

## Python Poetry manually(advanced) installation

<https://python-poetry.org/docs/#installing-manually>

## For developers to develop new features on Windows Powershell or on Ubuntu Linux or macOS

```bash
python3 -m venv .venv
. ./.venv/bin/activate
pip install -U pip setuptools
pip install poetry
```

## Usage in Python virtual environment

```bash
poetry shell
poetry install
llm_benchmark hello jason
```

### Example #1 send systeminfo and benchmark results to a remote server

```bash
llm_benchmark run
```

### Example #2 Do not send systeminfo and benchmark results to a remote server

```bash
llm_benchmark run --no-sendinfo
```

### Example #3 Benchmark run on explicitly given the path to the ollama executable (When you built your own developer version of ollama)

```bash
llm_benchmark run --ollamabin=~/code/ollama/ollama
```

### Example #4 run custom benchmark models

1. Create a custom benchmark file like following yaml format, replace with your own benchmark models, remember to use double quote for your model name

```yaml
file_name: "custombenchmarkmodels.yml"
version: 2.0.custom
models:
  - model: "deepseek-r1:1.5b"
  - model: "qwen:0.5b"
```

2. run with the flag and point to the path of custombenchmarkmodels.yml

```bash
llm_benchmark run --custombenchmark=path/to/custombenchmarkmodels.yml
```

## Reference

[Ollama](https://ollama.com)
