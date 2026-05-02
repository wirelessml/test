// Joy-Con 2 BLE プロトコル定数
// 出典: maruta/joycon2-usb-presenter (Apache 2.0) + 上流 reverse engineering 系プロジェクト
// 詳細: docs/projects/joycon2-protocol.md

namespace JoyCon2Mouse;

/// <summary>
/// Joy-Con 2 BLE GATT サービス・キャラクタリスティック UUID と初期化コマンド。
/// </summary>
internal static class Protocol
{
    // ----- GATT UUIDs -----

    /// <summary>Nintendo カスタムサービス。</summary>
    public static readonly Guid ServiceUuid =
        new("ab7de9be-89fe-49ad-828f-118f09df7fd0");

    /// <summary>Input notify characteristic（同 service 内）。Notify subscribe で 60+ bytes パケット受信。</summary>
    public static readonly Guid InputNotifyUuid =
        new("ab7de9be-89fe-49ad-828f-118f09df7fd2");

    /// <summary>Write characteristic（別 service 内）。enable / LED / vibration コマンド送信用。</summary>
    public static readonly Guid WriteCharUuid =
        new("649d4ac9-8eb7-4e6c-af44-1ea54fe5f005");

    // ----- 初期化コマンド -----

    /// <summary>
    /// Input enable (standard report)。
    /// ペア接続後、enable_std と enable_ext を交互に約 300ms 間隔で複数回送信する。
    /// </summary>
    public static readonly byte[] EnableStd = new byte[]
    {
        0x0c, 0x91, 0x01, 0x02, 0x00, 0x04, 0x00, 0x00,
        0xff, 0x00, 0x00, 0x00,
    };

    /// <summary>Input enable (extended)。EnableStd と交互に送信。</summary>
    public static readonly byte[] EnableExt = new byte[]
    {
        0x0c, 0x91, 0x01, 0x04, 0x00, 0x04, 0x00, 0x00,
        0xff, 0x00, 0x00, 0x00,
    };

    /// <summary>Player LED コマンドを生成（mask: bit0=LED1, bit1=LED2, bit2=LED3, bit3=LED4）。</summary>
    public static byte[] BuildPlayerLedCommand(byte mask) => new byte[]
    {
        0x09, 0x91, 0x01, 0x07, 0x00, 0x04, 0x00, 0x00,
        mask, 0x00, 0x00, 0x00,
    };

    // ----- ボタン bit position (24-bit bitmap、bytes 4-6 を LE 読み取り) -----

    public const int JC_Y       = 0;
    public const int JC_X       = 1;
    public const int JC_B       = 2;
    public const int JC_A       = 3;
    public const int JC_R_SR    = 4;
    public const int JC_R_SL    = 5;
    public const int JC_R       = 6;
    public const int JC_ZR      = 7;
    public const int JC_MINUS   = 8;
    public const int JC_PLUS    = 9;
    public const int JC_RJ      = 10;
    public const int JC_LJ      = 11;
    public const int JC_HOME    = 12;
    public const int JC_CAPT    = 13;
    public const int JC_C       = 14;
    public const int JC_DOWN    = 16;
    public const int JC_UP      = 17;
    public const int JC_RIGHT   = 18;
    public const int JC_LEFT    = 19;
    public const int JC_L_SR    = 20;
    public const int JC_L_SL    = 21;

    // ----- スティック中央値 (12-bit、~0x800 = 2048) -----

    public const int StickCenter = 2048;
}
