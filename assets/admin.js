/* Admin page: reads everything through the admin_* functions (docs/supabase-comments.sql); needs the admin key. */
(function () {
  "use strict";
  var cfg = window.DSRB_CONFIG || {};
  var base = (cfg.supabaseUrl || "").replace(/\/+$/, "") + "/rest/v1/rpc/";
  var $ = function (s, e) { return (e || document).querySelector(s); };
  var $$ = function (s, e) { return Array.prototype.slice.call((e || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var key = sessionStorage.getItem("dsrb.admin") || "";
  var titles = {}, stats = null, comments = [], suggestions = [], sort = { by: "idea", dir: 1 };

  /* ---------- languages: [Russian, Serbian Latin, English]; Serbian Cyrillic is made from the Latin text ---------- */
  var STR = {
    doc: ["Админка · Digitalna Srbija", "Admin · Digitalna Srbija", "Admin · Digital Serbia"],
    brand: ["Digitalna Srbija · админка", "Digitalna Srbija · admin", "Digital Serbia · admin"],
    logout: ["Выйти", "Odjavi se", "Sign out"],
    login_h: ["Вход", "Prijava", "Sign in"],
    login_lead: ["Введите админ-ключ (длинный секрет из SQL-настройки). Он хранится только в этой вкладке и не сохраняется на сервере сайта.",
      "Unesi administratorski ključ (dugačku tajnu iz SQL podešavanja). Čuva se samo u ovoj kartici i ne ostaje na serveru sajta.",
      "Enter the admin key (the long secret from the SQL setup). It is kept only in this tab and is not saved on the website’s server."],
    key_ph: ["админ-ключ", "administratorski ključ", "admin key"],
    key_label: ["Админ-ключ", "Administratorski ključ", "Admin key"],
    enter: ["Войти", "Prijavi se", "Sign in"],
    bad_key: ["Неверный ключ.", "Pogrešan ključ.", "Wrong key."],
    login_fail: ["Не удалось войти: {e}. Проверьте, что SQL из {f} выполнен.", "Prijava nije uspela: {e}. Proveri da li je izvršen SQL iz fajla {f}.", "Could not sign in: {e}. Check that the SQL from {f} has been run."],
    error: ["Ошибка: {e}", "Greška: {e}", "Error: {e}"],
    updated: ["обновлено {t}", "osveženo u {t}", "updated {t}"],
    h_admin: ["Админка", "Admin", "Admin"],
    tabs: ["Разделы", "Odeljci", "Sections"],
    tab_stats: ["Обзор", "Pregled", "Overview"],
    tab_comments: ["Комментарии", "Komentari", "Comments"],
    tab_sugg: ["Предложения", "Predlozi", "Suggestions"],
    refresh: ["Обновить", "Osveži", "Refresh"],
    s_profiles: ["Профилей всего", "Ukupno profila", "Profiles in total"],
    s_profiles7: ["Новых за 7 дней", "Novih za 7 dana", "New in 7 days"],
    s_active7: ["Активных за 7 дней", "Aktivnih za 7 dana", "Active in 7 days"],
    s_comments: ["Комментариев всего", "Ukupno komentara", "Comments in total"],
    s_comments7: ["Комментариев за 7 дней", "Komentara za 7 dana", "Comments in 7 days"],
    s_hidden: ["Скрыто", "Sakriveno", "Hidden"],
    s_replies: ["Ваших ответов", "Tvojih odgovora", "Your replies"],
    s_sugg: ["Предложений из формы", "Predloga iz obrasca", "Suggestions from the form"],
    by_day: ["Комментарии по дням (30 дней)", "Komentari po danima (30 dana)", "Comments by day (30 days)"],
    ideas_h: ["Идеи: комментарии и голоса", "Ideje: komentari i glasovi", "Ideas: comments and votes"],
    ideas_hint: ["Нажмите на заголовок столбца, чтобы отсортировать. Красным выделены идеи без комментариев.",
      "Klikni na naslov kolone da bi sortirao. Crvenom su označene ideje bez komentara.",
      "Click a column title to sort. Ideas without comments are marked in red."],
    th_idea: ["Идея", "Ideja", "Idea"], th_comments: ["Комм.", "Kom.", "Comm."], th_authors: ["Авторов", "Autora", "Authors"],
    th_up: ["За", "Za", "Up"], th_down: ["Против", "Protiv", "Down"], th_score: ["Баланс", "Bilans", "Score"],
    f_idea: ["Идея №", "Ideja br.", "Idea no."], f_all: ["все", "sve", "all"],
    f_search: ["Поиск", "Pretraga", "Search"], f_search_ph: ["текст или имя", "tekst ili ime", "text or name"],
    f_hidden: ["только скрытые", "samo sakriveni", "hidden only"],
    f_staff: ["только мои ответы", "samo moji odgovori", "my replies only"],
    shown: ["Показано: {a} из {b}", "Prikazano: {a} od {b}", "Shown: {a} of {b}"],
    only_newest: [" (загружены только 1000 самых новых; фильтры ищут среди них)", " (učitano je samo 1000 najnovijih; filteri pretražuju samo njih)", " (only the 1000 newest are loaded; filters search among them)"],
    staff_name: ["Вы (команда)", "Ti (tim)", "You (team)"],
    no_profile: ["удалённый профиль", "obrisan profil", "deleted profile"],
    idea_n: ["идея № {n}", "ideja br. {n}", "idea no. {n}"],
    reply_to: ["ответ на #{n}", "odgovor na #{n}", "reply to #{n}"],
    by_author: ["удалён автором", "obrisao autor", "deleted by the author"],
    hidden_tag: ["скрыт", "sakriven", "hidden"],
    unhide: ["Показать", "Prikaži", "Show"], hide: ["Скрыть", "Sakrij", "Hide"], reply: ["Ответить", "Odgovori", "Reply"],
    reply_ph: ["Официальный ответ (виден всем, помечен как «Tim»)", "Zvaničan odgovor (vide ga svi, označen kao „Tim“)", "Official reply (visible to everyone, marked “Team”)"],
    reply_send: ["Отправить ответ", "Pošalji odgovor", "Send reply"],
    sugg_hint: ["Предложения из формы «Predloži ideju». Публично они не показываются.", "Predlozi iz obrasca „Predloži ideju“. Ne prikazuju se javno.", "Suggestions from the “Suggest an idea” form. They are not shown publicly."],
    contact: ["контакт:", "kontakt:", "contact:"],
    empty: ["Пока пусто.", "Za sada nema ničega.", "Nothing here yet."]
  };
  var LANGS = {
    ru: { col: 0, html: "ru", locale: "ru-RU", short: "RU" },
    "sr-lat": { col: 1, html: "sr-Latn", locale: "sr-Latn-RS", short: "SR" },
    "sr-cyr": { col: 1, html: "sr-Cyrl", locale: "sr-Cyrl-RS", short: "СР" },
    en: { col: 2, html: "en", locale: "en-GB", short: "EN" }
  };
  // the admin page keeps its own choice: the public site has no Russian
  var lang = "ru";
  try { lang = localStorage.getItem("dsrb.adminLang") || lang; } catch (e) { /* private mode */ }
  if (!Object.prototype.hasOwnProperty.call(LANGS, lang)) lang = "ru";
  var loginError = null, updatedAt = null;

  function cyr(text) { return lang === "sr-cyr" ? window.Translit.toCyr(text) : text; }
  // values are put in after the Cyrillic conversion, so file names and messages stay as they are
  function t(k, vars) {
    var s = cyr(STR[k][LANGS[lang].col]);
    return vars ? s.replace(/\{(\w)\}/g, function (m, n) { return n in vars ? vars[n] : m; }) : s;
  }
  // idea titles exist in Serbian and English; Russian shows the Serbian ones
  function titleOf(n) {
    var x = titles[n];
    if (!x) return "";
    return lang === "en" ? x.en || x.sr || "" : cyr(x.sr || "");
  }
  function time(d) { return d.toLocaleTimeString(LANGS[lang].locale, { hour: "2-digit", minute: "2-digit" }); }
  function showLoginError() {
    var msg = $("#loginMsg");
    msg.hidden = !loginError;
    msg.textContent = loginError ? t(loginError.k, loginError.vars) : "";
  }
  function showUpdated() { $("#who").textContent = updatedAt && !$("#app").hidden ? t("updated", { t: time(updatedAt) }) : ""; }

  function rpc(name, args) {
    args = args || {}; args.p_key = key;
    return fetch(base + name, {
      method: "POST",
      headers: { apikey: cfg.supabaseAnonKey, Authorization: "Bearer " + cfg.supabaseAnonKey, "Content-Type": "application/json" },
      body: JSON.stringify(args)
    }).then(function (r) {
      return r.json().catch(function () { return null; }).then(function (j) {
        if (!r.ok) { var e = new Error((j && j.message) || "HTTP " + r.status); e.code = (j && j.message) || ""; throw e; }
        return j;
      });
    });
  }
  function fmt(iso) { var d = new Date(iso); return d.toLocaleDateString(LANGS[lang].locale) + " " + time(d); }

  function show(logged) {
    $("#login").hidden = logged; $("#app").hidden = !logged; $("#logout").hidden = !logged;
    showUpdated();
  }
  function login(k) {
    key = k;
    return rpc("admin_stats").then(function (s) {
      sessionStorage.setItem("dsrb.admin", key); stats = s; show(true); return loadAll();
    });
  }
  $("#loginForm").addEventListener("submit", function (e) {
    e.preventDefault();
    loginError = null; showLoginError();
    login($("#key").value.trim()).catch(function (err) {
      key = "";
      loginError = err.code === "forbidden" ? { k: "bad_key" } : { k: "login_fail", vars: { e: err.message, f: "docs/supabase-comments.sql" } };
      showLoginError();
    });
  });
  $("#logout").addEventListener("click", function () { sessionStorage.removeItem("dsrb.admin"); key = ""; show(false); });

  function loadAll() {
    return Promise.all([
      fetch("/assets/ideas.json").then(function (r) { return r.json(); }).catch(function () { return {}; }),
      rpc("admin_stats"), rpc("admin_comments", { p_limit: 1000 }), rpc("admin_suggestions", { p_limit: 500 })
    ]).then(function (r) {
      titles = r[0]; stats = r[1]; comments = r[2] || []; suggestions = r[3] || [];
      renderStats(); renderComments(); renderSugg();
      updatedAt = new Date(); showUpdated();
    }).catch(function (err) {
      if (err.code === "forbidden") { show(false); key = ""; sessionStorage.removeItem("dsrb.admin"); }
      else alert(t("error", { e: err.message }));
    });
  }
  $("#refresh").addEventListener("click", loadAll);

  $$("[data-tab]").forEach(function (b) {
    b.addEventListener("click", function () {
      $$("[data-tab]").forEach(function (x) { x.setAttribute("aria-selected", String(x === b)); });
      $$("[data-pane]").forEach(function (p) { p.hidden = p.dataset.pane !== b.dataset.tab; });
    });
  });

  /* ---------- overview ---------- */
  function renderStats() {
    var s = stats;
    var cards = [
      ["s_profiles", s.profiles_total], ["s_profiles7", s.profiles_7d], ["s_active7", s.active_7d],
      ["s_comments", s.comments_total], ["s_comments7", s.comments_7d], ["s_hidden", s.hidden],
      ["s_replies", s.staff_replies], ["s_sugg", s.suggestions]
    ];
    $("#cards").innerHTML = cards.map(function (c) { return '<div class="stat"><b>' + esc(c[1]) + "</b><span>" + esc(t(c[0])) + "</span></div>"; }).join("");
    var days = {};
    (s.by_day || []).forEach(function (d) { days[d.day] = d.n; });
    var out = [], max = 1, i, d, k;
    for (i = 29; i >= 0; i--) { d = new Date(Date.now() - i * 864e5); k = d.toISOString().slice(0, 10); out.push([k, days[k] || 0]); max = Math.max(max, days[k] || 0); }
    $("#bars").innerHTML = out.map(function (x) { return '<i style="height:' + Math.round(x[1] / max * 100) + '%" data-t="' + x[0] + ": " + x[1] + '"></i>'; }).join("");
    renderIdeas();
  }
  function ideaRows() {
    var byIdea = {}, votes = {};
    (stats.by_idea || []).forEach(function (x) { byIdea[x.idea] = x; });
    (stats.votes || []).forEach(function (x) { votes[x.idea] = x; });
    var rows = [], ids = Object.keys(titles).map(Number);
    ids.sort(function (a, b) { return a - b; });
    ids.forEach(function (n) {
      var c = byIdea[n] || { comments: 0, authors: 0 }, v = votes[n] || { up: 0, down: 0 };
      rows.push({ idea: n, title: titleOf(n), comments: c.comments, authors: c.authors, up: v.up, down: v.down, score: v.up - v.down });
    });
    return rows;
  }
  function renderIdeas() {
    var rows = ideaRows();
    rows.sort(function (a, b) {
      var x = a[sort.by], y = b[sort.by];
      return (typeof x === "string" ? x.localeCompare(y, LANGS[lang].locale) : x - y) * sort.dir;
    });
    $("#ideasTable tbody").innerHTML = rows.map(function (r) {
      return '<tr class="' + (r.comments ? "" : "zero") + '"><td class="n">' + r.idea + "</td><td>" + esc(r.title) + '</td><td class="n">' + r.comments + '</td><td class="n">' + r.authors + '</td><td class="n">' + r.up + '</td><td class="n">' + r.down + '</td><td class="n">' + r.score + "</td></tr>";
    }).join("");
  }
  $$("#ideasTable th").forEach(function (th) {
    th.addEventListener("click", function () {
      var by = th.dataset.sort;
      sort = { by: by, dir: sort.by === by ? -sort.dir : (by === "idea" || by === "title" ? 1 : -1) };
      $$("#ideasTable th").forEach(function (x) { x.removeAttribute("aria-sort"); });
      th.setAttribute("aria-sort", sort.dir > 0 ? "ascending" : "descending");
      renderIdeas();
    });
  });

  /* ---------- comments ---------- */
  function renderComments() {
    // keep unsent replies: the list is drawn again when filters or the language change
    var drafts = $$("#cList [data-slot] textarea").map(function (a) { return [a.closest("[data-slot]").dataset.slot, a.value]; });
    var fi = $("#fIdea").value, ft = $("#fText").value.trim().toLowerCase(), fh = $("#fHidden").checked, fs = $("#fStaff").checked;
    var byId = {}; comments.forEach(function (c) { byId[c.id] = c; });
    var list = comments.filter(function (c) {
      if (fi && String(c.idea) !== fi) return false;
      if (fh && !c.hidden) return false;
      if (fs && !c.is_staff) return false;
      if (ft && (c.body + " " + (c.name || "")).toLowerCase().indexOf(ft) < 0) return false;
      return true;
    });
    $("#cCount").textContent = t("shown", { a: list.length, b: comments.length }) + (comments.length >= 1000 ? t("only_newest") : "");
    $("#cList").innerHTML = list.map(function (c) {
      var av = c.is_staff ? '<svg viewBox="0 0 64 64"><rect width="64" height="64" fill="#E30613"/><circle cx="32" cy="32" r="13" fill="#fff"/></svg>' : window.DSRB_AVATAR(c.avatar || 0);
      var title = titleOf(c.idea);
      return '<div class="cm' + (c.parent_id ? " rep" : "") + (c.hidden ? " hid" : "") + '" data-id="' + c.id + '"><span class="av">' + av + '</span><div class="grow">' +
        '<div class="meta"><b>' + esc(c.is_staff ? t("staff_name") : c.name || t("no_profile")) + "</b><span>" + esc(t("idea_n", { n: c.idea })) + (title ? " · " + esc(title) : "") + "</span><span>" + esc(fmt(c.created_at)) + "</span>" +
        (c.parent_id ? '<span class="tag">' + esc(t("reply_to", { n: c.parent_id })) + "</span>" : "") + (c.hidden ? '<span class="tag red">' + esc(t(c.deleted ? "by_author" : "hidden_tag")) + "</span>" : "") +
        (c.profile_id ? "<span>ID " + esc(String(c.profile_id).slice(0, 8)) + "</span>" : "") + "</div>" +
        '<div class="body">' + esc(c.body) + '</div><div class="acts">' +
        // what the author deleted stays deleted; a reply under it would not be visible
        (c.deleted ? "" : '<button class="ghost" data-hide="' + c.id + '" data-to="' + (!c.hidden) + '">' + esc(t(c.hidden ? "unhide" : "hide")) + "</button>" +
        (c.hidden || (byId[c.parent_id] && byId[c.parent_id].hidden) ? "" : '<button class="ghost" data-reply="' + c.id + '">' + esc(t("reply")) + "</button>")) + '</div><div data-slot="' + c.id + '"></div></div></div>';
    }).join("");
    drafts.forEach(function (d) {
      var b = $('#cList [data-reply="' + d[0] + '"]');
      if (b) openReply(Number(d[0])).value = d[1];
    });
  }
  function openReply(id) {
    var slot = $('[data-slot="' + id + '"]');
    slot.innerHTML = '<form><textarea maxlength="1000" placeholder="' + esc(t("reply_ph")) + '" aria-label="' + esc(t("reply")) + '" required></textarea><div><button class="btn" type="submit">' + esc(t("reply_send")) + "</button></div></form>";
    $("form", slot).addEventListener("submit", function (ev) {
      ev.preventDefault();
      var txt = $("textarea", slot).value.trim(); if (!txt) return;
      rpc("admin_reply", { p_parent: id, p_body: txt }).then(function () { slot.innerHTML = ""; return loadAll(); }).catch(function (er) { alert(er.message); });
    });
    return $("textarea", slot);
  }
  ["#fIdea", "#fText"].forEach(function (s) { $(s).addEventListener("input", renderComments); });
  ["#fHidden", "#fStaff"].forEach(function (s) { $(s).addEventListener("change", renderComments); });
  $("#cList").addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b) return;
    if (b.dataset.hide) {
      rpc("admin_set_hidden", { p_id: Number(b.dataset.hide), p_hidden: b.dataset.to === "true" }).then(loadAll).catch(function (er) { alert(er.message); });
    } else if (b.dataset.reply) {
      var slot = $('[data-slot="' + b.dataset.reply + '"]');
      if (slot.firstChild) { slot.innerHTML = ""; return; }
      openReply(Number(b.dataset.reply)).focus();
    }
  });

  /* ---------- suggestions ---------- */
  function renderSugg() {
    $("#sList").innerHTML = suggestions.length ? suggestions.map(function (s) {
      return '<div class="cm"><div class="grow"><div class="meta"><span>' + esc(fmt(s.created_at)) + "</span>" + (s.idea ? "<span>" + esc(t("idea_n", { n: s.idea })) + "</span>" : "") +
        (s.lang ? '<span class="tag">' + esc(s.lang) + "</span>" : "") + (s.contact ? "<span>" + esc(t("contact")) + " <b>" + esc(s.contact) + "</b></span>" : "") + '</div><div class="body">' + esc(s.message) + "</div></div></div>";
    }).join("") : '<p class="hint">' + esc(t("empty")) + "</p>";
  }

  /* ---------- language menu: the same one as on the site, plus Russian ---------- */
  function applyLang() {
    var L = LANGS[lang];
    document.documentElement.lang = L.html;
    document.title = t("doc");
    $$("[data-i18n]").forEach(function (el) { el.textContent = t(el.dataset.i18n); });
    $$("[data-i18n-ph]").forEach(function (el) { el.placeholder = t(el.dataset.i18nPh); });
    $$("[data-i18n-aria]").forEach(function (el) { el.setAttribute("aria-label", t(el.dataset.i18nAria)); });
    $$(".langmenu [data-opt]").forEach(function (b) { b.setAttribute("aria-checked", String(b.dataset.opt === lang)); });
    $(".lm-cur").textContent = L.short;
    $(".lm-btn").setAttribute("aria-label", L.short + " · Язык / Jezik i pismo / Language and script");
    showLoginError(); showUpdated();
    if (updatedAt) { renderStats(); renderComments(); renderSugg(); }
  }
  var menu = $(".langmenu"), mbtn = $(".lm-btn"), mlist = $(".lm-list");
  function openMenu(open) {
    mlist.hidden = !open;
    mbtn.setAttribute("aria-expanded", String(open));
    if (open) $('[aria-checked="true"]', mlist).focus();
  }
  mbtn.addEventListener("click", function () { openMenu(mlist.hidden); });
  $$("[data-opt]", menu).forEach(function (b) {
    b.addEventListener("click", function () {
      lang = b.dataset.opt;
      try { localStorage.setItem("dsrb.adminLang", lang); } catch (e) { /* private mode */ }
      applyLang(); openMenu(false); mbtn.focus();
    });
  });
  document.addEventListener("click", function (e) { if (!mlist.hidden && !menu.contains(e.target)) openMenu(false); });
  menu.addEventListener("focusout", function (e) { if (!mlist.hidden && e.relatedTarget && !menu.contains(e.relatedTarget)) openMenu(false); });
  menu.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !mlist.hidden) { openMenu(false); mbtn.focus(); }
    if ((e.key === "ArrowDown" || e.key === "ArrowUp") && !mlist.hidden) {
      e.preventDefault();
      var items = $$("[data-opt]", menu), i = items.indexOf(document.activeElement);
      items[(i + (e.key === "ArrowDown" ? 1 : items.length - 1)) % items.length].focus();
    }
  });
  applyLang();

  if (key) login(key).catch(function () { key = ""; show(false); }); else show(false);
})();
