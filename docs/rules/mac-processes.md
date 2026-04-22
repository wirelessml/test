## Mac 常駐プロセスのデフォルト構成（4/18 確定）

**常時起動（M1 8GB のデフォルト運用）:**

| プロセス | RSS 目安 | 役割 |
|---|---|---|
| Claude Desktop (`/Applications/Claude.app` + helpers) | 550–750 MB | メイン会話 / Code mode / Computer Use |
| Claude Code CLI (`claude --dangerously-skip-permissions`) | 650–750 MB | 現セッション本体 |
| claude-mem worker (bun) + Sonnet 4.6 子プロセス | 300–400 MB | 観察記録生成 |
| chroma-mcp (Python) | 280–290 MB | claude-mem ベクトル DB |
| Claude Desktop 由来の Virtualization VM | 70–80 MB | Claude Desktop サンドボックス |
| Terminal | 150 MB | Claude Code CLI のホスト |

**合計 ≒ 2.0–2.4 GB**（AI ツール関連）、 残り ≒ 5.5–6.0 GB をシステム・その他用途へ割当

**必要時のみ起動（常駐させない）:**
- Codex（Free 週枠制限タイト、Claude で代替）
- Manus（タスク実行時のみ起動、普段は閉じる）
- OBS / ブラウザ多タブ / 動画系プロセス
- QEMU Windows XP VM

**メモリ圧迫時の対処順:**
1. Chrome など重いブラウザを閉じる
2. 使用中でない AI アプリ (Codex / Manus) を閉じる
3. claude-mem の chroma-mcp は残す（観察中断すると記録欠損）
4. Claude Desktop は残す（今日の判断: Code mode / メイン会話用に維持）
5. 最後の手段として Claude Code CLI を終了してセッション再開

