## 運用ルーチン（タスク管理との二層構造）

- **CLAUDE.md = マスター**（Single Source of Truth、永続、git管理、次セッション以降も継続）
- **タスク管理システム = セッション作業ビュー**（進行状況、依存関係、セッションローカル）
- フロー: 新タスク発生 → CLAUDE.md追記 + TaskCreate / 進行 → TaskUpdate / 完了 → CLAUDE.md「完了」セクション移動 + git commit

