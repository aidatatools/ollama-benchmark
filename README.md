# ollama-benchmark
LLMs Throughput Benchmark for Ollama

## Installation Steps
```bash
pip3 install -r requirements.txt
```
It's tested on Python 3.9 and above.

## ollama installation with the following models installed
7B model can be run on machines with 8GB of RAM

13B model can be run on machines with 16GB of RAM

```bash
ollama run mistral:7b
ollama run llama2:7b
ollama run llama2:13b
ollama run llava:7b
ollama run llava:13b
```
## Step 1 (optional) : How to run test
```bash
jason@ubuntu:~/workspace/ollama-benchmark (main)
$ pwd
/home/jason/workspace/ollama-benchmark
jason@ubuntu:~/workspace/ollama-benchmark (main)
$ cd test
jason@ubuntu:~/workspace/ollama-benchmark/test (main)
$ python3 test_llm.py
```

## Step 2 (optional) : How to run benchmark performance test metrics (tokens/s) for one model
It's running in WSL2 on Windows 11
```bash
jason@ubuntu:~/workspace/ollama-benchmark (main)
$ cd ollama-benchmark/
jason@ubuntu:~/workspace/ollama-benchmark/ollama-benchmark (main)
$ python3 query_llm.py
model = llama2:7b
 total_duration time =   38344.98 ms
  load_duration time =     739.50 ms
   prompt eval time  =    4353.11 ms /     34 tokens
          eval time  =   33247.05 ms /    219 tokens
Performance:       6.59(tokens/s)
```

It's running on Apple Mac mini (Apple M1 Chip)
```bash
➜  ollama-benchmark git:(main) ✗ pwd
/Users/jason/workspace/ollama-benchmark
➜  ollama-benchmark git:(main) ✗ cd ollama-benchmark
➜  ollama-benchmark git:(main) ✗ python3 query_llm.py
model = llama2
 total_duration time =   23425.13 ms
  load_duration time =       0.63 ms
   prompt eval time  =     442.39 ms /     13 tokens
          eval time  =   22978.32 ms /    337 tokens
Performance:      14.67(tokens/s)
```
## Step 3 : How to check benchmark models installed on your machine
If you are on 8GB RAM machine, please comment out  - model: llama2:13b and - model: llava:13b
```bash
version: 1.0
models:
  - model: mistral:7b
  - model: llama2:7b
  #- model: llama2:13b
  - model: llava:7b
  #- model: llava:13b
```

```bash
jasontgi@M014-2312004:~/workspace/ollama-benchmark/ollama-benchmark (main)
$ python3 ./ollama-benchmark/check_models.py -h
jason@ubuntu:~/workspace/ollama-benchmark (main)
$ python3 ./ollama-benchmark/check_models.py -m data/benchmark_models.yml
args.models file path：data/benchmark_models.yml
```


## Reference
[Ollama](https://ollama.ai)