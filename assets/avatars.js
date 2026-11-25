/* 50 abstract avatars, drawn from code: 10 colour sets x 5 shapes. DSRB_AVATAR(n) returns an SVG string (n = 0..49). */
(function (root) {
  "use strict";
  var SETS = [
    ["#FFE3E0", "#E30613", "#1D3F72"], ["#E3F1FF", "#2F6FEB", "#F2A100"], ["#E6F6EA", "#12A150", "#0C4076"],
    ["#FFF1D6", "#F2A100", "#C6363C"], ["#EFE8FF", "#6A45F0", "#F2A100"], ["#FFE6F0", "#D1246A", "#24407A"],
    ["#E0F6F8", "#0A9AAE", "#E30613"], ["#F0F5DC", "#7CA10A", "#24407A"], ["#1D3F72", "#FFFFFF", "#F2A100"],
    ["#222", "#F2A100", "#E30613"]
  ];
  function shapes(kind, a, b) {
    switch (kind) {
      case 0: return '<circle cx="26" cy="27" r="15" fill="' + a + '"/><circle cx="40" cy="38" r="15" fill="' + b + '" opacity=".9"/>';
      case 1: return '<path d="M12 36a20 20 0 0 1 40 0z" fill="' + a + '"/><rect x="20" y="40" width="24" height="14" rx="4" fill="' + b + '"/>';
      case 2: return '<path d="M32 10l20 34H12z" fill="' + a + '"/><path d="M32 54L18 30h28z" fill="' + b + '" opacity=".85"/>';
      case 3: return '<circle cx="32" cy="32" r="21" fill="none" stroke="' + a + '" stroke-width="7"/><circle cx="32" cy="32" r="9" fill="' + b + '"/>';
      default: return '<path d="M6 24q13-14 26 0t26 0" fill="none" stroke="' + a + '" stroke-width="7" stroke-linecap="round"/>' +
                      '<path d="M6 42q13-14 26 0t26 0" fill="none" stroke="' + b + '" stroke-width="7" stroke-linecap="round"/>';
    }
  }
  root.DSRB_AVATAR = function (n) {
    n = Math.max(0, Math.min(49, Number(n) | 0));
    var set = SETS[n % 10];
    return '<svg viewBox="0 0 64 64" aria-hidden="true" focusable="false"><rect width="64" height="64" fill="' + set[0] + '"/>' +
           shapes(Math.floor(n / 10), set[1], set[2]) + "</svg>";
  };
})(typeof window !== "undefined" ? window : globalThis);
