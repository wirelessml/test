# 毎朝の求人サーチ（戎町500m + 関西本社リモート、計50件）

> 確定: 2026-06-04。masup WSL2 の Codex CLI で毎朝実行し、GitHub に自動公開。

## 何をするルーチンか

仲啓輔の就活用に、毎朝 求人を50件集めて日次レポート化し、公開 GitHub リポジトリに push する。

- **① 戎町近辺（半径約500m以内）の求人を全業種・全雇用形態で全件**（介護/事務/販売/飲食/軽作業/IT/教育/警備/医療/清掃 等）
- **② 50件に満たない分を「本社が兵庫・大阪・京都」のリモート/在宅求人で補完**（近い順 兵庫＞大阪＞京都。全国どこでも可の純リモートは対象外）。仕事内容は限定しない。
- 合計 約50件。個人情報（氏名・住所・電話）は載せない。応募代行はしない（リスト化のみ）。

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
