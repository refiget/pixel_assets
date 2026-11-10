#!/usr/bin/env python3
import argparse
import ipaddress
import json
import secrets
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW_PATH = PROJECT_ROOT / "ComfyUI/user/default/workflows/Pixel-Dragon-Local-api.json"


def request_json(url, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    headers = {} if payload is None else {"Content-Type": "application/json"}
    request = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description="Generate an image through the LAN ComfyUI API.")
    parser.add_argument("--host", required=True, help="ComfyUI host address, for example 192.168.1.170")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--output", type=Path, default=Path("lan-output"))
    args = parser.parse_args()

    host = ipaddress.ip_address(args.host)
    if host not in ipaddress.ip_network("192.168.1.0/24"):
        parser.error("--host must be in 192.168.1.x")

    base_url = f"http://{host}:8188"
    workflow = json.loads(WORKFLOW_PATH.read_text())
    seed = secrets.randbits(64) if args.seed is None else args.seed
    workflow["5"]["inputs"]["text"] = args.prompt
    workflow["8"]["inputs"]["noise_seed"] = seed
    workflow["14"]["inputs"]["filename_prefix"] = f"lan-api/{uuid.uuid4().hex}"

    queued = request_json(f"{base_url}/prompt", {"prompt": workflow})
    if queued.get("node_errors"):
        raise RuntimeError(json.dumps(queued["node_errors"], ensure_ascii=False))

    prompt_id = queued["prompt_id"]
    print(f"Queued {prompt_id}; seed={seed}")
    while True:
        history = request_json(f"{base_url}/history/{prompt_id}")
        result = history.get(prompt_id)
        if result is not None:
            status = result.get("status", {})
            if status.get("status_str") == "error":
                raise RuntimeError(json.dumps(status.get("messages", []), ensure_ascii=False))
            if status.get("completed"):
                break
        time.sleep(1)

    images = [
        image
        for node in result.get("outputs", {}).values()
        for image in node.get("images", [])
    ]
    if not images:
        raise RuntimeError("The workflow completed without producing an image.")

    args.output.mkdir(parents=True, exist_ok=True)
    for image in images:
        query = urllib.parse.urlencode(image)
        with urllib.request.urlopen(f"{base_url}/view?{query}") as response:
            image_data = response.read()
        output_path = args.output / Path(image["filename"]).name
        output_path.write_bytes(image_data)
        print(output_path.resolve())


if __name__ == "__main__":
    main()
