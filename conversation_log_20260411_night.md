# 会話記録 2026-04-11（夜・Windows PCからリモート）

## 概要

Windows PC（MASU-P55）のClaude Code CLIからSSH経由でMac（yuika.local / 100.99.41.2）の状態確認・プロセス整理を実施。

## Macが重くなっていた原因

### 状態（整理前）
- **ロードアベレージ: 31.44**（M1の4コアに対して約8倍の負荷）
- RAM 8GBに対しswapins 166M / swapouts 179M（メモリ完全に不足）
- Pages free: 4,028（約63MB空き = ほぼゼロ）

### 原因の内訳

| プロセス | CPU使用率 | 原因 |
|----------|-----------|------|
| Claude Desktop (Renderer) | 98.8% | 長時間稼働（17時間+）で肥大化 |
| Claude Desktop (Network) | 88.2% | 同上 |
| Cursor (pty-host) | 86.8% | ターミナルプロセスが暴走 |
| RVC multiprocessing workers ×7 | 各5-30% | 親プロセス死亡後の孤児プロセス |
| Gradio frpc tunnels ×5 | 微量 | WebUI再起動のたびに重複起動 |
| torch_shm_manager ×5 | 各15-20% | RVC学習失敗後の残骸 |
| Brave Browser | 1.9% | 通常動作 |

### なぜこうなったか

1. **RVC-WebUIを複数回起動/再起動した**
   - 起動のたびにGradio frpcトンネルが新しく作られるが、古いものが残り続けた（5個蓄積）
   - 16:25, 16:28, 16:57, 17:11, 17:50 と5回分のトンネルが生存

2. **RVC学習がDataLoaderでハングした**
   - 学習フェーズでCPU/MPS両方ともforward pass後にフリーズ
   - 親プロセスを強制終了したが、子のmultiprocessingワーカーが孤児化（PPID=1）
   - resource_tracker（7個）、torch_shm_manager（5個）も残存

3. **8GB RAMでは全く足りなかった**
   - Claude Desktop + Cursor + RVC + Brave を同時に動かすのはM1 8GBには無理
   - 大量スワップ発生 → ディスクI/O増大 → さらに遅くなる悪循環

## 実施した整理作業

### 1. Gradio frpcトンネル整理
- 古い4つ（PID 44282, 44434, 45118, 45456）をkill
- 最新の1つ（PID 47834）を残す
- **ロードアベレージ: 31 → 10**

### 2. RVC Pythonワーカー全停止
- `/opt/homebrew/Cellar/python@3.10` の全プロセスをkill
- resource_tracker 7個、torch_shm_manager 5個も削除
- ai-minimalist-shibu（Python 3.9）は影響なし

### 3. Claude Desktop停止
- killallで全プロセス終了
- **ロードアベレージ: 10 → 3.9**

### 4. Brave Browser停止
- killallで終了
- **ロードアベレージ: → 2.7**

### 5. Cursor停止
- killallで本体終了、残ったpty-host（PID 755）もkill
- **ロードアベレージ: → 2.9**

### 整理後の状態
- **ロードアベレージ: 2.92**（整理前の約1/10）
- **Pages free: 62,948**（整理前の約15倍）
- 動作中のユーザーアプリ: ai-minimalist-shibu（ポート8787）のみ
- CPU上位はシステムプロセスのみ（coreaudiod 15%等）

## その他の調査

### TTS（テキスト音声合成）の選択肢調査
- **Qwen3-TTS**: GitHub 60件のopen issues。音声歪み、メモリリーク、依存関係競合、RAM 96GB推奨。M1 8GBでは非現実的
- **ElevenLabs**: クラウドAPI型。月$5のStarterプランで音声クローン可。Python SDK + MCPサーバーあり。70言語対応
- CLAUDE.mdの記録通り、Qwen3-TTSとSpark TTSは「動いたが似てなかった」（品質不足）

## 教訓

- M1 8GBでRVC学習は不可能。推論のみ可能
- RVC-WebUIの再起動時は古いfrpcプロセスを確認・killすること
- Python multiprocessingの子プロセスは親が死んでも残るため、手動で確認が必要
- Claude Desktop + Cursor + 重いPythonプロセスの同時稼働はM1 8GBでは避ける

## 接続情報メモ

- SSH: `yuika@100.99.41.2`（Tailscale経由）
- Windows PCからparamikoで接続（sshpass/expectが未インストールのため）

