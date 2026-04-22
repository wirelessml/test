# Claude Code `@import` 機構

## 基本構文

```markdown
@docs/machines/shun-sensei-pc.md
@docs/journal/2026-04-22.md
@./CONTEXT.md
```

- `@` で始まる行を Claude Code が検出
- 相対パスまたはプロジェクトルート相対パス
- セッション開始時、または参照された時にロード

## ネスト深度

- 最大 **5 階層**までネスト対応
- それ以上は無視される
- 実用上 **3 階層以内**に収めるのが安全

**Good**:
```
CLAUDE.md
  → @docs/machines/shun-sensei-pc.md
    → @docs/machines/specs/i7-8700k.md (2 階層)
```

**Bad**:
```
CLAUDE.md
  → @a.md
    → @b.md
      → @c.md
        → @d.md
          → @e.md
            → @f.md (6 階層、無視される)
```

## パス解決ルール

| 記法 | 解決先 | 例 |
|---|---|---|
| `@docs/foo.md` | プロジェクトルート相対 | `/Users/yuika/Desktop/docs/foo.md` |
| `@./foo.md` | 現在のファイルと同じ階層 | 現在のファイルディレクトリ |
| `@../bar.md` | 1 つ上の階層 | 相対パス |
| `@~/foo.md` | ホームディレクトリ | `/Users/yuika/foo.md` (非推奨) |
| `@/absolute/path.md` | 絶対パス | 可読性低下、非推奨 |

**推奨**: プロジェクトルート相対 (`@docs/...`) で統一。

## 発火タイミング

1. **セッション開始時**: CLAUDE.md 読込時、直接の `@` 参照は**サマリー情報**として読まれる
2. **話題が該当したとき**: 対応する Context のファイルが完全ロードされる
3. **明示的指定**: ユーザーまたは Claude が `Read <path>` で読む

## 情報の重複を許す原則

**OK**: CLAUDE.md に 1-2 行サマリー + 詳細ファイルに完全版 (重複ではなく **多層化**)

```markdown
# CLAUDE.md
## しゅん先生 PC
コワーキング据え置き、2018 年 BTO、4/22 Plextor 死亡で Seagate 起動中。詳細: @docs/machines/shun-sensei-pc.md
```

```markdown
# docs/machines/shun-sensei-pc.md
# しゅん先生 PC
## 役割
コワーキングスペース据え置きの Windows メイン機...
## ハードウェア
### CPU
Intel Core i7-8700K @ 3.70GHz...
### RAM16GB DDR4-2666...
(以下 200 行の詳細)
```

この重複は**意図した冗長性**で、DDD でいう「Shared Kernel」に近い。

## アンチパターン

### 1. `@` 行を箇条書きの中に書くと解釈されないケース

**Bad**:
```markdown
- 詳細は @docs/foo.md を参照
```

リストアイテムの途中にある `@` は解釈が不安定。

**Good**:
```markdown
- 詳細: @docs/foo.md
```

または

```markdown
詳細は下記参照:

@docs/foo.md
```

独立した行にする、もしくは行頭の目印を工夫。

### 2. 相対パスが解決できないディレクトリから import

`docs/journal/2026-04-22.md` から `@../machines/foo.md` のような `..` を使うと、実行コンテキスト次第で解決失敗することがある。

**Good**: すべてプロジェクトルート相対 (`@docs/machines/foo.md`) で統一。

### 3. 循環参照

`A.md → @B.md → @A.md` は無限ループではなく**片方が無視**される（実装依存で不安定）。

### 4. 過度な `@` 乱用

1 ファイルに `@` 参照が 20 個以上あると、セッション開始時に全部 shallow load されて逆に重くなる。

**目安**: CLAUDE.md からの直接 `@` 参照は **10 個以下**。

## 検証手段

```bash
# CLAUDE.md 内の @ 参照を一覧化
grep -oE "@[a-zA-Z0-9_/\.-]+\.md" CLAUDE.md

# 各参照先の存在確認
grep -oE "@[a-zA-Z0-9_/\.-]+\.md" CLAUDE.md | while read p; do
  path="${p#@}"
  [ -f "$path" ] && echo "✓ $p" || echo "✗ MISSING: $p"
done

# 参照されてないファイルを発見（孤児）
find docs -name "*.md" | while read f; do
  if ! grep -q "$f" CLAUDE.md docs/*.md docs/*/*.md 2>/dev/null; then
    echo "ORPHAN: $f"
  fi
done
```

## プラットフォーム差異

- **Claude Code (CLI)**: `@` 自動解決、ネスト 5 階層
- **Claude.ai (web)**: `@` 参照を手動で展開する必要あり (Projects 機能使用時)
- **Gemini CLI**: 独自の `@` 機構（非互換）
- **Codex**: 公式には `@import` なし、実装による

CLAUDE.md の `@` 機構は **Claude Code 固有**。他ツールと共有する場合は注意。
