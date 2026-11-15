(function () {
  "use strict";
  var root = document.documentElement;
  var $$ = function (sel, el) { return Array.prototype.slice.call((el || document).querySelectorAll(sel)); };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } }
  };

  /* ---------- language ---------- */
  var TITLES = { sr: "Digitalna Srbija · 60 ideja", en: "Digital Serbia · 60 ideas" };

  function applyLang(lang) {
    root.dataset.lang = lang;
    root.lang = lang === "sr" ? "sr-Latn" : "en";
    document.title = TITLES[lang];
    $$("[data-set-lang]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.setLang === lang));
    });
  }

  function setLang(lang) {
    if (lang === root.dataset.lang) return;
    // keep the reader on the same card: texts differ in length between languages
    var anchor = null, fallback = null, offset = 0, line = 110;
    $$(".idea, .tier-head, main > section, .hero").some(function (el) {
      var r = el.getBoundingClientRect();
      if (!r.height) return false;
      if (!fallback && r.bottom > line) fallback = el;
      if (r.top >= line - 12 && r.top < window.innerHeight) { anchor = el; return true; }
      return r.top >= window.innerHeight;
    });
    anchor = anchor || fallback;
    if (anchor) offset = anchor.getBoundingClientRect().top;
    applyLang(lang);
    store.set("dsrb.lang", lang);
    try {
      var url = new URL(location.href);
      url.searchParams.set("lang", lang);
      history.replaceState(null, "", url);
    } catch (e) { /* file:// */ }
    if (anchor) {
      var prev = root.style.scrollBehavior;
      root.style.scrollBehavior = "auto";
      window.scrollBy(0, anchor.getBoundingClientRect().top - offset);
      root.style.scrollBehavior = prev;
    }
  }

  applyLang(root.dataset.lang === "en" ? "en" : "sr");
  $$("[data-set-lang]").forEach(function (b) {
    b.addEventListener("click", function () { setLang(b.dataset.setLang); });
  });

  /* ---------- tier filter ---------- */
  var chips = $$(".chip[data-filter]");
  function setFilter(f) {
    chips.forEach(function (c) {
      var on = c.dataset.filter === f;
      c.classList.toggle("on", on);
      c.setAttribute("aria-pressed", String(on));
    });
    $$(".tier-section").forEach(function (s) { s.hidden = f !== "all" && s.dataset.tier !== f; });
  }
  chips.forEach(function (c) {
    c.addEventListener("click", function () {
      setFilter(c.dataset.filter);
      var area = document.getElementById("ideas");
      if (area.getBoundingClientRect().top < 0) area.scrollIntoView();
    });
  });
  // a link to a hidden tier or idea must show it first
  function revealTarget() {
    var el = location.hash.length > 1 && document.getElementById(location.hash.slice(1));
    var sec = el && el.closest(".tier-section");
    if (sec && sec.hidden) { setFilter("all"); el.scrollIntoView(); }
  }
  window.addEventListener("hashchange", revealTarget);

  /* ---------- votes ---------- */
  // Each visitor's choice is kept in their browser. If a Supabase project is configured
  // in assets/config.js, totals are also counted for everyone (see README).
  var cfg = window.DSRB_CONFIG || {};
  var api = cfg.supabaseUrl && cfg.supabaseAnonKey ? cfg.supabaseUrl.replace(/\/+$/, "") + "/rest/v1" : null;
  var mine = {};
  try { mine = JSON.parse(store.get("dsrb.votes") || "{}") || {}; } catch (e) { mine = {}; }
  var totals = null; // { id: {up, down} } once loaded from the backend
  var boxes = {};
  $$("[data-vote]").forEach(function (b) { boxes[b.dataset.vote] = b; });

  function call(path, opts) {
    opts = opts || {};
    opts.headers = { apikey: cfg.supabaseAnonKey, Authorization: "Bearer " + cfg.supabaseAnonKey, "Content-Type": "application/json" };
    return fetch(api + path, opts).then(function (r) {
      if (!r.ok) throw new Error("votes: HTTP " + r.status);
      return r.json();
    });
  }

  function paint(id) {
    var box = boxes[id];
    if (!box) return;
    $$(".vbtn", box).forEach(function (btn) {
      var dir = btn.dataset.dir;
      btn.setAttribute("aria-pressed", String(mine[id] === dir));
      var count = btn.querySelector(".count");
      if (totals) {
        var t = totals[id] || { up: 0, down: 0 };
        // never show less than the visitor's own vote, even if the request is still in flight
        count.textContent = Math.max(t[dir], mine[id] === dir ? 1 : 0);
        count.hidden = false;
      } else {
        count.hidden = true;
      }
    });
  }

  function paintTally() {
    var up = 0, down = 0;
    Object.keys(mine).forEach(function (k) { if (mine[k] === "up") up++; else if (mine[k] === "down") down++; });
    var el = document.getElementById("tally");
    el.hidden = !(up || down);
    el.querySelector('[data-tally="up"]').textContent = up;
    el.querySelector('[data-tally="down"]').textContent = down;
  }

  function vote(id, dir, btn) {
    var prev = mine[id];
    var next = prev === dir ? undefined : dir; // pressing the same button again takes the vote back
    if (next) mine[id] = next; else delete mine[id];
    store.set("dsrb.votes", JSON.stringify(mine));
    var dUp = (next === "up" ? 1 : 0) - (prev === "up" ? 1 : 0);
    var dDown = (next === "down" ? 1 : 0) - (prev === "down" ? 1 : 0);
    if (totals) {
      var t = totals[id] || (totals[id] = { up: 0, down: 0 });
      t.up = Math.max(0, t.up + dUp);
      t.down = Math.max(0, t.down + dDown);
    }
    if (next) { btn.classList.remove("pop"); void btn.offsetWidth; btn.classList.add("pop"); }
    paint(id);
    paintTally();
    if (api) {
      call("/rpc/cast_vote", { method: "POST", body: JSON.stringify({ p_idea: Number(id), p_up: dUp, p_down: dDown }) })
        .then(function (row) {
          row = Array.isArray(row) ? row[0] : row;
          if (row && totals) { totals[id] = { up: row.up, down: row.down }; paint(id); }
        })
        .catch(function (e) { console.warn(e); });
    }
  }

  Object.keys(boxes).forEach(function (id) {
    $$(".vbtn", boxes[id]).forEach(function (btn) {
      btn.addEventListener("click", function () { vote(id, btn.dataset.dir, btn); });
    });
    paint(id);
  });
  paintTally();

  if (api) {
    call("/idea_votes?select=idea,up,down").then(function (rows) {
      totals = {};
      rows.forEach(function (r) { totals[r.idea] = { up: r.up, down: r.down }; });
      Object.keys(boxes).forEach(paint);
    }).catch(function (e) { console.warn(e); });
  }

  /* ---------- featured cards ---------- */
  var track = document.getElementById("fcTrack"), prev = document.getElementById("fcPrev"), next = document.getElementById("fcNext");
  function arrows() {
    prev.disabled = track.scrollLeft < 4;
    next.disabled = track.scrollLeft > track.scrollWidth - track.clientWidth - 4;
  }
  function slide(dir) {
    var c = track.querySelector(".fcard");
    track.scrollBy({ left: dir * (c.offsetWidth + 20), behavior: "smooth" });
  }
  prev.addEventListener("click", function () { slide(-1); });
  next.addEventListener("click", function () { slide(1); });
  track.addEventListener("scroll", arrows, { passive: true });
  track.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") { slide(1); e.preventDefault(); }
    if (e.key === "ArrowLeft") { slide(-1); e.preventDefault(); }
  });
  window.addEventListener("resize", arrows);
  arrows();

  /* ---------- scroll reveal ---------- */
  var items = $$(".reveal, .fcard");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }
  revealTarget();
})();
