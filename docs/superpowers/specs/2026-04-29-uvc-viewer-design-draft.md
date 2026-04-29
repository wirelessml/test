# GC313Pro UVC ビューワ — 設計ドラフト (保留中)

> Status: **DRAFT — 物理セットアップ後に最終決定**
> 作成: 2026-04-29 18:50 JST
> 確定予定: 2026-04-30 (物理セットアップ実機確認後)
> 関連: @docs/journal/2026-04-29.md (今日の追補で経緯を記録)

## 経緯サマリー

仲さんから「OBS のようなアプリを作ってくれますか?」要請 → 「ミニマリストらしくシンプルに」絞り込み → **「Mac M1 (内蔵モニタ壊れ) の画面を Windows しゅん先生 PC のモニタに映す」** が真の用途と判明 → 既存ツール (Deskreen など) では「GC313Pro を買った意味がない」 → **GC313Pro 経由のハードウェア構成 + Windows 側 UVC ビューワ** という方向性に到達。

## 確定済み要件

- **目的**: Mac M1 の HDMI 出力を GC313Pro でキャプチャし、Windows しゅん先生 PC の LG モニタにビューワで表示
- **トポロジ**: Mac → GC313Pro → Windows しゅん先生 PC → LG モニタ (1 モニタで Mac/Windows 両方視認)
- **Mac 用途**: Claude Code でターミナル作業中心 (50-100ms 遅延許容範囲、Q10.A)
- **OBS 不採用**: 過去の M1 8GB での使用経験で重く、避けたい
- **YouTube Live は別フロー**: YouTube Studio Web (Chrome) で対応、本アプリのスコープ外
- **実装言語候補**: Python + opencv-python (Q6.A 候補、ただし B/C/D も再検討余地あり)
- **想定行数**: 30-50 行
- **画面モード**: フルスクリーン or ウィンドウ、F キーで切替予定 (Q11 未確定)

## 想定コードスケルトン (草案、変更余地あり)

```python
# viewer.py — GC313Pro UVC fullscreen viewer (草案)
import cv2, sys, os

DEVICE_INDEX = int(os.environ.get("UVC_INDEX", "0"))
WIDTH, HEIGHT = 1920, 1080

cap = cv2.VideoCapture(DEVICE_INDEX, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YUY2'))

if not cap.isOpened():
    sys.exit(f"GC313Pro が開けません (index={DEVICE_INDEX})")

cv2.namedWindow("Mac via GC313Pro", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Mac via GC313Pro", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
fullscreen = True

while True:
    ok, frame = cap.read()
    if not ok: break
    cv2.imshow("Mac via GC313Pro", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == 27: break  # ESC
    if key == ord('f'):  # F でモード切替
        fullscreen = not fullscreen
        cv2.setWindowProperty(
            "Mac via GC313Pro", cv2.WND_PROP_FULLSCREEN,
            cv2.WINDOW_FULLSCREEN if fullscreen else cv2.WINDOW_NORMAL
        )

cap.release()
cv2.destroyAllWindows()
```

## 物理セットアップ確認待ち事項 (4/30 に解明)

| 項目 | 不明点 | 解明手段 |
|---|---|---|
| **Mac → GC313Pro のケーブル** | USB-C → HDMI 変換ケーブル 1 本で済むか / アダプタ + HDMI ケーブル 2 つ要るか / 既に持ってる物で行けるか | Mac の USB-C ポートに何が挿せるか実機確認 |
| **GC313Pro → Windows のケーブル** | USB-C → USB-C で SS 5Gbps 対応のケーブルが手元にあるか | 物理確認 |
| **GC313Pro が Windows で UVC として認識されるか** | 公式仕様上は OK だが、Windows しゅん先生 PC の USB-C ポートで実動作確認要 | 接続後デバイスマネージャーで確認 |
| **Python が Windows しゅん先生 PC に入っているか** | `python --version` で確認 | コマンドプロンプトで実行 |
| **opencv-python が CAP_DSHOW で GC313Pro 開けるか** | デバイス index 自動検出 / 環境変数指定どちらが現実的か | 実機テスト |
| **解像度 1920×1080@60fps が出るか** | GC313Pro の YUY2 60fps が Windows しゅん先生 PC で安定するか | 実測 |
| **遅延が実用範囲か** | 50-100ms 想定、実測で確認 | Mac でカウンタ表示 → モニタで時差目視 |

## ブレスト中に出た保留問題

### Q11 (画面モード) — 物理確認後に確定
- A. フルスクリーン専用
- B. ウィンドウモード専用
- C. 両方切替 (推奨案、F キー)

### Q12 (ケーブル形態) — 物理確認後に確定
- A. USB-C → HDMI 変換ケーブル使う (現状の推測)
- B. USB-C → USB-C 直結を期待 (GC313Pro 仕様上は不可だが要再確認)
- C. 取説確認待ち
- D. 機種変更 (GC313Pro → 別キャプチャ)

### スコープ外確定済み (今後追加しない)
- 録画機能 (将来 Q13 で再検討)
- RTMP 配信機能 (YouTube Studio Web で代替)
- GUI (デバイス選択ドロップダウン等)
- 自動起動・タスクトレイ常駐
- ログファイル出力

## 候補実装パターン (Q6 で提示済、未確定)

| 候補 | 行数 | 依存 | 状況 |
|---|---|---|---|
| **A. Python + OpenCV** | 30-40 行 | Python + opencv-python | 推奨候補 |
| **B. PowerShell + ffplay** | 3-5 行 | ffmpeg バイナリ | 究極のミニマル、Windows 専用 |
| **C. HTML + getUserMedia** | 15-30 行 | ブラウザのみ | 起動が「1 ボタン」感に欠ける |

## 明日のアクション

1. 物理セットアップ実施 (Mac → GC313Pro → Windows → LG モニタ)
2. Q12 (ケーブル形態) の確定
3. Windows しゅん先生 PC で GC313Pro が UVC として認識されるか確認
4. Python の有無確認 + opencv-python install
5. 遅延の実測
6. これらを踏まえて Q11 (画面モード) と最終実装案 (A/B/C) を決定
7. このドラフトを正式 spec (`2026-04-29-uvc-viewer-design.md`) に昇格 → writing-plans → 実装

## ステータス

- [x] ブレスト Q1-Q11 実施
- [x] 草案コードスケルトン作成
- [x] ドラフト保存 (このファイル)
- [ ] 物理セットアップ (4/30 予定)
- [ ] 最終要件確定
- [ ] 正式 spec 化
- [ ] 実装計画 (writing-plans)
- [ ] 実装 (Python OpenCV 想定 30-50 行)
