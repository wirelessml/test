"""doda 履歴書用写真 自動アップロード
mypageResumeUpload/ ページのキャリアシート（履歴書）用写真セクションに
setInputFiles で写真を投入。送信前 signal-file pause。
"""
import asyncio
import sqlite3
import hashlib
import sys
import subprocess
from pathlib import Path
from Crypto.Cipher import AES
from playwright.async_api import async_playwright


def get_chrome_safe_storage_key() -> str:
    return subprocess.run(
        ['security', 'find-generic-password', '-wa', 'Chrome'],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


CHROME_SAFE_STORAGE = get_chrome_safe_storage_key()
DODA_LOGIN_DB = '/tmp/chrome-login-data.db'
PHOTO_FILE = '/tmp/doda-docs/keisuke-rireki-photo-2026-0502.jpg'
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
    print(f"[doda-photo] {msg}", flush=True)


async def main():
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    for sig in (SUBMIT_SIGNAL, ABORT_SIGNAL):
        sig.unlink(missing_ok=True)

    username, password = get_doda_credentials()
    if not (username and password):
        log("ERROR: no doda creds")
        sys.exit(1)
    log(f"username: {username}")
    log(f"password length: {len(password)} chars (NOT echoed)")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled', '--no-default-browser-check'],
        )
        context = await browser.new_context(
            viewport={'width': 1400, 'height': 900},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        )
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
        page = await context.new_page()

        # ----- Phase 1: 直接 mypageResumeUpload へ -----
        log("Navigating directly to mypageResumeUpload...")
        await page.goto('https://doda.jp/dcfront/mypage/mypageResumeUpload/', wait_until='load')
        await asyncio.sleep(3)
        await page.screenshot(path=SCREENSHOT_DIR / 'photo-01-initial.png')
        log(f"URL: {page.url}")

        # 認証必要なら login (フォーム自動入力、ユーザーが ログインボタンクリック)
        if 'auth.doda.jp' in page.url:
            log("Need to login. Auto-filling form, please click ログイン button manually.")
            email_field = page.locator('input[placeholder*="dodaid"], input[placeholder*="@"], input[type="email"]').first
            await email_field.wait_for(state='visible', timeout=15000)
            await email_field.fill(username)
            await asyncio.sleep(0.3)
            await page.locator('input[type="password"]').first.fill(password)
            await asyncio.sleep(0.3)
            log("=" * 50)
            log("⏸ ユーザー操作: agent-browser Chrome で")
            log("  1. 「同意」チェックボックスにチェック")
            log("  2. 「ログイン」ボタンをクリック")
            log("(自動化は rate limit 回避のためスキップ)")
            log("=" * 50)
            await page.screenshot(path=SCREENSHOT_DIR / 'photo-02-please-login.png')
            # mypageResumeUpload へ navigate するまで待機 (最長 5 分)
            try:
                await page.wait_for_url('**/mypageResumeUpload/**', timeout=300000)
                log(f"Login completed by user. URL: {page.url}")
            except Exception as e:
                log(f"login wait timeout: {e}")
                await browser.close()
                sys.exit(2)
            await asyncio.sleep(3)

        await page.screenshot(path=SCREENSHOT_DIR / 'photo-02-page.png')

        # ----- Phase 2: 写真セクションの input[type=file] を探す -----
        log("Looking for photo section's file input...")
        # 全 input[type=file] を確認
        candidates = await page.evaluate("""() => {
            const inputs = [...document.querySelectorAll('input[type="file"]')];
            return inputs.map(el => ({
                accept: el.accept || '',
                id: el.id,
                name: el.name,
                cls: (el.className || '').toString().slice(0, 60),
                hidden: el.offsetParent === null,
                parent_text: (el.closest('section, div, td')?.innerText || '').slice(0, 100)
            }));
        }""")
        log(f"file inputs found: {len(candidates)}")
        for i, c in enumerate(candidates):
            log(f"  [{i}] {c}")

        # 写真用 input は accept=".jpg,.jpeg" or "image/*" or parent_text に "写真"
        photo_input_idx = None
        for i, c in enumerate(candidates):
            accept_lower = c['accept'].lower()
            if 'jpg' in accept_lower or 'jpeg' in accept_lower or 'image' in accept_lower:
                photo_input_idx = i
                log(f"matched by accept: idx {i} accept={c['accept']}")
                break
            if '写真' in c.get('parent_text', '') or 'photo' in c.get('cls', '').lower():
                photo_input_idx = i
                log(f"matched by context: idx {i} parent contains 写真")
                break

        if photo_input_idx is None:
            log("ERROR: 写真 input not identified")
            sys.exit(2)

        photo_input = page.locator('input[type="file"]').nth(photo_input_idx)
        log(f"Attaching photo: {PHOTO_FILE} (input idx {photo_input_idx})")
        await photo_input.set_input_files(PHOTO_FILE)
        await asyncio.sleep(2)
        await page.screenshot(path=SCREENSHOT_DIR / 'photo-03-attached.png')
        log("Photo attached")

        # ----- Phase 3: 送信前停止 -----
        log("=" * 50)
        log("READY TO SUBMIT 写真")
        log("送信実行: touch /tmp/doda-submit.signal")
        log("中止:  touch /tmp/doda-abort.signal")
        log("=" * 50)

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
            log("Timeout 30min")
            await browser.close()
            sys.exit(4)

        # ----- Phase 4: 送信 -----
        log("Submitting photo...")
        # ダイアログ内の「アップロード」ボタン (a.uploadButton)
        try:
            submit_btn = page.get_by_text("アップロード", exact=True).first
            await submit_btn.click(timeout=10000)
            await asyncio.sleep(5)
            await page.screenshot(path=SCREENSHOT_DIR / 'photo-04-submitted.png')
            log(f"Photo submitted. URL: {page.url}")
        except Exception as e:
            log(f"submit failed: {e}")
            await page.screenshot(path=SCREENSHOT_DIR / 'photo-04-fail.png')

        await asyncio.sleep(5)
        await browser.close()
        log("Done.")


if __name__ == '__main__':
    asyncio.run(main())
