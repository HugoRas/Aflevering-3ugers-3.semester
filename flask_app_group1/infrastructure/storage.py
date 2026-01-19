import os


def _cfg_get(cfg, key):
    return cfg[key] if isinstance(cfg, dict) else getattr(cfg, key)


def ensure_dirs(cfg):
    os.makedirs(_cfg_get(cfg, "RAW_DIR"), exist_ok=True)
    os.makedirs(_cfg_get(cfg, "FILTERED_DIR"), exist_ok=True)
    os.makedirs(_cfg_get(cfg, "PLOTS_DIR"), exist_ok=True)
    os.makedirs(_cfg_get(cfg, "LOG_DIR"), exist_ok=True)


def recording_raw_dir(cfg, recording_id: int) -> str:
    base = _cfg_get(cfg, "RAW_DIR")
    path = os.path.join(base, str(recording_id))
    os.makedirs(path, exist_ok=True)
    return path
