# Google Photos MCP セットアップ手順

## 準備済み
- [x] google-photos-mcp clone済み（~/Desktop/google-photos-mcp/）
- [x] npm install + build 完了
- [x] .env テンプレート準備済み
- [x] gcloud CLI インストール済み

## 次回Mac前で実行する手順（10分で完了）

### Step 1: Google Cloud Console でプロジェクト作成
1. ブラウザで https://console.cloud.google.com/ を開く
2. wirelessml@gmail.com でログイン
3. 「新しいプロジェクト」→ 名前: `google-photos-mcp`
4. プロジェクトを選択

### Step 2: Photos Library API を有効化
1. 左メニュー → APIとサービス → ライブラリ
2. 「Photos Library API」を検索
3. 「有効にする」をクリック

### Step 3: OAuth同意画面を設定
1. APIとサービス → OAuth同意画面
2. User Type: 「外部」
3. アプリ名: `google-photos-mcp`
4. ユーザーサポートメール: wirelessml@gmail.com
5. スコープ: `https://www.googleapis.com/auth/photoslibrary.readonly`
6. テストユーザー: wirelessml@gmail.com を追加

### Step 4: OAuth認証情報を作成
1. APIとサービス → 認証情報
2. 「認証情報を作成」→ OAuth クライアント ID
3. アプリケーションの種類: Webアプリケーション
4. 名前: `google-photos-mcp`
5. 承認済みのリダイレクトURI: `http://localhost:3000/auth/callback`
6. 作成 → Client ID と Client Secret をメモ

### Step 5: .env を設定
```bash
cd ~/Desktop/google-photos-mcp
nano .env
# GOOGLE_CLIENT_ID=取得したID
# GOOGLE_CLIENT_SECRET=取得したSecret
```

### Step 6: 認証実行
```bash
cd ~/Desktop/google-photos-mcp
npm start
# ブラウザで http://localhost:3000/auth を開く
# Googleアカウントで認証
```

### Step 7: Claude Code に追加
```bash
claude mcp add google-photos -- node ~/Desktop/google-photos-mcp/dist/index.js --stdio
```

### Step 8: 動作確認
Claude Code で「Google Photosの最近の写真を見せて」と聞く
