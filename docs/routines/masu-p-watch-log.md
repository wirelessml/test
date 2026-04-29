# MASU-p 毎日監視ログ

> 対象 1: https://masu-p.com/ (神戸市須磨区板宿コワーキング公式サイト)
> 対象 2: https://www.instagram.com/masup_official/ (Instagram 公式)
> 実行: LaunchAgent `com.yuika.masu-p-watch` (毎日 18:12 JST)
> スクリプト: `/Users/yuika/Desktop/scripts/masu-p-watch.sh`
> スナップショット: `docs/routines/masu-p-snapshots/`

監視ロジック:
- `masu-p.com` の `<body>` ハッシュが変わったら CHANGED
- Instagram は `og:description` + 最新投稿画像 URL key の組合せハッシュで判定
- 変化があった場合 HTML スナップショットを `masu-p-snapshots/` に保存して残す


## 2026-04-29 18:12:22 JST

- Web: baseline (size: 121168, hash: ab227cd001b6…)
  - 見出し抜粋:
    - About
    - Service
    - アクセスACCESS
- Instagram: baseline (size: 935571, hash: 5d3a6e5b31e3…)
  - og:description: &#x30d5;&#x30a9;&#x30ed;&#x30ef;&#x30fc;141&#x4eba;&#x3001;&#x30d5;&#x30a9;&#x30ed;&#x30fc;&#x4e2d;101&#x4eba;&#x3001;&#x6295;&#x7a3f;75&#x4ef6; &#x2015; MASU-p(&#x30de;&#x30b9;&#x30d4;&#x30fc;) | &#x5175;&#x5eab;&#x770c;&#x795e;&#x6238;&#x5e02;&#x9808;&#x78e8;&#x306e;&#x30b3;&#x30ef;&#x30fc;&#x30ad;&#x30f3;&#x30b0;&#x30b9;&#x30da;&#x30fc;&#x30b9;&amp;&#x30ec;&#x30f3;&#x30bf;&#x30eb;&#x30b9;&#x30da;&#x30fc;&#x30b9;&#x3055;&#x3093;(&#064;masup_official)&#x306e;Instagram&#x306e;&#x5199;&#x771f;&#x3068;&#x52d5;&#x753b;&#x3092;&#x30c1;&#x30a7;&#x30c3;&#x30af;&#x3057;&#x3088;&#x3046;
  - 最新投稿画像 key: 318546223_3304576813202385_8800960017401097906_n

## 2026-04-29 18:12:30 JST

- Web: unchanged (size: 121168, hash: ab227cd001b6…)
- Instagram: unchanged (size: 935594, hash: 5d3a6e5b31e3…)
