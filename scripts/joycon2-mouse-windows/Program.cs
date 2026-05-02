// Joy-Con 2 Windows マウス化ドライバ - Phase 2 minimum sample
//
// このサンプルは:
// 1. BLE 広告を Nintendo service UUID でフィルタしてスキャン
// 2. 最初に見つかった Joy-Con 2 に接続
// 3. service / characteristic を解決
// 4. input notify を subscribe
// 5. enable_std / enable_ext を交互送信
// 6. 受信したパケットを InputPacket でパースしてコンソール出力
//
// マウス注入は Phase 3 で実装。今は dump のみ。

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

    public static async Task<int> Main(string[] args)
    {
        Console.WriteLine("Joy-Con 2 BLE smoke test (Phase 2 scaffold)");
        Console.WriteLine($"  Service:  {Protocol.ServiceUuid}");
        Console.WriteLine($"  Input:    {Protocol.InputNotifyUuid}");
        Console.WriteLine($"  Write:    {Protocol.WriteCharUuid}");
        Console.WriteLine();

        // ----- 1. BLE スキャン -----
        var watcher = new BluetoothLEAdvertisementWatcher
        {
            ScanningMode = BluetoothLEScanningMode.Active,
        };
        watcher.AdvertisementFilter.Advertisement.ServiceUuids.Add(Protocol.ServiceUuid);

        var deviceFound = new TaskCompletionSource<ulong>();
        watcher.Received += (sender, evt) =>
        {
            Console.WriteLine($"  found: addr={evt.BluetoothAddress:X12} " +
                              $"rssi={evt.RawSignalStrengthInDBm} dBm " +
                              $"name={evt.Advertisement.LocalName}");
            deviceFound.TrySetResult(evt.BluetoothAddress);
        };
        watcher.Start();
        Console.WriteLine("Scanning for Joy-Con 2... (timeout 30s, hold SYNC ~5s on Joy-Con 2)");

        var winnerTask = await Task.WhenAny(deviceFound.Task, Task.Delay(TimeSpan.FromSeconds(30)));
        watcher.Stop();

        if (winnerTask != deviceFound.Task)
        {
            Console.WriteLine("\nNo Joy-Con 2 found within 30 seconds.");
            Console.WriteLine("Make sure: (a) Joy-Con 2 is in pairing mode (LED scrolling)");
            Console.WriteLine("           (b) it is disconnected from Switch 2");
            Console.WriteLine("Phase 2 scaffold compile-test mode: BLE flow not verified.");
            return 1;
        }

        ulong addr = deviceFound.Task.Result;

        // ----- 2. 接続 + service / characteristic 解決 -----
        Console.WriteLine($"\nConnecting to {addr:X12}...");
        var device = await BluetoothLEDevice.FromBluetoothAddressAsync(addr);
        if (device is null)
        {
            Console.WriteLine("Failed to obtain BluetoothLEDevice (was it unpaired?).");
            return 2;
        }

        var serviceResult = await device.GetGattServicesForUuidAsync(Protocol.ServiceUuid);
        if (serviceResult.Status != GattCommunicationStatus.Success || serviceResult.Services.Count == 0)
        {
            Console.WriteLine($"Nintendo service not found: {serviceResult.Status}");
            return 3;
        }
        var nintendoService = serviceResult.Services[0];
        Console.WriteLine($"  service: {nintendoService.Uuid} ✅");

        var inputCharResult = await nintendoService.GetCharacteristicsForUuidAsync(Protocol.InputNotifyUuid);
        if (inputCharResult.Status != GattCommunicationStatus.Success || inputCharResult.Characteristics.Count == 0)
        {
            Console.WriteLine($"Input notify char not found: {inputCharResult.Status}");
            return 4;
        }
        var inputChar = inputCharResult.Characteristics[0];
        Console.WriteLine($"  input notify: {inputChar.Uuid} ✅");

        // Write char は別 service にあるので、全 service を走査
        var allServices = await device.GetGattServicesAsync();
        GattCharacteristic? writeChar = null;
        foreach (var svc in allServices.Services)
        {
            var chResult = await svc.GetCharacteristicsForUuidAsync(Protocol.WriteCharUuid);
            if (chResult.Status == GattCommunicationStatus.Success && chResult.Characteristics.Count > 0)
            {
                writeChar = chResult.Characteristics[0];
                Console.WriteLine($"  write char: {writeChar.Uuid} (in service {svc.Uuid}) ✅");
                break;
            }
        }
        if (writeChar is null)
        {
            Console.WriteLine("Write characteristic not found in any service.");
            return 5;
        }

        // ----- 3. input notify subscribe -----
        inputChar.ValueChanged += OnInputNotify;
        var ccResult = await inputChar.WriteClientCharacteristicConfigurationDescriptorAsync(
            GattClientCharacteristicConfigurationDescriptorValue.Notify);
        Console.WriteLine($"  notify subscribe: {ccResult}");

        // ----- 4. enable_std / enable_ext を交互送信 -----
        Console.WriteLine("\nSending enable commands (std/ext alternating, 300ms apart)...");
        for (int i = 0; i < 6; i++)
        {
            byte[] cmd = (i % 2 == 0) ? Protocol.EnableStd : Protocol.EnableExt;
            var buf = cmd.AsBuffer();
            var w = await writeChar.WriteValueWithResultAsync(buf, GattWriteOption.WriteWithoutResponse);
            Console.WriteLine($"  step {i} ({(i % 2 == 0 ? "std" : "ext")}): {w.Status}");
            await Task.Delay(300);
        }

        Console.WriteLine("\n--- Receiving input data (Ctrl+C to stop) ---");

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

        Console.WriteLine("\nDisconnecting...");
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

        // ボタン変化時 or 10 フレームごとに表示
        bool changed = p.Buttons != _prevButtons;
        if (changed || _frameCount % 10 == 0)
        {
            string buttonNames = NamesFromButtons(p.Buttons);
            Console.WriteLine($"  [{_frameCount,5}] {p.ToShortString()} optD=({optDx,4},{optDy,4}) {buttonNames}");
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
