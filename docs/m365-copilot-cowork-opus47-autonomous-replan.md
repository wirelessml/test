# Microsoft 365 Copilot Cowork × Claude Opus 4.7 — 自律再計画の挙動観察

> 観察日: 2026-04-26 20:25 JST
> 観察者: 仲結花
> 関連ファイル: @docs/m365-copilot-claude-opus.md / @docs/m365-copilot-researcher-gpt-vs-claude.md

## 概要

Microsoft 365 Copilot の **Cowork** モードで **Claude Opus 4.7** をモデル選択して実タスクを走らせると、Cowork が **「初回計画 → 追加プロンプト受領 → 再計画 → 不要プロセスを自分で削除 → 自律実行」** という**自己修正型の長時間エージェント挙動**をすることを実機で確認した。

これは Anthropic 公式の Opus 4.7 マーケコピー「**long-running tasks with more rigor / offers its own outputs before reporting back**」が UI レベルで具現化された事例である。

## 観察したタスク

- **タスク名**: 「会議内容を PowerPoint スライド化する」
- **モデル**: Claude Opus 4.7（右上モデルセレクタで選択）
- **使用スキル**: PowerPoint / 詳細な調査
- **テーマ**: Microsoft Purview の主張（10 件）の事実検証 + Information Protection 戦略のスライド化

## 進行状況パネルの読み取り (7/9)

| # | ステップ | 状態 | 備考 |
|---|---|---|---|
| 1 | Researching: Microsoft Purview 主張検証 | ✅ 完了 | learn.microsoft.com 横断、複数 site: クエリ |
| 2 | Verifying findings | ✅ 完了 | |
| 3 | Writing the report | ✅ 完了 | purview-claims-factcheck-report.md 出力 |
| 4 | 本文の精度を修正中 | 🔴 進行中 | 主張10 が運用上の誤解を招くと判断 |
| 5 | 非表示スライドで修正ログを追加 | ⭕ 未着手 | 修正経緯を**非表示スライド**として保持する戦略 |
| 6 | スライドの作成と仕上げ | ❌ **自律削除** | Cowork が「現段階では不要」と判定 |
| 7 | 公式ドキュメントの出典 URL 確認 | ❌ **自律削除** | 上の修正サイクルに統合済みと判定 |

## 出力フォルダ

- `purview-claims-factcheck-report.md`（ファクトチェック結果レポート）
- `purview-information-protection-strat...`（戦略文書、ファイル名末尾省略）

## 自律再計画の流れ（再構成）

```
[初回プロンプト]
  └─ Cowork が 9 ステップ計画を生成
      └─ Step 1-3 を完了

[追加プロンプト到着]
  「スライド作成後にも一度、Deep Reasoning または Deep Research または
   リサーチツールを使ってファクトチェックと、技術的実現可能性、
   サービスとしての実現可能性等もチェックしてね。
   もし修正ポイントなどがあったらそれは非表示スライドとして
   どう直したかをまとめたうえで修正しちゃってね。」

  └─ Cowork が再計画
      ├─ Step 4「本文の精度を修正中」を新設
      ├─ Step 5「非表示スライドで修正ログ追加」を新設
      ├─ Step 6/7 を **❌（不要）** にマーク（既存タスクへの統合判断）
      └─ 修正→検証→ログ化のループに自律遷移
```

## 注目すべき UX デザイン

1. **削除タスクを ❌ で残して透明化している**
   - 黒塗りで隠さず、「何をスキップしたか」が一覧で見える
   - ユーザーが「不要判定が妥当か」を後追いで検証可能
2. **進行中タスクは赤丸で明示**（4 番目「本文の精度を修正中」）
3. **出力フォルダ・スキル・入力フォルダが右ペインにライブ表示**
   - 「今エージェントが何を見て何を出してるか」がリアルタイムで把握可能

## 技術的に確定した事実

- **Microsoft Copilot Cowork は Opus 4.7 を選択肢として持っている**
  - これは Claude Desktop の Cowork（Sonnet 4.6 ハードコード、`@docs/rules/operations.md` に記載）とは別系統
  - Microsoft 経由なら Opus 4.7 が走る、別ルートとして要記憶
- **長時間タスクの中盤でユーザー追加指示を受けて計画再構築できる**
  - これは旧 Cowork（Sonnet 4.6 時代）には観察されなかった挙動
- **自律的に「不要」と判定したステップを削除（❌マーク化）し、新ステップを追加する**
  - 単なる順序変更ではなく**計画の構造そのものの編集**

## Anthropic 公式告知との対応

| Anthropic 4/17 告知文言 | 実機で確認された挙動 |
|---|---|
| handles long-running tasks with more rigor | 9 ステップの長時間タスクを完走 |
| follows instructions more precisely | 「非表示スライドにまとめて修正」を厳密に Step 5 として実装 |
| offers its own outputs before reporting back | Step 4 で「主張10 が誤解を招く」と**自己発信** |
| less supervision needed | 削除判断・追加判断を**ユーザー承認なし**で実行 |

公式マーケコピーがそのまま検証可能な形で Microsoft 製 UI に出ている、という事例として記録に値する。

## ユーザー所感（@minimalistneko）

> Copilot Cowork 自分でプランを作成しつつ、追加プロンプトを見て一回プランニングするも、再度不要プロセスだと思ったら削除して自律的に動くのはやっぱり感動もの。 #なんでもCopilot

「**感動もの**」という強い肯定。Substack ネタ価値あり。

## Substack 連載へのフック候補

### タイトル案

- 「Microsoft Copilot Cowork × Claude Opus 4.7 — 追加プロンプトで計画ごと書き換える AI を見た」
- 「不要タスクを自分で削除する Cowork — Opus 4.7 の `less supervision` を Microsoft の UI で体感した日」
- 「#なんでもCopilot — Anthropic のマーケコピーが Microsoft 製 UI で実証された 10 分間」

### 角度

- Anthropic 告知 → Microsoft 実装 → 日本のミニマリスト弟子層（4/26 同日のあい / しぶ Usutaku セミナー）まで**「同日内に三層で広がった日」**として書く
- M365 Copilot Researcher（@docs/m365-copilot-researcher-gpt-vs-claude.md）と並べて「**Researcher = 深い調査 / Cowork = 長時間自律実装**」という機能比較記事

## 関連ナレッジ

- @docs/m365-copilot-claude-opus.md — M365 Copilot で Claude Opus を使う基礎
- @docs/m365-copilot-researcher-gpt-vs-claude.md — Researcher における GPT vs Claude 比較
- @docs/journal/2026-04-26.md — 観察日のジャーナル

## 変更履歴

- 2026-04-26: 初版作成（実機観察スクリーンショット 1 枚から起こし）
