# 引き継ぎ: M1 Mac → しゅん先生 PC (2026-04-30 午後)

> M1 Mac の Claude Code CLI セッションから しゅん先生 PC の Claude Code CLI へバトンタッチ。

## 目的

**Anthropic 4/28 公式 Autodesk Fusion connector を Claude Desktop 経由で動かす**

- M1 8GB では Claude Desktop + Fusion + Claude Code 同時起動でメモリ不足 (~9.4-10GB 試算)
- しゅん先生 PC (i7-8700K + 16GB DDR4 + Acer FA100 NVMe) で十分余裕
- Personal Use Free ライセンスで OK、ユーザーは Claude Max プラン

## しゅん先生 PC 現在の状況 (2026-04-30 16:50 時点)

### 環境
- Windows 11 25H2、4/29 Acer FA100 512GB NVMe に SSD 移行済 (CDM 3,374 MB/s)
- ローカル IP: **192.168.2.174** (YKSmas318 Wi-Fi、Intel AC 8265、Wi-Fi 5 5GHz、60/60 Mbps)
- MAC: D4:25:8B:30:F5:D4
- Tailscale **未インストール** (リモートから到達不可、物理アクセスのみ)

### インストール状況 (PowerShell Test-Path で確認済)
| ソフト | 状況 |
|---|---|
| Autodesk Fusion | **インストール中 (18% → 待機中)** |
| Claude Desktop | ❌ 未インストール |
| Tailscale | ❌ 未インストール (任意、将来用) |

## このセッションでやることリスト (順序固定)

1. ✅ **Fusion インストール完了を待つ** (今 18% 進行中、全 5-15 分程度)
2. ⏳ **Claude Desktop インストール**
   - DL: https://claude.ai/download
   - Fusion インストール完了後にダブルクリック (同時インストール衝突回避)
3. ⏳ **Autodesk アカウントで Fusion 初回サインイン**
   - 個人用無料ライセンス選択
   - ハブ作成 (4/30 午後 M1 で「ハブ作成画面で再起動中断」状態だった)
4. ⏳ **Fusion で MCP Server 有効化**
   - メニュー: Preferences (環境設定) → General → API
   - Fusion MCP Server にチェック
   - ポート番号メモ (デフォルト不明、表示値を Claude Desktop と一致させる)
5. ⏳ **Claude Desktop で connector 有効化**
   - 起動 → Max プラン (仲啓輔 / wirelessml@gmail.com) でサインイン
   - Settings → Connectors → Autodesk Fusion を ON
   - OAuth で Autodesk 認証 (Fusion で使ったのと同じ Autodesk アカウント)
6. ⏳ **動作テスト**
   - Claude Desktop で会話: 「Fusion で 50mm × 50mm × 50mm の立方体を作って」
   - Fusion ウィンドウに自動で立方体出現 → 成功
7. ⏳ **(任意) Tailscale 導入**
   - DL: https://tailscale.com/download/windows
   - サインイン (M1 と同じ wirelessml@ アカウント)
   - 以降 M1 から `ssh yuika@<tailscale-ip>` で遠隔可能に
   - **記録**: 取得した Tailscale IP を `docs/machines/shun-sensei-pc.md` に追記

## 参考情報 (Anthropic Fusion connector 仕様)

connector 詳細 (Claude.ai のディレクトリで確認済):
- 名称: **Autodesk Fusion**
- 説明: "Create, modify, and inspect CAD geometry in Fusion"
- 「The Fusion MCP server connects Claude to a live Autodesk Fusion session, allowing Claude to send tool requests and perform real-time modeling and command-based operations directly in Fusion」
- Local-only connection (MCP サーバーはローカル PC で稼働、データは外に出ない)
- **Requirements 明記**:
  - Fusion must be installed and running locally
  - The MCP server must be enabled in Fusion under Preferences > General > API > Fusion MCP Server
  - **Claude Desktop must be installed and configured with the correct port**

## M1 Mac 側で本日 (2026-04-30) すでに完了したこと

引き継ぎ後の しゅん先生 PC セッションでは触らなくていい:

1. Karabiner-Elements v15.9.0 + HCT 片手キーパッドルール (Caps+WASD 矢印 / 1-6→F1-F6 / F+G→Cmd+Tab)
2. Caps Lock alone tap → IME 英数⇄かな トグル ルール追加 (HCT 除外)
3. @ キー問題解決 (システム設定で「日本語 - ローマ字入力」選択)
4. Google日本語入力切替不可と判明 (macOS 26.5 Tahoe + Google IME 3.33 互換性なし、TIS API 拒否)
5. Desktop 整理: 80 ファイル (5.6GB) を `_archive_2026-04-30/` へ移動 (Desktop ルート 122→43 エントリ)
6. メモリ削減作業: WeatherWidget / Karabiner-Notification / Claude.app crashpad 等 kill (~520MB 解放)
7. M1 セッションは Fusion セットアップ中も維持 (現セッション PID 1910、PhysMem 7.2GB used / 671MB free)

## M1 Mac (このセッション) との連絡先

- M1 Tailscale IP: **100.99.41.2** (macbook-air)
- iPhone 15 Pro: 100.74.77.115
- MASU-p55 (別 Windows): 100.125.21.47

しゅん先生 PC の Claude Code CLI から M1 へ何か聞きたい場合:
- 現状 SSH 双方向設定なし
- M1 側はこのセッションが起きてれば Maestri 経由で会話可能 (要起動)

## 関連ドキュメント (M1 Desktop git repo)

- `CLAUDE.md` — プロジェクト糊 (現状・運用ルール)
- `docs/machines/shun-sensei-pc.md` — しゅん先生 PC 詳細 (4/29 NVMe 移行直後の状態反映済)
- `docs/journal/2026-04-30.md` — 今日の M1 作業日誌
- `docs/reminders.md` — 期限リスト

新セッションで `git pull` (M1 リポと同期されてれば) でこれらアクセス可能。同期されてなければ、このファイルの内容だけで十分進められる。

## 完了報告のポイント

新セッション側で全部済んだら、M1 のこのセッションに以下を報告してほしい:

- [ ] Fusion インストール完了 (バージョン番号)
- [ ] Claude Desktop インストール完了 (バージョン番号)
- [ ] Fusion MCP Server ポート番号
- [ ] Claude Desktop の Autodesk Fusion connector ON 完了
- [ ] テストプロンプト「50mm 立方体作って」の結果
- [ ] (任意) Tailscale 導入 → IP 取得
