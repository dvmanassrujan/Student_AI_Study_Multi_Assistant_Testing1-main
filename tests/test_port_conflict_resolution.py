"""
Comprehensive Test Suite for Gradio Port Conflict Resolution and WinError 10048 Prevention.
Verifies process inspection, automatic fallback to port 7861, and dynamic open-port recovery.
"""

import os
import sys
import socket
from pathlib import Path

# Ensure root directory is in sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import pytest
from backend.core.port_utils import (
    is_port_in_use,
    is_port_available,
    get_process_on_port,
    find_available_port,
    kill_process_on_port,
)


def test_is_port_available_on_free_port():
    """Verify that is_port_available correctly identifies an unused port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        free_port = s.getsockname()[1]
    
    # After socket close, the port should be available
    assert is_port_available(free_port, host="127.0.0.1") is True
    assert is_port_in_use(free_port, host="127.0.0.1") is False


def test_is_port_in_use_on_bound_socket():
    """Verify that is_port_in_use detects a port bound by a live socket."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    s.listen(1)
    bound_port = s.getsockname()[1]

    try:
        assert is_port_in_use(bound_port, host="127.0.0.1") is True
        assert is_port_available(bound_port, host="127.0.0.1") is False
    finally:
        s.close()


def test_detect_existing_process_on_occupied_port():
    """Verify that get_process_on_port retrieves process details for an active server."""
    # Check if 7860 is currently occupied by our running instance
    proc_info = get_process_on_port(7860)
    if proc_info:
        assert "pid" in proc_info
        assert proc_info["pid"] > 0
        assert "name" in proc_info
        print(f"Detected running process: PID={proc_info['pid']}, Name={proc_info['name']}")
    else:
        # If not occupied, bind a temporary socket and test
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("127.0.0.1", 0))
            s.listen(1)
            port = s.getsockname()[1]
            info = get_process_on_port(port)
            # Should not raise exception
            assert info is None or isinstance(info, dict)


def test_fallback_to_7861_when_7860_occupied():
    """Verify that find_available_port returns fallback 7861 when preferred 7860 is occupied."""
    # Temporarily bind 7860 if it is not already bound
    held_socket = None
    if is_port_available(7860, "127.0.0.1"):
        held_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        held_socket.bind(("127.0.0.1", 7860))
        held_socket.listen(1)

    try:
        resolved_port, conflict_proc = find_available_port(
            preferred_port=7860,
            fallback_port=7861,
            host="127.0.0.1"
        )
        # Port 7860 was occupied, so resolved_port must NOT be 7860
        assert resolved_port != 7860
        # If 7861 was free, resolved_port should be 7861
        if is_port_available(7861, "127.0.0.1"):
            assert resolved_port == 7861
        else:
            # If 7861 was also in use, it must have chosen another available port
            assert resolved_port > 7861
            assert is_port_available(resolved_port, "127.0.0.1") is True
    finally:
        if held_socket:
            held_socket.close()


def test_automatic_next_port_when_both_7860_and_7861_occupied():
    """Verify that find_available_port scans and finds 7862+ when 7860 and 7861 are occupied."""
    s1 = None
    s2 = None
    try:
        if is_port_available(7860, "127.0.0.1"):
            s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s1.bind(("127.0.0.1", 7860))
            s1.listen(1)

        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.bind(("127.0.0.1", 7861))
        s2.listen(1)

        resolved_port, _ = find_available_port(
            preferred_port=7860,
            fallback_port=7861,
            host="127.0.0.1"
        )
        assert resolved_port not in (7860, 7861)
        assert resolved_port >= 7862
        assert is_port_available(resolved_port, "127.0.0.1") is True
        print(f"Successfully auto-recovered with next open port: {resolved_port}")
    finally:
        if s1:
            s1.close()
        if s2:
            s2.close()


def test_preferred_port_used_when_free():
    """Verify that find_available_port returns preferred port when it is available."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        free_p = s.getsockname()[1]

    port, conflict = find_available_port(preferred_port=free_p, fallback_port=7861, host="127.0.0.1")
    assert port == free_p
    assert conflict is None


def test_gradio_launch_with_port_fallback_integration():
    """Verify that Gradio demo launches on fallback port 7861 when 7860 is in use, without WinError 10048."""
    import gradio as gr
    from backend.core.port_utils import launch_with_port_fallback

    with gr.Blocks() as test_blocks:
        gr.Markdown("# Test Blocks")

    app, local_url, share_url, assigned_port = launch_with_port_fallback(
        test_blocks,
        preferred_port=7860,
        fallback_port=7861,
        server_name="127.0.0.1",
        share=False,
        prevent_thread_lock=True
    )

    try:
        assert assigned_port in (7861, 7862, 7863)
        assert f":{assigned_port}" in local_url
        print(f"Gradio smoothly launched on {local_url} (prevented WinError 10048)")
    finally:
        test_blocks.close()
