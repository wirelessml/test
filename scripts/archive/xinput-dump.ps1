# xinput-dump.ps1 — Switch Pro 互換コンが xinput で何を出してるかリアルタイム確認
# 実行: powershell -File xinput-dump.ps1
# 終了: Ctrl+C

Add-Type -TypeDefinition @"
using System.Runtime.InteropServices;
public class XInput {
    [DllImport("xinput1_4.dll")]
    public static extern int XInputGetState(uint userIndex, out XINPUT_STATE state);
    [StructLayout(LayoutKind.Sequential)]
    public struct XINPUT_STATE {
        public uint dwPacketNumber;
        public XINPUT_GAMEPAD Gamepad;
    }
    [StructLayout(LayoutKind.Sequential)]
    public struct XINPUT_GAMEPAD {
        public ushort wButtons;
        public byte bLeftTrigger;
        public byte bRightTrigger;
        public short sThumbLX;
        public short sThumbLY;
        public short sThumbRX;
        public short sThumbRY;
    }
}
"@

$buttonNames = @{
    0x0001 = "DPAD_UP"
    0x0002 = "DPAD_DOWN"
    0x0004 = "DPAD_LEFT"
    0x0008 = "DPAD_RIGHT"
    0x0010 = "START"
    0x0020 = "BACK"
    0x0040 = "LSTICK_PUSH"
    0x0080 = "RSTICK_PUSH"
    0x0100 = "LB"
    0x0200 = "RB"
    0x1000 = "A"
    0x2000 = "B"
    0x4000 = "X"
    0x8000 = "Y"
}

Write-Host "xinput-dump - Push buttons on the controller. Ctrl+C to quit."
Write-Host "Looking for any of 4 controllers (slots 0-3)..."

$lastBitmap = 0
$lastTrigger = 0
while ($true) {
    for ($i = 0; $i -lt 4; $i++) {
        $state = New-Object XInput+XINPUT_STATE
        $r = [XInput]::XInputGetState($i, [ref]$state)
        if ($r -ne 0) { continue }
        $btn = $state.Gamepad.wButtons
        $lt = $state.Gamepad.bLeftTrigger
        $rt = $state.Gamepad.bRightTrigger
        $now = ($btn -ne 0) -bor ($lt -gt 30) -bor ($rt -gt 30)
        $prev = ($lastBitmap -ne 0) -bor ($lastTrigger -gt 30)
        if ($now -or $prev) {
            $names = @()
            foreach ($k in $buttonNames.Keys) {
                if (($btn -band $k) -ne 0) { $names += $buttonNames[$k] }
            }
            if ($lt -gt 30) { $names += "LT($lt)" }
            if ($rt -gt 30) { $names += "RT($rt)" }
            $line = "slot{0} btn=0x{1:X4} LT={2,3} RT={3,3} LX={4,6} LY={5,6} RX={6,6} RY={7,6} [{8}]" -f `
                $i, $btn, $lt, $rt, $state.Gamepad.sThumbLX, $state.Gamepad.sThumbLY, `
                $state.Gamepad.sThumbRX, $state.Gamepad.sThumbRY, ($names -join ",")
            Write-Host $line
        }
        $lastBitmap = $btn
        $lastTrigger = [Math]::Max($lt, $rt)
    }
    Start-Sleep -Milliseconds 80
}
