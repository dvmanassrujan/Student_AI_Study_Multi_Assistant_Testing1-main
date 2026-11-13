"""
Centralized Ollama & Local Hybrid Intelligence Adapter.
Targets local Ollama server running deepseek-coder:1.3b at http://localhost:11434,
with seamless zero-crash fallback to deterministic local Python intelligence engines.
Fully compatible with existing LangChain/LangGraph agent interfaces.
"""

import json
import logging
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional, Union

from backend.core.config import settings
from backend.intelligence.model_free_agent import (
    ModelFreeMessage,
    study_engine,
    classify_intent
)

# Configure module logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def check_ollama_connection() -> Dict[str, Any]:
    """
    Health check for the active Ollama server and deepseek-coder:1.3b model.
    Probes http://localhost:11434/api/tags.
    Returns structured connection status, model availability, and active models list.
    """
    target_model = settings.OLLAMA_MODEL or settings.MODEL_NAME or "deepseek-coder:1.3b"
    base_url = (settings.OLLAMA_BASE_URL or "http://localhost:11434").rstrip("/")

    try:
        req = urllib.request.Request(
            f"{base_url}/api/tags",
            headers={"User-Agent": "StudentAI-StudyAssistant/2.5"}
        )
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                models = [m.get("name", "") for m in data.get("models", [])]
                
                # Check for target model match (exact or prefix match, e.g. deepseek-coder:1.3b)
                target_base = target_model.split(":")[0].lower()
                target_clean = target_model.lower()
                model_found = any(
                    target_clean in m.lower() or (target_base in m.lower() and "1.3b" in m.lower())
                    for m in models
                )
                
                if model_found:
                    msg = f"Ollama server online at {base_url}. Model '{target_model}' loaded and ready."
                    logger.info(msg)
                    return {
                        'connected': True,
                        'model_available': True,
                        'message': msg,
                        'models': models
                    }
                else:
                    msg = (
                        f"Ollama server connected at {base_url}, but model '{target_model}' was not found. "
                        f"Available: {models}. Run: ollama pull {target_model}"
                    )
                    logger.warning(msg)
                    return {
                        'connected': True,
                        'model_available': False,
                        'message': msg,
                        'models': models
                    }

    except Exception as e:
        msg = (
            f"Ollama server unreachable at {base_url} ({e}). "
            f"Operating via local fallback engine for '{target_model}'. (To run Ollama: ollama run {target_model})"
        )
        logger.debug(msg)
        return {
            'connected': False,
            'model_available': False,
            'message': msg,
            'models': []
        }


class OllamaLLM:
    """
    Production-grade Ollama LLM adapter for deepseek-coder:1.3b.
    Implements standard LangChain BaseChatModel interface (`invoke`, `stream`, `__call__`).
    Directly communicates with Ollama's HTTP API (/api/chat and /api/generate).
    Gracefully and seamlessly falls back to local deterministic algorithms if the daemon is offline.
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: Optional[float] = None,
        timeout: Optional[int] = None
    ):
        self.model_name = model_name or settings.OLLAMA_MODEL or settings.MODEL_NAME or "deepseek-coder:1.3b"
        self.base_url = (base_url or settings.OLLAMA_BASE_URL or "http://localhost:11434").rstrip("/")
        self.temperature = float(temperature if temperature is not None else settings.LLM_TEMPERATURE)
        self.timeout = int(timeout or settings.LLM_TIMEOUT or 60)

    def _convert_messages_to_ollama(self, messages: Any) -> tuple:
        """Normalizes input messages into Ollama chat format and human prompt text."""
        chat_messages = []
        prompt_text = ""
        context_text = ""

        if isinstance(messages, list):
            for m in messages:
                role = "user"
                m_type = getattr(m, "type", "")
                m_role = getattr(m, "role", "")

                if m_type == "system" or m_role == "system":
                    role = "system"
                    context_text += str(getattr(m, "content", "")) + "\n"
                elif m_type in ("ai", "assistant") or m_role in ("ai", "assistant"):
                    role = "assistant"
                else:
                    role = "user"

                content = getattr(m, "content", "")
                if not content and isinstance(m, dict):
                    content = m.get("content", "")
                    m_dict_role = m.get("role") or m.get("type")
                    if m_dict_role:
                        role = m_dict_role

                content_str = str(content)
                chat_messages.append({"role": role, "content": content_str})
                if role == "user":
                    prompt_text = content_str

        elif isinstance(messages, str):
            prompt_text = messages
            chat_messages = [{"role": "user", "content": messages}]
        elif isinstance(messages, dict):
            prompt_text = str(messages.get("content", ""))
            chat_messages = [{"role": messages.get("role", "user"), "content": prompt_text}]
        else:
            prompt_text = str(messages)
            chat_messages = [{"role": "user", "content": prompt_text}]

        return chat_messages, prompt_text, context_text

    def invoke(self, messages: Any, **kwargs) -> ModelFreeMessage:
        """
        Executes inference via Ollama server (deepseek-coder:1.3b).
        If Ollama is unreachable, automatically routes to local deterministic intelligence.
        """
        chat_messages, prompt_text, context_text = self._convert_messages_to_ollama(messages)

        # 1. Attempt Live Ollama API Inference
        try:
            payload = {
                "model": self.model_name,
                "messages": chat_messages,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "top_p": settings.LLM_TOP_P,
                    "repeat_penalty": settings.LLM_REPEAT_PENALTY,
                    "num_ctx": settings.LLM_NUM_CTX,
                    "seed": settings.LLM_SEED,
                }
            }
            req = urllib.request.Request(
                f"{self.base_url}/api/chat",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json", "User-Agent": "StudentAI-StudyAssistant/2.5"}
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    ai_content = data.get("message", {}).get("content", "").strip()
                    if ai_content:
                        return ModelFreeMessage(content=ai_content)

        except Exception as e:
            logger.debug(f"Ollama direct API call not completed ({e}). Operating via deterministic engine fallback.")

        # 2. Seamless Deterministic Fallback Engine
        task_type = kwargs.get("task_type")
        next_agent = kwargs.get("next_agent")

        fallback_content = study_engine.process_prompt(
            prompt=prompt_text,
            task_type=task_type,
            next_agent=next_agent,
            context=context_text
        )
        return ModelFreeMessage(content=fallback_content)

    def stream(self, messages: Any, **kwargs):
        """Yields streaming response chunks from Ollama, or full response from fallback."""
        chat_messages, prompt_text, context_text = self._convert_messages_to_ollama(messages)

        try:
            payload = {
                "model": self.model_name,
                "messages": chat_messages,
                "stream": True,
                "options": {
                    "temperature": self.temperature,
                    "top_p": settings.LLM_TOP_P,
                    "repeat_penalty": settings.LLM_REPEAT_PENALTY,
                    "num_ctx": settings.LLM_NUM_CTX,
                    "seed": settings.LLM_SEED,
                }
            }
            req = urllib.request.Request(
                f"{self.base_url}/api/chat",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json", "User-Agent": "StudentAI-StudyAssistant/2.5"}
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                for line in resp:
                    if line:
                        chunk_data = json.loads(line.decode("utf-8"))
                        content = chunk_data.get("message", {}).get("content", "")
                        if content:
                            yield ModelFreeMessage(content=content)
            return

        except Exception as e:
            logger.debug(f"Streaming from Ollama unavailable ({e}). Streaming from fallback engine.")

        # Fallback single yield
        yield self.invoke(messages, **kwargs)

    def __call__(self, messages: Any, **kwargs) -> ModelFreeMessage:
        return self.invoke(messages, **kwargs)


# Backward-compatible alias
ModelFreeLLM = OllamaLLM


def get_llm(model_name: Optional[str] = None) -> OllamaLLM:
    """
    Factory function returning the centralized Ollama LLM adapter.
    Defaults to deepseek-coder:1.3b at http://localhost:11434 with deterministic fallback.

    Returns:
        OllamaLLM: Active LLM instance configured for deepseek-coder:1.3b.
    """
    target = model_name or settings.MODEL_NAME or settings.OLLAMA_MODEL or "deepseek-coder:1.3b"
    return OllamaLLM(model_name=target, temperature=settings.LLM_TEMPERATURE)
