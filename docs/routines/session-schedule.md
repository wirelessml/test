## Claude Codeセッションスケジュール（4/17〜、毎日繰り返し、JST）

Googleカレンダー登録済み（RRULE:FREQ=DAILY、colorId:7 Peacock）。4/18 10:00に見直し予定。

| 時刻 | セッション | 主な用途 |
|---|---|---|
| 9:00 | セッション1 | 朝の状況確認・当日TODO整理・X情報収集 |
| 14:00 | セッション2 | メイン作業・X情報収集 |
| 19:00 | セッション3 | 夕方作業・配信メンテ・X情報収集 |
| 0:00 | セッション4 | 1日のまとめ・git commit・X情報収集 |
| 5:00 | セッション5 | 夜間監視ログ確認・X情報収集 |

### X情報収集ルーチン（各セッション毎回実施）
- **手段**: agent-reach の `twitter` CLI（Cookie取得済み、@minimalistneko）
  - Cookie更新: `agent-reach configure --from-browser chrome`（Chromeでログイン維持すればOK）
  - バックアップ手段: X PWA（`com.google.Chrome.app.lodlkdfmihgonocnmddehnfgiljnadcf`、full tier）
- **対象**:
  1. For Youタイムライン: `twitter -c feed | head -30`
  2. キーワード検索: `twitter -c search "Claude"` / `"Anthropic"` / `"Opus 4.7"` など
- **出力**:
  1. `docs/x-daily-briefing.md` にセッション日時でセクション追記
  2. 要約をチャットで報告（注目ポスト・トレンド・インフルエンサー反応）
- **twitterコマンド主要**: `feed`/`search`/`likes`/`followers`/`article`/`post`/`show`（全て `-c` でLLM向けJSON）

