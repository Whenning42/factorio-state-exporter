set -eu

trap 'kill -- -$$' EXIT INT TERM

~/Games/factorio/bin/x64/factorio --enable-lua-udp 6001 >/dev/null 2>&1 &
python state_reader.py &
wait
