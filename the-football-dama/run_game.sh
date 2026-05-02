#!/bin/bash
# The Football DAMA - Launch Script

echo "⚽  THE FOOTBALL DAMA ⚽"
echo "======================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed!"
    exit 1
fi

# Navigate to game directory
cd "$(dirname "$0")"

# Run the game
python3 src/game.py
