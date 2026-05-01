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
    "きゃ": "kya", "きゅ": "kyu", "きょ": "kyo",
    "しゃ": "sha", "しゅ": "shu", "しょ": "sho",
    "ちゃ": "cha", "ちゅ": "chu", "ちょ": "cho",
    "にゃ": "nya", "にゅ": "nyu", "にょ": "nyo",
    "ひゃ": "hya", "ひゅ": "hyu", "ひょ": "hyo",
    "みゃ": "mya", "みゅ": "myu", "みょ": "myo",
    "りゃ": "rya", "りゅ": "ryu", "りょ": "ryo",
    "ぎゃ": "gya", "ぎゅ": "gyu", "ぎょ": "gyo",
    "じゃ": "ja", "じゅ": "ju", "じょ": "jo",
    "びゃ": "bya", "びゅ": "byu", "びょ": "byo",
    "ぴゃ": "pya", "ぴゅ": "pyu", "ぴょ": "pyo",
  };

  function toRomaji(s) {
    let out = "", i = 0;
    while (i < s.length) {
      // sokuon: small tsu doubles next consonant
      if (s[i] === "っ" && i + 1 < s.length) {
        const r = YOON[s.substr(i + 1, 2)] || HIRA[s[i + 1]];
        if (r) { out += r[0]; i++; continue; }
      }
      // yo-on: digraph with small ya/yu/yo
      if (i + 1 < s.length && YOON[s.substr(i, 2)]) {
        out += YOON[s.substr(i, 2)]; i += 2; continue;
      }
      if (HIRA[s[i]]) { out += HIRA[s[i]]; i++; continue; }
      if (s[i] === "ー") { out += "-"; i++; continue; }
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
  window.__autoTyper = setInterval(() => {
    const p = readPrompt();
    if (!p || p === lastTyped) return;
    lastTyped = p;
    const r = toRomaji(p);
    window.__autoTyperLog.push({ p, r });
    for (const ch of r) fireKey(ch);
  }, 100);

  return "auto-typer started";
})();
