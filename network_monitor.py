import time
import psutil
from threading import Lock

# Thread-safe shared state
_lock = Lock()
_state = {
    "upload_kbps": 0.0,
    "download_kbps": 0.0,
    "total_sent_mb": 0.0,
    "total_recv_mb": 0.0,
    "timestamp": None,
}

def _now():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def _get_counters():
    return psutil.net_io_counters()

def get_network_state():
    with _lock:
        return dict(_state)

def _update_state(upload_kbps, download_kbps, total_sent_mb, total_recv_mb):
    with _lock:
        _state.update({
            "upload_kbps": round(upload_kbps, 2),
            "download_kbps": round(download_kbps, 2),
            "total_sent_mb": round(total_sent_mb, 2),
            "total_recv_mb": round(total_recv_mb, 2),
            "timestamp": _now(),
        })

def start_network_monitor(interval=1):
    """Background loop to compute per-interval network speeds and totals."""
    prev = _get_counters()
    prev_time = time.time()
    # initialize totals
    total_sent_mb = prev.bytes_sent / (1024*1024)
    total_recv_mb = prev.bytes_recv / (1024*1024)
    _update_state(0.0, 0.0, total_sent_mb, total_recv_mb)

    while True:
        time.sleep(interval)
        cur = _get_counters()
        cur_time = time.time()
        dt = max(cur_time - prev_time, 1e-6)
        # bytes per second
        up_bps = (cur.bytes_sent - prev.bytes_sent) / dt
        down_bps = (cur.bytes_recv - prev.bytes_recv) / dt
        # convert to kilobytes per second
        upload_kbps = up_bps / 1024.0
        download_kbps = down_bps / 1024.0
        total_sent_mb = cur.bytes_sent / (1024*1024)
        total_recv_mb = cur.bytes_recv / (1024*1024)
        _update_state(upload_kbps, download_kbps, total_sent_mb, total_recv_mb)
        prev, prev_time = cur, cur_time
