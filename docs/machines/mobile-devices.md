# モバイル・周辺機器

> Last updated: 2026-04-22

## iPhone 15 Pro（名前: 結花）

- **役割**: メインスマホ
- 機能: Dispatch（Claude Desktop）、Tailscale 接続、iPhone Claude Desktop からリモート指示
- Tailscale IP: `100.74.77.115`
- Tailscale: 1.96.5、iOS 26.5.0
- 撮影用途: CrystalDiskInfo 等のスクリーン撮影、しぶ情報収集

## 初代 iPad Pro 9.7 インチ（名前: 彩羽）

- **役割**: テザリング用サブ機
- SIM: 楽天 SIM 挿入
- 用途: テザリング、Instagram 監視（非常用）

## テレビ・モニター

### パナソニック VIERA TH-40CX700
- 2015 年モデル 4K TV
- 自宅設置
- HDR 非対応（iPad → HDMI 接続時 HDR 設定選択の罠あり）

### LG 40WP95C-W
- 39.7 インチ 5K2Kウルトラワイドモニター
- Mac（M1 MacBook Air）接続用
- 自宅設置

## その他

### Nintendo Switch
- 所有済み
- Switch 2 本体は未購入（GC313Pro でのキャプチャは 4/22 公式動作確認済）

## テザリング接続ポリシー

- Wi-Fi: `YKSmas318`（コワーキングスペース Wi-Fi、メイン）
- Wi-Fi バックアップ: `rams502`（コワーキング、パスワードは `~/.claude/local-notes/wifi.txt`）
- テザリング検出: `ifconfig en5 2>/dev/null` で iPhone USB 接続確認
- テザリング名表記:
  - 結花 = iPhone 15 Pro
  - 彩羽 = iPad Pro 9.7

## 関連ファイル

- リモートコントロール運用: @docs/routines/remote-control-report.md
