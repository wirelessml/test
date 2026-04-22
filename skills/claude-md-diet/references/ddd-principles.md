# DDD 原則の CLAUDE.md 運用への適用

Domain-Driven Design (DDD) の 3 つの核概念を CLAUDE.md 運用に借用する。

## 1. Bounded Context (境界づけられたコンテキスト)

### 原義
同じ用語・モデルが一貫した意味を持つ範囲。異なる Context では同じ用語が違う意味を持つ。

### CLAUDE.md 運用への翻訳
- **1 ファイル = 1 Context**
- 機材 Context、プロジェクト Context、ルーチン Context を混ぜない
- 例: `docs/machines/shun-sensei-pc.md` はそのマシンだけの情報。しぶプロジェクトの話は書かない

### 適用例

**Bad**（コンテキスト混在）:
```markdown
## しゅん先生 PC
- Intel i7-8700K
- 4/22 Plextor 死亡
- しぶの YouTube 動画 20 本はここで編集予定
- iPhone の音楽プレイヤー問題も関連
```

**Good**（Context 分離）:
```markdown
# docs/machines/shun-sensei-pc.md
## しゅん先生 PC
- Intel i7-8700K
- 4/22 Plextor 死亡、Seagate 延命中

# docs/projects/shibu.md
## しぶプロジェクト
- 動画編集作業機: しゅん先生 PC (@docs/machines/shun-sensei-pc.md)

# docs/projects/iphone-music.md
## iPhone 音楽問題
- 別件として分離
```

## 2. Aggregate Root (集約ルート)

### 原義
関連するエンティティ群のエントリポイント。外部からは Root 経由でのみアクセスする。

### CLAUDE.md 運用への翻訳
- **CLAUDE.md が Aggregate Root**
- 詳細ファイルには CLAUDE.md 経由（`@import`）でアクセス
- 詳細ファイル同士の横断参照は最小限に

### 適用例

```markdown
# CLAUDE.md (Root)

## 機材
- しゅん先生 PC: @docs/machines/shun-sensei-pc.md
- MASU-P55: @docs/machines/masu-p55.md
- M1: @docs/machines/m1-macbook-air.md

## プロジェクト
- しぶ観察: @docs/projects/shibu.md
- Substack: @docs/projects/substack.md
```

Claude Code はセッション開始時に CLAUDE.md を読み、必要に応じて `@` 参照をたどる。ユーザーが「しゅん先生 PC で作業」と言ったときだけ `shun-sensei-pc.md` がロードされる = lazy loading。

## 3. Ubiquitous Language (ユビキタス言語)

### 原義
1 つの Bounded Context 内では、開発者・ドメイン専門家・ドキュメントが同じ用語を使う。

### CLAUDE.md 運用への翻訳
- **各ファイル内で用語を統一**
- CLAUDE.md で俗称、詳細ファイルで正式名称、を混在させない
- プロジェクト全体で通じる用語集を `docs/glossary.md` に

### 適用例

**Bad**（同一対象を複数の呼び方）:
```markdown
# あるファイル
- 愛 (ikeai_minimalist) = Minimal Arts の広報担当

# 別のファイル
- あい (@ikeai) = 福岡の女性

# さらに別のファイル
- Ikeai (33 歳) = しぶの弟子
```

**Good**（統一）:
```markdown
# docs/glossary.md
- **あい** (@ikeai_minimalist): 33 歳、福岡、Minimal Arts 広報担当、しぶの直属の弟子

# 他のファイルでは
「あい」表記で統一（詳細: @docs/glossary.md）
```

## Instruction Dilution (指示希釈) の緩和

### 現象
CLAUDE.md に 50 個ルールを書くと、AI は重要度を推測で並べ替えて上位 3-5 個しか守らなくなる。これは長い prompt でも同じ現象が起きる。

### DDD 的解決策

1. **ルールを Context ごとに分離**: 機材操作ルールは `docs/rules/machines.md`、コーディング規約は `docs/rules/coding.md` へ
2. **発動条件を明記**: 「この Context の作業時にのみ適用」を明記
3. **優先順位の宣言**: CLAUDE.md には「最重要 3 ルール」だけ書き、それ以外は Context 別ファイルへ
4. **ルールの集約**: `docs/rules/index.md` で一覧化し、細部は個別ファイル

### 例

**Bad**（CLAUDE.md に全部入り）:
```markdown
## 操作上の注意
- 記事削除前は件数確認
- computer-use 時は事前説明せず
- Dispatch 使わない
- Manus が推奨
- Claudeデスクトップは...
- ブラウザは tier "read"
- X PWA は full tier
- ...
(以下 50 項目)
```

**Good**（最重要のみ CLAUDE.md）:
```markdown
## 操作上の注意 (最重要 3 つ)

1. 記事削除・一括更新前は件数を報告して確認
2. 金銭トランザクション（発注・送金・取引）は代行しない
3. 認証・ログイン操作はユーザー実行のみ

詳細な操作規約: @docs/rules/operations.md
Context 別のルール:
- 機材操作: @docs/rules/machines.md
- コーディング: @docs/rules/coding.md
- セキュリティ: @docs/rules/security.md
```

## 参考

- Eric Evans "Domain-Driven Design: Tackling Complexity in the Heart of Software" (2003)
- Vaughn Vernon "Implementing Domain-Driven Design" (2013)
- Martin Fowler "BoundedContext" (https://martinfowler.com/bliki/BoundedContext.html)
