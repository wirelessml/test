## Macプロセス管理の教訓（4/11夜）

### M1 8GBの限界
- Claude Desktop + Cursorだけでも重い（合計CPU ~300%）
- RVC学習は不可能（DataLoaderでハング）。推論のみ可能
- 重いPythonプロセスとの同時稼働は避ける

### RVC-WebUI運用時の注意
- 再起動時は `ps aux | grep frpc` で古いGradioトンネルを確認・kill
- 学習失敗後は `ps aux | grep python3.10` で孤児ワーカーを確認・kill
- `torch_shm_manager` も残るので `ps aux | grep torch_shm` で確認

### リモート監視（Windows PCから）
- SSH: `yuika@100.99.41.2`（Tailscale経由、paramiko使用）
- 負荷確認: `uptime` + `ps aux | sort -nrk 3,3 | head -10`
- メモリ確認: `vm_stat`（Pages freeが数千以下なら危険）

### agent-browser supervisor の罠（5/2 朝）

**症状**: `agent-browser close --all` 実行後も chrome プロセスが復活し続ける（数秒〜数分後）。`pkill -9 -f "Chrome for Testing"` で殺しても**自動再起動**。

**真犯人**: `/Users/yuika/local/lib/node_modules/agent-browser/bin/agent-browser-darwin-arm64`（parent PID 1 で孤立デーモン化した supervisor プロセス）が裏で生き続けて chrome を spawn し直す。`close --all` は CDP 接続を閉じるだけで supervisor は止めない。

**完全停止コマンド**:
```bash
pkill -9 -f "agent-browser-darwin"   # supervisor を先に殺す
pkill -9 -f "Chrome for Testing"     # chrome 子プロセス群
pkill -9 -f "agent-browser-chrome"   # 念押し
```

3 つを順番に実行することで chrome の復活ループ停止。

**インパクト**: 解放されないと chrome helper × 8-12 個で **~1 GB RAM 占有**継続、M1 8GB では司令塔運用が破綻する。

**運用ルール**（5/2 朝確定）:
- agent-browser を使ったタスクが完了したら、**`close --all` だけで終わらせず supervisor まで倒す**
- 連続使用セッション（Conductor Studio 7 コース連戦等）でも、終了時に必ず supervisor 倒す
- 「使い終わったら即解放」を徹底（M1 8GB 司令塔モードの絶対条件）

**確認方法**:
```bash
ps -eo pid,ppid,etime,rss,comm | grep -E "agent-browser-darwin|Chrome for Testing" | grep -v grep
# 何も出なければ完全停止
```

### 司令塔モードの維持原則（5/2 朝確定）

M1 8GB は**指揮系統の司令塔**として常に軽量である必要がある。重い作業はしゅん先生 PC（コワーキング据え置き、16-32GB）に SSH or Remote Control 経由で逃がす。

| 項目 | M1 で OK | M1 で NG（しゅん先生 PC へ） |
|---|---|---|
| Claude Code CLI（コーディング指揮） | ✅ | - |
| claude-mem stack（観察記録） | ✅ | - |
| Terminal + tmux 並走 | ✅ | - |
| ブラウザ自動化（一時、即解放） | ⚠️ タスク完了 → supervisor まで完全停止 | ✅（heavyweight タスクなら） |
| sniffnet / Wireshark GUI | ⚠️ 計測時のみ、終わり次第 kill | - |
| **VSCode / Cursor 常駐** | ❌（800MB-1.5GB、即 swap） | ✅ |
| ローカル LLM 推論 | ❌ | ✅ |
| ビルド / コンパイル | ❌（並走時） | ✅ |
| 動画編集 | ❌ | ✅ |
| Codex CLI 常駐 | ❌（Pro クォータ別物理機の方が分離良い） | ✅ |
| OBS / 配信 | ❌ | ✅ |
| Manus 常駐 | ❌ | - |

**メモリ予算**（M1 8GB 司令塔モード）:
- システム + Wired: 約 1.5-1.8 GB
- AI スタック (Claude Code + claude-mem): 約 1.5-2 GB
- Terminal + 雑務: 約 200-300 MB
- **作業余地（バッファ）: 4-5 GB を死守**

free が 500 MB を切ったら警戒、200 MB を切ったら即クリーンアップ着手。

