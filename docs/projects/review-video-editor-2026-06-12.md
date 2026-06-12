# shibu-video-editor 静的レビュー

## 1. 全体評価

設計は「transcribe → plan → cuts → metadata」という段階が明確で、Pydantic による編集計画モデルも読みやすいです。  
一方で、外部境界である Claude API / ffmpeg / ffprobe / Whisper / ElevenLabs をほぼ生で呼んでおり、失敗時の回復やユーザー向け診断は弱いです。  
最も大きい実害は、パイプライン一括実行の壊れやすさ、ffmpeg スクリプトが仕様どおりのカット境界フェードになっていない点、AI 生成プランの時刻検証不足です。  
テストは smoke と仕様定数の確認が中心で、実ワークフローの異常系・巨大入力・外部 API モックがまだ薄いです。

## 2. バグ・正確性の問題

1. `shibu_editor/cli.py:310`  
   `pipeline` が `typer.Context(transcribe)` を作って `ctx.invoke(...)` していますが、`transcribe` は Click Command ではなく登録済みの Python 関数です。通常の Typer/Click の使い方ではここで壊れるため、`transcript` 未指定の一括パイプラインが開始直後に失敗します。

2. `shibu_editor/cuts.py:106` / `shibu_editor/cuts.py:107`  
   仕様上は「カット境界の 30ms フェード」ですが、実装は `[0:a]...afade=t=in:d=0.03:st=0[a]` で出力冒頭だけを fade-in しています。各カット境界にはフェードや crossfade が入らないため、ブツ音防止という `CROSSFADE_MS` の目的を満たしません。

3. `shibu_editor/cuts.py:24` / `shibu_editor/cuts.py:55` / `shibu_editor/plan.py:21`  
   Claude が返す `start_seconds/end_seconds/raw_duration_seconds` に範囲・順序・非負・動画長内の検証がありません。`end < start`、負値、動画長超過を受け入れると、重複 keep、動画外 keep、CSV と ffmpeg の不一致が発生します。

4. `shibu_editor/cuts.py:88` / `shibu_editor/cuts.py:106`  
   全区間がカット対象になると `keeps` が空になり、`select_clauses_v` が空文字のまま `select=''` を含む ffmpeg スクリプトを生成します。ユーザーには事前診断なしで ffmpeg 実行時エラーになります。

5. `shibu_editor/cli.py:130` / `shibu_editor/cli.py:134` / `shibu_editor/transcribe.py:118`  
   `--video` なしの `plan` は transcript の最後の要素の `end_ms` だけで raw duration を推定します。`load_transcript` はソートや必須キーを検証しないため、未ソート・欠損・空文字混入で動画長が誤り、以後のカット計算全体がずれます。

6. `shibu_editor/cuts.py:35` / `shibu_editor/cuts.py:36`  
   `do_not_touch` と少しでも重なる cut は丸ごと捨てられます。保護範囲外の前後だけは安全に切れるケースでも全体が無視されるため、AI が少し広めに cut を返すと不要部分が残ります。

7. `shibu_editor/cli.py:351` / `shibu_editor/cli.py:353` / `shibu_editor/cli.py:355`  
   `pipeline` の Step 4 は「description / tags / chapters」と表示しますが、実際に書くのは `chapters.txt` と `tags.txt` だけです。`metadata` コマンド相当の description/title は生成されず、README の一括ワークフロー期待とずれます。

8. `tests/build_ground_truth.py:162`  
   テスト補助スクリプトが `/Users/yuika/Desktop` を固定参照します。公開 OSS の検証手順としては他環境でそのまま再現不能で、README の「ローカルで再生成」と噛み合いません。

## 3. 堅牢性の穴

- ffmpeg 失敗時・異常終了時の扱い  
  `transcribe` は `extract_audio_with_ffmpeg(video, audio_tmp)` を `try/finally` の外で呼ぶため、抽出失敗時に部分的な `.tmp.wav` が残ります（`shibu_editor/cli.py:70` / `shibu_editor/cli.py:72` / `shibu_editor/cli.py:88`）。`extract_audio_with_ffmpeg` は stderr を capture しますが失敗時に整形表示せず、ユーザーには Python 例外中心になります（`shibu_editor/transcribe.py:95`）。`cuts/pipeline` の ffmpeg 実行も `CalledProcessError` をそのまま上げ、壊れた出力 mp4 の削除や再試行はありません（`shibu_editor/cli.py:235` / `shibu_editor/cli.py:348`）。

- 日本語ファイル名/パス・スペース入りパスの扱い  
  subprocess の list 引数と生成スクリプト内の `_shell_quote` は、通常の日本語・スペース・シングルクォートには概ね対応しています（`shibu_editor/cuts.py:104` / `shibu_editor/cuts.py:117`）。ただし生成スクリプトのコメントへパスを無加工で埋め込むため、改行など制御文字を含むファイル名では shell script injection になります（`shibu_editor/cuts.py:96` / `shibu_editor/cuts.py:97`）。出力先ディレクトリを自動作成しないコマンドもあり、パスが正しくても親ディレクトリ未作成で落ちます（`shibu_editor/cli.py:92` / `shibu_editor/cli.py:155` / `shibu_editor/cli.py:226`）。

- Claude API 呼び出しの失敗/リトライ/レート制限/コスト暴走ガード  
  アプリ側で API キー有無の事前チェック、timeout、明示的 retry/backoff、rate limit 待ち、429/5xx の分類、部分レスポンス保存がありません（`shibu_editor/plan.py:123` / `shibu_editor/plan.py:148`）。`max_tokens=64000` かつ transcript 全量を JSON 文字列で投入するため、長尺動画では一回の呼び出しが高額化しやすく、事前トークン見積もりや確認プロンプトもありません（`shibu_editor/plan.py:133` / `shibu_editor/plan.py:150`）。

- 長尺動画・巨大ファイルでの挙動  
  transcript 全体を `read_text` → `json.loads` → `json.dumps` で丸ごとメモリに載せます（`shibu_editor/transcribe.py:118` / `shibu_editor/plan.py:133`）。ffmpeg は keep segment 数だけ `between(t,...)` を連結した 1 本の filter expression を作るため、カットが多い長尺動画ではコマンド長制限や ffmpeg filter の評価コストに当たりやすいです（`shibu_editor/cuts.py:88`）。Whisper はモデルを毎回ロードし、音声全体を一括処理するため、長尺時の一時ファイル・メモリ・処理時間の上限管理がありません（`shibu_editor/transcribe.py:33` / `shibu_editor/transcribe.py:34`）。

## 4. テストの欠落

1. `pipeline` の `transcript` 未指定パスを Typer の `CliRunner` 等で通すテスト。現状の `typer.Context(transcribe)` 問題を捕まえられます。

2. ffmpeg スクリプトの意味検証。複数カット、全区間カット、隣接カット、padding 重なり、カット境界フェードが実際に成立するかを小さい合成動画か filter 構文検査で見るべきです。

3. AI 生成 plan の異常値テスト。負の時刻、`end < start`、動画長超過、保護範囲との部分重複、空 `keeps` を Pydantic/計算層で拒否できるかが未確認です。

4. Claude API のモック異常系。API キーなし、429、5xx、stream 中断、JSON コードフェンス、前後説明付き JSON、不正 JSON、巨大 transcript の扱いが未カバーです。

5. transcript 入力検証。`words` 欠損、`end_ms` 欠損、未ソート、空配列、dict/list 以外、日本語・スペース入りパス、親ディレクトリ未作成の出力先を確認するテストがありません。

## 5. 改善提案トップ10

1. `pipeline` から `typer.Context(...).invoke(...)` をやめ、内部処理を `_transcribe_video(...)` のような純関数に切り出して CLI と pipeline で共有する。

2. `EditingPlan` に Pydantic validator を追加し、全 time range の `0 <= start < end <= raw_duration`、質問順序、`do_not_touch` 必須範囲、空 keep 禁止を検証する。

3. カット生成を `trim/atrim` セグメント単位の `concat` filter に寄せ、各境界で `afade` または `acrossfade` を入れる。少なくとも現在の「冒頭だけ fade-in」は仕様名と分離する。

4. ffmpeg/ffprobe ラッパーを作り、存在チェック、stderr の要約表示、親ディレクトリ作成、部分出力の cleanup、終了コード別メッセージを統一する。

5. 一時音声は入力動画横ではなく `tempfile.TemporaryDirectory` に置き、抽出処理も含めて `try/finally` で確実に消す。既存 `.tmp.wav` の上書き削除も避ける。

6. Claude 呼び出しに timeout、retry/backoff、429 の待機、最大入力サイズ、概算コスト表示、`--yes` なしでは高額実行を止めるガードを入れる。

7. Claude 出力は JSON schema/structured output 相当で縛り、enum・必須項目・余剰項目・時刻整合を検証してから保存する。失敗時は raw response を別ファイルに残す。

8. 長尺対応として transcript を章・時間窓で分割し、セクション検出と cut 抽出を段階化する。巨大な `between(...) + ...` ではなく concat list や filter graph ファイルを使う。

9. CLI テストを増やし、`CliRunner` と monkeypatch で Whisper/ElevenLabs/Claude/ffmpeg を差し替える。実外部依存なしで正常系・異常系を通せる形にする。

10. 公開リポ向けにローカル絶対パスを引数化し、プライバシー・API コスト・生成物に含まれる個人情報・削除依頼動画の扱いを README の運用チェックリストにする。

## 6. セキュリティ/公開リポとしての注意点

- `cuts.py` の生成 shell script は実行ファイルとして保存され、直後に `bash` で実行されます（`shibu_editor/cli.py:225` / `shibu_editor/cli.py:235`）。実引数は quote されていますが、コメント内のパス埋め込みは改行を sanitize しておらず、悪意あるファイル名で script injection になります。

- Claude API に transcript 全文を送る設計です。受講生インタビューは個人情報・住居情報・生活状況を含み得るため、README に明示的な同意、保存期間、送信先 API、redaction 前処理の注意が必要です。

- `plan.json` / `plan.md` / `description.txt` は transcript 由来の個人情報を含み得ますが、`.gitignore` は transcript と tests/output だけを対象にしています（`.gitignore:12` / `.gitignore:16`）。実運用の `output/`、`plan*.json`、`plan*.md` も誤 commit 防止対象にした方が安全です。

- README に作者メールアドレスが掲載されています（`README.md:174`）。意図的な公開なら問題ありませんが、OSS 公開時の連絡先として個人メールを晒すリスクは確認対象です。
