# 自律就職活動プログラム — ブレスト引き継ぎ仕様（v0）

> 作成: 2026-06-03（Claude Code → masup WSL2 Codex 引き継ぎ用）
> 状態: ブレスト途中。**Q5（プロファイルの元データ）未確定**。Codex がこの続きから設計を進める。
> 配置: masup `~/job-hunt-brainstorm.md` ＋ git `docs/projects/job-hunt-program.md`

## 目的（確定）
**C: 両取り** — 自分の就活を実際に楽にする実用ツール ＋ OSS/プロダクト/発信ネタとして公開（作ること自体が AI エンジニアのポートフォリオになる）。

## 就活の範囲（確定）
広義：正社員 ＋ 業務委託 ＋ フリーランス案件。

## 勤務地フィルタ（確定）
**onsite 求人の勤務地は「須磨区戎町近辺」に絞る。コワーキング「MASU-p」（板宿）は勤務地候補から除外。**
（リモート/フリーランス案件は地理不問。これは**勤務地フィルタのみ**＝他の項目は応募条件に含めない。「MASU-p」は地名ではなく板宿のコワーキングスペースの名称、masu-p.com）

## 自律度（確定）
希望は Lv3（完全自動送信）だが、現実解は **B「体感ほぼ自動」ダッシュボード**：
- 探索・マッチング・応募物ドラフトまで全自動
- 送信は「ワンクリック一括送信」キューに積む（人間が最後にクリック＝規約セーフ）
- 理由: 求人サイトの bot 対策/利用規約により完全自動送信(Lv3)は不可・アカウント BAN リスク。Cloudflare Turnstile 等が CDP/自動ブラウザを弾く。メール応募のみ「真の自動送信」が可能。

## v1 チャネル（確定）
- **(iv) AI/技術特化**（Findy / LAPRAS / GitHub / X求人 / AI系コミュニティ）— 仲氏の強み＆発信ネタと相性◎
- **(iii) メール直応募**（採用メール / mailto / 知人・X 経由）— 唯一「真のワンクリック自動送信」が効く経路
- ＋ **闇バイト/詐欺案件フィルタ（v1 必須セーフティ）**: 異常な高報酬・即日現金・身分証/口座/暗号資産ウォレットの先出し要求・Telegram/匿名アカウント誘導・面接なし即採用 等を赤フラグ検知してキューから自動除外

## パイプライン（確定）
探索 → マッチング（合致理由付きランキング）→ 応募物の自動ドラフト（職務経歴書 / 応募文 / カバーレター / メール）→ レビューキュー（編集＋ワンクリック送信）

## 未確定 / Codex が次に詰めるべき点
1. ~~**Q5（最優先）: プロファイルの元データ**~~ → **確定: A（既存の職務経歴書/履歴書ベース）**（2026-06-03 仲氏回答）
   - A) 既存の職務経歴書/履歴書を使う（最速） ← **採用**
   - B) オンラインの自分から自動生成（GitHub: wirelessml ＋ Substack: 仲啓輔 ＋ X: @minimalistneko）
   - C) 対話で一から作る
   - D) 併用（Codex 推奨だったが不採用）
   → 仲氏判断: **最速・品質安定・事実誤認少**を優先して A。
2. v1 のアプローチを 2-3 案（トレードオフ付き）→ 設計（アーキ / 構成要素 / データフロー / エラー処理 / テスト）
3. 技術スタック: 既存資産（Codex/Claude/Gemini、masup=Codex 専用 WSL2）を活かす方針

## ユーザー文脈（参考）
- 仲啓輔、現在無職、ミニマリスト志向、AI エージェント多用
- 機材役割分離: Mac=Claude Code 専用 / masup=Codex 専用 / しゅん先生 PC=据え置きメイン
- GitHub: wirelessml（OSS 実績: shibu-video-editor 等）、Substack: 仲啓輔名義、X: @minimalistneko
- 須磨区在住

## Codex への初手指示
この仕様の続きから設計を進めてください。まず **Q5（プロファイルの元データ A/B/C/D）**について仲氏に確認すべき質問を整理し、決まったら v1 のアプローチを 2-3 案（トレードオフ付き）提示 → 設計、の順で。

---

## Codex の初手（masup WSL2 / `codex exec` / 2026-06-03、read-only）

> 引き継ぎ実行: `ssh masu-p55 "wsl bash -lc '~/.local/bin/codex exec --skip-git-repo-check --sandbox read-only …'"`（ファイル変更なし、設計テキストのみ出力）

### Codex が整理した「仲氏への Q5 確認事項」
単に A/B/C/D を選ぶのではなく「どの情報を正(canonical)として扱うか」を確認すべき、として 6 点：
1. **既存の職務経歴書/履歴書はあるか**（最終更新日・形式・鮮度、そのまま応募に使える品質か）
2. **公開情報を自動生成に使ってよいか**（GitHub `wirelessml` / Substack 仲啓輔 / X `@minimalistneko`）。公開でも応募書類に入れたくない内容はあるか
3. **事実確認の基準**（GitHub コミット/README を証拠採用してよいか、発信を「経験/関心/思想」として使うか、実務経験と個人開発・発信を明確に分けるか）
4. **対話で補正する項目**（希望職種＝AI/LLM/エージェント/ML/フルスタック等、契約形態の優先順位、希望単価・年収、稼働開始時期・週稼働日数・リモート可否、NG 条件＝常駐/SES色/営業色/低単価/レガシー中心 など）
5. **個人情報・センシティブ情報の扱い**（住所を「神戸市須磨区近辺」に丸めるか、無職期間の表現、本名/電話/メール/SNSリンクの自動挿入範囲）
6. **v1 の完成物(正)は何か**（応募用プロフィール JSON / 職務経歴書 MD・PDF / スキルタグ / 応募文テンプレ / 企業別カバーレター）

→ 仲氏への集約質問：「v1 のプロファイル生成は A/B/C/D どれを主軸にするか。**推奨は D**（公開情報で叩き台→対話で事実確認・希望/NG 補正→最終プロフィール固定）」

### v1 アプローチ 3 案（トレードオフ）
| 案 | 概要 | メリット | デメリット |
|---|---|---|---|
| **案1 A中心・最速MVP** | 既存書類を正データ→JSON 変換、探索〜応募〜レビューキューを最短実装 | 実装最速 / 書類品質安定 / 事実誤認少 | 仲氏の OSS・発信・AI 活用の強みが薄い / 面白み弱い / 書類が古いと精度低下 |
| **案2 B中心・公開情報生成** | GitHub/Substack/X から根拠付き自動生成 | 仲氏らしさ◎ / 根拠リンク付き応募文 / プロダクト見栄え◎ | API/規約/取得安定性 / 発信のノイズ補正要 / 実務と個人活動の境界誤認リスク |
| **案3 D中心・ハイブリッド（推奨）** | B叩き台→C補正→A事実確認→canonical_profile | 実用性・精度・見栄えのバランス◎ / 根拠付き / 育てる前提に強い | 実装範囲広め / 初回だけ対話の手間 / データモデルを丁寧に設計 |

### データ構造（Codex 提案）
`profile_sources`（A/B/C の元データを保持）＋ `canonical_profile`（応募で使う確定情報だけ集約）。各スキル・実績・希望条件に `evidence`（GitHub / Substack / 対話回答 / 既存書類 のどれ由来か）を持たせて追跡。

### 最小 v1 の順番
①Q5 確認 → ②canonical profile スキーマ作成 → ③各ソースからプロフィール生成 → ④AI/技術特化求人＋メール直応募先の収集 → ⑤闇バイト/詐欺フィルタ → ⑥マッチング理由付きランキング → ⑦応募文・メール文ドラフト → ⑧人間レビュー後のワンクリック送信キュー

### 次のブロッカー（解消）
**Q5 = A（既存書類ベース）に確定（2026-06-03）。** 次手＝A中心 v1 の設計（既存書類の取り込み形式 → canonical_profile スキーマ → マッチング → ドラフト → レビューキュー）。設計時点では現物書類は不要、ランタイムで必要。**残確認: 職務経歴書/履歴書の有無・鮮度・配置パス。**

---

## Codex の A中心 v1 設計（masup WSL2 / `codex exec` / 2026-06-03、read-only、gpt-5.5）

> 全文 capture: masup `~/job-hunt-design-a.txt`（673行、preamble込み）。以下は設計本体。

### 仲氏への残確認（A中心の前提・**次のブロッカー**）
1. **職務経歴書は存在するか**。最終更新日、形式（PDF/DOCX/Markdown/Google Docs export 等）、配置パス、最新版か。
2. **履歴書は存在するか**。最終更新日、形式、配置パス、写真・住所・電話番号・メールの扱い。
3. **既存書類はそのまま応募に使える品質か**。古い職歴、未反映プロジェクト、削除したい記載、盛りすぎ表現の有無。
4. 職務経歴書と履歴書で矛盾時、どちらを正とするか（原則: 履歴書=個人情報/学歴/職歴年月、職務経歴書=スキル/実績/職務内容）。
5. 希望条件の最新値（正社員/業務委託/フリーランス優先度、年収/単価、稼働開始時期、週稼働日数、リモート可否、onsite は須磨区戎町近辺限定）。
6. 応募文に自動挿入してよい個人情報（本名、メール、電話、住所粒度、GitHub/Substack/X URL）。
7. v1 の生成物形式（`canonical_profile.json` / 職務経歴書 MD・PDF / 企業別応募メール / カバーレター / レビューキューDB のどこまで必須か）。
8. 書類配置ルール（例: `~/job-hunt/input/resume.*` `~/job-hunt/input/cv.*`、生成物は `~/job-hunt/output/`）。

### 1. 基本方針
v1 は既存の職務経歴書/履歴書を**唯一の一次情報**として扱う。GitHub/Substack/X は v1 では自動補完に使わず、書類内に URL がある場合のみリンク保持。狙いは「速く・事実誤認少なく・応募可能なドラフトまで到達」。

### 2. パース方針
入力を `source_documents`（原本パス・ハッシュ・抽出テキスト・抽出日時）として保存。PDF/DOCX/MD/TXT 優先、画像PDF/スキャンは v1.1（OCR 失敗はレビューキュー）。2段階: ①deterministic extraction（見出し/表/箇条書き/年月/URL/メール/電話を構造化）→ ②LLM structured parsing（スキーマへマッピング、各フィールドに `source_ref`）。衝突解決優先順位: 個人情報/学歴/職歴年月=履歴書、職務内容/技術/実績/自己PR=職務経歴書、希望条件=書類より仲氏の最新回答、不明/矛盾=自動推測せず `needs_review`。

### 3. canonical_profile JSON スキーマ案
```json
{
  "schema_version": "1.0",
  "updated_at": "ISO-8601",
  "person": {
    "name": "string", "email": "string|null", "phone": "string|null",
    "location_public": "string", "location_private": "string|null",
    "links": {"github":"string|null","substack":"string|null","x":"string|null","portfolio":"string|null"}
  },
  "job_preferences": {
    "employment_types": ["full_time","contract","freelance"],
    "target_roles": ["string"], "industries": ["string"],
    "remote": "remote_only|hybrid_ok|onsite_ok",
    "onsite_location_rule": {"enabled": true, "allowed_area": "神戸市須磨区戎町近辺", "excluded_places": ["MASU-p"]},
    "salary_or_rate": {"annual_jpy_min":"number|null","monthly_jpy_min":"number|null","hourly_jpy_min":"number|null"},
    "availability": {"start_date":"string|null","weekly_days":"number|null","notes":"string|null"},
    "ng_conditions": ["string"]
  },
  "summary": {"headline":"string","short_bio":"string","strengths":["string"]},
  "skills": [{"name":"string","category":"language|framework|cloud|ml_ai|tool|domain|other","level":"beginner|intermediate|advanced|expert|null","years":"number|null","evidence":[{"source_id":"string","quote":"string"}]}],
  "work_history": [{"company":"string","role":"string","employment_type":"string|null","start":"YYYY-MM|null","end":"YYYY-MM|null","description":"string","achievements":["string"],"technologies":["string"],"source_refs":["string"]}],
  "projects": [{"name":"string","type":"work|oss|personal|writing|other","url":"string|null","description":"string","impact":"string|null","technologies":["string"],"source_refs":["string"]}],
  "education": [{"school":"string","degree_or_department":"string|null","start":"YYYY-MM|null","end":"YYYY-MM|null"}],
  "certifications": [{"name":"string","issued_by":"string|null","issued_at":"YYYY-MM|null"}],
  "application_assets": {"base_resume_path":"string|null","base_cv_path":"string|null","default_cover_letter_tone":"concise_professional"},
  "review_flags": [{"field":"string","severity":"info|warning|blocking","message":"string"}]
}
```

### 4. データフロー
- **探索**: 求人ソースは AI/技術特化＋メール直応募に限定。Findy/LAPRAS 等は規約に合わせ手動エクスポート or 許可 API/通知メール起点。URL・本文・会社名・職種・勤務地・報酬・連絡先・応募方法を `job_posting` に保存。
- **マッチング**: `canonical_profile` × `job_posting` でスキル/役割/契約形態/勤務地/報酬/リモート/NG/詐欺リスクをスコア化。順位＋「応募すべき理由/懸念/訴求軸」を必ず持たせる。
- **ドラフト**: 求人ごとに応募メール/カバーレター/（必要なら）職務経歴書強調版。書類の事実を超える主張は禁止、`source_refs` 付き項目からのみ。
- **レビューキュー**: 状態 `draft|needs_edit|ready_to_send|sent|rejected|blocked_scam`。画面に求人本文/マッチ理由/リスク判定/ドラフト/編集欄/送信先/添付を表示。送信は手動クリック or メール直応募のみワンクリック。

### 5. 闇バイト/詐欺フィルタ判定項目
即時ブロック候補: 業務曖昧×高報酬/日払い/即日現金 ・面接なし/履歴書不要/誰でも/スマホだけ/短時間高収入 ・Telegram/Signal/個人LINE/匿名SNS誘導 ・身分証/口座/クレカ/暗号資産ウォレット/ログイン情報の先出し要求 ・荷物受取/口座貸与/名義貸し/決済・送金・レビュー代行 ・会社名/所在地/法人番号/採用ページ/固定メールドメイン不明 ・相場乖離報酬 ・契約書前の個人情報/金銭要求 ・コピペ風本文/外部誘導のみ/仕事内容が頻繁変化。判定は `risk_score 0-100` ＋ `risk_level: low|medium|high|blocked`。`high` 以上はキュー表示するが送信不可、`blocked` は自動除外。

### 6. エラー処理
書類未配置=`blocking` で停止しパス提示 / パース失敗=原本・抽出テキスト・理由保存し別形式変換促す / スキーマ検証失敗=`review_flags` 行き・ドラフトに使わない / 矛盾=`needs_review`（自動で丸めない）/ 求人取得失敗=ソース単位リトライ・他は継続 / ドラフト失敗=スナップショット保存し再生成可 / 送信失敗=メール直応募のみ送信ログ・再送可否保存。

### 7. テスト方針
- ユニット: PDF/DOCX/MD/TXT 抽出 / スキーマ検証 / 履歴書×職務経歴書の衝突解決 / **勤務地フィルタ（onsite は須磨区戎町近辺のみ・MASU-p は候補にしない）** / 詐欺フィルタ赤フラグ / スコアリング基本ケース
- ゴールデン: サンプル職務経歴書→期待JSON / サンプル求人→期待するマッチ理由・懸念・訴求軸 / ドラフトが書類にない実績を捏造しない
- E2E: 書類配置→パース→profile生成→求人投入→フィルタ→マッチング→ドラフト→キュー登録 / 詐欺疑いは送信可能状態にならない / メール直応募は送信前プレビュー必須

**v1 完成条件**: 既存書類から正規プロフィールを作り、求人を安全にふるい分け、応募文を生成し、人間レビュー付きで送信直前まで持っていけること。

---

## v1 スコープ更新（2026-06-03、仲氏指示で確定）
- **既存書類あり → A中心成立。既存の職務経歴書/履歴書の「フル活用」が唯一のプロファイル源**（GitHub/Substack/X の自動補完は v1 では不要＝「それが全て」）。
- **闇バイト/詐欺フィルタは v1 から除外**（仲氏指示）。→ 上記設計の「5. 詐欺フィルタ判定項目」、データフローの安全フィルタ段・`blocked_scam` 状態、詐欺フィルタ系テストは v1 で実装しない。マッチングは「適合スコア＋応募理由/懸念/訴求軸」に集中。
- **残（実 ingest に必要）**: 既存書類の形式（PDF/DOCX/MD 等）と配置パス。

---

## Codex の v1 実装入口設計（masup / `codex exec` / 2026-06-03、read-only、gpt-5.5）

> 全文 capture: masup `~/job-hunt-impl.txt`（554行）。

### 仲氏への残確認（実 ingest 用・これだけ）
1. 職務経歴書の形式（PDF / DOCX / Markdown / TXT / その他）
2. 職務経歴書の配置パス（例 `~/job-hunt/input/cv.pdf`）
3. 履歴書の形式
4. 履歴書の配置パス（例 `~/job-hunt/input/resume.pdf`）

### v1 確定（再掲）
既存の職務経歴書/履歴書が**唯一のプロファイル源**。公開情報の自動補完なし（書類内 URL は保持可）。**詐欺フィルタ完全除外**（安全フィルタ段・`blocked_scam`・詐欺スコア・詐欺テスト無し）。評価軸＝適合度・応募理由・懸念・訴求軸。

### モジュール分割
| モジュール | 責務 | 入力 | 出力 |
|---|---|---|---|
| `config` | パス/LLM/DB/v1固定ルール読込 | `config.yaml`,env | `AppConfig` |
| `document_loader` | 書類の存在確認・ハッシュ・テキスト抽出 | 書類パス | `SourceDocument[]` |
| `profile_parser` | 抽出テキスト→構造化 | `SourceDocument[]` | `CanonicalProfile`,`review_flags` |
| `profile_validator` | スキーマ検証・必須欠落・矛盾検出（推測で埋めない） | `CanonicalProfile` | validated / errors |
| `job_ingest` | 求人を手動/CSV/JSON/MDから取込 | 求人ファイル/URLメモ | `JobPosting[]` |
| `job_filter` | v1範囲フィルタのみ（AI/技術系・メール直応募・勤務地） | `JobPosting[]`,config | filtered |
| `matcher` | 照合・順位付け | profile,`JobPosting[]` | `MatchResult[]` |
| `draft_generator` | 応募メール/カバーレター生成（書類由来の事実だけ） | profile,job,match | `ApplicationDraft` |
| `queue` | レビューキュー永続化 | draft,match,job | `ApplicationItem` |
| `ui` | レビュー/編集/状態変更/送信前確認 | queue DB | dashboard |
| `mailer` | メール直応募のみ・レビュー後送信 | approved item | send log |

キュー状態（v1）: `draft` / `needs_edit` / `ready_to_send` / `sent` / `rejected`

### 最小ディレクトリ構成
```text
job-hunt/
  pyproject.toml  README.md  .env.example
  config/config.yaml
  input/{resume.*, cv.*, jobs/sample_jobs.md}
  output/{canonical_profile.json, drafts/}
  data/job_hunt.sqlite
  src/job_hunt/{__init__,config,document_loader,profile_parser,profile_validator,job_ingest,job_filter,matcher,draft_generator,queue,mailer,cli,ui,schemas}.py
  tests/{fixtures/, test_document_loader.py, test_profile_parser.py, test_matcher.py, test_draft_generator.py, test_e2e_minimal.py}
```

### 最初に作る順番（最小E2E最短）
1. `schemas.py`（`SourceDocument`/`CanonicalProfile`/`JobPosting`/`MatchResult`/`ApplicationDraft`/`ApplicationItem`）
2. `config.py`（書類パス/DB/LLM/勤務地ルール）
3. `document_loader.py`（PDF/DOCX/MD/TXT 抽出、まず MD/TXT を確実に）
4. `profile_parser.py`（抽出→`canonical_profile.json`、初手 LLM structured output）
5. `profile_validator.py`（欠落/矛盾を `review_flags`、補完しない）
6. `job_ingest.py`（`input/jobs/sample_jobs.md` から投入）
7. `job_filter.py`（onsite=須磨区戎町近辺、MASU-p 除外）
8. `matcher.py`（スキル/職種/契約/勤務地/リモート/報酬で単純スコア）
9. `draft_generator.py`（1求人→応募メール1通）
10. `queue.py`（SQLite に `draft` 保存）
11. `cli.py`（`ingest-profile → ingest-jobs → match → draft → list-queue` の最小E2E）
12. `ui.py`（CLI E2E 後に Streamlit）

最小E2E ゴール: `job-hunt ingest-profile` → `ingest-jobs input/jobs/sample_jobs.md` → `match` → `draft --top 3` → `queue`

### 一次情報源 確定（2026-06-03、仲氏指示）
- **参政党スタッフ応募で提出した書類が最新＝v1 の唯一の源**（`~/Desktop/sanseito-application/`）:
  - `スタッフ 仲啓輔 履歴書.pdf`（履歴書 / PDF。中身は `docs/job-search/rireki-2023-0720.pdf` と同一バイト）
  - `sanseito_staff_resume_template.xlsx`（参政党フォーマット、最新 5/21。**Excel ＝ `document_loader` に xlsx パーサ `openpyxl` を追加**。記入済みかは PII 保護のため未 open）
  - `スタッフ 仲啓輔 証明写真.jpg`（証明写真 ＝ application asset。プロフィール本文の抽出対象ではない）
- → Codex 残確認（形式/配置パス）**解消**。`docs/job-search/` の shokumu/rireki 各版（v1/v2/2023）は予備（参政党提出物を正とする）。
- ⚠️ **PII**: 履歴書・写真は個人情報（氏名・住所等）。**masup は共用機**なので、開発・テストは redacted fixtures で行い、実書類は実行時のみ・配置先限定。実装時に厳守。

---

## 実装ステータス（2026-06-03）

### v1 実装入口を masup で scaffold 済み（作る順 1〜3 ＋ 足場）
- **場所**: masup WSL2 `/home/gci_admin/job-hunt/`（Linux ext4、独立 git リポジトリ。Mac の知識ベース repo とは別）。`sanseito-application/` 等の PII は未参照・未コミット、`input/*` は `.gitignore` 済み。
- **生成**: masup Codex（gpt-5.5、`codex exec --sandbox workspace-write`）
- **生成物**: `pyproject.toml`（hatchling/uv、`pythonpath=["src"]`）/ `.env.example` / `config/config.yaml` / `src/job_hunt/{__init__,schemas,config,document_loader}.py` / `tests/fixtures/{sample_resume.md,sample_resume.txt,sample_jobs.md}`（**架空・redacted**）/ `tests/test_document_loader.py`
  - `schemas.py`: pydantic v2、`CanonicalProfile` ほか全モデル。`OnsiteLocationRule(allowed_area="神戸市須磨区戎町近辺", excluded_places=["MASU-p"])`、`ApplicationStatus` に `blocked_scam` 無し（詐欺フィルタ除外を反映）
  - `document_loader.py`: MD/TXT 直読、PDF=pymupdf / DOCX=python-docx / XLSX=openpyxl は**遅延 import**（未導入時は `needs_review` フォールバック）、画像は OCR 未対応(v1.1)で review 行き。`extract_document` は pydantic 非依存の純関数
  - `config.py`: YAML＋env オーバーライド、`LLMConfig.api_key` は env 参照（秘密値を埋めない）
- **独立検証（Claude が自分で実行）**: `py_compile` 全 OK / `uv run --no-project --with pytest pytest` = **2 passed** / pydantic 下で `schemas`＋`config` import OK・`CanonicalProfile` 構築可・`onsite excluded=['MASU-p']` 確認
- **全文ログ**: masup `~/job-hunt-scaffold.log`

### #4 profile_parser 完了（2026-06-03）
- **生成物**: `src/job_hunt/llm.py` / `src/job_hunt/profile_parser.py` / `tests/fixtures/expected_profile.json`（架空・PII無し）/ `tests/test_profile_parser.py`
  - `profile_parser.build_canonical_profile(sources, llm)`: LLM 構造化出力を `CanonicalProfile` に pydantic 検証。**捏造禁止・欠損/矛盾→`review_flag`・MASU-p 除外をコード側で強制**（LLM 任せにしない）。person.name/summary.headline 等の必須欠落は blocking フラグ＋空文字。skills の evidence・work_history/projects の source_refs 欠落は warning。
  - `llm.py`: `StructuredProfileLLM`(Protocol) / `OpenAIStructuredLLM`(実行時用、`openai` を遅延 import、responses.parse と beta.chat.completions.parse の両対応、API キーは config/env) / `StubProfileLLM`(テスト注入用)。
- **独立検証（Claude が自分で実行）**: `py_compile` OK / `pytest` = **4 passed**（document_loader 2 ＋ profile_parser 2）/ `llm`+`profile_parser` import で `openai` が読み込まれない＝**オフライン動作確認**
- **全文ログ**: masup `~/job-hunt-parser.log`

### 未実装（次の増分）
`profile_validator`(#5) → `job_ingest`(#6) → `job_filter`(#7、勤務地フィルタ) → `matcher`(#8) → `draft_generator`(#9) → `queue`(#10) → `cli`(#11、最小E2E) → `ui`(#12、Streamlit)。**詐欺フィルタは作らない。**

### 技術スタック
Python 3.11/3.12 ・ `uv` ・ CLI=`typer` ・ 型/スキーマ=`pydantic` ・ DB=SQLite+`sqlmodel`(or `sqlite-utils`) ・ PDF=`pymupdf` ・ DOCX=`python-docx` ・ LLM=OpenAI structured outputs（masup WSL2 に集約） ・ UI=CLI→`streamlit` ・ test=`pytest` ・ `ruff`+`mypy` 早め ・ メールは後半 SMTP/Gmail API（初手は `.eml` 生成まで）。**実装入口＝`schemas.py` + `document_loader.py`**。
