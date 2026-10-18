"""Prompt operands must not be interpreted as Ollama command-line options."""

import json
import os
import shlex
import subprocess
import sys

import pytest
import yaml

from llm_benchmark import run_benchmark


pytestmark = pytest.mark.skipif(os.name != "posix", reason="POSIX executable/wrapper regression")


@pytest.fixture
def fake_ollama(tmp_path, monkeypatch):
    record = tmp_path / "arguments.jsonl"
    executable = tmp_path / "ollama"
    executable.write_text(
        "#!" + sys.executable + "\n"
        + """
import argparse
import json
import os
import sys

if sys.argv[1] == "stop":
    sys.exit(0)
parser = argparse.ArgumentParser()
parser.add_argument("command", choices=["run"])
parser.add_argument("model")
parser.add_argument("prompt", nargs="+")
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()
with open(os.environ["OLLAMA_ARG_RECORD"], "a", encoding="utf-8") as stream:
    stream.write(json.dumps({"prompt": " ".join(args.prompt), "verbose": args.verbose}) + "\\n")
if not args.verbose:
    sys.exit(3)
print("eval rate:            21.00 tokens/s", file=sys.stderr)
""",
        encoding="utf-8",
    )
    executable.chmod(0o755)
    monkeypatch.setenv("OLLAMA_ARG_RECORD", str(record))
    monkeypatch.setenv("PATH", str(tmp_path) + os.pathsep + os.environ.get("PATH", ""))
    monkeypatch.chdir(tmp_path)
    return executable, record


def write_benchmark(tmp_path, model, prompt):
    models = {"models": [{"model": model}]}
    benchmarks = {"modeltypes": [{
        "type": "instruct",
        "models": models["models"],
        "prompts": [{"prompt": prompt, "keywords": "image.png"}],
    }]}
    model_file = tmp_path / "models.yml"
    benchmark_file = tmp_path / "benchmark.yml"
    model_file.write_text(yaml.safe_dump(models), encoding="utf-8")
    benchmark_file.write_text(yaml.safe_dump(benchmarks, allow_unicode=True), encoding="utf-8")
    return model_file, benchmark_file


@pytest.mark.parametrize("model", ["fixture:latest", "llava:latest"])
@pytest.mark.parametrize("prompt", [
    "--help",
    "-leading prompt",
    "-> a leading arrow",
    "Translate -> Artificial intelligence",
    "请翻译 -> Hello 世界",
    "first line\nsecond  line -> text",
])
def test_prompt_is_literal_data(tmp_path, fake_ollama, model, prompt):
    executable, record = fake_ollama
    model_file, benchmark_file = write_benchmark(tmp_path, model, prompt)

    result = run_benchmark.run_benchmark(
        str(model_file), str(benchmark_file), "instruct", str(executable)
    )

    assert result == {model: "21.00"}
    assert json.loads(record.read_text(encoding="utf-8").splitlines()[0]) == {
        "prompt": prompt, "verbose": True,
    }


@pytest.mark.parametrize("model", ["fixture:latest", "llava:latest"])
def test_forwarded_translation_prompt_does_not_become_an_option(tmp_path, fake_ollama, model):
    executable, record = fake_ollama
    wrapper = tmp_path / "wrapper"
    wrapper.write_text("#!/bin/sh\nexec " + shlex.quote(str(executable)) + " $*\n")
    wrapper.chmod(0o755)
    prompt = "Translate the following English paragraph into Chinese -> Artificial intelligence."
    model_file, benchmark_file = write_benchmark(tmp_path, model, prompt)

    result = run_benchmark.run_benchmark(
        str(model_file), str(benchmark_file), "instruct", str(wrapper)
    )

    assert result == {model: "21.00"}
    assert json.loads(record.read_text(encoding="utf-8").splitlines()[0]) == {
        "prompt": prompt, "verbose": True,
    }


def test_standalone_benchmark_still_collects_verbose_metrics(tmp_path, fake_ollama):
    _, record = fake_ollama
    model_file, _ = write_benchmark(tmp_path, "fixture:latest", "unused")
    result = subprocess.run(
        [sys.executable, "-m", "llm_benchmark.run_benchmark_one", "--models", str(model_file)],
        capture_output=True, text=True, check=True, encoding="utf-8",
    )
    assert "21.0" in result.stdout
    assert json.loads(record.read_text(encoding="utf-8").splitlines()[0])["verbose"] is True
