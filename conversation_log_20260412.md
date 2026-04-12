# 会話記録 2026-04-12（朝・コワーキング）

## 概要

MacBook Air M1にて作業。4/11のWindows PC作業の振り返り、ElevenLabs声クローン音声の生成・調整、Mac環境の最適化を実施。

## 環境

- Wi-Fi: YKSmas318（コワーキング、5GHz）
- Mac起動: 04:28 JST

## 実施内容

### 1. 4/11 Windows PC作業の振り返り
- git log確認: 4/11は**44コミット**の大量作業
- Windows PCにSSH接続して未push分を発見
- **Mac側にない3コミット**を発見・pull:
  - ElevenLabs Starter($6/月)契約 → 声クローン作成（Voice ID: LIDNtfJHRfi2AFJWPFeV）
  - TTS版 + STS版の比較（TTSの方が品質良好）
  - 荘園解説の声クローン音声生成
  - Starterプラン即解約済み（5/11まで有効、残クレジット約35,000）

### 2. ElevenLabs声クローン音声の生成
- Windows PCのClaude CodeメモリからAPIキーの保管場所を特定
  - `~/.zshrc`の`ELEVENLABS_API_KEY`環境変数に保存されていた
- **MacからcurlでElevenLabs API直叩き**で音声生成（Python SDK不要）
- 『詳説日本史改訂版』荘園記述の変更点を読み上げ
- **8回の読み調整**を実施（ひらがな読み指定で誤読を修正）
  - 荘園→しょうえん、寄進→きしん、領主→りょうしゅ
  - 鹿子木荘事書→かなこぎのしょうことがき
  - 神護寺領紀伊国田荘→じんごじりょうきいのくにかせだのしょう
  - 預所→あずかりしょ、下司→げし、公文→くもん 等
- 最終版は**eleven_v3**（最新モデル）で生成（1分18秒）
- サイトにテキスト全文 + ループ再生音声プレーヤーを追加
- GitHub Pages公開: https://wirelessml.github.io/test/ai-minimalist-shibu/#voice

### 3. ElevenLabsモデル比較
| モデル | 状態 |
|--------|------|
| eleven_v3 | 最新（採用） |
| eleven_multilingual_v2 | 旧版（初回使用） |
| eleven_flash_v2_5 | 高速版 |
| eleven_turbo_v2_5 | 高速版 |

### 4. Mac環境の最適化
- **キーリピート設定**: `KeyRepeat=1`, `InitialKeyRepeat=10`（約6倍速）
  - 反映にはMac再起動が必要
- **Claude Desktopを閉じてメモリ解放**:
  - Pages free: 3,648（57MB） → 35,257（550MB）、約10倍に回復
- **Cursor Renderer問題**: CPU 69% → 100%に上昇
  - Electron長時間稼働による肥大化
  - 対策: 定期的なアプリ再起動

### 5. 技術トピックの議論
- **Superwhisper**: Mac用ローカル音声入力アプリ。しぶ的には「まずApple標準を試せ」
- **AIコーディングハーネス**: 自作→GitHubからDL時代へ。型通りに作れるのが最速
- **LLMへの知識注入**: CLAUDE.mdやナレッジファイル設計自体がスキル
- **Claude Codeの敷居**: ターミナル・ファイルパス・gitの理解が前提
- **AIが書くコードの冗長性**: デフォルトで安全側に振る問題。事前に「パフォーマンス優先」と指示すべき
- **M1 8GBの構造**: CPU/GPU統合SoC、ユニファイドメモリ、CUDA不可

## バージョン情報
- Claude Code: 2.1.101（Mac/Windows共に最新）
- Cursor: 3.0.16
- ElevenLabs Python SDK: 2.42.0（Windows）
- Claude Model: Opus 4.6（1Mコンテキスト）

## 次の作業
- Mac再起動（キーリピート設定反映）
