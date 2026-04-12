# 会話記録 2026-04-12（午前〜午後・コワーキング）

## 概要

Mac再起動後、Terminal.appでClaude Code直接起動の実験を実施。Cursorを終了してリソースを解放し、Terminal.app構成での長時間安定運用を確認。定時報告ループ（5分間隔、Gmail下書き）を2時間19分・22回実行。しぶの新Mac購入情報の記録、PC比較、SwitchBot AIハブ調査なども実施。

## 環境

- Wi-Fi: YKSmas318（コワーキング、2GHz/5GHz自動切替）
- Mac起動: 10:21（再起動後）
- Claude Code: Terminal.appで直接起動（`claude --dangerously-skip-permissions`）

## 実施内容

### 1. Terminal.appへの移行テスト
- 目的: Cursorを閉じてCPU/メモリを解放しつつClaude Codeを維持
- 結果: **成功**
  - Cursor終了でロードアベレージ 3.90 → 1.48（62%低下）
  - Pages free: 3,799 → 96,192（約25倍に増加、約1.5GB解放）
  - MCP接続（Gmail、Chrome DevTools等）正常維持
- 前セッション（s001）はCursor終了時に自動終了していた
- **結論: M1 8GBではCursorなしのTerminal.app構成が最適**

### 2. 定時報告ループ（5分間隔×22回）
- 10:54〜12:40の2時間19分間、Gmail下書きに定時報告を作成
- ScheduleWakeup（270秒間隔）でループ継続
- 報告内容: CPU、メモリ、トッププロセス、ネットワーク

#### CPU推移
- ロードアベレージ: 3.90（Cursor起動中） → 1.04〜1.98（Terminal.app構成）
- 平均約1.55、一度も危険域に入らず
- M1 8コアの約19%使用率 → **CPUは余裕たっぷり**

#### Claude CLIメモリ推移
- 390 → 572（ピーク①） → 480（圧縮） → 534 → 587 → 572 → 502（圧縮） → 480 → 534 → 552 → 587 → 575 → 611 → 626 → 648（ピーク②） → 617（圧縮） → 644MB
- 600〜650MBレンジで安定化（増加→圧縮のサイクル）
- 700MBに到達せず、長時間運用に耐える

#### 観測された一時的イベント
- Safari SafeBrowsing: CPU 52%（DB更新、一過性）
- mediaanalysisd: 263MB → 143MB（メモリ解放進行）
- Wi-Fi チャンネル自動切替: ch6 → ch52 → ch6 → ch11 → ch6

### 3. しぶInstagramストーリー新情報
- **M5 MacBook Air購入**（424,800円）
  - 10コアCPU / 10コアGPU / 32GB / 4TB SSD / ミッドナイト
  - 用途: 「自立型AI入門、家に置いてClaude動かしっぱなし用🖥」
  - 31歳誕生日（3/30）の自分へのプレゼント
- **旧MacBook Air（M1）をりくとに譲渡**
  - @rikuto_takemoto「MacBook Air しぶモデル受け継いだ！これでAIと友達になります！」
- **AI秘書「しぶ次郎（Bot）」Discord上で稼働中**
- **誕生日に朝から晩までAI指導**: OpenClaw・Claude Code・Cursorをゼロから学習
- → ナレッジ `shibu-ai-adoption.md` に保存済み（git commit済み）

### 4. PC比較分析
#### 4台比較（Claude Code用途）
| PC | CPU | メモリ | ストレージ | 評価 |
|---|---|---|---|---|
| M1 MacBook Air | M1 8コア | 8GB | 256GB | モバイル最適 |
| MASU-P55（Windows） | i5-1235U 10コア | 8GB | 238GB | M1に劣る |
| MacBook Neo（注文品） | M1相当 | 8GB | 256GB | M1と互角、99,800円 |
| **デスクトップPC** | **i7-8700K 6C/12T** | **16GB** | **2TB** | **ベスト（メモリ）** |

- CPU対決: M1 > i5-1235U（シングルコア・電力効率で勝ち）
- **ベストPC: デスクトップ（16GBメモリが決め手）**
- M1 MacBook Air ≒ MacBook Neo（実質同等）

#### Windows PC（MASU-P55）SSH接続
- Tailscale経由でsshpass使用、スペック取得成功
- i5-1235U / 8GB / 238GB SSD (SK hynix) / Intel UHD / Windows 11 Pro 25H2

### 5. SwitchBot AIハブ調査
- **AIハブ（39,980円）+ シーリングライト（6,580円）** の組み合わせ
- OpenClaw対応: AIエージェントで家電操作
- **LLMは内蔵されていない** → ユーザーがAPIキーを用意（GPT/Claude/Gemini等）
- AI+プラン（VLM）: 月2,980円（初月無料）、AWSの日本リージョン
- 6TOPSのAIチップ搭載（ローカル推論用）

#### 無料で使う方法
- Ollama + ローカルLLM（Qwen 2.5等）で完全無料運用可能
- ただし別途PC（16GB推奨）でOllama常時稼働が必要
- デスクトップPC（i7-8700K/16GB）なら可能、M1 8GBでは厳しい

### 6. Qwenファミリー整理
| モデル | 用途 |
|---|---|
| Qwen 2.5 | LLM（考える） |
| Qwen3-TTS | 音声合成（喋る） |
| Qwen-VL | 画像理解（見る） |
| Qwen-Audio | 音声理解（聞く） |
| Qwen-Coder | コード生成 |

### 7. agent-browser記事（Zenn）
- 著者: しんや（4/11投稿）
- agent-browser = Claude Code最適のブラウザ自動化ツール
- Playwright MCP = Claude Desktop向け
- CLAUDE.mdの構成（agent-browser優先）と一致

### 8. MacBook Neo注文
- 13インチ MacBook Neo ブラッシュ: 99,800円
- 配送先: はりきゅう整体 しゅん（兵庫県伊丹市）
- 通常配送 明日届き

## バージョン情報
- Claude Code: Terminal.appで直接起動
- Claude Model: Opus 4.6（1Mコンテキスト）
- macOS: 26.5.0
- Terminal.app: 標準

## 教訓
- **M1 8GBでのClaude Code最適構成 = Terminal.app + bypass permissions**
- Cursorは不要（Electronのメモリ圧迫がボトルネック）
- Claude CLIメモリは600〜650MBで安定（圧縮サイクルが有効）
- CPUは19%程度でM1には十分な余力がある
- ボトルネックは常にメモリ（8GB）
