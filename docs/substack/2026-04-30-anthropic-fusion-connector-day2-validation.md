# Anthropic「Claude × Autodesk Fusion」connector を 2 日で殴り倒した日 — M1 8GB から Windows 16GB へリレーして 3D ベアリングブロックまで

> Anthropic が 4/28 にリリースした 9 個の Creative Connectors のうち Autodesk Fusion 連携を 2 日後 (4/30) に実機検証。M1 MacBook Air 8GB のメモリ壁で詰まり、コワーキング据置の Windows PC (i7-8700K + 16GB) へバトンタッチ、ポート 27182 で MCP server 接続、自然言語から **50mm 立方体 → 機械部品レベルのベアリングブロック** まで作成完遂。本日の検証ログ全部。

---

## 起こったこと一行で

「Claude Desktop に "50mm 立方体作って" と打ったら、別ウィンドウで動いてる Autodesk Fusion 側に立方体が出現した」

---

## 何が新しいのか

2026 年 4 月 28 日、Anthropic が **Claude for Creative Work** という新カテゴリーを発表し、9 つのプロ向けクリエイティブツール統合 (Adobe / Autodesk Fusion / Blender / Ableton / SketchUp / Splice / Affinity / Resolume / Wire) を一斉ローンチした。MCP (Model Context Protocol) ベースで、各ベンダーが自前で MCP server を維持する形式。

その中で Autodesk Fusion connector は:

- **Fusion subscription があれば全プラン即時利用可能**(Personal Use の無料ライセンスで OK)
- ローカル Fusion app に MCP サーバーを内蔵する localhost-only 接続 (データは外に出ない)
- Claude が **fusion_mcp_execute / fusion_mcp_read / fusion_mcp_update** の 3 ツール経由で Fusion の API を叩く
- 「Text to CAD」だけでなく、既存モデルへのパラメトリック編集や寸法読取も可

Anthropic 側のアナウンスは [Claude for Creative Work](https://www.anthropic.com/news/claude-for-creative-work)、Autodesk 側は [Bringing Fusion onto Claude for Creative Work](https://aps.autodesk.com/blog/bringing-fusion-claude-creative-work) で同時掲載。

---

## 詰まりポイント 1: Claude Desktop 縛り

最初は Claude.ai (ブラウザ) 経由で済ませようとしたが、connector ページに堂々と書いてある:

> **この拡張機能を使用するには Claude for Desktop を入手してください**

事前調査で「Claude.ai と Claude Code でも使える」という記事を見ていたが、それは他コネクター全般の話。Fusion 限定では Claude Desktop **強制**だった。Anthropic が公開している [MCP Registry API](https://api.anthropic.com/mcp-registry/v0/servers) を直接叩いて 217 サーバーをページネーション全件チェックしても、Fusion / Blender / Adobe 系は登録なし — つまり Claude Desktop の内蔵ディレクトリ専用配信になっている。

---

## 詰まりポイント 2: M1 8GB のメモリ壁

Claude Desktop (Electron、~700-900 MB) + Fusion (アイドル 1.5-2 GB) + 既存の Claude Code CLI セッション (~600 MB) を同時起動すると **試算 9.4-10 GB**。M1 MacBook Air 8GB では確実に swap が走る。

メモリ削減を全方位でやってはみた:

- Karabiner-NotificationWindow / WeatherWidget / Claude.app crashpad 孤児 / Steam ipcserver / mediaanalysisd など計 7 プロセス kill
- macOS は容赦なく respawn してくる (contactsd / sharingd は kill 直後に同等サイズで復活)
- それでも Spotlight reindex 副次効果で 519 MB 解放、free 124 → 671 MB

しかし Fusion を起動する余裕はない。判断: **コワーキング据置の Windows メイン機 (i7-8700K + 16GB DDR4 + 4/29 移行直後の Acer FA100 NVMe) へリレー**。

---

## 引き継ぎプロセス

M1 で書いた引き継ぎドキュメント (`docs/journal/2026-04-30-handoff-shun-sensei-pc.md`、106 行) を git push、Windows 側で `git pull` で受け取る。Claude Code CLI で「セッション引き継ぎ」プロンプトを投げる方式。

ドキュメント本文は:
- 目的 (4/28 Fusion connector 検証)
- M1 側の制約 (メモリ事情) と 環境差分 (Windows 11 25H2、IP 192.168.2.174、Tailscale 未参加)
- 順序固定の手順リスト 7 ステップ
- M1 で完了済みの作業 7 項目 (新セッションが触らなくていい範囲)
- Anthropic 公式仕様の抜粋 (Local-only / Requirements 明記)

---

## 詰まりポイント 3: ポート 27182

Claude Desktop の Autodesk Fusion connector 設定で「Port (The port number of Fusion MCP server)」**27182** がデフォルト表示される。気付いた瞬間思わず笑った:

> **27182 = e (ネイピア数 / Euler's number) の頭 5 桁**
> e = **2.7182** 81828 45904 5235...

CAD ベンダーである Autodesk が MCP server のデフォルトポートに **自然対数の底**を選ぶ engineer joke。e は微分方程式・指数関数・成長モデル等、工学全般で頻出する基本定数なので、エンジニア向けツールとしては π より e の方が文脈に合う。

検証: Fusion 側で **Preferences → General → API → Fusion MCP Server** を有効化、ポート 27182 で listen 開始 → Claude Desktop の connector トグル OFF→ON で再接続 → ピンクのエラー消失。

---

## 動作確認 — 50mm 立方体

Claude Desktop の新規チャットで:

```
Fusion で 50mm × 50mm × 50mm の立方体を作って
```

Claude の応答 (実際のメッセージから引用):

1. アクティブなデザインがないようです。開いているドキュメントを確認します。
2. 開いているドキュメントがないので、新規ドキュメントを作成してから立方体を作ります。
3. 50mm 立方体が作成できました。確認のためスクリーンショットを撮ります。
4. 完成しました。新規 Fusion デザインに 50mm × 50mm × 50mm の立方体 (バウンディングボックスで実測値も一致) を作成しています。

つまり:

- `fusion_mcp_read` でデザイン状態を確認
- `fusion_mcp_execute` で新規ドキュメント + スケッチ + 押し出し
- `fusion_mcp_read` でバウンディングボックス再検証

を順序立てて自律実行。Fusion ウィンドウ側を見ると 50mm 立方体が現れていて、タイムラインに「スケッチ」+「押し出し 1」がフィーチャーとして残っている (= 後から寸法編集できる **真の parametric モデル**)。

---

## 発展形 — ベアリングブロック

立方体ができたなら次は実用部品。追加プロンプトを矢継ぎ早に:

- 押し出しを 100mm に変更 (タイムライン経由で寸法編集)
- 中央に Φ20 貫通穴
- 4 隅に M5 ボルト用座ぐり穴

結果、機械加工レベルの **ベアリングブロック / モーターマウント風** 部品ができ上がった。Fusion 3D ビューで isometric 表示すると、シャフト穴と取付穴が綺麗に並ぶ。エッジ面取りや材質設定 (ASTM A36 鋼)、重量計算、STEP 書き出しまで自然言語で進められる手応え。

---

## 検証で得た事実

| 項目 | 値 |
|---|---|
| connector 名 | Autodesk Fusion |
| 露出ツール | `fusion_mcp_execute` / `fusion_mcp_read` / `fusion_mcp_update` |
| デフォルトポート | **27182** (= π の 4-7 桁) |
| 必須環境 | Claude Desktop + ローカル Fusion 起動 |
| ライセンス | **Personal Use Free で動く** (subscription 不要) |
| 通信方式 | localhost-only |
| OS | Windows / Mac 両対応 (検証は Windows 11) |
| デフォルト権限 | 各ツール「承認が必要」(実行前にダイアログ) |

---

## 何が嬉しいか

これまで Fusion を使うには:
1. Fusion 起動
2. ハブ選択
3. ファイル新規作成
4. メニューから XY 平面選択
5. スケッチ作成
6. 矩形描画
7. 寸法拘束
8. 押し出し
9. 寸法入力

の **9 ステップ** を毎回手動でやっていた。これが「**Fusion で 50mm 立方体作って**」の 11 文字に圧縮される。複雑な部品でも自然言語で指示しながら、生成された **parametric なタイムライン**は後で手動で微調整できる。AI 生成 + 人間レビュー + パラメトリック編集 のハイブリッドが理想形だが、Fusion connector はそれをそのまま実装している。

---

## 何が惜しいか

- **Claude Desktop 縛り** — Claude Code CLI / Claude.ai web では今のところ使えない。Anthropic が今後 remote MCP として開放する可能性はある。
- **M1 8GB はキツい** — Claude Desktop + Fusion で 2-3 GB は最低でも食う。8GB 機 + Cursor 系 IDE 並行作業の人は別マシンでやる前提。
- **複雑形状ではまだ手動修正が必要** — 単純な機械部品は問題ないが、有機形状 (鋳造部品の R 面継ぎ等) はプロンプトで詰めるよりマウス操作の方が早い局面もある。

---

## まとめ

Anthropic 4/28 ローンチの Autodesk Fusion connector を、ローンチ 2 日後に M1 Mac → Windows PC リレーで初動から実用部品作成まで完遂。**ポート 27182 = π の 4-7 桁**、`fusion_mcp_execute` / `fusion_mcp_read` / `fusion_mcp_update` の 3 ツール構成、Personal Use Free で全機能利用可。CAD 操作の 9 ステップが自然言語の 11 文字に圧縮される未来は、もう来ている。

---

## 関連リンク

- [Anthropic — Claude for Creative Work](https://www.anthropic.com/news/claude-for-creative-work)
- [Autodesk APS — Bringing Fusion onto Claude for Creative Work](https://aps.autodesk.com/blog/bringing-fusion-claude-creative-work)
- [DEVELOP3D — 'Claude for CAD' arrives with Blender and Autodesk Fusion connectors](https://develop3d.com/ai/claude-for-cad-blender-autodesk-fusion/)
- [9to5Mac — Anthropic releases 9 Claude connectors for creative tools](https://9to5mac.com/2026/04/28/anthropic-releases-9-new-claude-connectors-for-creative-tools-including-blender-and-adobe/)

(仲啓輔 / 2026-04-30)
