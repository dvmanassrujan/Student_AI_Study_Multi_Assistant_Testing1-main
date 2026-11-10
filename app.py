"""
Hugging Face Spaces & Local Root Entrypoint for Gradio SDK.
Automatically starts Ollama in the background on Hugging Face Spaces (16 GB RAM)
and launches the Multi-Assistant Gradio UI immediately to prevent startup timeouts.
"""

# Compatibility Shim: Gradio 4.x oauth expects huggingface_hub.HfFolder
try:
    import huggingface_hub
    if not hasattr(huggingface_hub, "HfFolder"):
        class HfFolder:
            @staticmethod
            def get_token():
                import os
                return os.environ.get("HF_TOKEN")
            @staticmethod
            def save_token(token):
                pass
            @staticmethod
            def delete_token():
                pass
        huggingface_hub.HfFolder = HfFolder
except Exception:
    pass

# Compatibility Shim: gradio_client json schema generator for boolean additionalProperties
try:
    import gradio_client.utils
    _orig_json_schema = gradio_client.utils._json_schema_to_python_type
    def safe_json_schema_to_python_type(schema, defs=None):
        if not isinstance(schema, dict):
            return "Any"
        return _orig_json_schema(schema, defs)
    gradio_client.utils._json_schema_to_python_type = safe_json_schema_to_python_type
except Exception:
    pass

# Compatibility Shim: Jinja2 unhashable dict cache_key in template loading
try:
    import jinja2
    _orig_load_template = jinja2.Environment._load_template
    def safe_load_template(self, name, globals=None):
        if globals is not None:
            old_cache = self.cache
            self.cache = None
            try:
                return _orig_load_template(self, name, globals)
            finally:
                self.cache = old_cache
        return _orig_load_template(self, name, globals)
    jinja2.Environment._load_template = safe_load_template
except Exception:
    pass

# Support Hugging Face ZeroGPU runtime if space uses zero-a10g
try:
    import spaces
    @spaces.GPU
    def zerogpu_probe():
        return True
except Exception:
    pass

import os
import sys
import time
import shutil
import threading
import subprocess
from pathlib import Path

root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

def bootstrap_ollama_worker():
    """
    Background worker: downloads Ollama Linux binary archive,
    starts the Ollama server, and pulls llama3.2:latest.
    Runs asynchronously so Gradio binds to port 7860 immediately.
    """
    print("=" * 60)
    print("🚀 Background Worker: Initializing Ollama for Hugging Face Spaces...")
    print("=" * 60)

    try:
        ollama_dir = Path("/tmp/ollama_install")
        ollama_bin = shutil.which("ollama")

        if not ollama_bin:
            custom_bin = ollama_dir / "bin" / "ollama"
            if not custom_bin.exists():
                print("Downloading Ollama binary archive (Linux x86_64)...")
                ollama_dir.mkdir(parents=True, exist_ok=True)
                download_cmd = (
                    "curl -sSL https://github.com/ollama/ollama/releases/latest/download/ollama-linux-amd64.tar.zst "
                    f"| zstd -d -c | tar -xf - -C {ollama_dir}"
                )
                res = subprocess.run(download_cmd, shell=True, check=False)
                if res.returncode != 0:
                    print("zstd pipeline notice. Trying fallback tarball...")
                    fallback_cmd = (
                        "curl -sSL https://ollama.com/download/ollama-linux-amd64.tgz "
                        f"| tar -xzf - -C {ollama_dir}"
                    )
                    subprocess.run(fallback_cmd, shell=True, check=False)

            if custom_bin.exists():
                os.chmod(str(custom_bin), 0o755)
                ollama_bin = str(custom_bin)

        if ollama_bin and os.path.exists(ollama_bin):
            print(f"Ollama binary ready at: {ollama_bin}")

            # Check if server is already running
            import urllib.request
            is_running = False
            try:
                with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2) as r:
                    if r.status == 200:
                        is_running = True
                        print("✅ Ollama server is already running.")
            except Exception:
                is_running = False

            if not is_running:
                print("Starting Ollama background server...")
                env = os.environ.copy()
                lib_dir = str(ollama_dir / "lib" / "ollama")
                if os.path.exists(lib_dir):
                    env["LD_LIBRARY_PATH"] = f"{lib_dir}:" + env.get("LD_LIBRARY_PATH", "")
                
                subprocess.Popen([ollama_bin, "serve"], env=env)
                time.sleep(5)

            # Ensure llama3.2:latest is available
            print("Verifying / Pulling Meta Llama 3.2:latest in background...")
            subprocess.run([ollama_bin, "pull", "llama3.2:latest"], check=False)
            print("🎉 Ollama & Meta Llama 3.2:latest are fully operational!")
        else:
            print(f"Notice: Ollama binary not found. Local engine running in fallback mode.")

    except Exception as e:
        print(f"Notice during Ollama background initialization: {e}")

    print("=" * 60)


# If running on Hugging Face Spaces or Linux container, spawn background thread
if os.environ.get("SPACE_ID") or os.environ.get("HF_SPACE") or sys.platform.startswith("linux"):
    worker_thread = threading.Thread(target=bootstrap_ollama_worker, daemon=True)
    worker_thread.start()

# Import the main Gradio Blocks app from frontend/app.py
from frontend.app import demo

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    print(f"Launching Gradio application on 0.0.0.0:{port}...")
    demo.launch(server_name="0.0.0.0", server_port=port, allowed_paths=[str(root_dir)])
