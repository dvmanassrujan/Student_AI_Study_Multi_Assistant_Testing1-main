"""
Hugging Face Spaces & Local Root Entrypoint for Gradio SDK.
Automatically bootstraps Ollama on Hugging Face Spaces (Linux) with 16 GB RAM
and launches the Multi-Assistant Gradio UI.
"""

import os
import sys
import time
import subprocess
import shutil
from pathlib import Path

root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

def bootstrap_ollama_for_hf_spaces():
    """
    On Hugging Face Spaces (Gradio SDK), downloads user-space Ollama binary,
    starts the server in background, and pulls llama3.2:latest into the 16 GB RAM space.
    """
    print("=" * 60)
    print("🚀 Initializing Environment for Hugging Face Spaces (Gradio SDK)...")
    print("=" * 60)
    
    ollama_bin = shutil.which("ollama")
    if not ollama_bin:
        custom_bin = "/tmp/ollama_bin/bin/ollama"
        if not os.path.exists(custom_bin):
            print("Downloading user-space Ollama binary...")
            os.makedirs("/tmp/ollama_bin", exist_ok=True)
            subprocess.run(
                "curl -L https://ollama.com/download/ollama-linux-amd64.tar.gz | tar -xz -C /tmp/ollama_bin/",
                shell=True,
                check=False
            )
        ollama_bin = custom_bin

    # Ensure executable permissions
    if os.path.exists(ollama_bin):
        os.chmod(ollama_bin, 0o755)

    # Check if Ollama daemon is already running
    import urllib.request
    try:
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2)
        print("✅ Ollama daemon is already running.")
    except Exception:
        print("Starting Ollama daemon in background...")
        subprocess.Popen([ollama_bin, "serve"])
        time.sleep(5)

    # Ensure llama3.2:latest is pulled
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=3) as resp:
            import json
            data = json.loads(resp.read().decode())
            models = [m.get("name") for m in data.get("models", [])]
            if not any("llama3.2" in m for m in models):
                print("Pulling Meta Llama 3.2:latest model into Space...")
                subprocess.run([ollama_bin, "pull", "llama3.2:latest"], check=False)
            else:
                print("✅ Model 'llama3.2:latest' is already available in Ollama.")
    except Exception as e:
        print(f"Notice during model verification: {e}")
        subprocess.run([ollama_bin, "pull", "llama3.2:latest"], check=False)

    print("=" * 60)

# Check if running inside Hugging Face Spaces environment
if os.environ.get("SPACE_ID") or os.environ.get("HF_SPACE"):
    bootstrap_ollama_for_hf_spaces()

# Import the demo application from frontend
from frontend.app import demo

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port, allowed_paths=[str(root_dir)])

