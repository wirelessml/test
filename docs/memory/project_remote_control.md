---
name: Remote control status report
description: 毎時スクリーンショット+Gmail下書き+git pushのcronジョブによるリモートコントロール状態報告の仕組み
type: project
---

リモートコントロール状態報告: 毎時33分にスクリーンショット撮影 → log.json更新 → Gmail下書き作成 → git commit & pushを行うcronジョブ。

**Why:** ユーザーが外出中でもMacの状態を確認できるようにするため。セッション切断によるタイムアウト対策も兼ねる。

**How to apply:** 新しいセッション開始時にcronジョブの再設定が必要（セッション限りのため）。screencaptureコマンドを使用（computer-useのスクリーンショットはCursorがフィルタされるため不可）。スクリーンショットは ~/Desktop/screenshots/ に保存、GitHub Pagesで閲覧可能（wirelessml.github.io/test/）。
