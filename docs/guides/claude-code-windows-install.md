# Claude Code CLI を Windows にインストールする手順書

> 作成: 2026-04-25（しゅん先生 PC 実機検証）
> 対象 OS: Windows 11 (Build 26300.8276 GE Prerelease, Insider Preview)
> 検証バージョン: Claude Code 2.1.119
> 所要時間: 15-20 分（Node.js + Git for Windows 既インストールなら 5 分）
> 結論: **Mac 版とは違って 2 つの "見えない罠" を踏む。事前に潰しておくと迷わない**

## TL;DR

```powershell
# 1. Node.js (LTS 22.x)
winget install OpenJS.NodeJS.LTS

# 2. PowerShell 実行ポリシー変更（罠 1 対策）
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force

# 3. Claude Code インストール
npm install -g @anthropic-ai/claude-code

# 4. Git for Windows (罠 2 対策、git-bash が必要)
winget install --id Git.Git -e --source winget

# 5. PowerShell 再起動 → 認証
claude
```

---

## なぜこの手順書が必要か

Mac で `npm install -g @anthropic-ai/claude-code` した経験があると、Windows でも同じノリで進めようとしてハマる罠が **2 つ** ある:

| 罠 | エラー文面 | 対策 |
|---|---|---|
| **罠 1: PowerShell 実行ポリシー** | `npm.ps1 を読み込むことができません` `PSSecurityException` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| **罠 2: git-bash 必須（Windows 版固有）** | `Claude Code on Windows requires git-bash` | Git for Windows をインストール |

両方とも事前に潰しておけば、実質 5 分で導入完了する。

---

## 前提条件

- [ ] Windows 10/11 (検証は Windows 11 Insider Preview 26300)
- [ ] **管理者権限の PowerShell**
- [ ] インターネット接続
- [ ] Anthropic アカウント（Claude.ai Pro / Max / Team / Enterprise いずれか、または Console API キー）
- [ ] 約 500 MB のディスク空き（Node.js + Git + npm modules 合計）

---

## Phase 1: Node.js インストール（5 分）

Claude Code は npm 経由で配布されるため Node.js が必要。

### 1-1. 既存確認

```powershell
node --version
npm --version
```

→ どちらもバージョン番号が出れば OK、Phase 2 へ。

### 1-2. インストール（未導入の場合）

**winget が一番速い**:

```powershell
winget install OpenJS.NodeJS.LTS
```

GUI 派は公式インストーラ:
- https://nodejs.org/ja/download → **LTS (22.x) Windows Installer (.msi) 64-bit**
- ダウンロード → 実行 → Next 連打（デフォルトで OK、PATH 自動追加にチェック）

### 1-3. PowerShell を閉じて開き直す

PATH 反映のため必須。

### 1-4. 確認

```powershell
node --version    # → v22.x.x
npm --version     # → 11.x.x（Node.js 22 同梱）
```

---

## Phase 2: PowerShell 実行ポリシー変更（罠 1 対策、1 分）

### 問題の正体

Windows PowerShell はデフォルトで `Restricted` 実行ポリシー（`.ps1` スクリプト実行禁止）。`npm` コマンドの実体は `C:\Program Files\nodejs\npm.ps1` なので、デフォルト状態だと:

```
npm : このシステムではスクリプトの実行が無効になっているため、
      ファイル C:\Program Files\nodejs\npm.ps1 を読み込むことができません。
```

このエラーで詰まる。

### 対策

**現在のユーザースコープで RemoteSigned に変更**（システム全体は触らない、安全）:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
```

確認:

```powershell
Get-ExecutionPolicy -List
```

→ `CurrentUser` が `RemoteSigned` になっていれば OK。

#### RemoteSigned の意味

- ローカルで作った .ps1 → 実行可
- ネットからダウンロードした .ps1 → 署名必須
- npm.ps1 はインストール時に作られたローカルファイルなので実行可になる

#### システム全体ポリシーが GroupPolicy で固定されている場合

会社支給 PC など稀なケース。この場合は代替策:

```powershell
# (A) npm.cmd を直接呼ぶ（.cmd は実行ポリシー対象外）
npm.cmd install -g @anthropic-ai/claude-code

# (B) cmd.exe 経由
cmd /c "npm install -g @anthropic-ai/claude-code"

# (C) Bypass で 1 セッションだけ許可
powershell -ExecutionPolicy Bypass -Command "npm install -g @anthropic-ai/claude-code"
```

---

## Phase 3: Claude Code インストール（2 分）

```powershell
npm install -g @anthropic-ai/claude-code
```

→ **`added 2 packages in 20s`** 程度の出力で成功。

確認:

```powershell
claude --version
# → 2.1.119 (Claude Code) など
```

---

## Phase 4: Git for Windows インストール（罠 2 対策、5 分）

### 問題の正体

`claude --version` は通るが、`claude` を実行すると:

```
Claude Code on Windows requires git-bash (https://git-scm.com/downloads/win).
If installed but not in PATH, set environment variable pointing to your bash.exe,
similar to: CLAUDE_CODE_GIT_BASH_PATH=C:\Program Files\Git\bin\bash.exe
```

Claude Code on Windows は内部的に **bash 環境**を要求している。WSL ではなく Git for Windows 同梱の **git-bash** を使う設計。

### インストール

**winget が最速**:

```powershell
winget install --id Git.Git -e --source winget
```

または公式インストーラ:
- https://git-scm.com/downloads/win → 「64-bit Git for Windows Setup」
- インストーラ実行、ほぼデフォルトで OK

#### インストーラで 1 つだけ注意するページ

「Adjusting your PATH environment」画面:
- ✅ **Git from the command line and also from 3rd-party software**（真ん中、デフォルト推奨）

これを選ぶと `git`、`bash`、`ssh` 等が PATH に通る。

### PowerShell を閉じて開き直す

PATH 反映のため必須。

### 確認

```powershell
git --version
# → git version 2.x.x.windows.1

where.exe bash
# → C:\Program Files\Git\bin\bash.exe
```

### PATH に通らなかった場合（手動環境変数設定）

```powershell
# 永続化（ユーザースコープ）
[Environment]::SetEnvironmentVariable(
    "CLAUDE_CODE_GIT_BASH_PATH",
    "C:\Program Files\Git\bin\bash.exe",
    "User"
)
```

→ PowerShell 再起動して `claude` 実行。

---

## Phase 5: 認証（3 分）

```powershell
claude
```

初回起動の流れ:

1. ブラウザが自動で開く（claude.ai のログインページ）
2. **Mac で使ってるアカウントと同じ Anthropic アカウント**でログイン
   - Pro / Max プランで Mac と Windows 両方で使える（ただし枠は共有）
3. 「Allow Claude Code to access your account」みたいなボタンを押す
4. PowerShell に戻ると認証完了の表示
5. `Welcome back <名前>!` が出れば成功

### 確認できる情報

- **アカウント名**（claude.ai のユーザー名、例: 仲啓輔）
- **モデル**（Opus 4.7 / Sonnet 4.6 / Haiku 4.5、プラン次第）
- **コンテキスト長**（Pro: 200K、Max: 1M）
- **Organization**（個人 or Team）
- **作業ディレクトリ**

### 同時利用について

同じアカウントで Mac と Windows 同時起動 OK。ただし:
- **5 時間枠 / 週次枠は共有**（Mac で消費すると Windows でも減る）
- **同時セッション数の制限**は特になし（観測上）
- **会話は独立**（Mac セッションと Windows セッションは別物）

---

## Phase 6: 推奨初期設定（任意、5 分）

### 6-1. dangerously-skip-permissions で起動するエイリアス

毎回 `--dangerously-skip-permissions` 付けるのが面倒なので:

```powershell
# PowerShell プロファイルに追記
notepad $PROFILE

# 中身:
function claudei { claude --dangerously-skip-permissions @args }
Set-Alias -Name c -Value claudei
```

→ 以降 `c` で起動できる。

### 6-2. opusplan モデル設定

Claude プロンプト内で:

```
/model opusplan
```

→ 思考 = Opus、実行 = Sonnet の自動切り替え。コスパ最高。

### 6-3. デフォルトモデル設定

`/model` コマンドで Opus 4.7 (1M context) max effort 等を選択。設定は永続化される。

### 6-4. リモートコントロール接続

Mac セッションと同じ運用にするなら `/remote-control` を実行。

---

## トラブルシューティング

### Q. `npm install` で長時間止まる

ファイアウォール・プロキシ・antivirus の干渉。とりあえず:
```powershell
npm install -g @anthropic-ai/claude-code --verbose
```
で詳細ログ確認。registry 接続できないなら社内プロキシ設定:
```powershell
npm config set proxy http://proxy.example.com:8080
npm config set https-proxy http://proxy.example.com:8080
```

### Q. `claude` 起動時に「No module found」

Node.js バージョンが古い可能性。LTS 18 以下だと NG。22.x を使う。

### Q. ブラウザ認証が無限ループする

- ブラウザのキャッシュクリア
- 別ブラウザで試す（Brave → Edge 等）
- claude.ai を一度ログアウト → 再ログイン

### Q. `claude` 起動するが日本語入力できない

PowerShell の入力モード問題。Windows Terminal を使う or 一時的に半角英数モードで入力。

### Q. 既存セッションを引き継ぎたい

Mac セッションと Windows セッションは独立。引き継ぎ機能は無い（2026-04 時点）。代わりに:
- 重要情報は CLAUDE.md / docs/ に書き出して git で同期
- claude-mem の観察記録経由でメモリ共有

---

## 比較: Mac インストールとの違い

| 項目 | Mac | Windows |
|---|---|---|
| パッケージマネージャ | npm or Homebrew | npm (winget で Node.js) |
| 実行ポリシー設定 | 不要 | **必要（PowerShell の罠）** |
| bash 環境 | OS 標準 | **Git for Windows 必須** |
| PATH 設定 | 自動 | Node/Git インストーラで自動 |
| 認証 | ブラウザ起動 | ブラウザ起動（同じ） |
| アップデート | `npm update -g @anthropic-ai/claude-code` | 同上 |

→ Windows 固有の罠 2 つ（実行ポリシー + git-bash）さえクリアすれば、あとは Mac と同じ。

---

## 関連リンク

- [Claude Code 公式ドキュメント](https://docs.claude.com/claude-code)
- [Node.js LTS ダウンロード](https://nodejs.org/ja/download)
- [Git for Windows 公式](https://git-scm.com/downloads/win)
- [PowerShell 実行ポリシーの詳細](https://learn.microsoft.com/ja-jp/powershell/module/microsoft.powershell.core/about/about_execution_policies)

## 関連ファイル

- @docs/journal/2026-04-25.md（しゅん先生 PC への Claude Code 導入記録）
- @docs/machines/shun-sensei-pc.md（マシン詳細、要更新）
- @CLAUDE.md（運用ルール本体）

## 変更履歴

- 2026-04-25: 初版（しゅん先生 PC 実機検証、維新の嵐ゲームトラブル解決のため Claude Code を Windows に導入する文脈で作成）
