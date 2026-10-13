"""Custom benchmark preflight against an Ollama-compatible HTTP server."""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

import ollama
import pytest
import yaml
from typer.testing import CliRunner

from llm_benchmark import check_models
from llm_benchmark.main import app


@pytest.fixture
def model_server():
    state = {"models": [], "pulls": [], "missing": set()}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            assert self.path == "/api/tags"
            body = json.dumps({"models": [{"model": name, "name": name}
                                        for name in state["models"]]}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            assert self.path == "/api/pull"
            payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            name = payload["model"]
            state["pulls"].append(name)
            status = 500 if name in state["missing"] else 200
            body = json.dumps({"error": "pull model manifest: file does not exist"}
                              if status == 500 else {"status": "success"}).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    client = ollama.Client(host=f"http://127.0.0.1:{server.server_port}", trust_env=False)
    with patch.object(check_models, "ollama", client):
        yield state
    server.shutdown()
    server.server_close()
    worker.join()


def model_file(tmp_path, names):
    path = tmp_path / "models.yml"
    path.write_text(yaml.safe_dump({"models": [{"model": name} for name in names]}))
    return path


def test_custom_benchmark_uses_existing_local_model(tmp_path, model_server):
    name = "my-modelfile:Q6_K-test"
    model_server["models"] = [name]
    model_server["missing"] = {name}
    path = model_file(tmp_path, [name])
    with (
        patch("llm_benchmark.main.sysmain.get_extra", return_value={
            "memory": 32, "cpu": "test", "gpu": "test", "os_version": "test"}),
        patch("llm_benchmark.main.check_ollama.check_ollama_version", return_value="test"),
        patch("llm_benchmark.main.run_benchmark.run_benchmark", return_value={}) as run,
        patch("llm_benchmark.main.connection.send_benchmark") as upload,
        patch("llm_benchmark.main.connection.send_sysinfo") as sys_upload,
    ):
        result = CliRunner().invoke(app, ["run", "--no-sendinfo", "--custombenchmark", str(path)])
    assert result.exit_code == 0, (result.output, result.exception)
    assert model_server["pulls"] == []
    assert run.call_args.args[0] == str(path)
    upload.assert_not_called()
    sys_upload.assert_not_called()


@pytest.mark.parametrize("requested, installed", [
    ("local-model", "local-model:latest"),
    ("local-model:latest", "local-model:latest"),
    ("registry:5000/team/model", "registry:5000/team/model:latest"),
    ("local-model:Q8", "local-model:Q8"),
])
def test_custom_preflight_recognizes_local_tags(tmp_path, model_server, requested, installed):
    model_server["models"] = [installed]
    model_server["missing"] = {requested}
    check_models.pull_models(str(model_file(tmp_path, [requested])), skip_existing=True)
    assert model_server["pulls"] == []


def test_custom_preflight_pulls_missing_model_only(tmp_path, model_server):
    model_server["models"] = ["local:latest"]
    check_models.pull_models(str(model_file(tmp_path, ["local", "registry-model"])), skip_existing=True)
    assert model_server["pulls"] == ["registry-model"]


def test_default_preflight_still_updates_installed_model(tmp_path, model_server):
    model_server["models"] = ["registry-model:latest"]
    check_models.pull_models(str(model_file(tmp_path, ["registry-model"])))
    assert model_server["pulls"] == ["registry-model"]


def test_custom_preflight_preserves_missing_model_error(tmp_path, model_server):
    model_server["missing"] = {"missing-custom"}
    with pytest.raises(ollama.ResponseError, match="file does not exist"):
        check_models.pull_models(str(model_file(tmp_path, ["missing-custom"])), skip_existing=True)
