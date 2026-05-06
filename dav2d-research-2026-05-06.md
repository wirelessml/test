# dav2d 調査メモ

## 1. 概要

dav2d は、VideoLAN が公開した AV2 向けのオープンソース CPU デコーダ。AV1 における dav1d の役割を、次世代コーデック AV2 で再現しようとしている。開発主体は VLC で知られる VideoLAN。「ハードウェアデコーダが普及するまで、現実的に再生できる速いソフトウェアデコーダを用意する」ための先行実装である。

## 2. 現在のステータス

公開版は dav2d 0.0.1 “Merbanan”。Linuxiac は Jean-Baptiste Kempf が用意した「very early preview release」と紹介し、Arch Linux でも 2026-05-03 に入った。もう配布物として見えるが、API / ABI を固定前提で使う段階ではない。

実装面では、C デコーダの完成、使える API、主要プラットフォーム移植が進行中。assembly 最適化はこれからで、AVX2、SSSE3+、ARMv8、ARMv7、RISC-V、PPC、AVX-512、threading 改善などが並ぶ。Phoronix には “battle-tested and production-ready” という強い表現もあるが、0.0.1 の安定宣言とは分けて読むのが安全。

## 3. dav1d との比較

dav1d は AV1 の「速く、小さく、移植しやすく、正しく threaded」なデコーダとして成功した。AOMedia は、dav1d が Android、Apple、主要ブラウザ、主要 OS に広がった最重要 AV1 デコーダだと紹介している。dav2d はこの型を継承しつつ、AV2 の仕様確定前に表へ出てきた。

性能目標も同じく「全プラットフォームで最速」。ただし dav1d が成熟済み AV1 bitstream を相手にしたのに対し、dav2d はまだ揺れる AV2 draft を追う。「AV2 エコシステムの足場」として見る段階。

## 4. AV2 codec 自体の状況

AOMedia は 2025 年 9 月に AV2 を年末リリース予定と発表したが、公開仕様は 2026-01-05 付の draft release である。参照ソフトウェアは AVM の `research-v13.0.0`。

AV2 の bitstream は「実装者が触れる状態」には来たが、「もう変わらない状態」ではない。公式 Release Notes には multi-layer、random access、profile / level、metadata、decoder model など final までに直す既知課題が並ぶ。AOMedia は 5 年、数百回の会議、2700+ commits の成果として公開した、と説明している。

## 5. VLC / FFmpeg への組み込み予定

VLC 側は一歩先に動いている。AOMedia は、CES 2026 で VideoLAN が VLC 4 + AVM reference decoder plugin による AV2 リアルタイム再生を macOS laptop 上で見せた、と説明している。Google も Chrome / YouTube のカスタム環境で 1080p24 再生を示した。

ただし、安定版 VLC への dav2d 搭載日、FFmpeg への libdav2d 統合日はまだ公表されていない。順番としては、AV2 final、dav2d API の安定、VLC 4 / FFmpeg への wrapper 実装、各 distro / app への展開、という長い流れになる。

## 6. 競合プロジェクト

実質的な比較対象は AVM / libavm の reference decoder / encoder。これは正しさと仕様検証のための実装で、dav2d は実利用に向けて速く小さくする側に立つ。ほかに成熟した AV2 専用デコーダは確認できず、一般消費者向け GPU / SoC の AV2 ハードウェアデコーダ発表もまだ見えない。

## 7. 仲家文脈での意義

仲家の動画再生スタックでは、2026-05-03 にしゅん先生 PC へ VLC 3.0.23 を入れ、汎用動画は VLC、4K UHD Blu-ray は PowerDVD 14、変換は ffmpeg に整理済み。ここに dav2d を重ねると、「物理メディアの最終世代と、次世代オープン codec の入り口を同時に抱えている」話になる。

PowerDVD / SGX / UHD BD は、2018 年頃の PC でしか守れない閉じた再生スタック。一方で VLC / dav1d / dav2d は、仕様が固まる前から再生可能性を作る開いたスタック。「仕様より先にプレイヤーが走る時代」「UHD BD を守るしゅん先生 PC と、AV2 を待つ VLC」という切り口が使える。

## 8. 出典

- https://www.phoronix.com/news/Dav2d-Open-Source-AV2-Decode
- https://linuxiac.com/videolan-releases-dav2d-0-0-1-as-early-preview-av2-decoder/
- https://av2.aomedia.org/
- https://aomedia.org/blog%20posts/Demonstrating-Real-Time-AV2-Decoding-on-Consumer-Laptops/
- https://aomedia.org/av1-adoption-showcase/videolan-story/
