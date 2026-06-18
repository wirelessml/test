# 大学無償化ウォッチ 日次ダイジェスト 設計書

> 初版: 2026-06-19 / 仲啓輔
> 発端: おときた駿の「Claude+Pythonで政治ニュース・国会議事録を毎日自動要約」ツイートのリアリティチェック（@docs/journal/2026-06-19.md 追記2）→「同じことを大学無償化で」。
> 雛形: `scripts/job-search-daily-mac.py`（毎朝04:30の求人パイプライン）。LLM 不使用だった同スクリプトに対し、本件は **claude CLI 要約**が新規要素。

## 1. 目的

「大学無償化」関連の **国会発言（一次情報）＋政治ニュース** を毎日自動で収集し、新着のみを Claude（Haiku）で要約して、朝にメールで受け取る。

## 2. 方針（アプローチ）

- 既存 `job-search-daily.py` を**雛形に、独立した新規スクリプト** `seimu-watch-daily.py` として作る。求人パイプラインには一切手を入れない（事故隔離）。
- 流用するもの: `fetch()` 相当の HTTP 取得、`run_cmd()` 相当の堅牢実行、`send-email.py`＋`~/.config/masu-p-watch/email.json`（既存のメール基盤・新規シークレット不要）、LaunchAgent パターン。
- **GitHub push は使わない**（個人の関心トラッキングで公開不要。公開リポPII懸念も回避。今日直した git-同期バグの種類が最初から存在しない）。

## 3. データフロー

```
国会会議録API + Google News RSS 取得
  → キーワード絞り込み
  → 既出除外（状態ファイル: speechID / 記事URL）
  → claude -p (Haiku) で要約（新着をまとめて1回）
  → Markdown ダイジェスト生成
  → メール送信（send-email.py）＋ ローカル保存
  ＊ LaunchAgent で毎日 06:00 実行
```

## 4. コンポーネント

### 4.1 国会議事録（一次情報）
- API: `https://kokkai.ndl.go.jp/api/speech`（公式・無料・認証不要・JSON。2026-06-19 のファクトチェックで実在確認済み）。
- 検索: 任意語キーワード（`any`）＝下記キーワード、会議日レンジ `from=today-45 / until=today`、`maximumRecords=100`、`recordPacking=json`、必要なら `startRecord` でページング。
- 取得項目: `speechID` / `speaker` / `nameOfMeeting` / `date` / `speech`（本文）/ `speechURL` / `house` / `session`。
- **既出除外**: `seen-speech-ids.txt` に記録した `speechID` を除外。議事録は公開が数日〜数週遅れるため、**トレーリング窓（45日）＋ID重複排除**で「新規公開分」を取りこぼさず・二重報告せず拾う。

### 4.2 ニュース
- Google News RSS: `https://news.google.com/rss/search?q=<keyword>&hl=ja&gl=JP&ceid=JP:ja`（認証不要）。
- 取得項目: タイトル / リンク / pubDate / 媒体名。
- **既出除外**: `seen-news-urls.txt` に記録した記事URL（または guid）を除外。

### 4.3 キーワード（初期セット・スクリプト冒頭で調整可）
`大学無償化` / `高等教育無償化` / `授業料無償化` / `高等教育の修学支援新制度`

### 4.4 要約エンジン（claude CLI）
- 新着項目をまとめて **1日1回の `claude -p`** に渡す（呼び出し回数=1でレート枠消費を最小化）。
- モデル: Haiku（`--model claude-haiku-4-5-20251001`）。
- claude 実体: standalone（`~/.local/bin/claude`、フルパス指定で LaunchAgent から確実に解決）。既存ログイン認証を使用＝追加課金なし。Claude Code の5時間枠を消費するが Haiku＋1回/日で軽微。
- プロンプト出力: (a) 全体の要点 3〜5 行、(b) 各項目の 1〜2 文要約。
- **フォールバック**: claude 呼び出しが失敗・タイムアウトしても、**要約なしの一覧（リンク＋抜粋）＋警告でメールは送る**（リンクは必ず届く）。

### 4.5 出力フォーマット（Markdown）
```
# 【大学無償化ウォッチ】YYYY-MM-DD 新着N件

## 今日の要点
（Claude 全体サマリ 3〜5 行）

## 国会発言（M件）
- [YYYY-MM-DD｜会議名｜発言者] 要約1〜2文  → speechURL

## ニュース（K件）
- [媒体｜YYYY-MM-DD] 要約1文  → URL
```
新着0件のときはローカルレポート本文を「本日新着なし」とする（メール送信は §5 の判断によりスキップ）。

### 4.6 配信
- メール: `send-email.py`＋`~/.config/masu-p-watch/email.json`（既存基盤を流用）。宛先 `wirelessml@gmail.com`。
- 件名: `【大学無償化ウォッチ】YYYY-MM-DD 新着N件`（0件時は下記の判断に従う）。
- ローカル保存: `~/Library/Application Support/seimu-watch/reports/YYYY-MM-DD.md`。

## 5. 既定の判断

- **スケジュール**: 毎日 **06:00**（LaunchAgent `com.yuika.seimu-watch`。04:30 求人と非衝突）。
- **新着0件のときのメール**: **送らない（ログのみ）**。毎日の「新着なし」メールは受信箱ノイズになるため。ローカルレポートとログには記録する。※「0件でも届いた方が安心」なら送信に変更可（spec レビューで指定を）。
- **状態管理**: `seen-speech-ids.txt` / `seen-news-urls.txt`（追記式）。肥大化時は古い行を間引く（当面は放置で可）。
- **配置**: 全ファイルを `~/Library/Application Support/seimu-watch/` に置く（launchd の TCC 罠回避＝job-search の教訓）。git 正本は `scripts/seimu-watch-daily.py`、編集後 cp で同期。plist は `config/launchagents/` にも収容（bootstrap パターン）。

## 6. エラー処理（job-search の教訓を最初から）

- 取得が**全滅**（国会・ニュースとも0件取得＝ネットワーク/API異常の疑い）のときは、空ダイジェストを送らず**警告をログ＋メール件名に明示**。
- 「新着0件（取得は成功）」は**正常**（求人と違いエラーではない）。
- claude 要約失敗 → 4.4 フォールバック（要約なしで送る）。
- 二重送信防止: 当日送信済みマーカー（`last-sent-date.txt`）。
- すべての外部コマンドは run_cmd 相当で非0検知。

## 7. テスト / 受け入れ基準

- `SW_DRY_RUN=1`: 取得＋要約＋ローカル生成まで行い**メール送信しない**。
- 受け入れ基準:
  1. ドライランで、国会発言・ニュース双方を含む Markdown ダイジェストがローカル生成され、Claude 要約が入る。
  2. 同日2回目の実行で新着0件（dedup が効く）。
  3. 本番1回で正しい件名のメールが届く。
  4. claude を擬似的に失敗させても、要約なし＋警告でメールは出る。
  5. TCC: LaunchAgent 実行で `~/Library/Application Support/seimu-watch/` に正常書き込み（Desktop 不使用）。

## 8. 非対象（YAGNI）

- GitHub push / 公開アーカイブ（個人用途のため不要）。
- 複数トピックの汎用化（まず大学無償化1本。横展開は後日キーワードを足すだけ）。
- Web UI / ダッシュボード。
- Anthropic API キー（claude CLI で足りる）。
- 高度なニュース正規化・全文取得（RSS のタイトル＋要約で十分。必要時に拡張）。

## 9. ファイル構成

```
scripts/seimu-watch-daily.py                     ← git 正本
config/launchagents/com.yuika.seimu-watch.plist  ← git 正本（bootstrap 用）
~/Library/Application Support/seimu-watch/
  ├── seimu-watch-daily.py     （本番＝git正本のcp）
  ├── send-email.py            （job-report と同様に自ディレクトリへコピー。設定は共有の ~/.config/masu-p-watch/email.json を読む＝新規シークレット不要）
  ├── reports/YYYY-MM-DD.md
  ├── seen-speech-ids.txt
  ├── seen-news-urls.txt
  ├── last-sent-date.txt
  └── seimu-watch.log
~/Library/LaunchAgents/com.yuika.seimu-watch.plist
```

## 10. 関連

- 発端・ファクトチェック: @docs/journal/2026-06-19.md（追記2＝国会APIの実在確認、追記3＝求人パイプライン修理）
- 雛形: `scripts/job-search-daily-mac.py`
- メール基盤: `~/.config/masu-p-watch/email.json`（既存）
