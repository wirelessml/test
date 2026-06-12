## 1. 全体評価（3-5行）
外部公開前提では、現状のまま公開するのは危険です。`server.py` は `0.0.0.0:8787` で待ち受け、`start.sh` は Cloudflare Tunnel を起動する構成です。
重大リスクは、無認証の `/chat` と `/api/voice` による Claude/ElevenLabs 課金消費、会話ログの無認証エクスポート、`/stats` の保存型 XSS です。
`subprocess.run()` は配列引数で呼ばれており、典型的な `shell=True` 型の OS コマンドインジェクションは確認できません。
ただし Claude Code CLI がツール実行可能な設定なら、プロンプト注入がローカルファイル読み取りやコマンド実行へ広がる可能性があります(推測)。

## 2. 🔴 セキュリティ（最優先・確度順、file:line付き）

- **無認証で外部公開される構成。** `start.sh:19` が `cloudflared tunnel --url http://localhost:8787` を起動し、`server.py:747` が `0.0.0.0` で待ち受けます。認証処理は `Handler` 全体に存在せず、公開 URL を知る第三者がチャット、音声生成、ログ閲覧、ログエクスポートを直接叩けます。

- **Claude 課金・リソース消費が無認証で可能。** `server.py:656-664` の 5 秒/IP 制限だけで、`server.py:700-703` がユーザー入力を含むプロンプトを `claude -p` に渡します。NAT 配下では正規ユーザー同士も巻き込み、攻撃者は送信元分散や並行接続で容易に回避できます。`server.py:746-747` はスレッド上限なしのため、120 秒タイムアウトの Claude プロセスを大量に抱える DoS/コスト暴走が可能です。

- **`/api/voice` はレート制限すら通らず ElevenLabs 課金を焼ける。** `server.py:615-654` は `/api/voice` を先に処理して `return` し、レート制限はその後の `server.py:656-664` にあります。`server.py:622-640` で環境変数の `ELEVENLABS_API_KEY` を使って固定の ElevenLabs API に任意テキストを送れるため、公開時は無認証の課金エンドポイントになります。

- **全会話ログの無認証漏えい。** `server.py:37-47` がユーザー発話と AI 応答を日次 JSONL に保存し、`server.py:524-537` の `/api/export` と `server.py:576-594` の `/api/export-md` が全ログを返します。`server.py:538-550` の `/api/history` は当日直近 20 件、`server.py:595-599` の `/api/stats` は質問ランキングを返します。さらに `save-logs.sh:6-10` はログを git commit/push するため、リモートリポジトリ側にも個人相談内容が残る可能性があります。

- **`/stats` に保存型 XSS。** `server.py:472` がログ内のユーザー質問を `questions` に入れ、`server.py:477` で top questions として返します。`server.py:485-488` の `STATS_HTML` はその質問文字列をエスケープせず `innerHTML` に連結するため、攻撃者が `<img onerror=...>` 等を何度か投稿して上位質問に入れると、`/stats` を開いた管理者のブラウザで同一オリジン JS が実行されます。

- **CORS/CSRF 相当の課金トリガーが可能。** `server.py:496-504` は OPTIONS に `Access-Control-Allow-Origin: *` を返します。一方で実 POST レスポンスには CORS ヘッダーが無いため悪性サイトはレスポンスを読みにくいですが、ブラウザはリクエスト自体を送信でき、サーバ側処理と課金は発生します。加えて `server.py:611-615` 以降は `/api/voice` 以外の POST パスを検証せずチャット処理へ進むため、`/anything` への JSON POST でも Claude が呼ばれます。

- **Claude CLI 経由のプロンプト注入リスク(推測)。** `server.py:691-697` がユーザー制御の `history` と `message` をそのままプロンプト化し、`server.py:700-703` が `claude -p` を実行します。`shell=True` ではないので直接のシェル注入ではありませんが、使っている `claude` が Claude Code CLI でツール利用を許す設定の場合、外部ユーザーの指示でローカルファイル読み取りやコマンド実行に誘導されるおそれがあります(推測)。

- **API キーの扱いが公開運用に向かない。** ハードコードされた実シークレットは確認できませんでした。ただし `chat.html:49-51` は利用者に Anthropic API Key 入力を促し、`chat.html:80` と `chat.html:93` で `localStorage` に永続保存します。`chat.html:139-145` は `anthropic-dangerous-direct-browser-access` 付きでブラウザから直接 Anthropic に送信しており、同一オリジン XSS や端末共有時にキーが抜かれやすい構成です。`server.py:648-653` は ElevenLabs 側の例外文字列をそのままレスポンスに返すため、上流エラー詳細の漏えいもあります。

- **パストラバーサル/SSRF/任意ファイル読み出しの確認結果。** Web エンドポイントで、ユーザー入力を任意ファイルパスや任意 URL として使う箇所は確認できませんでした。`/api/search` はロード済み `knowledge_data` の文字列検索です(`server.py:551-565`)。`/api/voice` の送信先 URL は固定です(`server.py:631-640`)。補助 CLI の `youtube-transcript.py:30-34` は未検証の `video_id` をファイル名に含めますが、Web 入力からは呼ばれていません。

## 3. バグ・正確性の問題（file:line付き）

- **POST ルーティングが壊れている。** `server.py:611-615` は `/api/voice` だけを特別扱いし、それ以外の POST パスを `/chat` か確認していません。結果として `/health` や `/not-found` への POST でも、`server.py:666-703` の JSON パースと Claude 呼び出しに進みます。

- **不正 JSON/不足ヘッダーで 400 を返せない。** `server.py:616` と `server.py:666` は `Content-Length` を直接参照して `json.loads()` しており、ヘッダー欠落、不正 JSON、巨大 JSON で例外が未処理になります。クライアントには一貫した JSON エラーが返らず、スレッドがスタックトレースを吐く可能性があります。

- **`history` のスキーマ未検証で例外化する。** `server.py:687` は `h['role']`、`server.py:691-694` は `h['role']` と `h['content']` を直接参照します。攻撃者や壊れたクライアントが `history` に辞書以外、キー欠落、巨大文字列を入れると処理が壊れます。

- **クライアント側リトライが二重課金を起こし得る。** `server.py` 内の HTML では、`fetch('/chat')` 失敗時に同じ本文で再度 `fetch('/chat')` します(`server.py:296-318`)。最初のリクエストがサーバでは処理済みだが通信・JSON 解析だけ失敗した場合、Claude 呼び出しが二重になります。

- **失敗応答もキャッシュされる。** `server.py:711-716` は Claude タイムアウトやエラー文言も `reply` として `response_cache` に保存します。同じ質問への以後の応答が、再試行されず失敗文言で固定される可能性があります。

- **統計ページの表示がログ内容に依存して壊れる。** `server.py:485-488` は質問文字列を HTML 連結するため、XSS だけでなく、通常の `<` `&` を含む質問でも表示が崩れます。

## 4. 堅牢性（例外時の挙動・大量入力・並行リクエスト）

- **入力サイズ制限がありません。** `server.py:616` と `server.py:666` は `Content-Length` 分を丸ごと読みます。`/api/voice` は `text` を 678 文字に切っていますが、巨大 body を読み込んだ後です(`server.py:616-617`)。チャットも `message` と `history` の総量制限がなく、`server.py:691-697` で巨大プロンプト化できます。

- **並行リクエスト制御がありません。** `server.py:746-747` は `ThreadingMixIn` で接続ごとにスレッドを作り、`server.py:700-703` の Claude は最大 120 秒、`server.py:640` の ElevenLabs は最大 30 秒ブロックします。グローバル同時実行数やキューが無いため、少数の攻撃者でもプロセス・スレッド・外部 API 枠を枯渇できます。

- **共有状態がロックされていません。** `server.py:490-493` の `last_request` / `response_cache`、`server.py:62-83` の `knowledge_data`、`server.py:715-717` のキャッシュ更新、`server.py:729-731` のログ書き込みはスレッド間で同期されていません。高並行時に競合、ログ破損、レート制限抜けが起き得ます。

- **ログ全読み処理がリクエストごとに走ります。** `server.py:16-25` の `load_past_questions()` はチャットごとに全 JSONL を読み、`server.py:524-537` のエクスポートや `server.py:462-478` の統計も全ログを走査します。ログが増えるほど通常利用のレイテンシとメモリ消費が悪化します。

- **例外時のレスポンス設計が不完全です。** Claude の `TimeoutExpired` は扱っていますが(`server.py:711-712`)、JSON パース、BrokenPipe、ファイル読み書き、`hist` 形式不正、`os.listdir(KNOWLEDGE_DIR)` 失敗などは個別に処理されていません。公開サーバでは 500/接続断が増え、クライアント側の二重リトライとも相性が悪いです。

## 5. 改善提案トップ8（優先順、各1-2行、具体策）

1. **公開面を閉じる。** まず `server.py:747` を `127.0.0.1` バインドにし、`start.sh:19` の Cloudflare Tunnel 自動起動を削除または明示フラグ制にする。

2. **全 API に認証を入れる。** `/chat`、`/api/voice`、`/api/export*`、`/api/history`、`/api/stats`、`/api/search`、`/api/knowledge` に共有トークンまたは管理者ログインを必須化し、未認証は処理前に 401 で返す。

3. **課金ガードをサーバ側に実装する。** IP だけでなく認証主体ごとの分間/日次上限、全体同時実行数、日次コスト上限、`/api/voice` への同一制限を入れる。429 は Claude/ElevenLabs を呼ぶ前に返す。

4. **Claude CLI を隔離または API に置き換える。** 可能なら通常の Anthropic Messages API でツールなし実行にする。CLI を使うなら低権限ユーザー、専用空ディレクトリ、ツール無効化/許可リスト、環境変数最小化で起動する。

5. **ログ閲覧・保存を管理者専用にする。** `/api/export*` と `/api/history` は閉じるか管理者限定にし、ログは保存期間を短くする。`save-logs.sh` による自動 git push は個人情報混入前提で停止する。

6. **リクエスト検証を追加する。** POST は `/chat` と `/api/voice` 以外 404/405、`Content-Type`、JSON スキーマ、`message` 長、`history` 件数・各要素長、body 最大サイズを検証し、不正時は 400 を返す。

7. **CORS/CSRF を整理する。** `Access-Control-Allow-Origin: *` を削除し、必要なオリジンだけ許可する。課金が発生する POST には CSRF トークンまたは認証ヘッダーを要求し、単純 cross-site POST で処理されない形にする。

8. **XSS 対策とセキュリティヘッダーを入れる。** `/stats` は `innerHTML` 連結をやめて `textContent`/DOM API で描画し、`Content-Security-Policy`、`X-Content-Type-Options: nosniff`、`Referrer-Policy` を全 HTML/API 応答に付ける。
