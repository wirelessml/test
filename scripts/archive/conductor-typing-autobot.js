// Conductor Studio 2.0 typing auto-clearer
// https://studio.plotoftheprototype.com/typing
//
// Usage:
//   1. agent-browser open "https://studio.plotoftheprototype.com/typing"
//   2. Click into a course (e.g., "ひらがな 初級")
//   3. Paste this entire IIFE into agent-browser eval (or DevTools console)
//   4. Bot reads the prompt span structure, converts hiragana → romaji,
//      and dispatches synthetic KeyboardEvent on window every 100ms.
//   5. Achieves 十段 (max rank) on ひらがな 初級 in ~2:28 with 7848 streak.
//
// Why synthetic dispatch instead of agent-browser keyboard.type?
//   - Playwright keyboard.type doesn't reach this React app's window-level
//     keydown listener (CDP-level events go elsewhere).
//   - new KeyboardEvent + window.dispatchEvent works because React installs
//     its capture-phase listeners on `window`.
//   - navigator.webdriver:true does NOT block input on this page (verified).
//
// First successful run (2026-05-01 23:30 JST):
//   ひらがな 初級 → 十段 / WPM 668.3 / ACC 97.1% / SCORE 945.8 / BEST STREAK 7848

(() => {
  const HIRA = {
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    "さ": "sa", "し": "shi", "す": "su", "せ": "se", "そ": "so",
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
    "は": "ha", "ひ": "hi", "ふ": "fu", "へ": "he", "ほ": "ho",
    "ま": "ma", "み": "mi", "む": "mu", "め": "me", "も": "mo",
    "や": "ya", "ゆ": "yu", "よ": "yo",
    "ら": "ra", "り": "ri", "る": "ru", "れ": "re", "ろ": "ro",
    "わ": "wa", "を": "wo", "ん": "nn",
    "が": "ga", "ぎ": "gi", "ぐ": "gu", "げ": "ge", "ご": "go",
    "ざ": "za", "じ": "ji", "ず": "zu", "ぜ": "ze", "ぞ": "zo",
    "だ": "da", "ぢ": "di", "づ": "du", "で": "de", "ど": "do",
    "ば": "ba", "び": "bi", "ぶ": "bu", "べ": "be", "ぼ": "bo",
    "ぱ": "pa", "ぴ": "pi", "ぷ": "pu", "ぺ": "pe", "ぽ": "po",
  };
  const YOON = {
    // standard yo-on with small ya/yu/yo
    "きゃ": "kya", "きゅ": "kyu", "きょ": "kyo",
    "しゃ": "sha", "しゅ": "shu", "しょ": "sho",
    "ちゃ": "cha", "ちゅ": "chu", "ちょ": "cho",
    "にゃ": "nya", "にゅ": "nyu", "にょ": "nyo",
    "ひゃ": "hya", "ひゅ": "hyu", "ひょ": "hyo",
    "みゃ": "mya", "みゅ": "myu", "みょ": "myo",
    "りゃ": "rya", "りゅ": "ryu", "りょ": "ryo",
    "ぎゃ": "gya", "ぎゅ": "gyu", "ぎょ": "gyo",
    "じゃ": "ja", "じゅ": "ju", "じょ": "jo",
    "ぢゃ": "dya", "ぢゅ": "dyu", "ぢょ": "dyo",
    "びゃ": "bya", "びゅ": "byu", "びょ": "byo",
    "ぴゃ": "pya", "ぴゅ": "pyu", "ぴょ": "pyo",
    // foreign/katakana-style yo-on with small a/i/e/o (crucial for 中級 gadget terms)
    "じぇ": "je", "しぇ": "she", "ちぇ": "che",
    "つぁ": "tsa", "つぃ": "tsi", "つぇ": "tse", "つぉ": "tso",
    "てぃ": "thi", "でぃ": "dhi",
    "てゅ": "thu", "でゅ": "dhu",
    "とぅ": "twu", "どぅ": "dwu",
    "ふぁ": "fa", "ふぃ": "fi", "ふぇ": "fe", "ふぉ": "fo", "ふゅ": "fyu",
    "ゔぁ": "va", "ゔぃ": "vi", "ゔぇ": "ve", "ゔぉ": "vo",
    "うぃ": "wi", "うぇ": "we", "うぉ": "who",
    "いぇ": "ye",
    "くぁ": "qa", "くぃ": "qi", "くぇ": "qe", "くぉ": "qo",
    "ぐぁ": "gwa",
    "すぃ": "swi", "ずぃ": "zwi",
    // small kana (when standalone, use x-prefix wapuro convention)
  };
  const SMALL_FALLBACK = {
    "ぁ": "xa", "ぃ": "xi", "ぅ": "xu", "ぇ": "xe", "ぉ": "xo",
    "ゃ": "xya", "ゅ": "xyu", "ょ": "xyo", "っ": "xtu", "ゎ": "xwa",
  };
  const KATA = {
    // Katakana fallback (mirror of HIRA + YOON, in case prompts use カタカナ)
    "ア": "a", "イ": "i", "ウ": "u", "エ": "e", "オ": "o",
    "カ": "ka", "キ": "ki", "ク": "ku", "ケ": "ke", "コ": "ko",
    "サ": "sa", "シ": "shi", "ス": "su", "セ": "se", "ソ": "so",
    "タ": "ta", "チ": "chi", "ツ": "tsu", "テ": "te", "ト": "to",
    "ナ": "na", "ニ": "ni", "ヌ": "nu", "ネ": "ne", "ノ": "no",
    "ハ": "ha", "ヒ": "hi", "フ": "fu", "ヘ": "he", "ホ": "ho",
    "マ": "ma", "ミ": "mi", "ム": "mu", "メ": "me", "モ": "mo",
    "ヤ": "ya", "ユ": "yu", "ヨ": "yo",
    "ラ": "ra", "リ": "ri", "ル": "ru", "レ": "re", "ロ": "ro",
    "ワ": "wa", "ヲ": "wo", "ン": "nn",
    "ガ": "ga", "ギ": "gi", "グ": "gu", "ゲ": "ge", "ゴ": "go",
    "ザ": "za", "ジ": "ji", "ズ": "zu", "ゼ": "ze", "ゾ": "zo",
    "ダ": "da", "ヂ": "di", "ヅ": "du", "デ": "de", "ド": "do",
    "バ": "ba", "ビ": "bi", "ブ": "bu", "ベ": "be", "ボ": "bo",
    "パ": "pa", "ピ": "pi", "プ": "pu", "ペ": "pe", "ポ": "po",
    "ヴ": "vu",
  };

  function toRomaji(s) {
    let out = "", i = 0;
    while (i < s.length) {
      // sokuon: small tsu doubles next consonant (handles both hira ya-row and 2-char yo-on)
      if (s[i] === "っ" && i + 1 < s.length) {
        const r = YOON[s.substr(i + 1, 2)] || HIRA[s[i + 1]] || KATA[s[i + 1]];
        if (r) { out += r[0]; i++; continue; }
      }
      if (s[i] === "ッ" && i + 1 < s.length) {
        const r = YOON[s.substr(i + 1, 2)] || KATA[s[i + 1]] || HIRA[s[i + 1]];
        if (r) { out += r[0]; i++; continue; }
      }
      // yo-on: digraph (small ya/yu/yo or small a/i/e/o)
      if (i + 1 < s.length && YOON[s.substr(i, 2)]) {
        out += YOON[s.substr(i, 2)]; i += 2; continue;
      }
      if (HIRA[s[i]]) { out += HIRA[s[i]]; i++; continue; }
      if (KATA[s[i]]) { out += KATA[s[i]]; i++; continue; }
      if (s[i] === "ー") { out += "-"; i++; continue; }
      // Japanese punctuation → ASCII keys
      if (s[i] === "、") { out += ","; i++; continue; }
      if (s[i] === "。") { out += "."; i++; continue; }
      if (s[i] === "「") { out += "["; i++; continue; }
      if (s[i] === "」") { out += "]"; i++; continue; }
      if (s[i] === "！") { out += "!"; i++; continue; }
      if (s[i] === "？") { out += "?"; i++; continue; }
      if (s[i] === "・") { out += "/"; i++; continue; }
      if (s[i] === "　") { out += " "; i++; continue; }
      // Standalone small kana: x-prefix wapuro fallback (rarely needed but safe)
      if (SMALL_FALLBACK[s[i]]) { out += SMALL_FALLBACK[s[i]]; i++; continue; }
      // Pass through digits, ASCII letters, punctuation directly
      const cc = s.charCodeAt(i);
      if ((cc >= 0x30 && cc <= 0x39) || (cc >= 0x41 && cc <= 0x5A) || (cc >= 0x61 && cc <= 0x7A)) {
        out += s[i]; i++; continue;
      }
      i++;
    }
    return out;
  }

  function fireKey(key) {
    const code = key.match(/[a-z]/i) ? "Key" + key.toUpperCase() : key;
    const cc = key.toUpperCase().charCodeAt(0);
    const opts = { key, code, keyCode: cc, which: cc, bubbles: true, cancelable: true, composed: true };
    window.dispatchEvent(new KeyboardEvent("keydown", opts));
    window.dispatchEvent(new KeyboardEvent("keyup", opts));
  }

  // Read the FULL prompt by walking up to the parent container of the
  // currently-highlighted span (.border-b-2.border-foreground/60) and
  // reading its innerText. Earlier bug: parent.querySelectorAll("span")[1]
  // returned the current span itself, not the rest, producing duplicated chars.
  function readPrompt() {
    const cur = document.querySelector(".border-b-2.border-foreground\\/60");
    if (!cur) return null;
    return cur.parentElement.innerText.replace(/\s+/g, "");
  }

  if (window.__autoTyper) clearInterval(window.__autoTyper);

  let lastTyped = "";
  window.__autoTyperLog = [];
  window.__autoTyperEnded = null;
  const startTime = Date.now();
  // Cap criteria (whichever fires first):
  //   - bestStreak >= 300 (max +50% bonus locked) AND completed >= 50
  //   - elapsed wall-clock >= 90 seconds
  // Then: clearInterval + click 中断 → 中断する (skip result screen for time efficiency)
  const STREAK_CAP = 300;
  const DONE_CAP = 30;
  const TIMEOUT_SEC = 90;

  window.__autoTyper = setInterval(() => {
    // Type the next prompt if changed
    const p = readPrompt();
    if (p && p !== lastTyped) {
      lastTyped = p;
      const r = toRomaji(p);
      window.__autoTyperLog.push({ p, r });
      for (const ch of r) fireKey(ch);
    }

    // Self-cap check
    const txt = document.body.innerText;
    const streakMatch = txt.match(/連続\s*\d+\s*\/\s*最高(\d+)/);
    const doneMatch = txt.match(/(\d+)\s*問\s*完了/);
    const bestStreak = streakMatch ? parseInt(streakMatch[1]) : 0;
    const done = doneMatch ? parseInt(doneMatch[1]) : 0;
    const elapsed = (Date.now() - startTime) / 1000;

    const reachedBonus = bestStreak >= STREAK_CAP && done >= DONE_CAP;
    const timedOut = elapsed >= TIMEOUT_SEC;
    if (reachedBonus || timedOut) {
      clearInterval(window.__autoTyper);
      window.__autoTyper = null;
      window.__autoTyperEnded = {
        reason: reachedBonus ? "max-bonus-locked" : "timeout",
        bestStreak, done, elapsedSec: Math.round(elapsed),
      };
      // Click 中断 then confirm
      const cancelBtn = [...document.querySelectorAll("button")].find(b => b.textContent === "中断");
      if (cancelBtn) {
        cancelBtn.click();
        setTimeout(() => {
          const confirmBtn = [...document.querySelectorAll("button")].find(b => b.textContent === "中断する");
          if (confirmBtn) confirmBtn.click();
        }, 600);
      }
    }
  }, 100);

  return "auto-typer started (will self-cap at streak>=300+done>=50 OR 90sec)";
})();
