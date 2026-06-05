# 毎朝の求人サーチ（戎町500m + 関西本社リモート、計50件）

> 確定: 2026-06-04。masup WSL2 の Codex CLI で毎朝実行し、GitHub に自動公開。

## 何をするルーチンか

仲啓輔の就活用に、毎朝 求人を50件集めて日次レポート化し、公開 GitHub リポジトリに push する。

- **【最優先A】京都・同志社関係**（同志社大学/女子大学/中高/**国際中高**/学校法人同志社/関連法人・生協 等。**教員免許不要の職に限る**＝本人は教員免許なし・50代。onsite/リモート問わず）。あれば優先掲載、無ければ該当なし。
  - **明示監視（2026-06-05 改訂）**: 『学校法人同志社／同志社大学の**特定業務職員・契約職員・嘱託・アルバイト職員**（いずれも**教員免許不要**）』を必ず確認（窓口: recruitadm.doshisha.ac.jp、www.doshisha.ac.jp/recruit/ の特定業務職員ページ等）。**特定業務職員は年齢制限の記載がなく50代でも応募可＝本命枠**。⚠️ **職員（総合職）は新卒・既卒対象で『◯年4月2日以降生まれ』の生年要件＝50代は応募不可のため対象外**（以前『総合職が現実的』としていたのは誤り、年齢要件で不可と判明）。同志社国際中高そのものは独自採用ページ（intnl.doshisha.ac.jp/…recruit.php）の**事務/ICT/図書館 契約**＋**食堂・寮・清掃の委託（シダックス等、免許不要で校地に入れる）**を監視。専任教員・非常勤講師は免許必須で除外。詳細 @docs/journal/2026-06-05.md
- **【最優先B】高槻・将棋関係**（関西将棋会館＝2024年に高槻移転/日本将棋連盟関西本部/将棋道場・教室・イベント運営・普及 等。職種問わず・onsite/リモート問わず）。あれば優先掲載、無ければ該当なし。※本人の趣味＝将棋（職務経歴書記載）と合致。
- **① 戎町近辺（半径約500m以内）の求人を全業種・全雇用形態で全件**（介護/事務/販売/飲食/軽作業/IT/教育/警備/医療/清掃 等）
- **② 50件に満たない分を「本社が兵庫・大阪・京都」のリモート/在宅求人で補完**。その中で**本社所在地が戎町（須磨区）に物理的に近い順にピックアップ**（神戸市内＞明石・阪神間〔芦屋/西宮/尼崎〕＞大阪市＞大阪府下＞京都市＞京都府下）。全国どこでも可の純リモートは対象外。仕事内容は限定しない。
- 合計 約50件。レポートは **4セクション**（同志社関係 / 将棋関係(高槻) / 戎町近辺(500m) / リモート(関西本社)）。個人情報（氏名・住所・電話）は載せない。応募代行はしない（リスト化のみ）。

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
- **Mac LaunchAgent `com.yuika.job-report-email`**（`~/Library/LaunchAgents/com.yuika.job-report-email.plist`、**毎朝 05:00 JST**）が `~/Desktop/scripts/email-job-report.sh` を実行（04:10頃完成済のレポートを送る）。
- 流れ: masup が 04:00 に生成→GitHub push 済みなので、Mac は **公開リポジトリの raw を curl 取得**（ssh不要・公開repoなので無認証）→ Mac 既存の `scripts/lib/send-email.py`（`~/.config/masu-p-watch/email.json` の Gmail app password 再利用）で **wirelessml@gmail.com に送信**。
- 件名例: `【就活求人レポート】2026-06-04 計50件（戎町500m＋本社=兵庫/大阪/京都リモート, 同志社/将棋優先）`、本文=レポート全文。
- 一発ジョブ（数秒で終了・常駐しない）＝ Mac=Claude Code 専用/軽量方針と矛盾しない。Gmail app password は**私物Macのみ**（共用masupには置かない）。
- ログ: `~/Desktop/scripts/job-report-email.log` ＋ `/tmp/job-report-email-launchd.log`。
- 停止: `launchctl bootout gui/$(id -u)/com.yuika.job-report-email`。手動送信: `bash ~/Desktop/scripts/email-job-report.sh`。
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
