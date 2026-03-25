# 学校プリントHTML化 ナレッジベース

## 概要
神戸市立板宿小学校の学校プリント（おたより）をHTMLに変換し、PNGで出力するワークフロー。

## 学校情報
- **学校名**: 神戸市立板宿小学校
- **電話番号**: ７３２−４０５５
- **用紙サイズ**: A4（210mm × 297mm）

## ワークフロー

### 1. 入力
- 元のプリントの画像（写真・スキャン・スクリーンショット）
- または、テキスト内容の直接入力

### 2. HTML作成
- `templates/school-newsletter-template.html` をベースに作成
- `{{プレースホルダー}}` を実際の内容に置換
- 不要なセクションは削除、必要に応じてセクション追加

### 3. PNG出力（Playwright使用）
```python
from playwright.sync_api import sync_playwright
import os

html_path = os.path.abspath('出力ファイル名.html')
output_path = os.path.abspath('出力ファイル名.png')

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path='/root/.cache/ms-playwright/chromium-1194/chrome-linux/chrome'
    )
    page = browser.new_page(viewport={'width': 794, 'height': 1123})
    page.goto(f'file://{html_path}')
    page.wait_for_load_state('networkidle')
    height = page.evaluate('document.body.scrollHeight')
    page.set_viewport_size({'width': 794, 'height': height + 40})
    page.screenshot(path=output_path, full_page=True)
    browser.close()
```

### 4. 確認・修正
- 生成されたPNGを目視確認
- 修正が必要な場合はHTMLを編集して再生成

## デザインルール

### フォント
- **本文**: Yu Mincho（明朝体）- 学校プリントの標準
- **強調・赤字**: Yu Gothic（ゴシック体）
- **英字タイトル**: Arial / Helvetica

### よく使うCSSクラス一覧

| クラス名 | 用途 | 見た目 |
|---|---|---|
| `.header` | ヘッダー全体 | 左にタイトル、右に学校情報 |
| `.header-title` | プリントタイトル | 黒枠囲み、大文字 |
| `.section-title` | セクション見出し | ☆マーク付き太字 |
| `.underline-title` | サブ見出し | 下線付き中央寄せ |
| `.red-text` | 赤字強調 | 赤色ゴシック体 |
| `.notice-box` | 囲み注記 | 黒枠ボックス |
| `.item-list` | 持ち物リスト等 | ○マーク付き |
| `.numbered-list` | 番号付きリスト | 1. 2. 3. |
| `.schedule-table` | 予定表 | 罫線付きテーブル |
| `.footer-notes` | フッター注釈 | ★マーク付き小文字 |
| `.intro` | 前文段落 | 字下げあり |
| `.flex-section` | 横並びレイアウト | Flexbox |

### 文字サイズ
- 本文: 14px
- 見出し: 16px
- 赤字強調: 18px
- タイトル: 32px
- テーブル・フッター: 13px

### 行間
- 標準: 1.8（日本語に最適）

## プリントの種類別テンプレート構成

### 長期休み号（春休み・夏休み・冬休み）
1. ヘッダー（タイトル + 学校名 + 日付 + 号名）
2. 前文（学期の振り返り + 次学期への期待）
3. 休み中の学習について
4. 持ち物の整理
5. 新学期の予定（テーブル）
6. フッター注釈

### 学期始め号
1. ヘッダー
2. 前文（新学期の挨拶）
3. 時間割
4. 持ち物リスト
5. 今月の予定（テーブル）
6. お知らせ・連絡事項

### 月間予定表
1. ヘッダー
2. カレンダー形式テーブル
3. お知らせ事項
4. フッター

## 注意事項
- 全角数字を使用（１２３ではなく123は避ける）
- 句読点は「、」「。」を使用
- 中黒「・」で項目を区切る
- インデントには全角スペース「　」を使用
- GitHub画像キャッシュに注意（ファイル名変更で回避可能）

## ファイル命名規則
- HTML: `{内容}-{学年}.html`（例: `spring-break-3rd-grade.html`）
- PNG: `{内容}-{学年}.png`（例: `spring-break-3rd-grade.png`）
- 季節: spring-break, summer-break, winter-break
- 月間: monthly-{月}-{学年}（例: `monthly-april-4th-grade.html`）
