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
ollama run mistral
ollama run llama2
ollama run llama2:13b
ollama run llava
```
## How to run test
```bash
➜  ollama-benchmark git:(main) ✗ pwd
/Users/jason/workspace/ollama-benchmark
➜  ollama-benchmark git:(main) ✗ cd test
➜  test git:(main) ✗ python3 test_llm.py
```

## How to run benchmark to get performance metrics (tokens/s)
It's run on Apple Mac mini (Apple M1 CPU)
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

## Reference
[Ollama](https://ollama.ai)