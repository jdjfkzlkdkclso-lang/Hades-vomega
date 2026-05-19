#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

OUT="$HOME/EXTRACCION_TOTAL"
RAW="$OUT/raw"
UNZ="$OUT/unzipped"

SRC1="/storage/emulated/0"
SRC2="$(find / -type d -name ttf 2>/dev/null | head -n 1 || true)"

mkdir -p "$RAW" "$UNZ"

find "$SRC1" ${SRC2:+$SRC2} -type f \( \
  -iname "*.txt" -o -iname "*.zip" -o -iname "*.gz" -o -iname "*.md" -o -iname "*.py" \
  -o -iname "*.html" -o -iname "*.json" -o -iname "*.key" -o -iname "*.api" \
  -o -iname "*police*" -o -iname "*oro*" -o -iname "*nuevo*" -o -iname "*notas*" \
  -o -iname "*carpeta*" -o -iname "*prompts*" -o -iname "*tools*" \
\) 2>/dev/null | while IFS= read -r f; do
  cp -n --parents "$f" "$RAW/" || true
  case "$f" in
    *.zip)
      d="$UNZ/$(basename "$f" .zip)"
      mkdir -p "$d"
      unzip -oq "$f" -d "$d" || true
      ;;
    *.gz)
      d="$UNZ/$(basename "$f" .gz)"
      gunzip -c "$f" > "$d" || true
      ;;
  esac
done
