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
    var d = document.body.dataset;
    document.title = (lang === "sr" ? d.titleSr : d.titleEn) || TITLES[lang];
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

  /* ---------- filters: topic and difficulty ---------- */
  var state = { cat: "all", tier: "all" };
  var catChips = $$(".chip[data-cat]"), tierChips = $$(".chip[data-tier]"), emptyMsg = document.getElementById("empty");
  function applyFilters() {
    function mark(list, key, val) {
      list.forEach(function (c) {
        var on = c.dataset[key] === val;
        c.classList.toggle("on", on);
        c.setAttribute("aria-pressed", String(on));
      });
    }
    mark(catChips, "cat", state.cat);
    mark(tierChips, "tier", state.tier);
    var shown = 0;
    $$(".cat-section").forEach(function (s) {
      var any = 0;
      $$(".idea", s).forEach(function (a) {
        var ok = (state.cat === "all" || s.dataset.cat === state.cat) && (state.tier === "all" || a.dataset.tier === state.tier);
        a.hidden = !ok;
        if (ok) any++;
      });
      s.hidden = !any;
      shown += any;
    });
    if (emptyMsg) emptyMsg.hidden = shown > 0;
  }
  function toList() {
    var area = document.getElementById("ideas");
    if (area && area.getBoundingClientRect().top < 0) area.scrollIntoView();
  }
  catChips.forEach(function (c) {
    c.addEventListener("click", function () { state.cat = c.dataset.cat; applyFilters(); toList(); });
  });
  tierChips.forEach(function (c) {
    c.addEventListener("click", function () { state.tier = c.dataset.tier; applyFilters(); toList(); });
  });
  $$("[data-tier-filter]").forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      state.cat = "all"; state.tier = a.dataset.tierFilter;
      applyFilters();
      document.getElementById("ideas").scrollIntoView();
    });
  });
  // a link to a hidden topic or idea must show it first
  function revealTarget() {
    var el = location.hash.length > 1 && document.getElementById(location.hash.slice(1));
    if (el && (el.hidden || el.closest("[hidden]"))) {
      state.cat = "all"; state.tier = "all";
      applyFilters();
      el.scrollIntoView();
    }
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
    if (!el) return;
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
  if (track) initCards();
  function initCards() {
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
  }

  /* ---------- detail pages: stagger, hero scroll effect, local nav ---------- */
  if (document.body.classList.contains("pg")) initPage();
  function initPage() {
    var groups = ".pg-stages,.pg-cards,.pg-steps,.pg-check,.pg-faq,.pg-rel,.chain,.flow-row ol,.pg-hstats,.speeds";
    $$(groups).forEach(function (g) {
      Array.prototype.forEach.call(g.children, function (c, i) {
        c.classList.add("rv");
        c.style.setProperty("--d", Math.min(i, 6) * 90 + "ms");
      });
    });
    $$(".pg-head,.pg-prose p,.pg-note,.pg-tablewrap,.net,.clerk,.jr,.pg-bars,.phone-wrap,.flow-row,.pg-vote .wrap,.pg-nb")
      .forEach(function (e) { e.classList.add("rv"); });

    var bar = document.querySelector(".pg-progress");
    var links = $$(".pg-local-links a"), secs = links.map(function (a) { return document.querySelector(a.getAttribute("href")); });
    var tick = false;
    function frame() {
      tick = false;
      var y = window.scrollY, h = document.documentElement.scrollHeight - innerHeight;
      if (bar) bar.style.setProperty("--p", h > 0 ? Math.min(1, y / h).toFixed(4) : 0);
      var cur = -1;
      secs.forEach(function (s, i) { if (s && s.getBoundingClientRect().top < innerHeight * 0.4) cur = i; });
      links.forEach(function (a, i) { a.classList.toggle("on", i === cur); });
      if (cur >= 0) {
        var on = links[cur], box = on.parentNode;
        if (on.offsetLeft < box.scrollLeft || on.offsetLeft + on.offsetWidth > box.scrollLeft + box.clientWidth)
          box.scrollTo({ left: on.offsetLeft - 20, behavior: "smooth" });
      }
    }
    window.addEventListener("scroll", function () { if (!tick) { tick = true; requestAnimationFrame(frame); } }, { passive: true });
    window.addEventListener("resize", frame);
    frame();
  }

  /* ---------- drag to scroll with the mouse (touch already scrolls natively) ---------- */
  function enableDrag(el) {
    if (!el) return;
    var down = false, moved = false, startX = 0, startLeft = 0, id = null;
    el.classList.add("drag");
    el.addEventListener("pointerdown", function (e) {
      if (e.pointerType !== "mouse" || e.button !== 0) return;
      down = true; moved = false; startX = e.clientX; startLeft = el.scrollLeft; id = e.pointerId;
    });
    el.addEventListener("pointermove", function (e) {
      if (!down) return;
      var dx = e.clientX - startX;
      if (!moved && Math.abs(dx) > 5) {
        moved = true;
        el.classList.add("dragging");
        el.style.scrollSnapType = "none";
        try { el.setPointerCapture(id); } catch (err) { /* ignore */ }
      }
      if (moved) el.scrollLeft = startLeft - dx;
    });
    function end() {
      if (!down) return;
      down = false;
      if (moved) {
        el.classList.remove("dragging");
        el.style.scrollSnapType = "";
        try { el.releasePointerCapture(id); } catch (err) { /* ignore */ }
      }
    }
    el.addEventListener("pointerup", end);
    el.addEventListener("pointercancel", end);
    el.addEventListener("lostpointercapture", end);
    // a drag must not open the card it ended on
    el.addEventListener("click", function (e) {
      if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; }
    }, true);
    el.addEventListener("dragstart", function (e) { e.preventDefault(); });
  }
  enableDrag(document.getElementById("fcTrack"));
  $$(".pa-row").forEach(enableDrag);

  /* ---------- fixed 9:16 phones and 16:9 browser windows: shrink to fit, never squeeze ---------- */
  function fitMocks() {
    $$(".pa-browser").forEach(function (b) {
      var avail = b.parentNode.clientWidth;
      b.style.zoom = 1;
      b.style.zoom = avail && avail < 840 ? (avail / 840).toFixed(4) : 1;
    });
    $$(".pa-pair .pa-fig, .pa-phonepair .pa-fig").forEach(function (f) {
      var avail = f.parentNode.clientWidth;
      f.style.zoom = 1;
      f.style.zoom = avail && avail < 340 ? (avail / 340).toFixed(4) : 1;
    });
  }
  fitMocks();
  window.addEventListener("resize", fitMocks);
  window.addEventListener("load", fitMocks);

  /* ---------- phone galleries: arrows ---------- */
  $$(".pa-ctrl").forEach(function (box) {
    var row = box.parentNode.querySelector(".pa-row");
    $$("button", box).forEach(function (btn) {
      btn.addEventListener("click", function () {
        var f = row.querySelector(".pa-fig");
        row.scrollBy({ left: Number(btn.dataset.pa) * (f.offsetWidth + 36), behavior: "smooth" });
      });
    });
  });

  /* ---------- scroll reveal ---------- */
  var items = $$(".reveal, .fcard, .rv");
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
