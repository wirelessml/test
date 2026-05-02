// Joy-Con 2 input notify パケット (60+ bytes) のパース
// パケット構造詳細: docs/projects/joycon2-protocol.md

namespace JoyCon2Mouse;

/// <summary>1 回の input notify (60+ bytes) を解釈した結果。</summary>
internal readonly record struct InputPacket(
    uint Buttons,        // 24-bit bitmap (bytes 4-6 LE)
    byte StatusFlags,    // byte 7
    int LeftStickX,      // 12-bit (bytes 10-11)
    int LeftStickY,      // 12-bit (bytes 11-12)
    int RightStickX,     // 12-bit (bytes 13-14)
    int RightStickY,     // 12-bit (bytes 14-15)
    short OpticalX,      // int16 LE (bytes 16-17) ※累積カウンタ
    short OpticalY,      // int16 LE (bytes 18-19) ※累積カウンタ
    short GyroX,         // int16 LE (bytes 54-55) → 縦移動用
    short GyroZ          // int16 LE (bytes 58-59) → 横移動用
)
{
    /// <summary>60 bytes 以上のバイト列から InputPacket を構築。短ければ null。</summary>
    public static InputPacket? TryParse(ReadOnlySpan<byte> data)
    {
        if (data.Length < 60) return null;

        uint btn = (uint)(data[4] | (data[5] << 8) | (data[6] << 16));
        byte status = data[7];

        int lx = data[10] | ((data[11] & 0x0f) << 8);
        int ly = (data[11] >> 4) | (data[12] << 4);
        int rx = data[13] | ((data[14] & 0x0f) << 8);
        int ry = (data[14] >> 4) | (data[15] << 4);

        short optX = (short)(data[16] | (data[17] << 8));
        short optY = (short)(data[18] | (data[19] << 8));
        short gx   = (short)(data[54] | (data[55] << 8));
        short gz   = (short)(data[58] | (data[59] << 8));

        return new InputPacket(btn, status, lx, ly, rx, ry, optX, optY, gx, gz);
    }

    /// <summary>指定した bit position のボタンが押されているか。</summary>
    public bool IsPressed(int bitPosition) => (Buttons & (1u << bitPosition)) != 0;

    /// <summary>デバッグ用 1 行表示。</summary>
    public string ToShortString() =>
        $"btn=0x{Buttons:X6} L=({LeftStickX,4},{LeftStickY,4}) " +
        $"R=({RightStickX,4},{RightStickY,4}) " +
        $"opt=({OpticalX,5},{OpticalY,5}) gyro=({GyroX,5},{GyroZ,5})";
}

/// <summary>光学センサーの絶対累積値から差分 (delta) を計算する状態保持。</summary>
internal class OpticalDeltaTracker
{
    private short _prevX;
    private short _prevY;
    private bool _seeded;

    public (int dx, int dy) Update(short x, short y)
    {
        if (!_seeded)
        {
            _prevX = x;
            _prevY = y;
            _seeded = true;
            return (0, 0);
        }

        int dx = x - _prevX;
        int dy = y - _prevY;
        _prevX = x;
        _prevY = y;
        return (dx, dy);
    }
}
