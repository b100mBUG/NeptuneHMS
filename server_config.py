from pathlib import Path
import json
from clinicapi import app
import uvicorn

def get_config_path():
    config_path = Path.home() / "ClinicManagerData" / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    return config_path

def start_api_server():
    config_path = get_config_path()

    if not config_path.exists():
        default_config = {
            "host": "127.0.0.1",
            "port": 8000,
            "reload": False
        }
        with open(config_path, "w") as f:
            json.dump(default_config, f, indent=4)

    with open(config_path) as f:
        config = json.load(f)

    uvicorn.run(
        app,
        host=str(config.get("host", "127.0.0.1")),
        port=int(config.get("port", 8000)),
        reload=bool(config.get("reload", False)),
    )

if __name__ == "__main__":
    start_api_server()
