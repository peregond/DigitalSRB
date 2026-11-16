/* Serbian Latin <-> Cyrillic. Used by the Lat / Ćir switch and by the search box. */
(function (root) {
  "use strict";
  var LAT = "a b c č ć d đ e f g h i j k l m n o p r s š t u v z ž".split(" ");
  var CYR = "а б ц ч ћ д ђ е ф г х и ј к л м н о п р с ш т у в з ж".split(" ");
  var TO_CYR = {}, TO_LAT = {};
  LAT.forEach(function (l, i) {
    TO_CYR[l] = CYR[i]; TO_CYR[l.toUpperCase()] = CYR[i].toUpperCase();
    TO_LAT[CYR[i]] = l; TO_LAT[CYR[i].toUpperCase()] = l.toUpperCase();
  });
  TO_LAT["љ"] = "lj"; TO_LAT["Љ"] = "Lj"; TO_LAT["њ"] = "nj"; TO_LAT["Њ"] = "Nj"; TO_LAT["џ"] = "dž"; TO_LAT["Џ"] = "Dž";

  // names and words that stay in Latin script, also inside Cyrillic text
  var KEEP = /^(AI|ConsentID|Passkey|SmartBox|Apple|Google|Wallet|eIDAS|Visa|Mastercard|MasterCard|Dina|Internet|Explorer|Windows|macOS|Ubuntu|iOS|ISO|EUDI|NFC|IPS|QR|SR|EN)$/;
  // domains, addresses and shortcuts stay as they are
  var PROTECT = /((?:[A-Za-z0-9-]+\.)+(?:rs|com|org|net|eu|cc|gov|io)(?:\/[^\s]*)?|⌘K|\bRS\b|\bRSD\b)/;
  var WORD = /[A-Za-zČčĆćŠšŽžĐđ]+/g;

  function word(w) {
    if (KEEP.test(w) || /[qwxyQWXY]/.test(w)) return w;
    var allUp = w.length > 1 && w === w.toUpperCase();
    var out = "", i = 0, pair, up;
    while (i < w.length) {
      pair = w.substr(i, 2).toLowerCase();
      if (pair === "lj" || pair === "nj" || pair === "dž") {
        up = allUp || (w[i] !== w[i].toLowerCase() && (i === 0 || allUp));
        out += pair === "lj" ? (up ? "Љ" : "љ") : pair === "nj" ? (up ? "Њ" : "њ") : (up ? "Џ" : "џ");
        i += 2; continue;
      }
      out += TO_CYR[w[i]] || w[i]; i++;
    }
    return out;
  }

  function toCyr(text) {
    return text.split(PROTECT).map(function (part, k) {
      return k % 2 ? part : part.replace(WORD, word);
    }).join("");
  }

  function toLat(text) {
    return text.replace(/[Ѐ-ӿ]/g, function (c) { return TO_LAT[c] || c; });
  }

  // lower case, no diacritics, Cyrillic folded to Latin: for the search box
  function fold(text) {
    return toLat(String(text)).toLowerCase().replace(/đ/g, "dj").normalize("NFD").replace(/[̀-ͯ]/g, "");
  }

  root.Translit = { toCyr: toCyr, toLat: toLat, fold: fold };
  if (typeof module !== "undefined") module.exports = root.Translit;
})(typeof window !== "undefined" ? window : globalThis);
