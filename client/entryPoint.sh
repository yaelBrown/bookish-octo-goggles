#!/bin/bash
echo "Running entryPoint.sh"
echo ""
echo "╭━━━╮╱╱╱╱╱╭╮╭╮"
echo "┃╭━╮┃╱╱╱╱╭╯╰┫┃"
echo "┃┃╱╰╋━━┳━┻╮╭┫┃╭━━╮"
echo "┃┃╱╭┫╭╮┃━━┫┃┃┃┃┃━┫"
echo "┃╰━╯┃╭╮┣━━┃╰┫╰┫┃━┫"
echo "╰━━━┻╯╰┻━━┻━┻━┻━━╯"
echo "╭━╮╱╭╮╱╱╭╮╱╱╱╱╱╱╱╱╱╭╮"
echo "┃┃╰╮┃┃╱╭╯╰╮╱╱╱╱╱╱╱╱┃┃"
echo "┃╭╮╰╯┣━┻╮╭┫╭╮╭┳━━┳━┫┃╭╮"
echo "┃┃╰╮┃┃┃━┫┃╰╯╰╯┃╭╮┃╭┫╰╯╯"
echo "┃┃╱┃┃┃┃━┫╰╮╭╮╭┫╰╯┃┃┃╭╮╮"
echo "╰╯╱╰━┻━━┻━┻╯╰╯╰━━┻╯╰╯╰╯"
echo "╭━━━╮╱╱╱╱╱╱╱╱╱╱╱╱╱╭╮"
echo "┃╭━╮┃╱╱╱╱╱╱╱╱╱╱╱╱╭╯╰╮"
echo "┃┃╱╰╋━━┳━╮╭━━┳━┳━┻╮╭╋━━┳━╮"
echo "┃┃╭━┫┃━┫╭╮┫┃━┫╭┫╭╮┃┃┃╭╮┃╭╯"
echo "┃╰┻━┃┃━┫┃┃┃┃━┫┃┃╭╮┃╰┫╰╯┃┃"
echo "╰━━━┻━━┻╯╰┻━━┻╯╰╯╰┻━┻━━┻╯"
echo ""
cd /home/CNG/
echo "[01/02] Pip installing requirements"
pip3 install requests
echo ""
echo "[02/02] Running Application"
python3 client.py