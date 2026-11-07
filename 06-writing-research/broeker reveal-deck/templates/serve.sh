#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────
# serve.sh — Launch a Reveal.js deck with pre-flight checks
# Usage: ./serve.sh [port] [ttyd-font-size]    (defaults: 8765, 24)
# ──────────────────────────────────────────────────────────

set -euo pipefail

PORT=${1:-8765}
TTYD_FONT_SIZE=${2:-24}
DECK="index.html"

# ── Helpers ───────────────────────────────────────────────

red()   { printf '\033[0;31m%s\033[0m\n' "$*"; }
green() { printf '\033[0;32m%s\033[0m\n' "$*"; }
yellow(){ printf '\033[0;33m%s\033[0m\n' "$*"; }
bold()  { printf '\033[1m%s\033[0m\n' "$*"; }

port_in_use() {
  # Works on both macOS and Linux
  if command -v lsof &>/dev/null; then
    lsof -i ":$1" &>/dev/null
  elif command -v ss &>/dev/null; then
    ss -ltn "sport = :$1" | grep -q "$1"
  else
    # Fallback: try to connect
    (echo >/dev/tcp/localhost/"$1") 2>/dev/null
  fi
}

# ── Pre-flight: deck exists? ─────────────────────────────

if [ ! -f "$DECK" ]; then
  red "[ERROR] No $DECK found in $(pwd)"
  echo "  Run this script from your deck directory."
  exit 1
fi

bold "─── Reveal.js Deck Server ───"
echo ""

# ── Pre-flight: port available? ──────────────────────────

if port_in_use "$PORT"; then
  yellow "[WARN] Port $PORT is already in use."
  echo "  Either another deck is running, or use a different port:"
  echo "  ./serve.sh 8766"
  echo ""
  read -p "  Open http://localhost:$PORT anyway? [Y/n] " -n 1 -r
  echo ""
  if [[ $REPLY =~ ^[Nn]$ ]]; then
    exit 0
  fi
  bold "─── http://localhost:$PORT ───"
  exit 0
fi

# ── Pre-flight: ttyd for terminal slides ─────────────────

if grep -q 'localhost:768[0-9]' "$DECK" 2>/dev/null; then
  echo "  This deck has live terminal slides."
  echo ""

  # Extract ttyd ports (works on both macOS grep and GNU grep)
  PORTS=$(grep -o 'localhost:768[0-9]' "$DECK" | grep -o '768[0-9]' | sort -u)

  # Build associative array of port → working directory from HTML comments
  # Format: <!-- ttyd:7681:/path/to/dir -->
  declare -A TTYD_DIRS
  while IFS= read -r line; do
    if [[ "$line" =~ ttyd:([0-9]+):(.+)[[:space:]]*-- ]]; then
      TTYD_DIRS["${BASH_REMATCH[1]}"]="${BASH_REMATCH[2]}"
    fi
  done < <(grep -o '<!-- ttyd:[0-9]*:[^ ]* -->' "$DECK" 2>/dev/null || true)

  # Check if ttyd is installed
  if ! command -v ttyd &>/dev/null; then
    red "  [MISSING] ttyd is not installed."
    echo ""
    echo "  Install it:"
    echo "    Ubuntu/Debian:  sudo apt install ttyd"
    echo "    macOS:          brew install ttyd"
    echo "    Other:          https://github.com/tsl0922/ttyd#installation"
    echo ""
    TTYD_INSTALLED=0
  else
    TTYD_INSTALLED=1
  fi

  # Check each port — auto-start ttyd if installed but not running
  MISSING=0
  for P in $PORTS; do
    if port_in_use "$P"; then
      green "  [OK] ttyd running on port $P"
    else
      if [ "$TTYD_INSTALLED" -eq 1 ]; then
        TTYD_DIR="${TTYD_DIRS[$P]:-}"
        if [ -n "$TTYD_DIR" ]; then
          yellow "  [AUTO] Starting ttyd on port $P → $TTYD_DIR (font-size: $TTYD_FONT_SIZE)..."
          env -u CLAUDECODE ttyd -W -p "$P" -t fontSize="$TTYD_FONT_SIZE" -w "$TTYD_DIR" bash &
        else
          yellow "  [AUTO] Starting ttyd on port $P (font-size: $TTYD_FONT_SIZE)..."
          env -u CLAUDECODE ttyd -W -p "$P" -t fontSize="$TTYD_FONT_SIZE" bash &
        fi
        sleep 1
        if port_in_use "$P"; then
          green "  [OK] ttyd started on port $P (PID $!)"
        else
          red "  [FAIL] ttyd did not start on port $P"
          MISSING=1
        fi
      else
        red "  [!!] ttyd NOT running on port $P"
        MISSING=1
      fi
    fi
  done

  if [ "$MISSING" -eq 1 ]; then
    echo ""
    if [ "$TTYD_INSTALLED" -eq 0 ]; then
      echo "  Install ttyd to enable auto-start:"
      echo "    Ubuntu/Debian:  sudo apt install ttyd"
      echo "    macOS:          brew install ttyd"
      echo "    Other:          https://github.com/tsl0922/ttyd#installation"
    fi
    echo ""
    read -p "  Continue without terminal? [y/N] " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      exit 1
    fi
  fi
  echo ""
fi

# ── Start server ─────────────────────────────────────────

green "[OK] Serving deck at http://localhost:$PORT"
echo "  Press Ctrl+C to stop."
echo ""

python3 -m http.server "$PORT"
