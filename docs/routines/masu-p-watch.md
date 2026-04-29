# MASU-p 毎日監視ルーチン

> 開始: 2026-04-29 18:12 JST
> 動機: 普段使いのコワーキングスペース MASU-p (神戸市須磨区板宿) の公式情報を毎日チェック。新サービス、イベント、新規投稿を見逃さない。

## 監視対象

| URL | 内容 | 監視方法 |
|---|---|---|
| https://masu-p.com/ | 公式サイト | `<body>` ハッシュ差分 |
| https://www.instagram.com/masup_official/ | Instagram 公式 | `og:description` + 最新投稿画像 URL key の組合せハッシュ |

## ベースライン (2026-04-29 18:12)

**masu-p.com**:
- サイズ: 121,168 bytes
- 主要見出し: About / Service / アクセス
- 最新告知 (本文中): 「クリエイターズラボ プレオープン」(2025-07)

**Instagram @masup_official**:
- フォロワー 141 人 / フォロー中 101 人 / 投稿 75 件
- 最新投稿画像 key: `318546223_3304576813202385_8800960017401097906_n`
- (login 必須のため bio + メタタグまで取得、投稿本文・キャプションは不可視)

## 実装

### スクリプト
`/Users/yuika/Desktop/scripts/masu-p-watch.sh`

### LaunchAgent
- plist: `~/Library/LaunchAgents/com.yuika.masu-p-watch.plist`
- 実行時刻: 毎日 **08:23 JST** (Kioxia 08:17 と被らない)
- 出力ログ: `/tmp/masu-p-watch-launchd.log`
- エラーログ: `/tmp/masu-p-watch-launchd-error.log`
- Mac 起動中なら常時動作、Claude Code 不要

### スナップショット
変化検出時のみ HTML を保存:
- `docs/routines/masu-p-snapshots/web-YYYYMMDD-HHMM.html`
- `docs/routines/masu-p-snapshots/ig-YYYYMMDD-HHMM.html`

### 差分管理ファイル
- `masu-p-snapshots/web-latest.hash` (最新の web body ハッシュ)
- `masu-p-snapshots/ig-latest.hash` (最新の Instagram メタハッシュ)

### ログ
追記専用 Markdown: `docs/routines/masu-p-watch-log.md`

ログ形式:
```markdown
## YYYY-MM-DD HH:MM:SS JST

- Web: unchanged | baseline | 🚨 CHANGED (size, hash)
  - 見出し抜粋: (CHANGED 時のみ)
- Instagram: unchanged | baseline | 🚨 CHANGED (size, hash)
  - og:description: (CHANGED 時のみ)
  - 最新投稿画像 key: (CHANGED 時のみ)
```

## 手動実行

```bash
# 即時実行
/Users/yuika/Desktop/scripts/masu-p-watch.sh

# ログ確認
tail -50 /Users/yuika/Desktop/docs/routines/masu-p-watch-log.md

# LaunchAgent 状態
launchctl list | grep masu-p

# 手動でベースラインリセット
rm /Users/yuika/Desktop/docs/routines/masu-p-snapshots/*.hash
```

## 停止 / 削除

```bash
# 停止 (plist は残す)
launchctl unload ~/Library/LaunchAgents/com.yuika.masu-p-watch.plist

# 完全削除
launchctl unload ~/Library/LaunchAgents/com.yuika.masu-p-watch.plist
rm ~/Library/LaunchAgents/com.yuika.masu-p-watch.plist
rm /Users/yuika/Desktop/scripts/masu-p-watch.sh
rm -rf /Users/yuika/Desktop/docs/routines/masu-p-snapshots/
```

## 制約と既知の課題

1. **Instagram は login wall**: 投稿本文・キャプション・コメントは取得不可。og:description (フォロワー数 + フォロー数 + 投稿数) と最新投稿画像 URL key だけで「何かが変化した」事実を検知する。
2. **画像 URL の CDN ハッシュ**: Instagram CDN は同じ画像でもクエリパラメータが変わることがあるが、URL path 内の `XXXXXXXX_YYYYYYY_ZZZZZZZZZZ_n` 形式 key 部分は投稿固有なのでこれを抽出して使う。
3. **新規投稿時の挙動**: Instagram トップ画像 key が変わる → IG hash 変化 → 🚨 CHANGED でスナップショット保存。HTML を後から見て新規投稿を確認できる。
4. **メンテナンス**: Instagram の HTML 構造変更で正規表現が壊れる可能性。月次でスクリプト動作確認が必要。

## 改善 TODO

- [ ] 変化検出時の Gmail 下書き自動作成 (Kioxia と同じパターン)
- [ ] スナップショット古い分の自動掃除 (90 日以上)
- [ ] Instagram cookie ベース取得 (chromium + 保存セッション) で投稿本文まで取れるようにする
- [ ] ログサイズが膨らんだら年月別ローテーション

## 関連ファイル

- スクリプト: `/Users/yuika/Desktop/scripts/masu-p-watch.sh`
- ログ: `docs/routines/masu-p-watch-log.md`
- スナップショット: `docs/routines/masu-p-snapshots/`
- plist: `~/Library/LaunchAgents/com.yuika.masu-p-watch.plist`
- 関連: しゅん先生 PC が MASU-p に据え置き (@docs/machines/shun-sensei-pc.md)
