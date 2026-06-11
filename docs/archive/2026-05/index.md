# 2026-05 月次アーカイブ index

> CLAUDE.md「最近 2 週間」から退役したサマリー（2026-06-12 ダイエット時に作成）。
> 5/16〜5/30 はダイエット前の CLAUDE.md に未掲載だったため、ジャーナルから要約を起こして補完。
> ジャーナル本体はすべて @docs/journal/ に残存。

- **2026-05-30** (土): X 投稿の解決 2 件（M5 MacBook Air Wi-Fi 診断 / Windows 版 Codex の Computer Use 解禁）→ AI CLI 3 種を全 3 台で最新化 + **Codex Desktop = MSIX 経由と判明、しゅん先生 PC で Windows Computer Use 有効化成功**（真因 = `~/.codex/config.toml` の読み取り専用属性）。途中 SSH からの削除→再インストールで半壊状態を作り再起動 + Store GUI で復旧（@docs/journal/2026-05-30.md）
- **2026-05-26** (火): Mac Android Emulator 最新 AVD（Android 16 / API 36 / arm64）を `launchctl submit` 経由で起動確認（@docs/journal/2026-05-26.md）
- **2026-05-25** (日): 3 台の CLI 3 種アップデート。**Windows codex を 0.133.0 に誤更新 → 5/20 の「0.130.0 ピン留め」判断の見落としに気づき差し戻し復旧**。教訓 = 更新前に直近ジャーナルの意図的判断を確認（@docs/journal/2026-05-25.md）
- **2026-05-20** (水): **masu-p55 の Codex remote-control 自動復旧体制構築**（`C:\ProgramData\codex-watchdog\`、SYSTEM 権限 3 分間隔監視）+ **Codex 0.131 の Windows 退行発見 → 0.130.0 ピン留め確定** + Claude Code 全機 2.1.145 + iPhone Codex App の Windows 機能制限切り分け（@docs/journal/2026-05-20.md）
- **2026-05-16** (土): メモリ整理 + 3 台ツール最新化（claude 2.1.142 / codex 0.130.0）+ **ツイキャス有料アーカイブを Mac Brave 経由 DL + 3.5h 文字起こし**（codex の Mac 救援）+ 奥山俊宏×松本創対談から「集団浅慮」発掘 → X 投稿（@docs/journal/2026-05-16.md）
- **2026-05-12** (火): **🎉 Reco.app の Ollama 隠れ依存を mock サーバで完全突破**（Python 110 行 LaunchAgent `com.yuika.reco-ollama-mock`、本物 Ollama 4.6 GB を 99.8% 置換、オンボーディング 3 段全突破）+ **macOS launchd TCC 罠**（`~/Desktop` 読めず → `~/Library/Application Support/` 経由で回避）+ WhisperKit CoreML → ANE 変換知見 + 推測ミス訂正 2 件（@docs/journal/2026-05-12.md）
- **2026-05-08** (金): Codex 環境 3 機 0.129.0 統一 + SuperWhisper Mac 初設置 + 引き継ぎ書 4 部作完成 + **GitHub PAT rotate を「物・お金・デジタル 3 軸チェック」で「放置」と決断**（体験報告書コア理論のリアルタイム自己適用）（@docs/journal/2026-05-08.md）
- **2026-05-07** (木): **🚨 マックスプラン 5/8 解約予告受信 → Claude Code → Codex 完全引き継ぎ書作成**（AGENTS.md = CLAUDE.md symlink 確立）+ ミニマリストしぶ chibi pet 完成（Codex image_gen）+ codex MCP 登録 + VNC 有効化 + 「仲家 → 仲氏」呼称統一（5 ファイル 69 箇所）（@docs/journal/2026-05-07.md）
- **2026-05-06** (水・振替休日): Word 体験報告書 4 件修正完了（P3/P4/P5/P9）+ Claude Code 全 3 台 2.1.128→2.1.129 統一 + microsoft/edit v2.0.0 全 3 台 + Windows 11 26H1 = ARM 専用判明 + masu-p55 LAN SSH 経路確立 + カイル発見 + 黒田蒲鉾の真相 + なかそにー IG 分析（ミニマムライフコスト 3 者比較）+ Codex CLI 引き継ぎ第一弾 + 勝間 voice stack 確証（Windows ゲーミングノート、Mac 不使用）+ Noto/Pretendard JP デフォルト化 + npm localhost:1 ガード 3 台統一（@docs/journal/2026-05-06.md）
- **2026-05-04** (月・みどりの日): **国民年金 令和 7 年度免除申請完了**（03:53 マイナポータル、5 種類全チェック）+ **整理収納 1 級 体験報告書 Artifact 図表 10 個全完成**（A 評価 90 点+）+ 構成案 docs 新規作成 + 戦略確定（タイトル C / 提案編 / AI 概念のみ / ブランド名伏せ）+ AI 系 X 投稿 7+ 件ファクトチェック + フィッシング識別 4 通目 + 家族構成 context 修正（@docs/journal/2026-05-04.md）
- **2026-05-03** (土): しぶ動画 TRr6gtjHECM 分析 → **八木仁平 = しぶエコ「源流」レイヤー発見** + Joy-Con 2 Phase 3 実機検証 → 断念 + エディオン西代で Maxell BD-RE DL 購入（はばタンPay+）+ Gopher360 でコントローラマウス化 + VLC 導入（@docs/journal/2026-05-03.md）
- **2026-05-02** (金): agent-browser supervisor の罠解明（close --all では死なない）+ 司令塔モード維持原則確定 + sniffnet/Wireshark 環境構築（@docs/journal/2026-05-02.md）
- **2026-05-01**: NVMe クローン死闘記事の Substack 本編はボツ決定（Notes 完結）

関連: しぶコーチング応募は締切 5/6 23:59 を**超過**（5/7 ジャーナルに記録、失効扱い）。
