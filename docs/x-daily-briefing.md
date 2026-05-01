# X Daily Briefing

> ⚠️ **2026-05-02 朝にこのルーチンは廃止**。以下のログは過去のアーカイブ。
>
> 廃止理由: 定型的な巡回が情報の質より量に流れた。今後は必要時に都度 `twitter -c feed` / `twitter -c search` を判断で実施する形に切替。

~~各セッション（9/14/19/0/5時）でX情報を収集して追記するログ。~~

- ~~対象: For Youタイムライン + キーワード検索（AI・Claude関連）~~
- ~~手段: X PWA（@minimalistneko ログイン済み、computer-use full tier）~~
- ~~形式: セッション毎に日時・タイムライン・検索結果・注目ポイントを追記~~

---

## 2026-04-17 04:53 JST（セッション外・テスト収集）

### Today's News（X AI関連）
- **Anthropic Launches Claude Opus 4.7 Most Capable Model Yet**（20h前、446 posts）
- Google Upgrades Chrome AI Mode with Side-by-Side Browsing（1h前、238 posts）
- **Anthropic Launches @ClaudeDevs X Account for Claude Developers**（5h前、2,060 posts）

### For Youタイムライン
- **@oikonxid**: Anthropic発表のClaudeアップデートについて。Changelogs/APIリリース/コミュニティアップデート/Deep Dive用の@ClaudeDevsアカウント告知
- **@ClaudeDevs**: "For the developers building with Claude, a direct line from the team."（開発者向け新アカウント）

### キーワード検索「Claude Opus 4.7」
- **@Claude公式**: "Introducing Claude Opus 4.7, our most capable Opus model yet. It handles long-running tasks with more rigor, follows instructions more precisely, and offers its own outputs before reporting back. You can hand off your hardest work with less supervision."
- People: よし(@yoshi_ai_mentor) Claude Codeで副業収益配信、Claude Code研究所スパルタClaude Code塾

### Live on X
- スペース配信中（安さん出演、リスナー286）

### What's happening
- エンドフィールド新バージョン配信 / 神秘の召刀 / ヴィッセル神戸

### 注目ポイント
- **Opus 4.7正式告知**をCEO系公式とClaude公式が同時にアナウンス
- **@ClaudeDevs新設**: 開発者向けチャネル、5時間前に開始し既に2,060 posts
- Chrome Side-by-Side Browsing（AIモード）が1時間前の新トピック

---

## 2026-04-17 05:14 JST（Cookie取得後、twitter CLIテスト）

### `twitter -c search "Claude Opus 4.7"` 結果（抜粋）

| author | likes | RT | 要点 |
|---|---|---|---|
| @claudeai | 64,092 | 8,101 | Opus 4.7公式告知（長時間タスク・指示追従・自己出力確認） |
| @SuguruKun_ai | 76 | 9 | 高解像度ビジョン2,576px（3倍）・指示遵守大幅改善・自己検証・ツール使用エラー33%削減 |
| @okuyama_ai_ | 6 | 0 | 画像3倍（長辺2,576px=3.75MP）・価格据え置き（入力$5/出力$15/1M） |
| @bioshok3 | 29 | 5 | Mythos Previewより意図的に低能力、Opus 4.6から大幅改善、高度SWEで改善顕著 |
| @OpenAI | 7,260 | 614 | Codex for (almost) everything — Macアプリ連携・画像生成（対抗リリース） |

### 注目ポイント
- Anthropic公式告知64K likes到達（Opus 4.6告知時を上回る勢い）
- OpenAI Codexが同日アップデート（Macアプリ操作・画像生成で対抗）
- Opus 4.7の**ビジョン3倍**と**ツール使用エラー33%減**が開発者層で話題
- Opus 4.7は**Mythos Preview（内部強版）から意図的にトーンダウンしたモデル**という分析

---

## 2026-04-17 06:20 JST（セッション外・Gemini Windowsインストール完了）

### 実施内容（X収集ではない運用メモ）
- Windows PC（MASU-P55）に Google App（Gemini）v1.0.2.0 インストール完了
- 既存DL済みインストーラーは `Updater error: 75050 / 0x1252a`（Omaha tag parse `kUnrecognizedName`）で失敗
- `search.google/google-app/desktop` から再DLで解消（埋め込みタグが最新 Omaha 148.0.7730.0 と不一致だった）
- 起動: `C:\Users\gci_admin\AppData\Local\Google\Google\latest\google.exe --start_hidden` → Alt+Space
- **UI 英語固定**: v1.0.2.0（Canary 10% GA）は Assets/html に ja ロケール未同梱。`lang=ja` 指定再インストールも UI は英語のまま（翻訳リソースそのものが未同梱）
- 実用上は「Ask anything」に日本語入力で日本語応答可能

### 次セッション（9:00 JST）で X 収集実施予定

---

## 2026-04-17 09:10 JST（セッション1）

### For Youタイムライン（上位トピック）
- **@OpenAI**: "Codex for (almost) everything." — computer useでMacアプリ操作、gpt-image-1.5画像生成、90以上のプラグイン対応（9,533 likes / 895 RT）
- **@TheAmolAvasare**(Anthropic): "Opus 4.7 is a much more thorough and precise model. It does use more thinking tokens, and our new tokenizer can also create more tokens"（664 likes）
- **@JoshKale**: "Today Perplexity shipped everything Siri was supposed to be" — Perplexity Comet AssistantでiMessage・Macフォルダ全アクセス（477 likes / 24 RT）
- **@Google**: Chrome AI Mode Side-by-Side Browsing 正式展開（1,328 likes / 122 RT）
- **@bridgemindai**: "Claude Code usage just fully reset. Our voices have been heard."（285 likes）

### キーワード検索「Claude Opus 4.7」
| author | likes | 要点 |
|---|---|---|
| @SuguruKun_ai | 103 | ビジョン3倍・指示遵守改善・自己検証・ツールエラー33%減 |
| @bioshok3 | 47 | Mythos Previewより意図的に低能力だが高度SWEで大幅改善 |
| @AI_masaou | 38 | 「賢くなった」ではなく「崩れずに走り切るのが上手くなった」 |
| @claudecode_lab | 35 | 長時間タスク劇的向上、自己検証、最小監督で丸投げ可 |
| @ai_shinobix | 12 | "AIにめっちゃやる行動ベスト3"の改善 |

### 注目ポイント
- **Claude Code usage limit リセット** — 4/16深夜にAnthropicが週次リミット全面リセット（@bridgemindaiほか複数報告）
- **OpenAI Codex computer use** が同日に対抗発表、Macアプリ操作・gpt-image-1.5・プラグイン90+
- **Perplexity Comet** がiMessage/Macファイル統合で Apple Intelligence 代替を狙う動き
- **Opus 4.7のトーン**: 「能力ジャンプ」より「実運用の安定性」でポジショニング、長時間エージェントタスク訴求

### TL上の個別インフルエンサー反応
- @AI_masaou「価格据え置きのまま、自律運用・長文推論・ビジョンが一段強化」
- @hobbydevelop「長く走らせる仕事に最強の一般提供モデル」
- @t_tsuru（苦言）「Claude Codeが人間のフリして"X日かかります"と複雑な実装避けるのが多すぎる」

---

## 2026-04-18 12:04 JST（セッション追加）

### @SuguruKun_ai の video-use 解説スレッド（3連投）

author: すぐる | Chat... (@SuguruKun_ai、認証済)
対象: browser-use チーム製 **Video Use** スキル（https://github.com/browser-use/video-use）

**投稿1（フック）**: 「Claude Codeで動画編集が全自動になるスキルが出た」
- 素材フォルダ → 完成 mp4 自動生成
- フィラー・無音自動カット、字幕焼き込み、シーン別カラーグレード、カット境目の音割れ防止フェード、Manim/Remotion/PIL アニメ挿入
- 100% OSS・無料

**投稿2（仕組み）**: 「映像を見る前に全部テキスト化する」
1. 素材投入
2. ElevenLabs（Scribe）が音声を単語単位タイムスタンプ付きでテキスト化
3. AI が文章として読んで「ここカット」「ここに字幕」と判断
4. 必要最低限のみサムネイルで映像確認
5. final.mp4 書き出し
- 秒ではなく「単語」単位で精度、`project.md` でセッション跨ぎの再開可

**投稿3（インストール＋思想）**:
```
git clone github.com/browser-use/video-use
ln -s "$(pwd)" ~/.claude/skills/video-use
pip install -e .
```
- ElevenLabs API キー投入 → Claude Code で「動画編集して」と言うだけ
- 「ソフトの操作」→「AI への会話」へのパラダイムシフト
- `~/.claude/skills/` 配下へのシンボリックリンクで他プロジェクトからも呼び出せる

### 自分の実体験との突合（4/17 導入済）
- 記述はほぼ CLAUDE.md の導入メモと一致
- **スレッドで抜けている注意点**: `git clone` 直後に `cd video-use` が必要（でないと `$(pwd)` が親ディレクトリを指す）
- venv 利用が無難（Python 3.12 で `pip install -e .` 実施済）
- takes_packed.md (~12KB 圧縮) / timeline_view PNG / 自己評価ループ最大3回、までは @SuguruKun_ai 投稿では触れられていない

### 読み解き
- Opus 4.7 + 長時間エージェント運用の文脈で「編集者不要化」が次の話題に
- @SuguruKun_ai はここ連続で AI ツール紹介スレッドを伸ばしているアカウント（前回 Opus 4.7 の要点まとめで 103 likes）
- 今回のスレッドも類似の伸びが想定され、video-use 注目のきっかけになる可能性

---
