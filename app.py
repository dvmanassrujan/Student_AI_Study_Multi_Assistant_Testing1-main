"""
Hugging Face Spaces & Local Root Entrypoint for Gradio SDK.
Automatically starts Ollama in the background on Hugging Face Spaces (16 GB RAM)
and launches the Multi-Assistant Gradio UI immediately to prevent startup timeouts.
"""

import sys
try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass

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
    _orig_env_init = jinja2.Environment.__init__
    def safe_env_init(self, *args, **kwargs):
        _orig_env_init(self, *args, **kwargs)
        self.cache = None
    jinja2.Environment.__init__ = safe_env_init

    _orig_load_template = jinja2.Environment._load_template
    def safe_load_template(self, name, globals=None):
        self.cache = None
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

# Compatibility Shim: Gradio Windows frpc tunnel .exe extension
try:
    import gradio.tunneling
    if os.name == "nt" and not gradio.tunneling.BINARY_PATH.endswith(".exe"):
        old_bin = gradio.tunneling.BINARY_PATH
        new_bin = old_bin + ".exe"
        if os.path.exists(old_bin) and not os.path.exists(new_bin):
            import shutil
            shutil.copy2(old_bin, new_bin)
        gradio.tunneling.BINARY_PATH = new_bin
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

def initialize_model_free_engine():
    """
    Initializes the 100% Model-Free, API-Free, and Cost-Free Intelligence Engine.
    Executes local Python algorithms, deterministic logic, and AST static analysis.
    """
    print("=" * 60)
    print("🚀 Model-Free Intelligence Engine Initialized")
    print("⚡ 100% Local • Zero-API • Zero-Cost • Fast Deterministic NLP & AST Engine")
    print("=" * 60)

initialize_model_free_engine()

# Import the main Gradio Blocks app from frontend/app.py
from frontend.app import demo
from frontend.ui_components import NEURAL_NEXUS_CSS

if __name__ == "__main__":
    from backend.core.port_utils import find_available_port, launch_with_port_fallback, get_process_on_port
    
    preferred_port = int(os.environ.get("PORT", 7860))
    fallback_port = int(os.environ.get("FALLBACK_PORT", 7861))

    # Resolve available port, automatically checking existing process and falling back to 7861
    assigned_port, conflict_proc = find_available_port(
        preferred_port=preferred_port,
        fallback_port=fallback_port
    )

    _, local_url, share_url, final_port = launch_with_port_fallback(
        demo,
        preferred_port=assigned_port,
        fallback_port=fallback_port,
        server_name="0.0.0.0",
        share=True,
        allowed_paths=[str(root_dir)],
        prevent_thread_lock=True,
        css=NEURAL_NEXUS_CSS
    )
    if share_url:
        with open("public_url.txt", "w", encoding="utf-8") as f:
            f.write(share_url)
        print("=" * 60, flush=True)
        print(f"🌐 PUBLIC URL: {share_url}", flush=True)
        print("=" * 60, flush=True)
    print(f"🚀 Server running on local: {local_url} (Port {final_port})", flush=True)
    demo.block_thread()
