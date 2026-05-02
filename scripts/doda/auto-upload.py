"""doda 自動ログイン + 神戸徳洲会病院向け職務経歴書アップロード
Phase 1: ログイン→アップロード画面へ→ファイル添付 (送信前で停止、screenshot 取得)
Phase 2: /tmp/doda-submit.signal が作られたら最終送信、無ければ手動確認待ち

password はメモリ内のみ、stdout には漏らさない。
"""
import asyncio
import sqlite3
import hashlib
import sys
from pathlib import Path
from Crypto.Cipher import AES
from playwright.async_api import async_playwright

import subprocess


def get_chrome_safe_storage_key() -> str:
    """Mac Keychain から Chrome Safe Storage キーを取得 (ランタイムのみ、コードに直書きしない)"""
    result = subprocess.run(
        ['security', 'find-generic-password', '-wa', 'Chrome'],
        capture_output=True, text=True, check=True,
    )
    return result.stdout.strip()


CHROME_SAFE_STORAGE = get_chrome_safe_storage_key()
DODA_LOGIN_DB = '/tmp/chrome-login-data.db'
UPLOAD_FILE = '/tmp/doda-docs/shokumu-2026-0502.docx'
SCREENSHOT_DIR = Path('/Users/yuika/Desktop/screenshots/doda')
SUBMIT_SIGNAL = Path('/tmp/doda-submit.signal')
ABORT_SIGNAL = Path('/tmp/doda-abort.signal')


def decrypt_chrome_password(encrypted: bytes, key_str: str) -> str:
    if encrypted[:3] in (b'v10', b'v11'):
        encrypted = encrypted[3:]
    key = hashlib.pbkdf2_hmac('sha1', key_str.encode('utf-8'), b'saltysalt', 1003, dklen=16)
    iv = b' ' * 16
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    pad_len = decrypted[-1]
    return decrypted[:-pad_len].decode('utf-8')


def get_doda_credentials():
    conn = sqlite3.connect(DODA_LOGIN_DB)
    row = conn.execute(
        "SELECT username_value, password_value FROM logins WHERE origin_url LIKE '%auth.doda.jp%' LIMIT 1"
    ).fetchone()
    conn.close()
    if not row:
        return None, None
    username, encrypted = row
    pw = decrypt_chrome_password(encrypted, CHROME_SAFE_STORAGE)
    return username, pw


def log(msg):
    """stdout に出力するが password 値は絶対に echo しない"""
    print(f"[doda-auto] {msg}", flush=True)


async def main():
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    # クリーンアップ
    for sig in (SUBMIT_SIGNAL, ABORT_SIGNAL):
        sig.unlink(missing_ok=True)

    username, password = get_doda_credentials()
    if not (username and password):
        log("ERROR: no doda creds in Chrome Login Data")
        sys.exit(1)
    log(f"username retrieved: {username}")
    log(f"password length: {len(password)} chars (NOT echoed)")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-default-browser-check',
            ],
        )
        context = await browser.new_context(
            viewport={'width': 1400, 'height': 900},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        )
        # navigator.webdriver を false に偽装
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)
        page = await context.new_page()

        # ----- Phase 1.0: ログインページへ遷移 -----
        log("Navigating to doda login...")
        # progressTop へ goto する → auth.doda.jp/login へ自動 redirect
        # OAuth flow の最終 URL を待つ
        await page.goto('https://doda.jp/dcfront/progress/progressTop/', wait_until='load')
        # SPA のレンダリング完了を待つ (固定時間)
        await asyncio.sleep(3)
        await page.screenshot(path=SCREENSHOT_DIR / 'auto-01-login.png')
        log(f"Current URL: {page.url}")

        # 既にログイン済 (cookie 残存) なら progressTop に居る
        if '/progress/' in page.url and 'auth.doda.jp' not in page.url:
            log("Already logged in (cookie reuse), skipping login form")
        else:
            # ----- Phase 1.1: ログインフォーム入力 -----
            log("Filling login form...")
            # メールアドレス入力欄
            email_field = page.locator('input[placeholder*="dodaid"], input[placeholder*="@"], input[type="email"]').first
            await email_field.wait_for(state='visible', timeout=15000)
            await email_field.fill(username)
            await asyncio.sleep(0.3)
            # パスワード
            await page.locator('input[type="password"]').first.fill(password)
            await asyncio.sleep(0.3)
            # 利用規約同意チェックボックス (id=cbAgreementPC、span が overlay)
            # span#cbAgreementSpanPC をクリックする方が確実
            try:
                # span が visible なのでそれをクリック
                agree_span = page.locator('#cbAgreementSpanPC, span.ckWrapA_Cbox').first
                await agree_span.click(timeout=5000)
                log("Agreement span clicked")
            except Exception as e:
                log(f"span click failed, try direct checkbox check: {e}")
                try:
                    await page.locator('#cbAgreementPC').check(force=True, timeout=5000)
                    log("Agreement checkbox checked (force)")
                except Exception as e2:
                    log(f"force check also failed: {e2}")

            await asyncio.sleep(0.5)
            await page.screenshot(path=SCREENSHOT_DIR / 'auto-02-filled.png')
            log("Login form filled and agreement checked")

            # ----- Phase 1.2: ログインボタン押下 (もしくは自動遷移待ち) -----
            log("Clicking login button or waiting for auto-redirect...")
            # 同時に: navigation 待ち or login button click
            # (前回の実行で同意 click 後に自動 submit が観測された)
            try:
                # まず login button が click 可能ならクリック
                login_btn = page.locator('button:has-text("ログイン"):not(:has-text("ID")), input[type="submit"][value*="ログイン"]').first
                if await login_btn.is_visible(timeout=2000):
                    try:
                        await login_btn.click(timeout=5000)
                        log("Login button clicked")
                    except Exception as e:
                        log(f"login btn click err (may have navigated): {e}")
            except Exception:
                pass

            # progressTop URL への navigation を待つ (login button click か自動 submit いずれかで成立)
            try:
                await page.wait_for_url('**/progress/**', timeout=20000)
                log(f"Logged in, URL: {page.url}")
            except Exception as e:
                log(f"wait_for_url progress timeout: {e}")
                log(f"Current URL: {page.url}")

        # 短い固定待機 (SPA レンダリング) - networkidle は doda では成立しない
        await asyncio.sleep(3)

        # ナビゲーション待機 (login flow 完了)
        try:
            await page.wait_for_url('**/dcfront/**', timeout=20000)
        except Exception as e:
            log(f"wait_for_url timeout: {e}")
        await asyncio.sleep(3)
        await page.screenshot(path=SCREENSHOT_DIR / 'auto-03-after-login.png')
        log(f"After login URL: {page.url}")

        # ----- Phase 1.3: アップロード画面へ -----
        log("Looking for アップロードする button...")
        upload_btn = page.locator('button:has-text("アップロードする"), a:has-text("アップロードする")').first
        try:
            await upload_btn.click(timeout=10000)
            await asyncio.sleep(3)
            await page.screenshot(path=SCREENSHOT_DIR / 'auto-04-upload-form.png')
            log(f"Upload form URL: {page.url}")
        except Exception as e:
            log(f"アップロードする click failed: {e}")
            await page.screenshot(path=SCREENSHOT_DIR / 'auto-04-fail.png')
            log("Stopping. Please inspect screenshot.")
            await asyncio.sleep(600)
            sys.exit(2)

        # ----- Phase 1.4: ファイル添付 -----
        log(f"Attaching file: {UPLOAD_FILE}")
        try:
            file_input = page.locator('input[type="file"]').first
            await file_input.set_input_files(UPLOAD_FILE)
            await asyncio.sleep(2)
            await page.screenshot(path=SCREENSHOT_DIR / 'auto-05-attached.png')
            log("File attached")
        except Exception as e:
            log(f"file attach failed: {e}")
            await page.screenshot(path=SCREENSHOT_DIR / 'auto-05-fail.png')
            await asyncio.sleep(600)
            sys.exit(3)

        # ----- Phase 1.5: 送信前停止、シグナル待機 -----
        log("=" * 50)
        log("READY TO SUBMIT - 確認画面 screenshot 取得済")
        log("送信実行: touch /tmp/doda-submit.signal")
        log("中止: touch /tmp/doda-abort.signal")
        log("=" * 50)

        # シグナル待ち (最長 30 分)
        for _ in range(1800):
            if SUBMIT_SIGNAL.exists():
                log("SUBMIT signal received")
                SUBMIT_SIGNAL.unlink()
                break
            if ABORT_SIGNAL.exists():
                log("ABORT signal received")
                ABORT_SIGNAL.unlink()
                await browser.close()
                sys.exit(0)
            await asyncio.sleep(1)
        else:
            log("Timeout 30min, abort")
            await browser.close()
            sys.exit(4)

        # ----- Phase 2: 最終送信 -----
        log("Submitting...")
        # ダイアログ内の青「アップロード」ボタンを探す。
        # button / a / input / div / [role=button] 全部試す。
        # 「アップロードする」は別のボタンなので除外。
        await page.screenshot(path=SCREENSHOT_DIR / 'auto-06-pre-submit.png')
        try:
            # まず DOM を探索して候補を log
            candidates = await page.evaluate("""() => {
                const results = [];
                const all = document.querySelectorAll('button, a, input[type=submit], [role=button], [role=link], div[onclick], span[onclick]');
                for (const el of all) {
                    const txt = (el.innerText || el.value || '').trim();
                    if (txt === 'アップロード' || txt.match(/^アップロード$/)) {
                        const r = el.getBoundingClientRect();
                        results.push({
                            tag: el.tagName,
                            text: txt.slice(0, 40),
                            cls: (el.className || '').toString().slice(0, 50),
                            id: el.id,
                            x: Math.round(r.x), y: Math.round(r.y),
                            w: Math.round(r.width), h: Math.round(r.height),
                            visible: r.width > 0 && r.height > 0
                        });
                    }
                }
                return results;
            }""")
            log(f"アップロード候補: {len(candidates)} elements")
            for c in candidates:
                log(f"  {c}")

            # 完全一致 "アップロード" のみのテキストでクリック
            submit_btn = page.get_by_text("アップロード", exact=True).first
            await submit_btn.click(timeout=10000)
            await asyncio.sleep(5)
            await page.screenshot(path=SCREENSHOT_DIR / 'auto-06-submitted.png')
            log(f"Submitted. Final URL: {page.url}")
        except Exception as e:
            log(f"submit failed: {e}")
            await page.screenshot(path=SCREENSHOT_DIR / 'auto-06-submit-fail.png')

        await asyncio.sleep(5)
        await browser.close()
        log("Done. Browser closed.")


if __name__ == '__main__':
    asyncio.run(main())
