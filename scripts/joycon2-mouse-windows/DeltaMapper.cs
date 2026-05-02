// 入力センサー → マウス delta 変換 — Phase 3
//
// Joy-Con 2 の生センサー値 (光学 X/Y 累積、ジャイロ X/Z、スティック RX/RY、ボタン bitmap)
// から、SendInput に渡す mouse delta + wheel notches + クリック edge を 1 フレームで生成する。
//
// 状態保持:
//   - 光学センサー累積値の前回値（差分計算は InputPacket.cs 側 OpticalDeltaTracker が担当）
//   - ホイール accumulator（fractional notch を蓄積）
//   - 前回ボタン bitmap（edge detection 用）
//
// チューニング定数の根拠は test-logs/phase2-first-success-2026-0502-1200.log:
//   - 静止時 gyro: ~(-5, 11) → noise floor 14 程度 → DEADZONE=50 で除去
//   - 振り gyro: 数百〜千オーダー
//   - 静止時 right stick: (2063, 2007) ← 個体差で center=2048 から ±20 ずれ
//   - 光学 delta: 通常数十、SSH 越し抜けで稀に 2000+ → CLIP=200 で頭打ち

namespace JoyCon2Mouse;

internal readonly record struct StepResult(
    int Dx,
    int Dy,
    int WheelV,
    int WheelH,
    IReadOnlyList<(MouseButton Btn, bool Pressed)> Clicks);

internal class DeltaMapper
{
    // ----- チューニング定数 -----

    /// <summary>静止時 gyro noise を排除する閾値。Phase 2 ログ実測 ~14。</summary>
    public const int GyroDeadzone     = 50;

    /// <summary>gyro raw → mouse pixel の除算係数。大きいほど鈍い。</summary>
    public const int GyroDivisor      = 30;

    /// <summary>光学 delta → mouse pixel の除算係数。</summary>
    public const int OpticalDivisor   = 4;

    /// <summary>1 フレームで許容する光学 delta の絶対値上限 (BLE notify 抜け対策)。</summary>
    public const int OpticalDeltaClip = 200;

    /// <summary>右スティック中心からのズレ閾値。個体差吸収のため広めに。</summary>
    public const int StickDeadzone    = 250;

    /// <summary>スティック値の理論中央 (12-bit center)。</summary>
    public const int StickCenter      = 2048;

    /// <summary>スティック量 → ホイール notch の換算分母 (大きいほど低速)。</summary>
    public const float StickWheelDivisor = 8000f;

    // ----- 状態 -----

    private uint  _prevButtons;
    private bool  _firstFrame = true;
    private float _wheelVAccum;
    private float _wheelHAccum;

    /// <summary>
    /// 1 フレーム分の入力を delta に変換する。
    /// </summary>
    /// <param name="p">パース済み input packet。</param>
    /// <param name="optDx">光学 X の前回差分 (OpticalDeltaTracker 出力)。</param>
    /// <param name="optDy">光学 Y の前回差分 (OpticalDeltaTracker 出力)。</param>
    public StepResult Step(in InputPacket p, int optDx, int optDy)
    {
        // 1) mouse delta
        int dx = 0, dy = 0;

        // 1a) 光学 (常時 ON、SSH 越し抜けで暴れることがあるので clip)
        int oDx = Math.Clamp(optDx, -OpticalDeltaClip, OpticalDeltaClip);
        int oDy = Math.Clamp(optDy, -OpticalDeltaClip, OpticalDeltaClip);
        dx += oDx / OpticalDivisor;
        dy += oDy / OpticalDivisor;

        // 1b) ジャイロ (側面 SL/SR or トリガー押下中のみ = gating)
        if (IsGyroGated(p))
        {
            int gx = p.GyroX;
            int gz = p.GyroZ;
            if (Math.Abs(gx) > GyroDeadzone) dy += -gx / GyroDivisor;
            if (Math.Abs(gz) > GyroDeadzone) dx += -gz / GyroDivisor;
        }

        // 2) wheel: 右スティック傾き → 縦/横ホイール
        int rx = p.RightStickX - StickCenter;
        int ry = p.RightStickY - StickCenter;
        if (Math.Abs(ry) > StickDeadzone) _wheelVAccum += -ry / StickWheelDivisor;
        if (Math.Abs(rx) > StickDeadzone) _wheelHAccum +=  rx / StickWheelDivisor;

        int wheelV = (int)_wheelVAccum;
        int wheelH = (int)_wheelHAccum;
        _wheelVAccum -= wheelV;
        _wheelHAccum -= wheelH;

        // 3) ボタン edge detection → クリックリスト
        var clicks = _firstFrame
            ? Array.Empty<(MouseButton, bool)>()
            : DetectClickEdges(p.Buttons, _prevButtons);

        _prevButtons = p.Buttons;
        _firstFrame  = false;

        return new StepResult(dx, dy, wheelV, wheelH, clicks);
    }

    /// <summary>マウス注入を一時 OFF にしたい時、状態だけ進める (delta は捨てる)。</summary>
    public void StepIdle(in InputPacket p)
    {
        _prevButtons = p.Buttons;
        _firstFrame  = false;
        _wheelVAccum = 0;
        _wheelHAccum = 0;
    }

    // ----- private -----

    private static bool IsGyroGated(in InputPacket p) =>
        p.IsPressed(Protocol.JC_R_SL) || p.IsPressed(Protocol.JC_R_SR) ||
        p.IsPressed(Protocol.JC_L_SL) || p.IsPressed(Protocol.JC_L_SR) ||
        p.IsPressed(Protocol.JC_ZR)   || p.IsPressed(Protocol.JC_R)    ||
        p.IsPressed(Protocol.JC_L);

    private static (MouseButton, bool)[] DetectClickEdges(uint cur, uint prev)
    {
        var list = new List<(MouseButton, bool)>(3);
        AddIfChanged(list, cur, prev, Protocol.JC_ZR, MouseButton.Left);
        AddIfChanged(list, cur, prev, Protocol.JC_R,  MouseButton.Right);
        AddIfChanged(list, cur, prev, Protocol.JC_RJ, MouseButton.Middle);
        return list.ToArray();
    }

    private static void AddIfChanged(
        List<(MouseButton, bool)> list, uint cur, uint prev, int bit, MouseButton btn)
    {
        bool now = (cur & (1u << bit)) != 0;
        bool was = (prev & (1u << bit)) != 0;
        if (now != was) list.Add((btn, now));
    }
}
