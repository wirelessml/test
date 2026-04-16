#!/bin/bash
# Windows XP VM 起動スクリプト
# 用途: 維新の嵐 幕末志士伝（1998年コーエー）プレイ用
#
# 使い方:
#   bash ~/Desktop/winxp-start.sh              # スナップショットから即起動
#   bash ~/Desktop/winxp-start.sh --cdrom ISO  # CD-ROMイメージ付きで起動
#
# QEMU操作:
#   スクリーンショット: echo "screendump /tmp/qemu_screen.ppm" | nc -w 2 127.0.0.1 4444
#   キー入力: echo "sendkey ret" | nc -w 1 127.0.0.1 4444
#   マウス: echo "mouse_move X Y" | nc -w 1 127.0.0.1 4444
#   状態保存: echo "savevm winxp_ready" | nc -w 5 127.0.0.1 4444
#   シャットダウン: echo "system_powerdown" | nc -w 2 127.0.0.1 4444

DISK="$HOME/Desktop/winxp.qcow2"
ISO="$HOME/Desktop/winxp-sp3-ja.iso"
SNAPSHOT="winxp_ready"

CDROM_OPT=""
if [ "$1" = "--cdrom" ] && [ -n "$2" ]; then
    CDROM_OPT="-cdrom $2"
    echo "CD-ROM: $2"
fi

echo "Starting Windows XP VM..."
echo "Monitor: telnet 127.0.0.1:4444"

qemu-system-i386 \
  -machine pc-i440fx-7.2 \
  -m 512 \
  -cpu pentium3 \
  -smp 1 \
  -hda "$DISK" \
  $CDROM_OPT \
  -boot c \
  -vga std \
  -display cocoa \
  -net none \
  -usb \
  -device usb-tablet \
  -name "Windows XP" \
  -monitor telnet:127.0.0.1:4444,server,nowait \
  -loadvm "$SNAPSHOT" &

echo "PID: $!"
echo "VM started. Use telnet 127.0.0.1:4444 for monitor."
