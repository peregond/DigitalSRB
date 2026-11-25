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
  function fmt(iso) { var d = new Date(iso); return d.toLocaleDateString("ru-RU") + " " + d.toLocaleTimeString("ru-RU", { hour: "2-digit", minute: "2-digit" }); }

  function show(logged) {
    $("#login").hidden = logged; $("#app").hidden = !logged; $("#logout").hidden = !logged;
  }
  function login(k) {
    key = k;
    return rpc("admin_stats").then(function (s) {
      sessionStorage.setItem("dsrb.admin", key); stats = s; show(true); return loadAll();
    });
  }
  $("#loginForm").addEventListener("submit", function (e) {
    e.preventDefault();
    var msg = $("#loginMsg"); msg.hidden = true;
    login($("#key").value.trim()).catch(function (err) {
      key = ""; msg.hidden = false;
      msg.textContent = err.code === "forbidden" ? "Неверный ключ." : "Не удалось войти: " + err.message + ". Проверьте, что SQL из docs/supabase-comments.sql выполнен.";
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
      $("#who").textContent = "обновлено " + new Date().toLocaleTimeString("ru-RU", { hour: "2-digit", minute: "2-digit" });
    }).catch(function (err) {
      if (err.code === "forbidden") { show(false); key = ""; sessionStorage.removeItem("dsrb.admin"); }
      else alert("Ошибка: " + err.message);
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
      ["Профилей всего", s.profiles_total], ["Новых за 7 дней", s.profiles_7d], ["Активных за 7 дней", s.active_7d],
      ["Комментариев всего", s.comments_total], ["Комментариев за 7 дней", s.comments_7d], ["Скрыто", s.hidden],
      ["Ваших ответов", s.staff_replies], ["Предложений из формы", s.suggestions]
    ];
    $("#cards").innerHTML = cards.map(function (c) { return '<div class="stat"><b>' + esc(c[0] === "" ? "" : c[1]) + "</b><span>" + esc(c[0]) + "</span></div>"; }).join("");
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
      rows.push({ idea: n, title: (titles[n] && titles[n].sr) || "", comments: c.comments, authors: c.authors, up: v.up, down: v.down, score: v.up - v.down });
    });
    return rows;
  }
  function renderIdeas() {
    var rows = ideaRows();
    rows.sort(function (a, b) {
      var x = a[sort.by], y = b[sort.by];
      return (typeof x === "string" ? x.localeCompare(y) : x - y) * sort.dir;
    });
    $("#ideasTable tbody").innerHTML = rows.map(function (r) {
      return '<tr class="' + (r.comments ? "" : "zero") + '"><td class="n">' + r.idea + "</td><td>" + esc(r.title) + '</td><td class="n">' + r.comments + '</td><td class="n">' + r.authors + '</td><td class="n">' + r.up + '</td><td class="n">' + r.down + '</td><td class="n">' + r.score + "</td></tr>";
    }).join("");
  }
  $$("#ideasTable th").forEach(function (th) {
    th.addEventListener("click", function () {
      var by = th.dataset.sort;
      sort = { by: by, dir: sort.by === by ? -sort.dir : (by === "idea" || by === "title" ? 1 : -1) };
      renderIdeas();
    });
  });

  /* ---------- comments ---------- */
  function renderComments() {
    var fi = $("#fIdea").value, ft = $("#fText").value.trim().toLowerCase(), fh = $("#fHidden").checked, fs = $("#fStaff").checked;
    var byId = {}; comments.forEach(function (c) { byId[c.id] = c; });
    var list = comments.filter(function (c) {
      if (fi && String(c.idea) !== fi) return false;
      if (fh && !c.hidden) return false;
      if (fs && !c.is_staff) return false;
      if (ft && (c.body + " " + (c.name || "")).toLowerCase().indexOf(ft) < 0) return false;
      return true;
    });
    $("#cCount").textContent = "Показано: " + list.length + " из " + comments.length;
    $("#cList").innerHTML = list.map(function (c) {
      var av = c.is_staff ? '<svg viewBox="0 0 64 64"><rect width="64" height="64" fill="#E30613"/><circle cx="32" cy="32" r="13" fill="#fff"/></svg>' : window.DSRB_AVATAR(c.avatar || 0);
      var t = titles[c.idea] ? titles[c.idea].sr : "";
      return '<div class="cm' + (c.parent_id ? " rep" : "") + (c.hidden ? " hid" : "") + '" data-id="' + c.id + '"><span class="av">' + av + '</span><div class="grow">' +
        '<div class="meta"><b>' + esc(c.is_staff ? "Вы (команда)" : c.name || "удалённый профиль") + "</b><span>идея № " + c.idea + (t ? " · " + esc(t) : "") + "</span><span>" + esc(fmt(c.created_at)) + "</span>" +
        (c.parent_id ? '<span class="tag">ответ на #' + c.parent_id + "</span>" : "") + (c.hidden ? '<span class="tag red">скрыт</span>' : "") +
        (c.profile_id ? "<span>id " + esc(String(c.profile_id).slice(0, 8)) + "</span>" : "") + "</div>" +
        '<div class="body">' + esc(c.body) + '</div><div class="acts">' +
        '<button class="ghost" data-hide="' + c.id + '" data-to="' + (!c.hidden) + '">' + (c.hidden ? "Показать" : "Скрыть") + "</button>" +
        '<button class="ghost" data-reply="' + c.id + '">Ответить</button></div><div data-slot="' + c.id + '"></div></div></div>';
    }).join("");
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
      slot.innerHTML = '<form><textarea maxlength="1000" placeholder="Официальный ответ (виден всем, помечен как «Tim»)" required></textarea><div><button class="btn" type="submit">Отправить ответ</button></div></form>';
      $("textarea", slot).focus();
      $("form", slot).addEventListener("submit", function (ev) {
        ev.preventDefault();
        var txt = $("textarea", slot).value.trim(); if (!txt) return;
        rpc("admin_reply", { p_parent: Number(b.dataset.reply), p_body: txt }).then(loadAll).catch(function (er) { alert(er.message); });
      });
    }
  });

  /* ---------- suggestions ---------- */
  function renderSugg() {
    $("#sList").innerHTML = suggestions.length ? suggestions.map(function (s) {
      return '<div class="cm"><div class="grow"><div class="meta"><span>' + esc(fmt(s.created_at)) + "</span>" + (s.idea ? "<span>идея № " + s.idea + "</span>" : "") +
        (s.lang ? '<span class="tag">' + esc(s.lang) + "</span>" : "") + (s.contact ? "<span>контакт: <b>" + esc(s.contact) + "</b></span>" : "") + '</div><div class="body">' + esc(s.message) + "</div></div></div>";
    }).join("") : '<p class="hint">Пока пусто.</p>';
  }

  if (key) login(key).catch(function () { key = ""; show(false); }); else show(false);
})();
