# Browser 自動化 → しゅん先生 PC 実行（司令塔/実行機分離）

> 5/2 朝確定: M1 司令塔は軽量維持、ブラウザ自動化（Playwright / Chromium / agent-browser）は しゅん先生 PC へ逃す。

## 環境（しゅん先生 PC、2026-05-02 セットアップ済）

- **Python 3.13.13** at `C:\Users\wirel\AppData\Local\Programs\Python\Python313\python.exe`
- **Playwright** + **Chromium** ブラウザ (winldd 含む) at `C:\Users\wirel\AppData\Local\ms-playwright\`
- **pycryptodome**（AES 復号、Chrome Login Data 読込用、必要時）

## 標準ワークフロー（Mac → SSH → しゅん先生）

### 1. Mac 側でタスクスクリプト書く

```python
# /tmp/my-browser-task.py
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # GUI 必要なら False
        page = await browser.new_page()
        # ...タスク実行...
        await browser.close()

asyncio.run(main())
```

### 2. SCP でしゅん先生に転送

```bash
scp /tmp/my-browser-task.py wirel@desktop-atq36ks.local:./my-browser-task.py
```

### 3. SSH で実行

```bash
ssh shun-sensei 'C:\Users\wirel\AppData\Local\Programs\Python\Python313\python.exe C:\Users\wirel\my-browser-task.py'
```

### 4. 結果取得

```bash
# screenshot や output file を Mac に持ち帰る
scp wirel@desktop-atq36ks.local:./result.png /tmp/result.png
```

## ヘッドレス vs ヘッドフル

- **headless=True**: バックグラウンド実行、CPU/RAM 軽量、しゅん先生に画面表示なし
- **headless=False**: しゅん先生 PC のディスプレイに Chrome ウィンドウ表示。ユーザーが手動操作（login 等）しやすい

OAuth login / CAPTCHA / 多段認証が必要な場合は **headless=False** + ハイブリッド（Mac から SSH 起動 → しゅん先生 PC でユーザーが認証 → Mac でロジック自動化）。

## 司令塔モード保護のメリット

| 項目 | M1 司令塔 | しゅん先生 PC |
|---|---|---|
| Chromium プロセス常駐 | ❌（メモリ即圧迫）| ✅（16GB 余裕） |
| Defender / Anti-bot 検出 | ⚠️ user IP 露出 | ✅ 別 IP / プロファイル |
| 並列実行 | M1 では困難 | ✅ 複数 Chromium 並列可 |
| Mac の他作業 | 影響大 | 影響なし |

## 関連スクリプト

- `smoke-test.py`: 動作確認用 example.com → screenshot
- 実用例: `/Users/yuika/Desktop/scripts/doda/auto-upload.py`（Mac で実行した v1、しゅん先生に移植可能）
- 実用例: `/Users/yuika/Desktop/scripts/doda/photo-upload.py`（同上）

## SSH 接続（mDNS 動的解決、5/2 朝整備済）

- ssh alias: `shun-sensei`（HostName: `DESKTOP-ATQ36KS.local`）
- user: `wirel`
- 同 Wi-Fi 内のみ到達可（Tailscale 不採用方針）
- LAN 外なら masu-p55 (Tailscale 100.125.21.47) 経由 SSH ホップ

## 注意

- パスワード等の秘匿情報は **Python メモリのみ**で扱う（log/stdout に echo しない）
- `Crypto.Cipher.AES` で Chrome Safe Storage キー復号する場合は Mac の Keychain key 使用、Windows 側ではユーザー Keychain に同等情報がない場合あり
- doda 等 anti-bot 対策が厳しいサイトは `--disable-blink-features=AutomationControlled` + `Object.defineProperty(navigator, 'webdriver', {get: () => undefined})` を init_script に
- 連続自動 login で rate limit 食らったらハイブリッドへ切替（user manual click）
