#!/usr/bin/env bash
# deploy.sh
set -euo pipefail
HOST=dymco99@192.168.1.105
DEST=/home/dymco99/Documents/programs/gimbal

rsync -az --delete \
  --exclude '.git' --exclude '__pycache__' --exclude '.venv' \
  ./ "$HOST:$DEST/"

ssh -tX "$HOST" "sudo apt-get install -y swig liblgpio-dev && cd $DEST && .venv/bin/pip install -r src/requirements.txt && .venv/bin/python -m src $*"