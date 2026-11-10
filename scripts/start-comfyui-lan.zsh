#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="${0:A:h}"
PROJECT_ROOT="${SCRIPT_DIR:h}"
COMFYUI_ROOT="${COMFYUI_ROOT:-$HOME/ComfyUI-Installs/ComfyUI/ComfyUI}"
LAN_IP="$(/usr/sbin/ipconfig getifaddr en0)"

case "$LAN_IP" in
  192.168.1.*) ;;
  *)
    print -u2 "en0 must have a 192.168.1.x address; found: $LAN_IP"
    exit 1
    ;;
esac

print "ComfyUI LAN API: http://${LAN_IP}:8188"
cd "$COMFYUI_ROOT"
exec .venv/bin/python main.py \
  --listen "$LAN_IP" \
  --port 8188 \
  --extra-model-paths-config "$PROJECT_ROOT/ComfyUI/extra_model_paths.yaml" \
  --output-directory "$PROJECT_ROOT/assets/generated/dragon-girl/local-comfyui" \
  --disable-auto-launch
