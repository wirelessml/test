// Joy-Con 2 Windows マウス化ドライバ - Phase 3 entry point
//
// 起動フロー:
// 1. ペア済み Joy-Con 2 を Windows レジストリから探す
// 2. BluetoothLEDevice 取得 → service / characteristic 解決
// 3. input notify subscribe + enable_std / enable_ext 交互送信
// 4. パケット受信 → InputPacket でパース → DeltaMapper で mouse delta 化
// 5. --mouse 指定時のみ MouseInjector で SendInput 注入 (デフォルト OFF = dump のみ)
// 6. ランタイム HOME ボタンでマウス注入 ON/OFF をトグル可能 (緊急停止)
//
// CLI:
//   dotnet run                # dump only (Phase 2 互換)
//   dotnet run -- --mouse     # マウス注入 ON で起動

using System.Runtime.InteropServices.WindowsRuntime;
using Windows.Devices.Bluetooth;
using Windows.Devices.Bluetooth.Advertisement;
using Windows.Devices.Bluetooth.GenericAttributeProfile;
using Windows.Storage.Streams;

using JoyCon2Mouse;

internal class Program
{
    private static int _frameCount;
    private static uint _prevButtons;
    private static readonly OpticalDeltaTracker _opticalTracker = new();
    private static readonly DeltaMapper _mapper = new();

    /// <summary>SendInput 注入を有効化するかどうか。--mouse で起動時 ON、HOME ボタンで toggle。</summary>
    private static volatile bool _mouseEnabled;

    private static readonly string LogPath =
        Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), "joycon2-run.log");
    private static readonly object _logLock = new();

    /// <summary>Console.WriteLine + ファイル追記。SSH Services session でも見えるようにする。</summary>
    private static void Log(string line = "")
    {
        var timestamped = $"{DateTime.Now:HH:mm:ss.fff} {line}";
        Console.WriteLine(timestamped);
        lock (_logLock)
        {
            File.AppendAllText(LogPath, timestamped + Environment.NewLine);
        }
    }

    public static async Task<int> Main(string[] args)
    {
        // 旧ログクリア
        try { File.Delete(LogPath); } catch { }

        _mouseEnabled = args.Contains("--mouse", StringComparer.OrdinalIgnoreCase);

        Log("Joy-Con 2 mouse driver (Phase 3 scaffold)");
        Log($"  Log file:        {LogPath}");
        Log($"  Service:         {Protocol.ServiceUuid}");
        Log($"  Input:           {Protocol.InputNotifyUuid}");
        Log($"  Write:           {Protocol.WriteCharUuid}");
        Log($"  Mouse injection: {(_mouseEnabled ? "ON" : "OFF (dump only)")}");
        Log("  Runtime toggle:  HOME button (緊急停止)");
        Log();

        // ----- 1. ペア済デバイス探索 + 直接接続 -----
        // Joy-Con 2 が Windows BT 設定で paired 済ならアドバタイズしない。
        // 既ペア済リストから Joy-Con 2 を name で見つけて接続する。
        Log("Looking up paired Joy-Con 2 in Windows registry...");

        var selector = Windows.Devices.Bluetooth.BluetoothLEDevice.GetDeviceSelectorFromPairingState(true);
        var pairedDevices = await Windows.Devices.Enumeration.DeviceInformation.FindAllAsync(selector);
        Log($"Paired BLE devices: {pairedDevices.Count}");

        Windows.Devices.Enumeration.DeviceInformation? joyConDevInfo = null;
        foreach (var di in pairedDevices)
        {
            Log($"  - {di.Name} (id={di.Id})");
            if (di.Name.Contains("Joy-Con", StringComparison.OrdinalIgnoreCase) ||
                di.Name.Contains("JoyCon", StringComparison.OrdinalIgnoreCase))
            {
                joyConDevInfo = di;
            }
        }

        if (joyConDevInfo == null)
        {
            Log("Joy-Con 2 not found in paired devices. Pair via Windows Settings → Bluetooth first.");
            return 1;
        }
        Log($"Found Joy-Con 2: {joyConDevInfo.Name} (id={joyConDevInfo.Id})");

        // DeviceInformation.Id から BluetoothLEDevice 取得
        var device = await Windows.Devices.Bluetooth.BluetoothLEDevice.FromIdAsync(joyConDevInfo.Id);
        if (device == null)
        {
            Log("FromIdAsync returned null");
            return 2;
        }
        Log($"Device obtained: addr={device.BluetoothAddress:X12} name={device.Name} status={device.ConnectionStatus}");
        ulong addr = device.BluetoothAddress;

        // ConnectionStatusChanged を監視 (debugging visibility)
        device.ConnectionStatusChanged += (s, _) =>
            Log($"  >>> ConnectionStatusChanged: {s.ConnectionStatus}");

        // 接続が安定するまで 2 秒待つ
        Log("Waiting 2s for BLE link to stabilize...");
        await Task.Delay(2000);

        // ----- 2. service / characteristic 解決 -----
        // Cached モード優先。5/2 Phase 2 成功は Cached 経路。Uncached は WinRT が
        // 内部でディスカバリ用 ATT request を再送するが、Joy-Con 2 firmware が
        // それを切断トリガーとして扱ってしまうケースが今回確認された。
        // Cached が空なら Uncached にフォールバック。
        Log($"\nQuerying GATT services for {addr:X12}...");

        GattDeviceServicesResult? serviceResult = null;
        for (int retry = 1; retry <= 6; retry++)
        {
            // Cached を試す
            serviceResult = await device.GetGattServicesForUuidAsync(
                Protocol.ServiceUuid, BluetoothCacheMode.Cached);
            if (serviceResult.Status == GattCommunicationStatus.Success && serviceResult.Services.Count > 0)
            {
                Log($"  service via Cached on retry {retry}: {serviceResult.Services[0].Uuid} ✅");
                break;
            }
            // Cached 空なら Uncached
            serviceResult = await device.GetGattServicesForUuidAsync(
                Protocol.ServiceUuid, BluetoothCacheMode.Uncached);
            if (serviceResult.Status == GattCommunicationStatus.Success && serviceResult.Services.Count > 0)
            {
                Log($"  service via Uncached on retry {retry}: {serviceResult.Services[0].Uuid} ✅");
                break;
            }
            Log($"  retry {retry}/6: status={serviceResult.Status} link={device.ConnectionStatus} — press button");
            await Task.Delay(2000);
        }
        if (serviceResult is null
            || serviceResult.Status != GattCommunicationStatus.Success
            || serviceResult.Services.Count == 0)
        {
            Log($"Nintendo service unreachable after 6 retries.");
            return 3;
        }
        var nintendoService = serviceResult.Services[0];
        Log($"  ConnectionStatus now: {device.ConnectionStatus}");

        var inputCharResult = await nintendoService.GetCharacteristicsForUuidAsync(
            Protocol.InputNotifyUuid, BluetoothCacheMode.Cached);
        if (inputCharResult.Status != GattCommunicationStatus.Success || inputCharResult.Characteristics.Count == 0)
        {
            Log($"Input notify char not found: {inputCharResult.Status}");
            return 4;
        }
        var inputChar = inputCharResult.Characteristics[0];
        Log($"  input notify: {inputChar.Uuid} ✅");

        // Write char は別 service の可能性もあるので、全 service を走査 (cached)
        var allServices = await device.GetGattServicesAsync(BluetoothCacheMode.Cached);
        GattCharacteristic? writeChar = null;
        foreach (var svc in allServices.Services)
        {
            var chResult = await svc.GetCharacteristicsForUuidAsync(
                Protocol.WriteCharUuid, BluetoothCacheMode.Cached);
            if (chResult.Status == GattCommunicationStatus.Success && chResult.Characteristics.Count > 0)
            {
                writeChar = chResult.Characteristics[0];
                Log($"  write char: {writeChar.Uuid} (in service {svc.Uuid}) ✅");
                break;
            }
        }
        if (writeChar is null)
        {
            Log("Write characteristic not found in any service.");
            return 5;
        }

        // ----- 3. input notify subscribe -----
        inputChar.ValueChanged += OnInputNotify;
        var ccResult = await inputChar.WriteClientCharacteristicConfigurationDescriptorAsync(
            GattClientCharacteristicConfigurationDescriptorValue.Notify);
        Log($"  notify subscribe: {ccResult}");

        // ----- 4. enable_std / enable_ext を交互送信 -----
        Log("\nSending enable commands (std/ext alternating, 300ms apart)...");
        for (int i = 0; i < 6; i++)
        {
            byte[] cmd = (i % 2 == 0) ? Protocol.EnableStd : Protocol.EnableExt;
            var buf = cmd.AsBuffer();
            var w = await writeChar.WriteValueWithResultAsync(buf, GattWriteOption.WriteWithoutResponse);
            Log($"  step {i} ({(i % 2 == 0 ? "std" : "ext")}): {w.Status}");
            await Task.Delay(300);
        }

        Log("\n--- Receiving input data (Ctrl+C to stop) ---");

        // 永続待機 (Ctrl+C で抜ける)
        var cts = new CancellationTokenSource();
        Console.CancelKeyPress += (s, e) => { e.Cancel = true; cts.Cancel(); };
        try
        {
            await Task.Delay(Timeout.Infinite, cts.Token);
        }
        catch (OperationCanceledException)
        {
            // 正常終了
        }

        Log("\nDisconnecting...");
        device.Dispose();
        return 0;
    }

    private static void OnInputNotify(GattCharacteristic _, GattValueChangedEventArgs evt)
    {
        _frameCount++;

        var reader = DataReader.FromBuffer(evt.CharacteristicValue);
        var bytes = new byte[evt.CharacteristicValue.Length];
        reader.ReadBytes(bytes);

        var pkt = InputPacket.TryParse(bytes);
        if (pkt is null) return;
        var p = pkt.Value;

        var (optDx, optDy) = _opticalTracker.Update(p.OpticalX, p.OpticalY);

        // HOME ボタン押下 edge で mouse 注入 ON/OFF をトグル (緊急停止用)
        bool homeNow  = (p.Buttons     & (1u << Protocol.JC_HOME)) != 0;
        bool homePrev = (_prevButtons  & (1u << Protocol.JC_HOME)) != 0;
        if (homeNow && !homePrev)
        {
            _mouseEnabled = !_mouseEnabled;
            Log($"  *** Mouse injection toggled: {(_mouseEnabled ? "ON" : "OFF")} ***");
        }

        StepResult step;
        if (_mouseEnabled)
        {
            step = _mapper.Step(p, optDx, optDy);

            if (step.Dx != 0 || step.Dy != 0) MouseInjector.MoveRelative(step.Dx, step.Dy);
            if (step.WheelV != 0) MouseInjector.WheelV(step.WheelV);
            if (step.WheelH != 0) MouseInjector.WheelH(step.WheelH);
            foreach (var (btn, pressed) in step.Clicks)
                MouseInjector.Click(btn, pressed);
        }
        else
        {
            // 状態だけ進めて delta は捨てる (再 ON 時に edge detection が暴発しないように)
            _mapper.StepIdle(p);
            step = default;
        }

        // ボタン変化時 or 30 フレームごとに表示 (Phase 3 はノイズ抑制で 30)
        bool changed = p.Buttons != _prevButtons;
        if (changed || _frameCount % 30 == 0)
        {
            string buttonNames = NamesFromButtons(p.Buttons);
            string mvInfo = _mouseEnabled
                ? $" -> mv=({step.Dx,3},{step.Dy,3}) wh=({step.WheelV,2},{step.WheelH,2})"
                : "";
            Log($"  [{_frameCount,5}] {p.ToShortString()} optD=({optDx,4},{optDy,4}){mvInfo} {buttonNames}");
        }
        _prevButtons = p.Buttons;
    }

    /// <summary>押されているボタンを名前で連結。</summary>
    private static string NamesFromButtons(uint btn)
    {
        if (btn == 0) return "";
        var pressed = new List<string>();
        if ((btn & (1 << Protocol.JC_Y)) != 0) pressed.Add("Y");
        if ((btn & (1 << Protocol.JC_X)) != 0) pressed.Add("X");
        if ((btn & (1 << Protocol.JC_B)) != 0) pressed.Add("B");
        if ((btn & (1 << Protocol.JC_A)) != 0) pressed.Add("A");
        if ((btn & (1 << Protocol.JC_R_SR)) != 0) pressed.Add("R_SR");
        if ((btn & (1 << Protocol.JC_R_SL)) != 0) pressed.Add("R_SL");
        if ((btn & (1 << Protocol.JC_R)) != 0) pressed.Add("R");
        if ((btn & (1 << Protocol.JC_ZR)) != 0) pressed.Add("ZR");
        if ((btn & (1 << Protocol.JC_MINUS)) != 0) pressed.Add("-");
        if ((btn & (1 << Protocol.JC_PLUS)) != 0) pressed.Add("+");
        if ((btn & (1 << Protocol.JC_RJ)) != 0) pressed.Add("RJ");
        if ((btn & (1 << Protocol.JC_LJ)) != 0) pressed.Add("LJ");
        if ((btn & (1 << Protocol.JC_HOME)) != 0) pressed.Add("HOME");
        if ((btn & (1 << Protocol.JC_CAPT)) != 0) pressed.Add("CAPT");
        if ((btn & (1 << Protocol.JC_C)) != 0) pressed.Add("C");
        if ((btn & (1 << Protocol.JC_DOWN)) != 0) pressed.Add("DN");
        if ((btn & (1 << Protocol.JC_UP)) != 0) pressed.Add("UP");
        if ((btn & (1 << Protocol.JC_RIGHT)) != 0) pressed.Add("R");
        if ((btn & (1 << Protocol.JC_LEFT)) != 0) pressed.Add("L");
        if ((btn & (1 << Protocol.JC_L_SR)) != 0) pressed.Add("L_SR");
        if ((btn & (1 << Protocol.JC_L_SL)) != 0) pressed.Add("L_SL");
        return $"[{string.Join(",", pressed)}]";
    }
}
