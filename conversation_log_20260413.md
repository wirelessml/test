# 2026-04-13 作業記録: Mac メンテナンス & OBS導入

## 実施内容

### 1. Mac負荷調査・解消
- **問題**: ロードアベレージ 5.16（M1 8GBとしては異常に高い）
- **原因**: ffmpegプロセスが5つ同時にYouTube Liveへ配信していた
  - PID 2792: testsrc → rtmp (CPU 94.4%, 324分稼働)
  - PID 2729: testsrc → rtmp (CPU 89.3%, 318分稼働)
  - PID 2589, 2618, 2677: avfoundation → rtmp
- **対応**: 全ffmpegプロセスを停止（kill → killall → kill -9）
- **結果**: ロードアベレージ 5.16 → 1.31 に改善

### 2. OBS Studio インストール
- **バージョン**: 32.1.1 (Apple Silicon版)
- **方法**: GitHub Releasesからdmgをダウンロード → /Applicationsにコピー
- **理由**: ffmpegでのYouTube Live配信はプロセス管理が困難で孤児プロセスが溜まりやすい

### 3. OBS配信設定作成
- **プロファイル「YouTube Live」を作成**:
  - 映像: 1280x720 / 30fps
  - エンコーダ: Apple VideoToolbox (M1ハードウェアエンコード)
  - ビットレート: 2500kbps映像 / 128kbps音声
  - 配信先: rtmp://a.rtmp.youtube.com/live2
- **シーン「YouTube配信」を作成**:
  - FaceTime HDカメラ (EAB7A68F-EC2B-4487-AADF-D8A91C1CB782)
  - マイク (デフォルト)
  - デスクトップ音声 (デフォルト)

### 4. macOS権限設定
- **カメラ権限**: ユーザーTCCデータベースに直接書き込み → 許可済み
- **マイク権限**: 同上 → 許可済み
- **画面収録権限**: システムTCCデータベースはSIP保護で書き込み不可 → GUI操作が必要

### 5. Claude CLI確認
- **場所**: /Users/yuika/.local/bin/claude (v2.1.104)
- **SSH経由での実行方法**: `zsh -i -c "claude ..."` (PATHを通すため)
- **ログイン**: 未認証（`claude -p` で確認）
- **/remote-control**: Mac側のClaude CLIでは利用不可

## 未完了事項
- [ ] OBS初回セットアップウィザードの完了（Mac側でGUI操作が必要）
- [ ] 画面収録権限の許可（システム環境設定 → プライバシー → 画面収録）
- [ ] OBSにYouTubeストリームキーを設定
- [ ] Claude CLIのログイン
- [ ] 画面共有（VNC）の有効化（任意）

## 技術メモ
- SSH経由のシェル (paramiko exec_command) はPATHが最小限 (/usr/bin:/bin:/usr/sbin:/sbin)
- .zshrcのカスタムPATHはログインシェルでは読まれない → `zsh -i -c` で解決
- macOSのAppleEventはSSHセッションからGUIにアクセスできない（-1712タイムアウト）
- ユーザーレベルTCC.dbはSIP有効でも書き込み可能、システムレベルは不可
