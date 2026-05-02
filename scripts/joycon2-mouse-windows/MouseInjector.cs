// SendInput Win32 API wrapper — Phase 3 マウス注入の最小レイヤ
//
// 責務: dx/dy / クリック / ホイールの「指示が来たら 1 回 SendInput を呼ぶ」だけ。
// レート制御・accum・gating は DeltaMapper 側に閉じ込める。
//
// 実装は user32!SendInput を直接呼ぶ単純な P/Invoke。Interception driver は
// Phase 5 でゲーム対応版を検討する余地として開けてある。

using System.Runtime.InteropServices;

namespace JoyCon2Mouse;

internal enum MouseButton
{
    Left,
    Right,
    Middle,
}

internal static class MouseInjector
{
    // ----- P/Invoke -----

    [DllImport("user32.dll", SetLastError = true)]
    private static extern uint SendInput(uint nInputs, INPUT[] pInputs, int cbSize);

    [StructLayout(LayoutKind.Sequential)]
    private struct INPUT
    {
        public uint type;
        public InputUnion data;
    }

    [StructLayout(LayoutKind.Explicit)]
    private struct InputUnion
    {
        [FieldOffset(0)] public MOUSEINPUT mi;
    }

    [StructLayout(LayoutKind.Sequential)]
    private struct MOUSEINPUT
    {
        public int dx;
        public int dy;
        public uint mouseData;
        public uint dwFlags;
        public uint time;
        public IntPtr dwExtraInfo;
    }

    private const uint INPUT_MOUSE            = 0;
    private const uint MOUSEEVENTF_MOVE       = 0x0001;
    private const uint MOUSEEVENTF_LEFTDOWN   = 0x0002;
    private const uint MOUSEEVENTF_LEFTUP     = 0x0004;
    private const uint MOUSEEVENTF_RIGHTDOWN  = 0x0008;
    private const uint MOUSEEVENTF_RIGHTUP    = 0x0010;
    private const uint MOUSEEVENTF_MIDDLEDOWN = 0x0020;
    private const uint MOUSEEVENTF_MIDDLEUP   = 0x0040;
    private const uint MOUSEEVENTF_WHEEL      = 0x0800;
    private const uint MOUSEEVENTF_HWHEEL     = 0x1000;

    private const int WHEEL_DELTA = 120;

    // ----- public API -----

    /// <summary>マウスを (dx, dy) ピクセル相対移動。</summary>
    public static void MoveRelative(int dx, int dy)
    {
        if (dx == 0 && dy == 0) return;
        var inp = new INPUT
        {
            type = INPUT_MOUSE,
            data = new InputUnion
            {
                mi = new MOUSEINPUT { dx = dx, dy = dy, dwFlags = MOUSEEVENTF_MOVE },
            },
        };
        SendInput(1, new[] { inp }, Marshal.SizeOf<INPUT>());
    }

    /// <summary>マウスボタンの押下/離上。</summary>
    public static void Click(MouseButton btn, bool pressed)
    {
        uint flag = btn switch
        {
            MouseButton.Left   => pressed ? MOUSEEVENTF_LEFTDOWN   : MOUSEEVENTF_LEFTUP,
            MouseButton.Right  => pressed ? MOUSEEVENTF_RIGHTDOWN  : MOUSEEVENTF_RIGHTUP,
            MouseButton.Middle => pressed ? MOUSEEVENTF_MIDDLEDOWN : MOUSEEVENTF_MIDDLEUP,
            _ => 0,
        };
        if (flag == 0) return;
        var inp = new INPUT
        {
            type = INPUT_MOUSE,
            data = new InputUnion { mi = new MOUSEINPUT { dwFlags = flag } },
        };
        SendInput(1, new[] { inp }, Marshal.SizeOf<INPUT>());
    }

    /// <summary>縦ホイール (notches 単位、+ で上スクロール、- で下)。</summary>
    public static void WheelV(int notches)
    {
        if (notches == 0) return;
        var inp = new INPUT
        {
            type = INPUT_MOUSE,
            data = new InputUnion
            {
                mi = new MOUSEINPUT
                {
                    mouseData = unchecked((uint)(notches * WHEEL_DELTA)),
                    dwFlags = MOUSEEVENTF_WHEEL,
                },
            },
        };
        SendInput(1, new[] { inp }, Marshal.SizeOf<INPUT>());
    }

    /// <summary>横ホイール (notches 単位、+ で右、- で左)。</summary>
    public static void WheelH(int notches)
    {
        if (notches == 0) return;
        var inp = new INPUT
        {
            type = INPUT_MOUSE,
            data = new InputUnion
            {
                mi = new MOUSEINPUT
                {
                    mouseData = unchecked((uint)(notches * WHEEL_DELTA)),
                    dwFlags = MOUSEEVENTF_HWHEEL,
                },
            },
        };
        SendInput(1, new[] { inp }, Marshal.SizeOf<INPUT>());
    }
}
