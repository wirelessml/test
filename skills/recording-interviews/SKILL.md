---
name: recording-interviews
description: Use when recording or transcribing 面談 / Zoom / Google Meet / 取材動画, when whisper output has repeating hallucination loops, when ffmpeg screen capture hangs on macOS, or when setting up mic + BlackHole audio capture
---

# 面談録画・文字起こしパイプライン（Mac M1）

## Overview

6/7〜6/11 に E2E 実証済みの 3 コマンド体制。**画面と音声を別系統で録り、音声は自分/相手を別トラックに分離**するのが核（相手の声が小さくても後から救える）。whisper.cpp はローカル・無料。

## Quick Reference

| コマンド（ダブルクリック実行） | 用途 | 出力 |
|---|---|---|
| `面談-録画.command` (v3) | 画面＋自分の声＋相手の声を別録り | `~/面談録画/面談-<TS>.mp4` + `-自分.wav` + `-相手.wav` |
| `面談-文字起こし.command` (v2) | 最新録音を自動選択して文字起こし | `.txt` / `.srt` / 別トラックなら【自分】【相手】ラベル付き `-会話.txt` |
| `訪問動画-下ごしらえ.command` | iPhone 動画＋Mac 別録り音声を合成→SRT 一気通貫 | `~/Desktop/訪問動画素材/<名前>-下ごしらえ.mp4/.srt/.txt` |
| `Bグループ面談-録音.command` | 音声のみ（旧方式、ミックス 1 ファイル） | `~/面談録音/面談録音-<TS>.wav` |

実体は `scripts/`（git 管理）と `~/Desktop/`（起動用コピー）の両方にある。**編集したら両方を同期すること**。

## 事前準備（面談前に 1 回、忘れると相手の声が録れない）

1. **システム設定 > サウンド > 出力 = 「複数出力装置」**（EarPods primary + BlackHole 2ch。Audio MIDI 設定で構成済み）
2. Zoom はアプリ不要、**Chrome ブラウザ参加で可**（zoom cask は sudo 必須でリモート導入不可、6/11 実証）
3. **M1 の蓋を閉じない**（蓋閉じで内蔵マイクが HW 切断される、6/11 教訓）

## 罠と対策（ハマったら最初にここを見る)

| 症状 | 原因と対策 |
|---|---|
| ffmpeg の画面キャプチャが無応答 | **macOS では avfoundation 画面入力がハングする**。画面は `screencapture -x -v`、音声だけ ffmpeg に分担（v3 方式） |
| whisper が同じ文を延々繰り返す | 繰り返し幻覚。**`-mc 0`（max-context 0）を常時付与**（6/11 GVC 面談の教訓、v2 で標準化済み） |
| 文字起こしの先頭タイムスタンプが潰れる | 録音先頭の長い無音で whisper のタイムスタンプが歪む。先頭無音を ffmpeg `-ss` で切ってから流す |
| 録音デバイスが見つからない/別デバイスを掴む | 連係カメラ(iPhone)接続で avfoundation の**番号がズレる**。番号でなく**名前指定** `-i ":MacBook Airのマイク"` / `-i ":BlackHole 2ch"` |
| 仕上げ MP4 が無い | Ctrl+C 後の合成中に窓を閉じた。素材 wav/mov は残る設計なので手動合成可能 |

## 技術メモ（スクリプト改修時用）

- **ffmpeg 1 プロセスで 2 入力 2 出力**: `-f avfoundation -i ":マイク" -f avfoundation -i ":BlackHole 2ch" -map 0:a -ac 1 自分.wav -map 1:a -ac 1 相手.wav`（プロセス 1 個なので Ctrl+C 一発で両方止まる）
- **映像は常に無劣化** `-c:v copy`（再エンコードしない。6/10 imovie-min-test で実証した方式）
- whisper モデル: `~/whisper-models/ggml-large-v3-turbo.bin`（1.5GB、日本語精度実証済み。medium へ自動フォールバック）。whisper-cli は `/opt/homebrew/bin/whisper-cli`、入力は 16kHz mono に変換してから
- 処理時間目安: 文字起こしは音声長の約 1/5（30 分録音 → 自分+相手で計 10 分）
- 会話マージ: 自分/相手の SRT を秒でソートしてラベル付き合成（文字起こし.command 内の python ヒアドキュメント）

## 運用ルール

- 録画の YouTube 等への公開は**肖像権・プライバシーの確認なしに進めない**（6/11 に公開希望を止めた前例）
- 録画ファイルは大きい（25 分 4K ≒ 3.3GB）。git に入れない
