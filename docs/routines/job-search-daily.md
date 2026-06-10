# 毎朝の求人サーチ（全職種: 戎町500m全件 + 関西本社リモート在宅、計~50件）

> 確定: 2026-06-04。masup WSL2 の Codex CLI で毎朝実行し、GitHub に自動公開。

## 何をするルーチンか

仲啓輔の就活用に、毎朝求人を最大50件集めて日次レポート化し、公開 GitHub リポジトリに push する。

> 🔄 **2026-06-07 改訂**: **同志社（京都）・将棋/高槻 の優先枠を廃止**し、地元・戎町近辺に集中。**戎町近辺(onsite)を全件網羅＋不足分を関西本社リモートで補完**の2本立てに変更（旧priority枠の経緯は @docs/journal/2026-06-05.md ／ @docs/journal/2026-06-07.md）。
>
> 🔄 **2026-06-10 改訂（事務職限定）**: 対象職種を**事務職のみ**に変更（一般事務/営業事務/経理・財務/総務/人事・労務/受付/データ入力/医療・調剤・介護・学校事務/貿易・法務事務/秘書/バックオフィス全般）。営業・販売・コールセンター/CS・テクサポ・軽作業・製造・清掃・警備・介護職（介護事務は対象）・IT開発・アノテーション等は除外。**事務職以外で件数を埋めることを禁止**＝事務職で50件に満たない日は少ないまま提出（Codex 水増し対策）。あわせて Mac 側メール件名も「事務職限定」に更新。
>
> 🔄 **2026-06-10 改訂3（午後・事務職限定を解除＝全職種に復帰）**: ユーザー指示「事務縛りやめて戎町近辺500mを全部出しましょう」により、朝の事務職限定（改訂1）を**同日中に解除**。**戎町500m内は職種不問で全件網羅**、在宅可補完も職種不問（在宅デスクワーク実態のあるもの）に戻す。改訂2の実在・勤務地検証と6/9の在宅可4段階優先順は維持。Mac側メール件名も「全職種」に更新。
>
> 🔄 **2026-06-10 改訂2（実在・勤務地の検証を必須化）**: 同日午前、初回レポートの2件で問題が発覚（①ウィルウェイ校舎事務=実体は学園都市駅勤務なのに『板宿駅すぐ』と誤記＝検索結果ページの駅名を勤務地と誤認 ②瀧川学園・入試広報事務嘱託=Codexのサーバーサイド検索では見えるが実ブラウザのIndeedでは出ない＝掲載終了/キャッシュの可能性）。対策として **各求人は詳細ページ（viewjob・/jb/等）を開いて (a)応募可能な現掲載 (b)勤務地住所が条件内 (c)会社名と職種の対応 を確認してからリスト化**し、URL欄は検索一覧ではなく**詳細ページ直リンク**を原則とするようPROMPTに追加（確認できない求人は載せない）。
>
> 🔄 **2026-06-09 改訂（在宅可の優先順を明確化）**: リモート補完を「物理的に近い順」から **在宅可の4段階優先順**に変更＝**①神戸市本社/拠点 → ②兵庫県内 → ③大阪市本社の完全在宅/出社少 → ④京都市本社の完全在宅**。あわせて**在宅実態（研修/機材受け取り/面談来社/月次・週次の定例出社）の確認を必須化**し、出社頻度が高く実質在宅でないものは除外、無期雇用派遣(SES)・客先常駐・『フルリモート』が外回り直行直帰のものはその旨明記。経緯と実調査は @docs/journal/2026-06-09-remote-job-priority.md（リモートコントロール経由の handoff 反映）。

- **① 戎町近辺（半径約500m以内）の求人を職種不問・全雇用形態で全件網羅【最優先】**（板宿駅至近の 戎町・飛松町・大黒町・大田/平田/前池町の駅寄り 等。**500m超は含めない＝件数稼ぎで範囲を広げない**が、範囲内の求人は職種を問わず取りこぼさず網羅する）
- **② 50件に満たない分を在宅可（リモート/在宅）求人で補完**。優先順は **①神戸市本社または神戸市内に拠点・勤務登録地がある在宅可 ＞ ②神戸市以外の兵庫県内（明石・阪神間〔芦屋/西宮/尼崎〕等、神戸に近い順）＞ ③大阪市本社の完全在宅または出社頻度が少ない（多くて月数回まで）＞ ④京都市本社の完全在宅**。上位から先に埋め、上位が少ないときだけ下位へ広げる。本社・拠点が関西3府県のいずれにも無い「全国どこでも可の純リモート」は対象外。各件で**在宅実態（研修/機材/面談/定例出社の有無）を確認**し、所在地・在宅条件・出社頻度・未経験可否・仕事内容・応募導線をセットで明記。職種は不問（ただし在宅デスクワークとして実態のあるもの）。
- フィルタ: 応募者は50代。**年齢上限・生年要件で50代不可と明記された求人は除外**（ただし応募者の年齢・属性は本文に書かない＝個人情報）。
- 合計 約50件。レポートは **2セクション**（戎町近辺(500m)の求人・全職種 / 在宅可の求人：神戸優先, 本社=兵庫/大阪/京都）。個人情報（氏名・住所・電話）は載せない。応募代行はしない（リスト化のみ）。

> 経緯: 当初「戎町近辺」が曖昧で Codex が目標件数までローカルを水増し（24→34→40→50 と常に総数に張り付き）→ リモートが出なかった。**半径500m に固定**したことで onsite が自然に ~32件に収まり、不足 ~18件が関西本社リモートで埋まるようになった（さくらインターネット/フェンリル/Helpfeel/はてな 等の高単価フルリモートが該当）。

## スケジュール / 実行経路

- **トリガー**: masup の Windows タスクスケジューラ `JobHuntDailySearch`（**毎日 04:00 JST**、`StartWhenAvailable`＝PC オフで逃したら起動後に実行）
- **アクション**: `wsl.exe -e bash -lc "/home/gci_admin/job-search-daily/daily-job-search.sh"`
- **本体**: WSL2 の `~/.local/bin/codex exec`（Web 検索でレポート生成、約5-8分）

## ファイル / 出力

- スクリプト: masup `/home/gci_admin/job-search-daily/daily-job-search.sh`
- レポート: masup `/home/gci_admin/job-search-daily/reports/job-report-YYYY-MM-DD.md`（＋ codex 実行ログ `codex-run-*.log`）
- 公開先: **https://github.com/wirelessml/job-hunt-reports**（public、`reports/` に日次蓄積、コミット作者 `wirelessml`＝実名なし）
- ツール本体（OSS）: **https://github.com/wirelessml/job-hunt**（public、MIT）

## GitHub 自動 push の仕組み

- Windows 側に clone: `C:\Users\gci_admin\job-hunt-reports`
- WSL の日次スクリプト末尾が、生成レポートを clone の `reports/` にコピー → **Windows の `git.exe`** で add/commit/push
- 認証: Windows の `gh`（wirelessml ログイン済）＋ `gh auth setup-git` 済 → git.exe が gh トークンを使用
- コミット作者は `-c user.name=wirelessml -c user.email=wirelessml@gmail.com` で固定（実名を出さない）

## レポートの読み方

- 一番早い: 公開リポジトリを見る → https://github.com/wirelessml/job-hunt-reports/tree/main/reports
- Claude に「**就活レポート**」と言う → 最新を SSH で読んで要約報告（朝の cron `7a830b54` でも自動報告するが、これは **Claude セッション限定＝セッションが落ちると消える**点に注意）
- 手動: `ssh masu-p55 'wsl bash -lc "ls -1t ~/job-search-daily/reports/job-report-*.md | head -1 | xargs cat"'`

## メール自動報告（毎朝・確定）

毎朝レポートが**メールで届く**（masupに秘密情報を置かない設計）:
- **Mac LaunchAgent `com.yuika.job-report-email`**（`~/Library/LaunchAgents/com.yuika.job-report-email.plist`、**毎朝 05:00 JST**）が `~/Library/Application Support/job-report/email-job-report.sh` を実行（04:10頃完成済のレポートを送る）。**※2026-06-07 移設**：以前は `~/Desktop/scripts/email-job-report.sh` だったが、**launchd は `~/Desktop` をTCCで読めず `Operation not permitted`（戻り値126）で6/6以降ずっと失敗**していた → ジョブ一式（`email-job-report.sh`＋`send-email.py`）を `~/Library/Application Support/job-report/` に移して解消（launchdから実行可）。
- 流れ: masup が 04:00 に生成→GitHub push 済みなので、Mac は **公開リポジトリの raw を curl 取得**（ssh不要・公開repoなので無認証）→ Mac 既存の `scripts/lib/send-email.py`（`~/.config/masu-p-watch/email.json` の Gmail app password 再利用）で **wirelessml@gmail.com に送信**。
- 件名例: `【就活求人レポート】2026-06-11 計50件（全職種: 戎町500m全件＋在宅可 本社=兵庫/大阪/京都）`（2026-06-10 午後に「全職種」へ更新）、本文=レポート全文。
- 一発ジョブ（数秒で終了・常駐しない）＝ Mac=Claude Code 専用/軽量方針と矛盾しない。Gmail app password は**私物Macのみ**（共用masupには置かない）。
- ログ: `~/Library/Application Support/job-report/job-report-email.log` ＋ `/tmp/job-report-email-launchd.log`。
- 停止: `launchctl bootout gui/$(id -u)/com.yuika.job-report-email`。手動送信: `bash "$HOME/Library/Application Support/job-report/email-job-report.sh"`。
- ⚠️ 教訓: **launchd から起動するスクリプト/ログは `~/Desktop` に置かない**（TCCで `Operation not permitted`）。`~/Library/Application Support/` 配下に置く。`~/.config/` と `/tmp/` はlaunchdから読み書き可。
- 注意: 05:00 に Mac が起動していれば即送信、スリープ/オフなら**朝 Mac を開いた瞬間（次回起床時）**に送る（StartCalendarInterval の取りこぼし起床実行）。※08:02→05:00 に変更（2026-06-05。レポートは04:10頃完成済で待つ意味がなく、起床時に即届くよう前倒し）。

## 設定を変えるとき

`daily-job-search.sh` の `PROMPT` を編集して再配置（base64 で送る）:

```bash
# Mac でスクリプトを編集後:
base64 < daily-job-search.sh | ssh masu-p55 'wsl bash -lc "base64 -d > /home/gci_admin/job-search-daily/daily-job-search.sh && chmod +x /home/gci_admin/job-search-daily/daily-job-search.sh"'
# 反映テスト（1回手動実行）:
ssh masu-p55 'wsl bash -lc "bash /home/gci_admin/job-search-daily/daily-job-search.sh"'
```

調整ポイント: 半径（500m/1km…）/ リモート本社の対象府県 / 合計件数 / 分野。
※ 注意: 範囲を緩めると Codex が件数まで onsite を水増しし、リモートが出なくなる（半径を絞るのが効く）。

## タグ
#就活 #日次ルーチン #masup #Codex #戎町500m #関西本社リモート #GitHub公開 #wirelessml
