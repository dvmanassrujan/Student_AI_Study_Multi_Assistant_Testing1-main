"""
DeepSeek-Coder:1.3b Ollama Service Diagnostics & Verification Script
Verifies:
1. Ollama server connection (http://localhost:11434).
2. Presence and loading of deepseek-coder:1.3b.
3. Live inference across Coding, Algorithms, Educational Q&A, and Mathematics.
"""

import sys
try:
    import requests
except ImportError:
    requests = None
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.core.config import settings, OLLAMA_BASE_URL, OLLAMA_MODEL
from backend.core.llm import get_llm, check_ollama_connection
try:
    from langchain_core.messages import SystemMessage, HumanMessage
except ImportError:
    from backend.agents.orchestrator import SystemMessage, HumanMessage

def check_ollama():
    print("=" * 65)
    print("⚡ DeepSeek-Coder:1.3b Ollama Service Diagnostics")
    print("=" * 65)
    print(f"Target URL: {OLLAMA_BASE_URL}")
    print(f"Required Model: {OLLAMA_MODEL}")
    print("-" * 65)

    status = check_ollama_connection()
    print(f"Server Status: {'ONLINE' if status['connected'] else 'OFFLINE'}")
    print(f"Model Availability: {'READY' if status['model_available'] else 'NOT FOUND'}")
    print(f"Available Models: {status['models']}")
    print(f"Message: {status['message']}")
    print("-" * 65)

    if not status['connected']:
        print("❌ Ollama server is offline. Run: ollama serve")
        return False
    if not status['model_available']:
        print(f"⚠️ Model '{OLLAMA_MODEL}' missing. Run: ollama pull {OLLAMA_MODEL}")
        return False

    print("Executing Live DeepSeek-Coder:1.3b Educational & Coding Inference Tests...")
    try:
        llm = get_llm()

        # 1. Coding & DSA Test
        print("\n1. Testing Coding & DSA Assistance (Python Palindrome)...")
        c_msg = [
            SystemMessage(content="You are a Senior Coding Mentor. Provide clean code and brief explanation."),
            HumanMessage(content="Write a Python function to check if a string is a palindrome.")
        ]
        c_resp = llm.invoke(c_msg)
        print(f"✅ Code Output:\n{c_resp.content.strip()[:250]}...")

        # 2. Educational Q&A Test
        print("\n2. Testing Educational Q&A...")
        q_msg = [
            SystemMessage(content="You are an expert AI Teacher. Explain clearly and concisely in bullet points."),
            HumanMessage(content="Explain Binary Search in 2 short bullet points.")
        ]
        q_resp = llm.invoke(q_msg)
        print(f"✅ Q&A Output:\n{q_resp.content.strip()[:250]}...")

        # 3. Mathematics Test
        print("\n3. Testing Mathematical Problem Solving...")
        m_msg = [
            SystemMessage(content="You are a Math Tutor. State the formula and answer concisely."),
            HumanMessage(content="What is the derivative of f(x) = 3x^2 + 5x - 7?")
        ]
        m_resp = llm.invoke(m_msg)
        print(f"✅ Math Output:\n{m_resp.content.strip()[:250]}...")

        # 4. Summarization Test
        print("\n4. Testing Summarization...")
        s_msg = [
            SystemMessage(content="You are an academic summarizer. Provide 1 key takeaway."),
            HumanMessage(content="Summarize: Artificial neural networks learn patterns from data by adjusting synaptic weights through backpropagation.")
        ]
        s_resp = llm.invoke(s_msg)
        print(f"✅ Summary Output:\n{s_resp.content.strip()[:250]}...")

        print("\n" + "=" * 65)
        print("🎉 ALL OLLAMA DEEPSEEK-CODER:1.3B TESTS PASSED SUCCESSFULLY!")
        print("=" * 65)
        return True

    except Exception as e:
        print(f"\n❌ Error during Ollama inference: {e}")
        return False

if __name__ == "__main__":
    check_ollama()
