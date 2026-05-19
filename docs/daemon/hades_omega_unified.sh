#!/data/data/com.termux/files/usr/bin/bash
# HADES vΩ OMEGA UNIFIED - NÚCLEO NATIVO TERMUX
command -v jq >&- || pkg in -y jq >&-
while read -rp $'\e[31mHADES» \e[0m' c a; do
  case $c in
    bash|b) eval "$a" ;;
    estado|e) jq -cn --arg v "$BASH_VERSION" '{st:"OK",v:$v}' ;;
    blockchain|bc) jq -cn --arg w "${a:-0x0}" '{addr:$w,bal:0}' ;;
    salir|q) exit 0 ;;
    *) [[ $c ]] && jq -cn --arg c "$c" '{err:404,cmd:$c}' ;;
  esac
done
