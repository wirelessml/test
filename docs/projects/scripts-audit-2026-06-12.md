# scripts/ 棚卸し提案（2026-06-12）

> 監査実行: masup WSL2 の Codex CLI（codex exec、117,740 tokens）に scripts/ 一式を tar 転送して分類させ、Claude（Fable 5）が全件検証・3 点訂正のうえ最終化。
> **削除はまだ実行していない。** 下記「提案 A〜D」の承認をもって実行する（運用ルール 1: 削除前の件数確認）。

## 検証で訂正した点（Codex 原案 → 最終）

1. **`._*` AppleDouble 58 件は実在しない** — tar 転送時の副産物で、Mac 実ディレクトリには 0 件と確認済み（`ls scripts/._*` → なし）。Codex の「delete候補 77 件」は実質 **19 件**
2. `job-report-email.log` — Codex は keep → **delete候補 に変更**（scripts/ 内の迷子ログ。本番ログは `~/Library/Application Support/job-report/` 側）
3. `reco-ollama-mock.py` — Codex は archive → **keep に変更**（稼働中 LaunchAgent `com.yuika.reco-ollama-mock` の git 正本。kanno-watch と同じ「実体は App Support、正本は scripts/」パターン）

加えて masup 実機調査で「要確認 7 件」のうち 4 件の正体を確定（下記 C）。

## 最終分類（49 ファイル + 3 サブディレクトリ）

### keep — 13 件（現役・git 正本・直近実用）

| ファイル | 根拠 |
|---|---|
| amazon-kioxia-monitor.sh / kanno-watch.sh / masu-p-watch.sh / lib/send-email.py | LaunchAgent 稼働中の git 正本（6/12 に App Support 移設、scripts/ 側が正本） |
| reco-ollama-mock.py | 同上（`com.yuika.reco-ollama-mock` の正本） |
| job-search-daily-mac.py / email-job-report.sh | 就活ルーチン本番（App Support 側）の開発元 |
| daily-job-search.sh | 6/10 移管直前の masup Codex 版（移行比較元として当面保持） |
| biz-analyze.sh / sibu-analyze.sh | 6/6 作成の現役分析ランナー |
| 面談-録画.command / 面談-文字起こし.command / 訪問動画-下ごしらえ.command | 録画 v3 体制の正本（recording-interviews スキル参照先） |

### A) archive 提案 — 16 件 → `scripts/archive/` へ git mv

再利用価値はあるが現役参照なし: browser-automation/（README.md + smoke-test.py）, doda/（auto-upload.py + generate-shokumu.py + photo-upload.py）, codex-tui-pets-pr-watch.sh, conductor-typing-autobot.js, generate-shibu-pet-sprite.py, install-noto-defaults.ps1, install-noto-defaults-phase2.ps1, install-noto-defaults-p2-ascii.ps1, install-pretendard-jp.ps1, update-claude-win.ps1, update-claude-win-145.ps1, xinput-dump.ps1, install-codex-appserver-shun.ps1（※AppServer は 5/8 訂正どおりしゅん先生 PC に未設置＝歴史的資料）

※ 実行時は updating-ai-cli-fleet スキル内の `update-claude-win.ps1` 参照パスも追従修正する。

### B) delete 提案 — 20 件（うち 19 件は git 未追跡＝完全消失、復元不可）

- **5/19〜5/24 の codex watchdog / tokenchecker 一次デバッグ 19 件**（作戦終結済み）: capture-codex-debug.ps1 / -v2 / -v3, debug-codex-remote.ps1 / -v2, diag-current-state.ps1, diag-tokenchecker.ps1, disable-tokenchecker-restart-codex.ps1, elevate-and-test.ps1, extract-debug-log.ps1, extract-recent-debug.ps1, final-test.ps1, fix-tasks-settings.ps1, reset-codex-dir.ps1, restore-auth-fresh-start.ps1, test-codex-0133.ps1, test-watchdog-full.ps1, test-watchdog-loop.ps1, update-codex-tasks.ps1
- **迷子ログ 1 件**: job-report-email.log

### C) 条件付き delete — 4 件（masup ゾンビ watchdog の停止とセット）

masup 実機調査（6/12 10:17）の事実:
- スケジュールタスク `\codex-watchdog` が**今も 3 分毎に発火中**（最終実行 6/12 10:17:12）
- しかしログは 6/10 06:11 の「DOWN: codex.exe missing → FAIL」で停止＝**標的（Windows ネイティブ codex.exe remote-control）が消えた後も空発火し続けるゾンビ**。masup の codex は WSL2 側に移行済みで、この watchdog の存在意義は消滅
- `\codex-remote-control` / `\CodexWSLRemoteControl` タスクも残存（最終実行 N/A）
- 配備実体は `C:\ProgramData\codex-watchdog\`（codex-watchdog.ps1 / run-codex-remote.bat / ログ 2 本）

**提案**: masup の `\codex-watchdog` タスクを無効化（`schtasks /change /tn codex-watchdog /disable`、可逆）→ 承認後、Mac 側ソース 4 件を削除: codex-watchdog.ps1, run-codex-remote.bat, install-codex-watchdog-task.ps1, migrate-to-programdata.ps1（配備実体は ProgramData に残るため、再開したくなれば masup 側だけで復元可能）

### D) 保留 — 2 件（しゅん先生 PC 起動時に確認）

setup-shun-sensei-watchdog.ps1, setup-tokenchecker-task.ps1 — しゅん先生 PC が今日 SSH 不達のため、同 PC 側のタスク残存状況を確認してから判定（doctor 同様に `schtasks /query | findstr /i "codex token"` で確認可）

## 実行待ちアクション（承認が要るもの）

1. **B) 20 件の削除**（19 件は復元不可）
2. **C) masup `\codex-watchdog` 無効化 → ソース 4 件削除**
3. **A) 16 件の scripts/archive/ への移動**（git 履歴は保持、低リスク）

## タグ
#scripts棚卸し #masup-Codex委譲 #検証3点訂正 #ゾンビwatchdog #AppleDouble #Fable5期間
