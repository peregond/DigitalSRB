/* Comments under every idea, anonymous profiles (name + one of 50 avatars + a recovery code).
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
    p_title: ["Moj profil", "My profile"],
    p_code: ["Kod profila", "Profile code"],
    p_show: ["Prikaži kod", "Show code"],
    p_save: ["Sačuvaj promene", "Save changes"],
    p_out: ["Izađi iz profila u ovom pregledaču", "Sign out in this browser"],
    p_outq: ["Izaći iz profila? Kod će ti trebati da se vratiš.", "Sign out? You will need the code to come back."],
    p_rep: ["Odgovori na tvoje komentare", "Replies to your comments"],
    p_norep: ["Još nema odgovora.", "No replies yet."],
    p_on: ["Na tvoj komentar", "On your comment"],
    p_open: ["Otvori ideju", "Open the idea"],
    close: ["Zatvori", "Close"],
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
    else { store.del("dsrb.me"); store.del("dsrb.seenReply"); replies = []; fresh = false; }
    paintProfBtn();
  }
  // "seen" is the id of the newest reply the visitor has seen: no clock of the browser is involved
  function lastReplyId() { return replies.reduce(function (m, r) { return Math.max(m, Number(r.id)); }, 0); }

  var profBtn = $("#profBtn");
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
  function avatarGrid(selected) {
    var out = '<div class="av-grid" role="radiogroup" aria-label="' + esc(str("m_pick")) + '">';
    for (var i = 0; i < 50; i++) {
      out += '<button type="button" class="av-opt" role="radio" aria-checked="' + (i === selected) + '" tabindex="' + (i === selected ? 0 : -1) + '" data-av="' + i + '" aria-label="' + (i + 1) + '">' + AV(i) + "</button>";
    }
    return out + "</div>";
  }
  function bindGrid(box, state) {
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
            '<p class="cm-lbl">' + h("m_pick") + "</p>" + avatarGrid(st.avatar) +
            '<p class="cm-msg" role="alert" hidden></p>' +
            '<div class="cm-actions"><button type="button" class="btn go">' + h("m_go") + '</button><button type="button" class="linkbtn cancel">' + h("cancel") + "</button></div>" +
            '<p class="cm-alt"><button type="button" class="linkbtn have">' + h("m_have") + "</button></p>";
          bindGrid(box, st);
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

  /* ---------- profile window + replies ---------- */
  function loadReplies() {
    if (!me) return Promise.resolve();
    return rpc("get_my_replies", { p_code: me.code }).then(function (rows) {
      replies = rows || [];
      fresh = lastReplyId() > Number(store.get("dsrb.seenReply") || 0);
      paintProfBtn();
    }).catch(function (e) { if (e && e.code === "unknown_code") setMe(null); });
  }
  function openProfile() {
    if (!me) return;
    loadReplies().then(function () {
      if (!me) return; // the server no longer knows this code
      store.set("dsrb.seenReply", String(lastReplyId()));
      fresh = false; paintProfBtn();
      openModal(function (box) {
        var st = { avatar: me.avatar };
        var list = replies.length ? replies.map(function (r) {
          var staff = r.is_staff;
          return '<li><span class="cm-av sm">' + (staff ? '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" fill="#E30613"/><circle cx="32" cy="32" r="13" fill="#fff"/></svg>' : AV(r.avatar)) + "</span><div>" +
            '<p class="cm-h"><strong>' + esc(staff ? str("teamName") : r.name) + "</strong><time>" + esc(when(r.created_at)) + "</time></p>" +
            '<p class="cm-t">' + esc(r.body) + '</p><p class="cm-on">' + h("p_on") + ": “" + esc(String(r.parent_body).slice(0, 80)) + '”</p>' +
            '<button type="button" class="linkbtn" data-goto="' + r.idea + '">' + h("p_open") + " № " + r.idea + "</button></div></li>";
        }).join("") : '<li class="empty">' + h("p_norep") + "</li>";
        box.innerHTML = "<h3>" + h("p_title") + "</h3>" +
          '<label class="cm-lbl">' + h("m_name") + '<input type="text" class="cm-in-name" maxlength="30" value="' + esc(me.name) + '"></label>' +
          '<p class="cm-lbl">' + h("m_pick") + "</p>" + avatarGrid(me.avatar) +
          '<p class="cm-msg" role="alert" hidden></p>' +
          '<div class="cm-actions"><button type="button" class="btn save">' + h("p_save") + '</button><button type="button" class="linkbtn showcode">' + h("p_show") + '</button></div>' +
          '<p class="cm-code" hidden>' + esc(me.code) + "</p>" +
          '<h4>' + h("p_rep") + '</h4><ul class="cm-reps-list">' + list + "</ul>" +
          '<div class="cm-actions end"><button type="button" class="linkbtn out">' + h("p_out") + '</button><button type="button" class="linkbtn close">' + h("close") + "</button></div>";
        bindGrid(box, st);
        var msg = $(".cm-msg", box);
        $(".close", box).addEventListener("click", closeModal);
        $(".showcode", box).addEventListener("click", function () { $(".cm-code", box).hidden = false; });
        $(".out", box).addEventListener("click", function () {
          if (!window.confirm(str("p_outq"))) return;
          setMe(null); closeModal(); renderOpen();
        });
        $(".save", box).addEventListener("click", function () {
          var name = $(".cm-in-name", box).value.trim();
          if (name.length < 2) { msg.hidden = false; msg.textContent = str("e_name"); return; }
          rpc("update_profile", { p_code: me.code, p_name: name, p_avatar: st.avatar }).then(function (rows) {
            var r = (Array.isArray(rows) ? rows[0] : rows) || { name: name, avatar: st.avatar };
            setMe({ code: me.code, id: me.id, name: r.name, avatar: r.avatar });
            // comments already on the page show the new name and picture
            Object.keys(data).forEach(function (i) {
              (data[i] || []).forEach(function (c) { if (c.profile_id === me.id) { c.name = r.name; c.avatar = r.avatar; } });
            });
            closeModal(); renderOpen();
          }).catch(function (e) { msg.hidden = false; msg.textContent = errText(e); });
        });
        box.addEventListener("click", function (e) {
          var g = e.target.closest("[data-goto]");
          if (g) { var n = Number(g.dataset.goto); closeModal(); openIdea(n); }
        });
      });
    });
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
    if (overlay && modalRender) { var box = $(".cmodal-box", overlay); box.innerHTML = ""; modalRender(box); nameDialog(box); }
  }).observe(root, { attributes: true, attributeFilter: ["data-lang", "class"] });
})();
