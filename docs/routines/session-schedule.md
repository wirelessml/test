## Claude Codeセッションスケジュール（4/17〜、毎日繰り返し、JST）

Googleカレンダー登録済み（RRULE:FREQ=DAILY、colorId:7 Peacock）。4/18 10:00に見直し予定。

| 時刻 | セッション | 主な用途 |
|---|---|---|
| 9:00 | セッション1 | 朝の状況確認・当日TODO整理 |
| 14:00 | セッション2 | メイン作業 |
| 19:00 | セッション3 | 夕方作業・配信メンテ |
| 0:00 | セッション4 | 1日のまとめ・git commit |
| 5:00 | セッション5 | 夜間監視ログ確認 |

### ~~X情報収集ルーチン（各セッション毎回実施）~~ **廃止（5/2 朝決定）**

各セッションで定型的に X を巡回するルーチンは廃止。情報収集は **必要時に都度判断**で実施する形に変更。

- 必要時の手段: `twitter -c feed | head -30` / `twitter -c search "<keyword>"` / X PWA（`com.google.Chrome.app.lodlkdfmihgonocnmddehnfgiljnadcf`、full tier）
- agent-reach `twitter` CLI の Cookie は取得済み（@minimalistneko）、いつでも使える
- 過去の収集ログは `docs/x-daily-briefing.md` にアーカイブ済（追記停止）

