#!/usr/bin/env bash
set -euo pipefail

# Local project installer.
# It prepares Python virtual environment and installs dependencies.
# Run from repository root.

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example. Fill tokens before starting bots."
fi

mkdir -p data logs

echo "Installation completed."
echo "Next steps:"
echo "1. Edit .env"
echo "2. Run: python src/telegram_bot_full.py"
echo "3. Run: python src/vk_bot_full.py"
echo "4. Run logger: python src/data_logger.py"
