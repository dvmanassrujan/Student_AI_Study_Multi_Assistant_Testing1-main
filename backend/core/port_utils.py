"""
Port Management and Conflict Resolution Utility.
Provides automatic detection, process inspection, and safe fallbacks
to resolve Gradio WinError 10048 and port conflicts on Windows, Linux, and macOS.
"""

import os
import sys
import socket
import logging
from typing import Optional, Dict, Any, Tuple, List

logger = logging.getLogger("port_utils")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def is_port_in_use(port: int, host: str = "0.0.0.0") -> bool:
    """
    Checks whether a port is currently in use and cannot be bound.
    Tests connect_ex, native bind attempt (without SO_REUSEADDR on Windows to detect WinError 10048),
    and active OS connection inspection.
    """
    # 1. Check if a server is actively accepting connections
    for connect_host in ("127.0.0.1", "localhost"):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.2)
                if s.connect_ex((connect_host, port)) == 0:
                    return True
        except Exception:
            pass

    # 2. Attempt binding to test address
    targets = [host]
    if host in ("0.0.0.0", "::"):
        targets.append("127.0.0.1")
    
    for test_host in targets:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Do NOT set SO_REUSEADDR on Windows, as that bypasses WinError 10048
                if os.name != "nt":
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((test_host, port))
        except OSError:
            return True
        except Exception:
            pass

    # 3. Check psutil active listening sockets
    try:
        import psutil
        for conn in psutil.net_connections(kind="inet"):
            if conn.laddr and conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                return True
    except Exception:
        pass

    return False


def is_port_available(port: int, host: str = "0.0.0.0") -> bool:
    """Returns True if the port is free to bind, False otherwise."""
    return not is_port_in_use(port, host)


def get_process_on_port(port: int) -> Optional[Dict[str, Any]]:
    """
    Inspects the OS network connections to find any process actively listening on the given port.
    Returns a dictionary with PID, process name, commandline, status, and create time, or None.
    """
    # 1. Try psutil first for detailed process metadata
    try:
        import psutil
        for conn in psutil.net_connections(kind="inet"):
            if conn.laddr and conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                pid = conn.pid
                if pid:
                    try:
                        p = psutil.Process(pid)
                        cmdline = " ".join(p.cmdline()[:4]) if p.cmdline() else ""
                        return {
                            "pid": pid,
                            "name": p.name(),
                            "cmdline": cmdline,
                            "status": p.status(),
                            "create_time": p.create_time()
                        }
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        return {
                            "pid": pid,
                            "name": "unknown (access denied)",
                            "cmdline": "",
                            "status": "listening",
                            "create_time": 0
                        }
    except Exception:
        pass

    # 2. Windows fallback using netstat
    if os.name == "nt":
        try:
            import subprocess
            cmd = f'netstat -ano | findstr :{port}'
            output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
            for line in output.strip().splitlines():
                parts = line.split()
                if len(parts) >= 5 and "LISTENING" in parts:
                    pid = int(parts[-1])
                    return {
                        "pid": pid,
                        "name": f"PID {pid}",
                        "cmdline": "",
                        "status": "LISTENING",
                        "create_time": 0
                    }
        except Exception:
            pass

    return None


def kill_process_on_port(port: int) -> bool:
    """
    Safely terminates the process occupying the specified port.
    Returns True if a process was found and terminated, False otherwise.
    """
    proc_info = get_process_on_port(port)
    if not proc_info or not proc_info.get("pid"):
        logger.warning(f"No active process found listening on port {port}.")
        return False

    pid = proc_info["pid"]
    logger.info(f"Terminating process on port {port} (PID {pid}: {proc_info.get('name')})...")

    try:
        import psutil
        p = psutil.Process(pid)
        p.terminate()
        try:
            p.wait(timeout=3)
            logger.info(f"Process {pid} terminated cleanly.")
            return True
        except psutil.TimeoutExpired:
            p.kill()
            logger.info(f"Process {pid} force-killed.")
            return True
    except Exception as e:
        logger.warning(f"psutil termination error: {e}. Trying system taskkill...")

    if os.name == "nt":
        import subprocess
        res = subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True, text=True)
        return res.returncode == 0

    return False


def find_available_port(
    preferred_port: int = 7860,
    fallback_port: int = 7861,
    max_search_range: int = 50,
    host: str = "0.0.0.0"
) -> Tuple[int, Optional[Dict[str, Any]]]:
    """
    Safely resolves an available port to eliminate WinError 10048.
    
    1. Checks preferred_port (default 7860). If available, returns (preferred_port, None).
    2. If occupied:
       - Checks AUTO_KILL_PORT_CONFLICT environment variable. If true, kills conflicting process.
       - Identifies existing process metadata (PID, name, cmdline) and logs diagnostic details.
       - Checks fallback_port (default 7861). If free, returns (fallback_port, conflict_proc).
       - Automatically scans ports in range (fallback_port+1 ... preferred_port+max_search_range).
       - Dynamically allocates an OS ephemeral port if all checked ports are busy.
    """
    # Check if user explicitly configured auto-kill
    if os.environ.get("AUTO_KILL_PORT_CONFLICT", "false").lower() in ("true", "1"):
        if is_port_in_use(preferred_port, host):
            kill_process_on_port(preferred_port)

    # 1. Check preferred port
    if is_port_available(preferred_port, host):
        return preferred_port, None

    # Inspect the process blocking preferred_port
    conflict_proc = get_process_on_port(preferred_port)
    if conflict_proc:
        proc_desc = f"PID {conflict_proc['pid']} ({conflict_proc['name']})"
        if conflict_proc.get("cmdline"):
            proc_desc += f" [cmd: {conflict_proc['cmdline']}]"
        logger.warning(f"⚠️  [Port Conflict] Port {preferred_port} is already occupied by {proc_desc} (WinError 10048 prevention).")
    else:
        logger.warning(f"⚠️  [Port Conflict] Port {preferred_port} is already occupied by an external service (WinError 10048 prevention).")

    # 2. Check fallback port (7861)
    if is_port_available(fallback_port, host):
        logger.info(f"✅ [Auto-Recovery] Falling back to port {fallback_port} to prevent conflict.")
        return fallback_port, conflict_proc

    fallback_proc = get_process_on_port(fallback_port)
    fallback_desc = f"PID {fallback_proc['pid']}" if fallback_proc else "an active service"
    logger.warning(f"⚠️  [Port Conflict] Fallback port {fallback_port} is also occupied by {fallback_desc}.")

    # 3. Automatically search subsequent ports
    start_port = max(preferred_port, fallback_port) + 1
    end_port = preferred_port + max_search_range
    for candidate in range(start_port, end_port + 1):
        if is_port_available(candidate, host):
            logger.info(f"✅ [Auto-Recovery] Found available port {candidate} automatically.")
            return candidate, conflict_proc

    # 4. OS Ephemeral port allocation as guaranteed fallback
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, 0))
            ephemeral_port = s.getsockname()[1]
            logger.info(f"✅ [Auto-Recovery] Dynamically bound to ephemeral port {ephemeral_port}.")
            return ephemeral_port, conflict_proc
    except Exception as e:
        logger.error(f"Failed to allocate ephemeral port: {e}. Defaulting to fallback {fallback_port}.")
        return fallback_port, conflict_proc


def launch_with_port_fallback(
    demo,
    preferred_port: int = 7860,
    fallback_port: int = 7861,
    server_name: str = "0.0.0.0",
    share: bool = True,
    allowed_paths: Optional[List[str]] = None,
    prevent_thread_lock: bool = True,
    **kwargs
) -> Tuple[Any, str, Optional[str], int]:
    """
    Safely launches a Gradio demo with automatic port conflict handling and retries.
    Returns (app, local_url, share_url, assigned_port).
    """
    port, conflict_proc = find_available_port(
        preferred_port=preferred_port,
        fallback_port=fallback_port,
        host=server_name
    )

    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            logger.info(f"Launching Gradio on {server_name}:{port} (share={share})...")
            launch_res = demo.launch(
                server_name=server_name,
                server_port=port,
                share=share,
                allowed_paths=allowed_paths,
                prevent_thread_lock=prevent_thread_lock,
                **kwargs
            )
            # demo.launch returns (app, local_url, share_url)
            if isinstance(launch_res, tuple) and len(launch_res) == 3:
                app, local_url, share_url = launch_res
                return app, local_url, share_url, port
            return demo.server_app, getattr(demo, "local_url", f"http://{server_name}:{port}"), getattr(demo, "share_url", None), port

        except OSError as e:
            # WinError 10048 / Address already in use
            if "10048" in str(e) or "already in use" in str(e).lower() or getattr(e, "winerror", None) == 10048:
                logger.warning(f"Port {port} encountered race condition conflict ({e}). Trying next port...")
                port, _ = find_available_port(preferred_port=port + 1, fallback_port=fallback_port + attempt + 1, host=server_name)
            else:
                raise e

    raise RuntimeError(f"Unable to bind Gradio to an available port after {max_attempts} attempts.")
