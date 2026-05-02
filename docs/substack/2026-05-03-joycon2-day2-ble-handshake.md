# Joy-Con 2 と Bluetooth でハンドシェイクする (Day 2)

> 連載「Switch 2 Joy-Con を Windows でマウス化する 5 日」第 2 回
> 公開予定: 2026-05-06 以降
> 著者: 仲啓輔

[Day 1](./2026-05-03-joycon2-day1-motivation-and-protocol.md) では仕様書を再構成した。今日はそれを使って **C# で Joy-Con 2 と実際につなぐ**。動くと bool 1 個で確認できるところまで。

## 想定: BLE スキャンで見つけて接続

WinRT の BLE API は素直で、一般的にはこういう手順:

```csharp
var watcher = new BluetoothLEAdvertisementWatcher
{
    ScanningMode = BluetoothLEScanningMode.Active,
};
watcher.AdvertisementFilter.Advertisement.ServiceUuids.Add(serviceUuid);
watcher.Received += async (s, e) =>
{
    var device = await BluetoothLEDevice.FromBluetoothAddressAsync(e.BluetoothAddress);
    // ...
};
watcher.Start();
```

**この想定は外れた。**

## ハマり 1: Joy-Con 2 は LocalName も ServiceUuid も広告しない

実機を SYNC モードにしてスキャンを回しても、フィルタに 1 件もヒットしない。フィルタを外して全 advertisement を出してみると、**MAC アドレスだけの advertisement がたくさん流れている**ことが分かった。

つまり Joy-Con 2 はペアリング前は LocalName も ServiceUuid もばらまかない。これだと「これは Joy-Con 2 だ」と判別する手がかりが MAC ベンダープレフィックスしかない。

逆に **Windows の Bluetooth 設定でペアリングを済ませてしまえば**、`DeviceInformation.FindAllAsync` で「ペア済み BLE デバイス一覧」が取れる。Joy-Con 2 もペア時には LocalName を返してくるので、ここに `Joy-Con 2 (R)` として登録される。

そこで設計を変えた。**ペアリングは Windows 設定 GUI でユーザーに 1 回やってもらい、起動後はペア済みリストから名前で見つけて直接接続する**。

```csharp
var selector = BluetoothLEDevice.GetDeviceSelectorFromPairingState(true);
var pairedDevices = await DeviceInformation.FindAllAsync(selector);

DeviceInformation? joyConInfo = pairedDevices.FirstOrDefault(di =>
    di.Name.Contains("Joy-Con", StringComparison.OrdinalIgnoreCase));

var device = await BluetoothLEDevice.FromIdAsync(joyConInfo.Id);
```

advertisement に頼らないので、Joy-Con 2 が起動済み・接続済みでなくてもこのコードは通る (FromIdAsync が auto-connect してくれる)。

## ハマり 2: write characteristic は別 service と書いてあったが…

仕様書（maruta の README）では Write Characteristic が **別の service** に存在していた。それを真に受けて「Nintendo Service と Write Service を別々に取得する」コードを書いていたが、実機では **Nintendo Service の中に write characteristic も入っていた**。

```
service ab7de9be-...-fd0  ← Nintendo Service
  ├── ab7de9be-...-fd2 (input notify)   ✅ ここ
  └── 649d4ac9-...-f005 (write char)    ✅ ここにもいた!
```

仕様書のとおり「別 service」を探すと見つからない。Joy-Con 2 のファームウェア更新で同じ service に集約された可能性もあるし、maruta が解析した時点と環境が違うのかもしれない。

なので実装は **全 service を走査して `WriteCharUuid` を持つ characteristic を探す** という防御的な書き方にした:

```csharp
GattCharacteristic? writeChar = null;
var allServices = await device.GetGattServicesAsync();
foreach (var svc in allServices.Services)
{
    var r = await svc.GetCharacteristicsForUuidAsync(WriteCharUuid);
    if (r.Status == GattCommunicationStatus.Success && r.Characteristics.Count > 0)
    {
        writeChar = r.Characteristics[0];
        break;
    }
}
```

仕様書が外れていても動くようになった。

## ハマり 3: SSH 越しに stdout が出ない

しゅん先生 PC（コワーキング据え置きの Windows 11）に Mac の Tailscale + SSH でつないで `dotnet run` を叩く運用をしている。普通の `Console.WriteLine` は OpenSSH Server の Services session で stdout が見えなかった。

なので、ログを `Console.WriteLine` + `File.AppendAllText` の二重出力にして、どっちで動かしても確認できるようにした:

```csharp
private static readonly string LogPath =
    Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
                 "joycon2-run.log");

private static void Log(string line = "")
{
    var ts = $"{DateTime.Now:HH:mm:ss.fff} {line}";
    Console.WriteLine(ts);
    File.AppendAllText(LogPath, ts + Environment.NewLine);
}
```

これで `tail -f ~/joycon2-run.log` を Mac 側 SSH で叩けば、何が起きてるか見える。

## ハンドシェイクが通った瞬間

11:59:21、6 回連続で `Success`:

```
11:59:21.440   step 0 (std): Success
11:59:21.748   step 1 (ext): Success
11:59:22.054   step 2 (std): Success
11:59:22.356   step 3 (ext): Success
11:59:22.663   step 4 (std): Success
11:59:22.970   step 5 (ext): Success
```

そして 60 byte パケットが降りはじめる:

```
[10] btn=0x000000 L=(2047,2047) R=(2063,2007) opt=(0,0) gyro=(-5,11)
[20] btn=0x000000 L=(2047,2047) R=(2063,2005) opt=(0,0) gyro=(-4,11)
```

L スティック中央 `(2047, 2047)` は仕様書通りの 12-bit center 値。R スティックは `(2063, 2007)` で **2048 から ±20 ずれてる**。これは個体差で、後でキャリブレーションが要りそう。ジャイロは `(-5, 11)` 前後の小さい値、これが **noise floor** = 静止時のゼロドリフト。マウス化するときは絶対値 50 以下を deadzone で潰す必要がある。

R_SL ボタンを押すと:

```
[230] btn=0x000020  ... [R_SL]
```

`0x20 = 0b100000` = bit 5 = `JC_R_SL`。仕様書通り。**ハンドシェイクが完全に通っている**。

光学センサーは机に置いて滑らせると:

```
[267] btn=0x000040 ... opt=(-4544,-2503) optD=(-40,-352) [R]
```

`opt` が累積値、`optD` が前フレームとの差分。-40, -352 は 1 フレームで動いた量で、これを `SendInput` に渡せばマウスカーソルが動く——はず。それは Phase 3 の話。

## まとめ

reverse engineered プロトコルを真に受けすぎず、**実機で全部走査して動くものを探す**のが地味に大事だった。

- advertisement に頼らない (ペア済みリストから検出)
- write char は **service 横断で探す**
- ログは **ファイル出力併用**

Phase 2 完了。Phase 3 は **`SendInput` でマウスカーソルを実際に動かす**。光学とジャイロを足し算してマウス delta にして、ボタン edge detection で左右クリックして、HOME ボタンで「**やばいから止めて**」と言える緊急停止スイッチを作る。

明日書く。

---

#Switch2 #JoyCon #Windows #BLE #CSharp #リバースエンジニアリング
