/* Comments under every idea, anonymous profiles (name + a picture + a recovery code).
 * Needs the Supabase project from assets/config.js and docs/supabase-comments.sql. Without them the buttons stay hidden. */
(function () {
  "use strict";
  var cfg = window.DSRB_CONFIG || {};
  if (!cfg.supabaseUrl || !cfg.supabaseAnonKey || !window.DSRB_AVATAR) return;
  var root = document.documentElement, T = window.Translit, AV = window.DSRB_AVATAR;
  var base = cfg.supabaseUrl.replace(/\/+$/, "") + "/rest/v1/rpc/";
  var $ = function (sel, el) { return (el || document).querySelector(sel); };
  var $$ = function (sel, el) { return Array.prototype.slice.call((el || document).querySelectorAll(sel)); };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } },
    del: function (k) { try { localStorage.removeItem(k); } catch (e) { /* ignore */ } }
  };

  /* ---------- texts: [Serbian (Latin), English] ---------- */
  var S = {
    btn: ["Komentari", "Comments"],
    none: ["Još nema komentara. Budi prvi.", "No comments yet. Be the first."],
    ph: ["Tvoj komentar ili pitanje…", "Your comment or question…"],
    send: ["Pošalji komentar", "Send comment"],
    rules: ["Komentari su javni. Budi korektan i ne piši lične podatke. Uvredljive komentare uklanjamo.", "Comments are public. Be kind and do not share personal data. Abusive comments are removed."],
    as: ["Pišeš kao", "Posting as"],
    anon: ["Pri slanju biraš ime i sliku", "You choose a name and a picture when you send"],
    reply: ["Odgovori", "Reply"],
    del: ["Obriši", "Delete"],
    cancel: ["Otkaži", "Cancel"],
    team: ["Tim", "Team"],
    teamName: ["Digitalna Srbija", "Digital Serbia"],
    loadErr: ["Komentari trenutno nisu dostupni.", "Comments are not available right now."],
    sending: ["Šaljem…", "Sending…"],
    e_slow: ["Malo sporije: sačekaj 15 sekundi.", "Slow down a little: wait 15 seconds."],
    e_daily: ["Dnevna granica komentara je dostignuta. Probaj sutra.", "You have reached the daily comment limit. Try again tomorrow."],
    e_body: ["Komentar mora imati od 1 do 1000 znakova.", "A comment must be 1 to 1000 characters."],
    e_gen: ["Nije uspelo. Pokušaj ponovo.", "That did not work. Please try again."],
    e_code: ["Nepoznat kod. Proveri da li je tačan.", "Unknown code. Check that it is correct."],
    e_name: ["Ime mora imati od 2 do 30 znakova.", "The name must be 2 to 30 characters."],
    m_title: ["Ko si ti?", "Who are you?"],
    m_lead: ["Izaberi ime i sliku. Nema e-pošte ni lozinke. Ime i slika su javni, pa ne moraš da koristiš pravo ime.", "Pick a name and a picture. No email and no password. The name and picture are public, so you do not have to use your real name."],
    m_name: ["Ime ili nadimak", "Name or nickname"],
    m_pick: ["Izaberi sliku", "Choose a picture"],
    m_shuffle: ["Nasumično", "Surprise me"],
    m_go: ["Nastavi", "Continue"],
    m_have: ["Već imam profil: vrati ga kodom", "I already have a profile: restore it with a code"],
    r_title: ["Vrati profil", "Restore your profile"],
    r_lead: ["Unesi kod koji si dobio pri pravljenju profila.", "Enter the code you got when you made the profile."],
    r_code: ["Kod profila", "Profile code"],
    r_go: ["Vrati profil", "Restore"],
    r_back: ["Nazad", "Back"],
    d_title: ["Profil je napravljen", "Profile created"],
    d_lead: ["Sačuvaj ovaj kod. Njime vraćaš profil u drugom pregledaču ili posle brisanja podataka. Pokazuje se samo jednom.", "Save this code. It restores your profile in another browser or after clearing data. It is shown only once."],
    d_copy: ["Kopiraj kod", "Copy code"],
    d_copied: ["Kopirano", "Copied"],
    d_ok: ["Sačuvao sam kod", "I saved the code"],
    p_mine: ["Moji komentari", "My comments"],
    p_nomine: ["Još nema tvojih komentara.", "You have not written any comments yet."],
    p_isrep: ["odgovor", "reply"],
    p_idea: ["Ideja", "Idea"],
    p_edit: ["Ime i slika", "Name and picture"],
    p_hide: ["Sakrij kod", "Hide code"],
    p_code: ["Kod profila", "Profile code"],
    p_show: ["Prikaži kod", "Show code"],
    p_save: ["Sačuvaj promene", "Save changes"],
    p_out: ["Izađi iz profila u ovom pregledaču", "Sign out in this browser"],
    p_outq: ["Izaći iz profila? Kod će ti trebati da se vratiš.", "Sign out? You will need the code to come back."],
    p_rep: ["Odgovori na tvoje komentare", "Replies to your comments"],
    p_norep: ["Još nema odgovora.", "No replies yet."],
    p_on: ["Na tvoj komentar", "On your comment"],
    p_open: ["Otvori ideju", "Open the idea"],
    p_label: ["Profil", "Profile"],
    p_new: ["novi odgovori", "new replies"],
    have: ["Imaš profil? Vrati ga kodom", "Have a profile? Restore it"],
    delq: ["Obrisati komentar? Ne može da se vrati.", "Delete this comment? This cannot be undone."]
  };

  function lang() { return root.dataset.lang === "en" ? "en" : "sr"; }
  function cyr() { return root.classList.contains("cyr") && T; }
  function str(k) { var v = S[k]; return lang() === "en" ? v[1] : (cyr() ? T.toCyr(v[0]) : v[0]); }
  function h(k) { // both languages in the markup, like the rest of the site
    var v = S[k];
    return '<span lang="sr-Latn">' + esc(cyr() ? T.toCyr(v[0]) : v[0]) + '</span><span lang="en">' + esc(v[1]) + "</span>";
  }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function when(iso) {
    try {
      var d = new Date(iso).toLocaleDateString(lang() === "en" ? "en-GB" : "sr-Latn-RS", { day: "numeric", month: "short", year: "numeric" });
      return lang() === "sr" && cyr() ? T.toCyr(d) : d;
    }
    catch (e) { return ""; }
  }

  /* ---------- backend ---------- */
  function rpc(name, args) {
    return fetch(base + name, {
      method: "POST",
      headers: { apikey: cfg.supabaseAnonKey, Authorization: "Bearer " + cfg.supabaseAnonKey, "Content-Type": "application/json" },
      body: JSON.stringify(args || {})
    }).then(function (r) {
      return r.json().catch(function () { return null; }).then(function (j) {
        if (!r.ok) { var e = new Error((j && (j.message || j.hint)) || "http_" + r.status); e.code = (j && j.message) || ""; throw e; }
        return j;
      });
    });
  }
  function errText(e) {
    var c = (e && e.code) || "";
    if (c === "slow_down") return str("e_slow");
    if (c === "daily_limit") return str("e_daily");
    if (c === "bad_body") return str("e_body");
    if (c === "unknown_code") return str("e_code");
    if (c === "bad_name") return str("e_name");
    return str("e_gen");
  }

  /* ---------- profile in this browser ---------- */
  var me = null, replies = [], fresh = false; // fresh: there are replies not seen yet
  try { me = JSON.parse(store.get("dsrb.me") || "null"); } catch (e) { me = null; }
  function setMe(p) {
    me = p;
    if (p) store.set("dsrb.me", JSON.stringify(p));
    else { store.del("dsrb.me"); store.del("dsrb.seenReply"); replies = []; fresh = false; closePop(); }
    paintProfBtn();
  }
  // "seen" is the id of the newest reply the visitor has seen: no clock of the browser is involved
  function lastReplyId() { return replies.reduce(function (m, r) { return Math.max(m, Number(r.id)); }, 0); }

  var profBtn = $("#profBtn");
  if (profBtn) { profBtn.setAttribute("aria-haspopup", "dialog"); profBtn.setAttribute("aria-expanded", "false"); }
  function paintProfBtn() {
    if (!profBtn) return;
    profBtn.hidden = !me;
    if (!me) return;
    profBtn.innerHTML = AV(me.avatar) + '<i class="prof-dot"' + (fresh ? "" : " hidden") + "></i>";
    profBtn.setAttribute("aria-label", str("p_label") + ": " + me.name + (fresh ? " (" + str("p_new") + ")" : ""));
  }

  /* ---------- modal ---------- */
  var overlay = null, modalRender = null, lastFocus = null;
  function closeModal() {
    if (!overlay) return;
    overlay.remove(); overlay = null; modalRender = null;
    document.removeEventListener("keydown", onKey, true);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  function onKey(e) {
    if (!overlay) return;
    if (e.key === "Escape") { e.stopPropagation(); closeModal(); return; }
    if (e.key !== "Tab") return;
    var f = $$("button:not([disabled]), input, textarea, [tabindex]:not([tabindex='-1'])", overlay).filter(function (x) { return x.offsetParent; });
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }
  function openModal(render) {
    if (!overlay) {
      lastFocus = document.activeElement;
      overlay = document.createElement("div");
      overlay.className = "cmodal";
      overlay.innerHTML = '<div class="cmodal-box" role="dialog" aria-modal="true"></div>';
      overlay.addEventListener("mousedown", function (e) { if (e.target === overlay) closeModal(); });
      document.body.appendChild(overlay);
      document.addEventListener("keydown", onKey, true);
    }
    modalRender = render;
    var box = $(".cmodal-box", overlay);
    box.innerHTML = "";
    render(box);
    nameDialog(box);
    var f = $("input, textarea, button.btn", box);
    if (f) f.focus();
  }
  function nameDialog(box) {
    var title = $("h3", box);
    if (title) { title.id = "cmTitle"; box.setAttribute("aria-labelledby", "cmTitle"); }
  }
  function shuffled(n) {
    var a = [], i, j, t;
    for (i = 0; i < n; i++) a.push(i);
    for (i = n - 1; i > 0; i--) { j = Math.floor(Math.random() * (i + 1)); t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  // four random pictures that differ in both shape and colour (n = shape * 10 + colour); "keep" comes first
  function fourAvatars(keep) {
    var shapes = shuffled(5), colours = shuffled(10), out = [keep], i;
    if (keep === undefined) out = [];
    else {
      shapes = shapes.filter(function (x) { return x !== Math.floor(keep / 10); });
      colours = colours.filter(function (x) { return x !== keep % 10; });
    }
    for (i = 0; out.length < 4; i++) out.push(shapes[i] * 10 + colours[i]);
    return out;
  }
  function avatarOptions(list, selected) {
    return list.map(function (n, i) {
      return '<button type="button" class="av-opt" role="radio" aria-checked="' + (n === selected) + '" tabindex="' + (n === selected ? 0 : -1) + '" data-av="' + n + '" aria-label="' + esc(str("m_pick")) + " " + (i + 1) + '">' + AV(n) + "</button>";
    }).join("");
  }
  // the current choice is always one of the four
  function avatarPicker(selected) {
    return '<div class="av-pick"><div class="av-grid" role="radiogroup" aria-label="' + esc(str("m_pick")) + '">' + avatarOptions(fourAvatars(selected), selected) +
      '</div><button type="button" class="linkbtn av-shuffle">' + h("m_shuffle") + "</button></div>";
  }
  function bindPicker(box, state) {
    bindOptions(box, state);
    $(".av-shuffle", box).addEventListener("click", function () {
      var list = fourAvatars();
      // the new choice differs from the old one, so every press visibly changes it
      while (list[0] === state.avatar) list = fourAvatars();
      state.avatar = list[0];
      $(".av-grid", box).innerHTML = avatarOptions(list, state.avatar);
      bindOptions(box, state);
    });
  }
  function bindOptions(box, state) {
    var all = $$(".av-opt", box);
    function pick(b) {
      state.avatar = Number(b.dataset.av);
      all.forEach(function (x) { x.setAttribute("aria-checked", String(x === b)); x.tabIndex = x === b ? 0 : -1; });
    }
    all.forEach(function (b, i) {
      b.addEventListener("click", function () { pick(b); });
      b.addEventListener("keydown", function (e) {
        var step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
        if (!step) return;
        e.preventDefault();
        var next = all[(i + step + all.length) % all.length];
        pick(next); next.focus();
      });
    });
  }

  // resolves with the profile once one exists (made, restored or already there); rejects when the visitor cancels
  function ensureProfile(startWithRestore) {
    if (me) return Promise.resolve(me);
    return new Promise(function (resolve, reject) {
      var done = false;
      function finish(p) { done = true; closeModal(); resolve(p); }
      function stepSetup() {
        openModal(function (box) {
          var st = { avatar: Math.floor(Math.random() * 50) };
          box.innerHTML = "<h3>" + h("m_title") + "</h3><p class=\"cm-lead\">" + h("m_lead") + "</p>" +
            '<label class="cm-lbl">' + h("m_name") + '<input type="text" class="cm-in-name" maxlength="30" autocomplete="nickname"></label>' +
            '<p class="cm-lbl">' + h("m_pick") + "</p>" + avatarPicker(st.avatar) +
            '<p class="cm-msg" role="alert" hidden></p>' +
            '<div class="cm-actions"><button type="button" class="btn go">' + h("m_go") + '</button><button type="button" class="linkbtn cancel">' + h("cancel") + "</button></div>" +
            '<p class="cm-alt"><button type="button" class="linkbtn have">' + h("m_have") + "</button></p>";
          bindPicker(box, st);
          var msg = $(".cm-msg", box), go = $(".go", box);
          $(".cancel", box).addEventListener("click", function () { closeModal(); reject(new Error("cancel")); });
          $(".have", box).addEventListener("click", stepRestore);
          function submit() {
            if (go.disabled) return; // Enter pressed twice must not make two profiles
            var name = $(".cm-in-name", box).value.trim();
            if (name.length < 2) { msg.hidden = false; msg.textContent = str("e_name"); return; }
            go.disabled = true; msg.hidden = true;
            rpc("register_profile", { p_name: name, p_avatar: st.avatar }).then(function (rows) {
              var r = Array.isArray(rows) ? rows[0] : rows;
              setMe({ code: r.code, id: r.id, name: r.name, avatar: r.avatar });
              stepCode(r.code);
            }).catch(function (e) { go.disabled = false; msg.hidden = false; msg.textContent = errText(e); });
          }
          go.addEventListener("click", submit);
          $(".cm-in-name", box).addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); submit(); } });
        });
      }
      function stepCode(code) {
        openModal(function (box) {
          box.innerHTML = "<h3>" + h("d_title") + "</h3><p class=\"cm-lead\">" + h("d_lead") + "</p>" +
            '<p class="cm-code" id="cmCode">' + esc(code) + "</p>" +
            '<div class="cm-actions"><button type="button" class="linkbtn copy">' + h("d_copy") + '</button><button type="button" class="btn ok">' + h("d_ok") + "</button></div>";
          $(".copy", box).addEventListener("click", function (e) {
            var b = e.currentTarget;
            try { navigator.clipboard.writeText(code); } catch (x) { /* ignore */ }
            b.innerHTML = h("d_copied");
          });
          $(".ok", box).addEventListener("click", function () { finish(me); });
        });
      }
      function stepRestore() {
        openModal(function (box) {
          box.innerHTML = "<h3>" + h("r_title") + "</h3><p class=\"cm-lead\">" + h("r_lead") + "</p>" +
            '<label class="cm-lbl">' + h("r_code") + '<input type="text" class="cm-in-code" maxlength="24" autocomplete="off" spellcheck="false" placeholder="XXXX-XXXX-XXXX-XXXX"></label>' +
            '<p class="cm-msg" role="alert" hidden></p>' +
            '<div class="cm-actions"><button type="button" class="btn go">' + h("r_go") + '</button><button type="button" class="linkbtn back">' + h("r_back") + "</button></div>";
          var msg = $(".cm-msg", box), go = $(".go", box), inp = $(".cm-in-code", box);
          $(".back", box).addEventListener("click", stepSetup);
          function submit() {
            if (go.disabled) return;
            var code = inp.value.trim();
            if (code.length < 8) { msg.hidden = false; msg.textContent = str("e_code"); return; }
            go.disabled = true; msg.hidden = true;
            rpc("restore_profile", { p_code: code }).then(function (rows) {
              var r = Array.isArray(rows) ? rows[0] : rows;
              code = (code.toUpperCase().replace(/[^0-9A-Z]/g, "").match(/.{1,4}/g) || []).join("-");
              setMe({ code: code, id: r.id, name: r.name, avatar: r.avatar });
              loadReplies();
              finish(me);
            }).catch(function (e) { go.disabled = false; msg.hidden = false; msg.textContent = errText(e); });
          }
          go.addEventListener("click", submit);
          inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); submit(); } });
        });
      }
      if (startWithRestore) stepRestore(); else stepSetup();
      // closing by Esc or by clicking outside also cancels
      var iv = setInterval(function () { if (!overlay && !done) { clearInterval(iv); if (me) resolve(me); else reject(new Error("cancel")); } else if (done) { clearInterval(iv); } }, 250);
    });
  }

  /* ---------- comments under an idea ---------- */
  var data = {};          // idea -> array of comments
  var counts = {};        // idea -> number
  var open = {};          // idea -> true when its panel is open

  function paintCount(idea) {
    var b = $('[data-cm="' + idea + '"] .ccount');
    if (!b) return;
    var n = counts[idea] || 0;
    b.textContent = n ? n : "";
  }
  function commentHtml(c, idea, isReply) {
    var staff = c.is_staff, mine = me && c.profile_id && c.profile_id === me.id;
    var name = staff ? str("teamName") : (c.name || "?");
    var av = staff ? '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" fill="#E30613"/><circle cx="32" cy="32" r="13" fill="#fff"/></svg>' : AV(c.avatar);
    return '<div class="cm-c' + (isReply ? " rep" : "") + '" data-id="' + c.id + '">' +
      '<span class="cm-av">' + av + "</span><div class=\"cm-b\">" +
      '<p class="cm-h"><strong>' + esc(name) + "</strong>" + (staff ? '<span class="cm-badge">' + h("team") + "</span>" : "") +
      '<time>' + esc(when(c.created_at)) + "</time></p>" +
      '<p class="cm-t">' + esc(c.body) + "</p>" +
      '<p class="cm-a">' + (isReply ? "" : '<button type="button" class="linkbtn" data-reply="' + c.id + '">' + h("reply") + "</button>") +
      (mine ? '<button type="button" class="linkbtn" data-del="' + c.id + '">' + h("del") + "</button>" : "") + "</p>" +
      '<div class="cm-slot" data-slot="' + c.id + '"></div>' +
      (isReply ? "" : '<div class="cm-reps" data-reps="' + c.id + '"></div>') + "</div></div>";
  }
  function formHtml(idea, parent) {
    return '<form class="cm-form" data-idea="' + idea + '"' + (parent ? ' data-parent="' + parent + '"' : "") + ' novalidate>' +
      '<textarea rows="' + (parent ? 2 : 3) + '" maxlength="1000" required placeholder="' + esc(str("ph")) + '" aria-label="' + esc(str("ph")) + '"></textarea>' +
      '<div class="cm-row"><span class="cm-me">' + (me ? '<span class="cm-av sm">' + AV(me.avatar) + "</span>" + h("as") + " <strong>" + esc(me.name) + "</strong>" : h("anon") + ' <button type="button" class="linkbtn" data-restore>' + h("have") + "</button>") + "</span>" +
      '<span class="cm-btns">' + (parent ? '<button type="button" class="linkbtn" data-cancel>' + h("cancel") + "</button>" : "") +
      '<button type="submit" class="btn sm">' + h("send") + "</button></span></div>" +
      '<p class="cm-msg" role="alert" hidden></p></form>';
  }
  function renderPanel(idea) {
    var panel = $("#cm-" + idea);
    if (!panel) return;
    var drafts = $$("form.cm-form", panel).map(function (f) { return { parent: f.dataset.parent || "", text: $("textarea", f).value }; });
    var list = data[idea];
    var html = "";
    if (list === undefined) html = '<p class="cm-note">…</p>';
    else if (list === null) html = '<p class="cm-note">' + h("loadErr") + "</p>";
    else {
      html = list.filter(function (c) { return !c.parent_id; }).length ? "" : '<p class="cm-note">' + h("none") + "</p>";
      var tops = list.filter(function (c) { return !c.parent_id; }).reverse();
      html += '<div class="cm-list">' + tops.map(function (c) { return commentHtml(c, idea, false); }).join("") + "</div>";
    }
    panel.innerHTML = '<div class="cm-wrap">' + html + (list === null ? "" : formHtml(idea) + '<p class="cm-rules">' + h("rules") + "</p>") + "</div>";
    if (list) {
      list.filter(function (c) { return c.parent_id; }).forEach(function (r) {
        var slot = $('[data-reps="' + r.parent_id + '"]', panel);
        if (slot) slot.insertAdjacentHTML("beforeend", commentHtml(r, idea, true));
      });
    }
    drafts.forEach(function (d) {
      var form;
      if (d.parent) {
        var slot = $('[data-slot="' + d.parent + '"]', panel);
        if (!slot) return;
        slot.innerHTML = formHtml(idea, Number(d.parent));
        form = $("form", slot);
      } else form = $(".cm-wrap > .cm-form", panel);
      if (form) $("textarea", form).value = d.text;
    });
  }
  function renderOpen() { Object.keys(open).forEach(function (i) { if (open[i]) renderPanel(Number(i)); }); }
  function load(idea) {
    data[idea] = undefined; renderPanel(idea);
    return rpc("get_comments", { p_idea: idea }).then(function (rows) {
      data[idea] = rows || [];
      // the list holds at most 300 threads; beyond that the number from get_comment_counts stays
      if (data[idea].filter(function (c) { return !c.parent_id; }).length < 300) { counts[idea] = data[idea].length; paintCount(idea); }
    }).catch(function () { data[idea] = null; }).then(function () { renderPanel(idea); });
  }
  function toggle(idea) {
    var panel = $("#cm-" + idea), btn = $('[data-cm="' + idea + '"]');
    var willOpen = panel.hidden;
    panel.hidden = !willOpen;
    btn.setAttribute("aria-expanded", String(willOpen));
    open[idea] = willOpen;
    if (willOpen && data[idea] === undefined) load(idea);
    else if (willOpen) renderPanel(idea);
  }
  function openIdea(idea) {
    var card = $("#idea-" + idea);
    if (!card) return;
    if (card.closest("[hidden]")) { // filtered out: app.js clears the filters for the idea in the address
      history.replaceState(null, "", "#idea-" + idea);
      window.dispatchEvent(new Event("hashchange"));
    }
    if (!open[idea]) toggle(idea);
    card.scrollIntoView({ block: "start" });
  }

  function submitForm(form) {
    var idea = Number(form.dataset.idea), parent = form.dataset.parent ? Number(form.dataset.parent) : null;
    var ta = $("textarea", form), msg = $(".cm-msg", form), sendBtn = $("button[type=submit]", form);
    var body = ta.value.trim();
    msg.hidden = true;
    if (!body) { ta.focus(); return; }
    sendBtn.disabled = true;
    ensureProfile().then(function (p) {
      return rpc("post_comment", { p_code: p.code, p_idea: idea, p_body: body, p_parent: parent });
    }).then(function (rows) {
      var c = Array.isArray(rows) ? rows[0] : rows;
      (data[idea] = data[idea] || []).push(c);
      counts[idea] = (counts[idea] || 0) + 1; paintCount(idea);
      // the sent text must not come back as a draft
      if (parent) form.remove(); else ta.value = "";
      renderOpen();
    }).catch(function (e) {
      sendBtn.disabled = false;
      if (e && e.message === "cancel") return;
      if (e && e.code === "unknown_code") { setMe(null); }
      msg.hidden = false; msg.textContent = errText(e);
    });
  }

  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-cm], [data-reply], [data-del], [data-cancel], [data-restore], #profBtn");
    if (!t) return;
    if (t.matches("[data-restore]")) { ensureProfile(true).then(renderOpen).catch(function () { /* cancelled */ }); return; }
    if (t.matches("[data-cm]")) { toggle(Number(t.dataset.cm)); return; }
    if (t.id === "profBtn") { openProfile(); return; }
    var panel = t.closest(".cm"), idea = panel ? Number(panel.id.replace("cm-", "")) : 0;
    if (t.matches("[data-reply]")) {
      var slot = $('[data-slot="' + t.dataset.reply + '"]', panel);
      if (slot.firstChild) { slot.innerHTML = ""; return; }
      slot.innerHTML = formHtml(idea, Number(t.dataset.reply));
      $("textarea", slot).focus();
    } else if (t.matches("[data-cancel]")) {
      t.closest(".cm-slot").innerHTML = "";
    } else if (t.matches("[data-del]")) {
      var id = Number(t.dataset.del);
      if (!me || !window.confirm(str("delq"))) return;
      rpc("delete_my_comment", { p_code: me.code, p_id: id }).then(function (ok) {
        if (ok === false) throw new Error("not_deleted");
        var before = (data[idea] || []).length;
        data[idea] = (data[idea] || []).filter(function (c) { return c.id !== id && c.parent_id !== id; });
        counts[idea] = Math.max(0, (counts[idea] || 0) - (before - data[idea].length)); paintCount(idea); renderPanel(idea);
      }).catch(function (err) { window.alert(errText(err)); });
    }
  });
  document.addEventListener("submit", function (e) {
    if (e.target.matches(".cm-form")) { e.preventDefault(); submitForm(e.target); }
  });

  /* ---------- profile menu + replies ---------- */
  function loadReplies() {
    if (!me) return Promise.resolve();
    return rpc("get_my_replies", { p_code: me.code }).then(function (rows) {
      replies = rows || [];
      fresh = lastReplyId() > Number(store.get("dsrb.seenReply") || 0);
      paintProfBtn();
      if (pop && popView === "menu") {
        var had = pop.contains(document.activeElement) ? $$("button", pop).indexOf(document.activeElement) : -1;
        renderPop();
        if (had >= 0) $$("button", pop)[had].focus();
      }
    }).catch(function (e) { if (e && e.code === "unknown_code") setMe(null); });
  }
  // the profile menu drops down from the picture in the top bar
  var pop = null, popView = "menu", popState = null; // popState: what the open view has loaded or typed
  var STAFF_AV = '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" fill="#E30613"/><circle cx="32" cy="32" r="13" fill="#fff"/></svg>';

  function icon(name) {
    var d = {
      pencil: "M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z",
      comment: "M21 11.5a8.4 8.4 0 0 1-8.5 8.5 8.9 8.9 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8A8.4 8.4 0 0 1 12.5 3 8.4 8.4 0 0 1 21 11.5z",
      reply: "M9 17l-5-5 5-5M4 12h11a5 5 0 0 1 5 5v2",
      key: "M14.5 14.5a6 6 0 1 0-5-2.7L3 18.3V21h4v-2.5h2.5V16l1.8-1.8a6 6 0 0 0 3.2.3zM16.5 7.5h.01",
      out: "M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"
    }[name];
    return '<svg class="ic ic-' + name + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="' + d + '"/></svg>';
  }
  function closePop(giveFocusBack) {
    if (!pop) return;
    pop.remove(); pop = null; popState = null;
    document.removeEventListener("pointerdown", onOutside, true);
    window.removeEventListener("resize", placePop);
    profBtn.setAttribute("aria-expanded", "false");
    if (giveFocusBack) profBtn.focus();
  }
  function onOutside(e) { if (!pop.contains(e.target) && !profBtn.contains(e.target)) closePop(); }
  // the box lives in <body>: inside the blurred top bar "position:fixed" would be measured from the bar
  function placePop() {
    var r = profBtn.getBoundingClientRect(), top = Math.round(r.bottom + 10);
    pop.style.top = top + "px";
    pop.style.right = Math.max(8, Math.round(root.clientWidth - r.right - 4)) + "px";
    pop.style.maxHeight = "calc(100vh - " + (top + 10) + "px)";
    pop.style.maxHeight = "calc(100dvh - " + (top + 10) + "px)";
  }
  function openProfile() {
    if (!me) return;
    if (pop) { closePop(true); return; }
    pop = document.createElement("div");
    pop.className = "ppop";
    pop.id = "profPop";
    pop.setAttribute("role", "dialog");
    pop.tabIndex = -1;
    pop.addEventListener("click", onPopClick);
    pop.addEventListener("keydown", onPopKey);
    document.body.appendChild(pop);
    document.addEventListener("pointerdown", onOutside, true);
    window.addEventListener("resize", placePop);
    profBtn.setAttribute("aria-expanded", "true");
    placePop();
    showView("menu");
    loadReplies(); // draws the red dot in the menu if something new has come
  }
  function onPopKey(e) {
    if (e.key === "Escape") { e.stopPropagation(); closePop(true); return; }
    if (e.key !== "Tab") return;
    var f = $$("button:not([disabled]):not([tabindex='-1']), input", pop);
    // tabbing past either end closes the menu and goes on from the picture in the top bar
    if (e.shiftKey && (document.activeElement === f[0] || document.activeElement === pop)) { e.preventDefault(); closePop(true); }
    else if (!e.shiftKey && document.activeElement === f[f.length - 1]) closePop(true);
  }
  function showView(view, focusOn) {
    popView = view;
    popState = view === "edit" ? { avatar: me.avatar, name: me.name } : {};
    renderPop();
    pop.scrollTop = 0;
    var f = $(focusOn || (view === "menu" ? ".ppop-item" : ".ppop-back"), pop);
    if (f) f.focus();
    if (view === "mine") loadMine();
    if (view === "replies") {
      var state = popState;
      loadReplies().then(function () {
        if (!pop || popState !== state) return;
        state.loaded = true;
        markSeen(); renderPop(); $(".ppop-back", pop).focus();
      });
    }
  }
  function markSeen() {
    store.set("dsrb.seenReply", String(lastReplyId()));
    fresh = false; paintProfBtn();
  }
  function loadMine() {
    var state = popState;
    rpc("get_my_comments", { p_code: me.code }).then(function (rows) {
      state.list = rows || [];
    }).catch(function (e) {
      if (e && e.code === "unknown_code") setMe(null);
      state.error = true;
    }).then(function () {
      if (pop && popState === state) { renderPop(); $(".ppop-back", pop).focus(); }
    });
  }
  function ideaTitle(n) {
    var card = $("#idea-" + n);
    if (!card) return "";
    if (lang() === "en") return card.getAttribute("data-t-en") || "";
    var t = card.getAttribute("data-t-sr") || "";
    return cyr() ? T.toCyr(t) : t;
  }
  function gotoBtn(idea) {
    return '<button type="button" class="linkbtn" data-goto="' + Number(idea) + '">' + h("p_open") + " № " + Number(idea) + "</button>";
  }
  function mineHtml() {
    if (popState.error) return '<p class="cm-note">' + h("loadErr") + "</p>";
    if (!popState.list) return '<p class="cm-note">…</p>';
    if (!popState.list.length) return '<p class="cm-note">' + h("p_nomine") + "</p>";
    return '<ul class="cm-reps-list">' + popState.list.map(function (c) {
      return "<li><div>" +
        '<p class="cm-on">' + h("p_idea") + " № " + Number(c.idea) + (ideaTitle(c.idea) ? " · " + esc(ideaTitle(c.idea)) : "") + "</p>" +
        '<p class="cm-h"><time>' + esc(when(c.created_at)) + "</time>" + (c.parent_id ? "<span>" + h("p_isrep") + "</span>" : "") + "</p>" +
        '<p class="cm-t">' + esc(c.body) + "</p>" +
        '<p class="cm-a">' + gotoBtn(c.idea) + '<button type="button" class="linkbtn" data-delmine="' + Number(c.id) + '">' + h("del") + "</button></p></div></li>";
    }).join("") + "</ul>";
  }
  function repliesHtml() {
    if (!replies.length) return '<p class="cm-note">' + (popState.loaded ? h("p_norep") : "…") + "</p>";
    return '<ul class="cm-reps-list">' + replies.map(function (r) {
      var staff = r.is_staff;
      return '<li><span class="cm-av sm">' + (staff ? STAFF_AV : AV(r.avatar)) + "</span><div>" +
        '<p class="cm-h"><strong>' + esc(staff ? str("teamName") : r.name) + "</strong><time>" + esc(when(r.created_at)) + "</time></p>" +
        '<p class="cm-t">' + esc(r.body) + '</p><p class="cm-on">' + h("p_on") + ": “" + esc(String(r.parent_body).slice(0, 80)) + "”</p>" +
        gotoBtn(r.idea) + "</div></li>";
    }).join("") + "</ul>";
  }
  function renderPop() {
    if (!pop || !me) return;
    var titles = { mine: "p_mine", replies: "p_rep", edit: "p_edit" };
    var html = popView === "menu"
      ? '<div class="ppop-head">' +
          // the picture, the name and the pencil are one button: it changes both
          '<button type="button" class="ppop-who" data-view="edit" title="' + esc(str("p_edit")) + '" aria-label="' + esc(str("p_edit") + ": " + me.name) + '">' +
            '<span class="cm-av">' + AV(me.avatar) + "</span><strong>" + esc(me.name) + "</strong>" + icon("pencil") + "</button>" +
          '<button type="button" class="ppop-out" data-out title="' + esc(str("p_out")) + '" aria-label="' + esc(str("p_out")) + '">' + icon("out") + "</button></div>" +
        '<button type="button" class="ppop-item" data-view="mine">' + icon("comment") + h("p_mine") + "</button>" +
        '<button type="button" class="ppop-item" data-view="replies">' + icon("reply") + h("p_rep") + (fresh ? '<i class="ppop-dot"></i><span class="sr-only"> (' + h("p_new") + ")</span>" : "") + "</button>" +
        '<button type="button" class="ppop-item" data-code aria-expanded="' + !!popState.code + '">' + icon("key") + h(popState.code ? "p_hide" : "p_show") + "</button>" +
        (popState.code ? '<p class="cm-code">' + esc(me.code) + "</p>" : "")
      : '<div class="ppop-top"><button type="button" class="linkbtn ppop-back" data-view="menu"><span aria-hidden="true">‹ </span>' + h("r_back") + "</button><h3>" + h(titles[popView]) + "</h3></div>" +
        (popView === "mine" ? mineHtml() : popView === "replies" ? repliesHtml()
          : '<label class="cm-lbl">' + h("m_name") + '<input type="text" class="cm-in-name" maxlength="30" value="' + esc(popState.name) + '"></label>' +
            '<p class="cm-lbl">' + h("m_pick") + "</p>" + avatarPicker(popState.avatar) +
            '<p class="cm-msg" role="alert" hidden></p>' +
            '<div class="cm-actions"><button type="button" class="btn sm save">' + h("p_save") + "</button></div>");
    pop.innerHTML = html;
    pop.setAttribute("aria-label", str("p_label") + ": " + me.name);
    if (popView === "edit") {
      var state = popState, inp = $(".cm-in-name", pop);
      bindPicker(pop, state);
      inp.addEventListener("input", function () { state.name = inp.value; });
      inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); saveProfile(); } });
    }
  }
  function saveProfile() {
    var state = popState, msg = $(".cm-msg", pop), btn = $(".save", pop);
    var name = state.name.trim();
    if (btn.disabled) return;
    if (name.length < 2) { msg.hidden = false; msg.textContent = str("e_name"); return; }
    btn.disabled = true; msg.hidden = true;
    rpc("update_profile", { p_code: me.code, p_name: name, p_avatar: state.avatar }).then(function (rows) {
      if (!me) return;
      var r = (Array.isArray(rows) ? rows[0] : rows) || { name: name, avatar: state.avatar };
      setMe({ code: me.code, id: me.id, name: r.name, avatar: r.avatar });
      // comments already on the page show the new name and picture
      Object.keys(data).forEach(function (i) {
        (data[i] || []).forEach(function (c) { if (c.profile_id === me.id) { c.name = r.name; c.avatar = r.avatar; } });
      });
      renderOpen();
      if (pop && popState === state) showView("menu", '[data-view="edit"]');
    }).catch(function (e) { btn.disabled = false; msg.hidden = false; msg.textContent = errText(e); });
  }
  // takes a deleted comment (and, for a thread, its replies) off the page
  function forget(idea, id) {
    var before = (data[idea] || []).length;
    if (!data[idea]) return;
    data[idea] = data[idea].filter(function (c) { return c.id !== id && c.parent_id !== id; });
    counts[idea] = Math.max(0, (counts[idea] || 0) - (before - data[idea].length)); paintCount(idea);
    if (open[idea]) renderPanel(idea);
  }
  function refreshCounts() {
    return rpc("get_comment_counts").then(function (rows) {
      var now = {};
      (rows || []).forEach(function (r) { now[r.idea] = Number(r.n); });
      $$("[data-cm]").forEach(function (b) { var i = Number(b.dataset.cm); counts[i] = now[i] || 0; paintCount(i); });
    }).catch(function () { /* the old numbers stay */ });
  }
  function onPopClick(e) {
    var b = e.target.closest("button");
    if (!b) return;
    if (b.dataset.view) {
      var from = popView;
      showView(b.dataset.view, b.dataset.view === "menu" ? '[data-view="' + from + '"]' : null);
    } else if (b.hasAttribute("data-code")) {
      popState.code = !popState.code; renderPop(); $("[data-code]", pop).focus();
    } else if (b.hasAttribute("data-out")) {
      if (!window.confirm(str("p_outq"))) return;
      setMe(null); renderOpen();
    } else if (b.classList.contains("save")) {
      saveProfile();
    } else if (b.dataset.goto) {
      var n = Number(b.dataset.goto); closePop(); openIdea(n);
    } else if (b.dataset.delmine) {
      var id = Number(b.dataset.delmine), state = popState;
      if (!window.confirm(str("delq"))) return;
      b.disabled = true;
      rpc("delete_my_comment", { p_code: me.code, p_id: id }).then(function (ok) {
        if (ok === false) throw new Error("not_deleted");
        var gone = state.list.filter(function (c) { return c.id === id; })[0];
        state.list = state.list.filter(function (c) { return c.id !== id; });
        if (gone) { forget(gone.idea, id); if (!data[gone.idea]) refreshCounts(); }
        if (pop && popState === state) {
          // replies under a deleted thread disappear too, so the list is asked for again
          loadMine(); renderPop(); $(".ppop-back", pop).focus();
        }
      }).catch(function (err) { b.disabled = false; window.alert(errText(err)); });
    }
  }

  /* ---------- start ---------- */
  $$("[data-cm]").forEach(function (b) { b.hidden = false; });
  paintProfBtn();
  rpc("get_comment_counts").then(function (rows) {
    (rows || []).forEach(function (r) { counts[r.idea] = Number(r.n); paintCount(r.idea); });
  }).catch(function () { /* the buttons simply show no number */ });
  loadReplies();

  // the language or the script changed: redraw what is open
  var viewKey = lang() + cyr();
  new MutationObserver(function () {
    var k = lang() + cyr();
    if (k === viewKey) return;
    viewKey = k;
    paintProfBtn();
    renderOpen();
    renderPop();
    if (overlay && modalRender) { var box = $(".cmodal-box", overlay); box.innerHTML = ""; modalRender(box); nameDialog(box); }
  }).observe(root, { attributes: true, attributeFilter: ["data-lang", "class"] });
})();
