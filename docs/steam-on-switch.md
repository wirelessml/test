# Steam Linux ARM64 ベータ版 & Nintendo Switch 導入事例

取得日: 2026-04-17
情報源: X（ポルトガル語ポスト、ユーザー翻訳経由）→ 元ネタ @aagaming.me（Bluesky、2026-04-16 19:18）

## 要点

- **Valve公式リリース**: Steam Linux ARM64 beta（実験版）
- **目的**: ARMプロセッサ上でPCゲーム（Steamライブラリ）を実行
- **x86_64→ARM64 バイナリ変換**: FEX-Emu ベース想定
- **Nintendo Switch（初代/OLED、Tegra X1 ARM64）に導入**する事例が登場
  - @aagaming.me が「Steamをインストールした最初の人（その一部）」として動画公開
  - Steam Client Update Channel を "Steam Beta Update" に設定
  - "Use experimental SteamRT3 Steam Client" を有効化して起動
  - ライブラリの特定ゲームを実行するデモを予告

## Valve の狙い（推測）

- Steam Deck 後継 = ARM ハンドヘルド市場を視野
- Steam Deck は x86_64（AMD Zen 2）、後継の省電力・モバイル展開に ARM64 対応が必要
- Nintendo Switch で動かせるインパクトは PR 的に大きい（Valve も黙認？）

## 制約・注意

- **Switch 導入は非公式** — Valve が Switch 対応を謳っているわけではない
- **初代 Switch のみ**（Tegra X1 は bootloader 解析済み、Linux 起動可）
- **Switch 2（T239）は現時点で不可** — bootloader 未解析
- **動くゲームは限定的** — ARM64 ネイティブ対応タイトルはまだ少数、x86_64 ゲームは FEX エミュレーションで重くなる
- **Nintendo 規約違反** — カスタム OS 起動は BAN リスクあり

## 維新の嵐（CD 版）との関係

- 維新の嵐 幕末志士伝は 1998 年 Win32 ゲーム（x86）
- Linux ARM 環境では動作不可（Wine + Box86/Box64 でも厳しい）
- **XP VM ルートで正解**（現在 QEMU i386 + WinXP SP3 構成済み）

## 関連 URL

- 元ポスト: https://bsky.app/profile/aagaming.me
- Valve Steam for Linux: https://partner.steamgames.com/doc/store/application/platforms

## 関連プロジェクト

- ユーザーの Switch 2 キャプチャ環境構築（AVerMedia GC313Pro 発注済み、CLAUDE.md TODO #9）とは別系統
- Switch 2 で Steam を動かす話ではない
