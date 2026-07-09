/* Darak Group — shared glassmorphic contact popup.
   Every /contact/ link opens this popup EXCEPT the one in the footer,
   which remains the only way to reach the full contact page. */
(function () {
  'use strict';
  if (window.__dcmInit) return; window.__dcmInit = true;

  var CARET = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='9' fill='none'%3E%3Cpath d='M1 1l6 6 6-6' stroke='%2369c9c4' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E";

  var css = ''
  + '.dcm-overlay{position:fixed;inset:0;z-index:100000;display:flex;align-items:center;justify-content:center;'
  +   'padding:24px;opacity:0;visibility:hidden;transition:opacity .4s ease,visibility .4s ease;'
  +   'background:radial-gradient(130% 120% at 50% 0%,rgba(0,45,43,.42),rgba(0,31,29,.62));'
  +   '-webkit-backdrop-filter:blur(9px);backdrop-filter:blur(9px);'
  +   "font-family:'Avenir Next LT Pro','Helvetica Neue',Arial,sans-serif;}"
  + '.dcm-overlay.is-open{opacity:1;visibility:visible;}'
  + '.dcm-card{position:relative;width:min(490px,100%);max-height:92vh;overflow-y:auto;overflow-x:hidden;border-radius:24px;'
  +   'padding:clamp(26px,4vw,42px);color:#06201e;isolation:isolate;overscroll-behavior:contain;'
  +   'background:linear-gradient(158deg,rgba(255,255,255,.86),rgba(228,246,244,.74));'
  +   '-webkit-backdrop-filter:blur(28px) saturate(1.4);backdrop-filter:blur(28px) saturate(1.4);'
  +   'border:1px solid rgba(105,201,196,.55);box-shadow:0 34px 90px rgba(0,31,29,.42);'
  +   'transform:translateY(20px) scale(.97);transition:transform .5s cubic-bezier(.16,1,.3,1);}'
  /* custom themed scrollbar (no native browser bar, never horizontal) */
  + '.dcm-card{scrollbar-width:thin;scrollbar-color:rgba(64,123,120,.55) transparent;}'
  + '.dcm-card::-webkit-scrollbar{width:8px;height:0;}'
  + '.dcm-card::-webkit-scrollbar-track{background:transparent;margin:14px 0;}'
  + '.dcm-card::-webkit-scrollbar-thumb{border-radius:999px;background:linear-gradient(180deg,#69c9c4,#407b78);'
  +   'border:2px solid transparent;background-clip:padding-box;}'
  + '.dcm-card::-webkit-scrollbar-thumb:hover{background:linear-gradient(180deg,#5bbbb6,#356b68);background-clip:padding-box;}'
  + '.dcm-card::-webkit-scrollbar-button{display:none;height:0;width:0;}'
  /* desktop with room to spare: size to content, no scroll at all */
  + '@media (min-width:600px) and (min-height:680px){.dcm-card{max-height:none;overflow:visible;}}'
  + '.dcm-overlay.is-open .dcm-card{transform:none;}'
  + '.dcm-card::before{content:"";position:absolute;z-index:-1;top:-40%;right:-30%;width:70%;height:70%;border-radius:50%;'
  +   'background:radial-gradient(circle,rgba(105,201,196,.5),transparent 70%);filter:blur(10px);pointer-events:none;}'
  + '.dcm-card::after{content:"";position:absolute;z-index:-1;bottom:-35%;left:-25%;width:60%;height:60%;border-radius:50%;'
  +   'background:radial-gradient(circle,rgba(64,123,120,.4),transparent 70%);filter:blur(12px);pointer-events:none;}'
  + '.dcm-close{position:absolute;top:14px;right:14px;width:38px;height:38px;border-radius:50%;cursor:pointer;'
  +   'border:1px solid rgba(0,45,43,.18);background:rgba(255,255,255,.5);color:#002d2b;font-size:19px;line-height:1;'
  +   'display:flex;align-items:center;justify-content:center;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);'
  +   'transition:background .3s,color .3s,transform .3s;}'
  + '.dcm-close:hover{background:#002d2b;color:#69c9c4;transform:rotate(90deg);}'
  + '.dcm-eyebrow{display:inline-flex;align-items:center;gap:9px;font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:#407b78;font-weight:600;}'
  + '.dcm-eyebrow::before{content:"";width:8px;height:8px;border-radius:50%;background:#69c9c4;}'
  + '.dcm-title{font-family:"novantique-serif",Georgia,serif;font-weight:400;font-size:clamp(27px,4vw,38px);color:#002d2b;margin:12px 0 6px;line-height:1.04;}'
  + '.dcm-sub{font-size:14px;color:#3c5b58;margin:0 0 22px;line-height:1.5;}'
  + '.dcm-field{margin-bottom:14px;}'
  + '.dcm-field label{display:block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#407b78;margin-bottom:7px;font-weight:600;}'
  + '.dcm-field input{width:100%;box-sizing:border-box;padding:12px 14px;border-radius:12px;'
  +   'border:1px solid rgba(0,45,43,.18);background:rgba(255,255,255,.55);color:#06201e;font:inherit;font-size:15px;'
  +   '-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);transition:border-color .25s,box-shadow .25s,background .25s;}'
  + '.dcm-field input::placeholder{color:rgba(64,123,120,.6);}'
  + '.dcm-field input:focus{outline:none;border-color:#407b78;box-shadow:0 0 0 3px rgba(105,201,196,.32);'
  +   'background:rgba(255,255,255,.82);caret-color:#69c9c4;}'
  /* custom glass dropdown (replaces the native <select>) */
  + '.dcm-combo{position:relative;}'
  + '.dcm-select{width:100%;box-sizing:border-box;display:flex;align-items:center;justify-content:space-between;gap:10px;'
  +   'padding:12px 14px;border-radius:12px;border:1px solid rgba(0,45,43,.18);background:rgba(255,255,255,.55);'
  +   'color:#06201e;font:inherit;font-size:15px;text-align:left;cursor:pointer;'
  +   '-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);transition:border-color .25s,box-shadow .25s,background .25s;}'
  + '.dcm-select:hover{border-color:rgba(64,123,120,.5);}'
  + '.dcm-select.placeholder .dcm-select-val{color:rgba(64,123,120,.6);}'
  + '.dcm-select:focus-visible,.dcm-select[aria-expanded="true"]{outline:none;border-color:#407b78;box-shadow:0 0 0 3px rgba(105,201,196,.32);background:rgba(255,255,255,.82);}'
  + '.dcm-caret{flex:0 0 auto;width:14px;height:9px;color:#407b78;display:flex;transition:transform .3s ease;}'
  + '.dcm-select[aria-expanded="true"] .dcm-caret{transform:rotate(180deg);}'
  + '.dcm-options{position:absolute;top:calc(100% + 8px);left:0;right:0;z-index:5;margin:0;padding:6px;list-style:none;'
  +   'border-radius:14px;border:1px solid rgba(105,201,196,.5);'
  +   'background:linear-gradient(160deg,rgba(255,255,255,.93),rgba(228,246,244,.85));'
  +   '-webkit-backdrop-filter:blur(24px) saturate(1.4);backdrop-filter:blur(24px) saturate(1.4);'
  +   'box-shadow:0 22px 50px rgba(0,31,29,.32);'
  +   'opacity:0;visibility:hidden;transform:translateY(-6px);transition:opacity .25s ease,transform .25s ease,visibility .25s ease;}'
  + '.dcm-options.on{opacity:1;visibility:visible;transform:none;}'
  + '.dcm-options--up{top:auto;bottom:calc(100% + 8px);}'
  + '.dcm-option{padding:11px 13px;border-radius:9px;font-size:15px;color:#06201e;cursor:pointer;'
  +   'display:flex;align-items:center;justify-content:space-between;gap:10px;transition:background .2s,color .2s;}'
  + '.dcm-option:hover,.dcm-option.active{background:rgba(105,201,196,.22);color:#002d2b;}'
  + '.dcm-option[aria-selected="true"]{color:#002d2b;font-weight:600;}'
  + '.dcm-option[aria-selected="true"]::after{content:"";width:7px;height:7px;border-radius:50%;background:#69c9c4;flex:0 0 auto;}'
  + '.dcm-submit{margin-top:6px;width:100%;display:inline-flex;align-items:center;justify-content:space-between;gap:14px;'
  +   'border:none;cursor:pointer;border-radius:999px;padding:7px 7px 7px 24px;font:inherit;font-size:13px;font-weight:600;'
  +   'letter-spacing:.14em;text-transform:uppercase;color:#f4f8f7;'
  +   'background:linear-gradient(120deg,#002d2b,#407b78);box-shadow:0 12px 30px rgba(0,45,43,.3);'
  +   'transition:transform .3s,box-shadow .3s;}'
  + '.dcm-submit:hover{transform:translateY(-2px);box-shadow:0 16px 38px rgba(0,45,43,.4);}'
  + '.dcm-submit .dcm-ico{flex:0 0 auto;width:40px;height:40px;border-radius:50%;background:#69c9c4;color:#001f1d;'
  +   'display:flex;align-items:center;justify-content:center;transition:transform .35s;}'
  + '.dcm-submit:hover .dcm-ico{transform:translateX(3px) rotate(0);}'
  + '.dcm-success{display:none;text-align:center;padding:18px 4px 6px;}'
  + '.dcm-success.on{display:block;}'
  + '.dcm-success .dcm-check{width:60px;height:60px;border-radius:50%;margin:0 auto 18px;display:flex;align-items:center;justify-content:center;'
  +   'background:rgba(105,201,196,.22);color:#002d2b;}'
  + '.dcm-success h3{font-family:"novantique-serif",Georgia,serif;font-weight:400;font-size:26px;color:#002d2b;margin:0 0 8px;}'
  + '.dcm-success p{font-size:14px;color:#3c5b58;margin:0;line-height:1.5;}'
  + 'body.dcm-lock{overflow:hidden;}'
  + '@media (prefers-reduced-motion:reduce){.dcm-overlay,.dcm-card,.dcm-close,.dcm-submit,.dcm-submit .dcm-ico{transition:none;}}';

  var ARROW = '<svg viewBox="0 0 14 14" width="13" height="13" fill="none"><path d="M2 12 12 2M12 2H5M12 2v7" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  var html = ''
  + '<div class="dcm-overlay" id="dcmOverlay" role="dialog" aria-modal="true" aria-labelledby="dcmTitle" aria-hidden="true">'
  +   '<div class="dcm-card">'
  +     '<button class="dcm-close" type="button" aria-label="Close">&times;</button>'
  +     '<span class="dcm-eyebrow">Get in touch</span>'
  +     '<h2 class="dcm-title" id="dcmTitle">Let&rsquo;s talk</h2>'
  +     '<p class="dcm-sub">Share a few details and our team will be in touch shortly.</p>'
  +     '<form class="dcm-form" novalidate>'
  +       '<div class="dcm-field"><label for="dcmName">Name</label><input id="dcmName" type="text" name="name" required placeholder="Your name"></div>'
  +       '<div class="dcm-field"><label for="dcmEmail">Email</label><input id="dcmEmail" type="email" name="email" required placeholder="you@email.com"></div>'
  +       '<div class="dcm-field"><label for="dcmPhone">Phone number</label><input id="dcmPhone" type="tel" name="phone" placeholder="+20 ..."></div>'
  +       '<div class="dcm-field"><label for="dcmBudget">Budget</label><input id="dcmBudget" type="text" name="budget" placeholder="e.g. EGP 5 – 8M"></div>'
  +       '<div class="dcm-field"><label id="dcmProjLabel">Project you&rsquo;re interested in</label>'
  +         '<div class="dcm-combo">'
  +           '<button type="button" class="dcm-select placeholder" id="dcmProject" aria-haspopup="listbox" aria-expanded="false" aria-labelledby="dcmProjLabel dcmProject">'
  +             '<span class="dcm-select-val">Select a project</span>'
  +             '<span class="dcm-caret" aria-hidden="true"><svg viewBox="0 0 14 9" width="14" height="9" fill="none"><path d="M1 1l6 6 6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
  +           '</button>'
  +           '<ul class="dcm-options" role="listbox" aria-labelledby="dcmProjLabel" tabindex="-1">'
  +             '<li class="dcm-option" role="option" aria-selected="false" data-val="Crystal Alamein">Crystal Alamein</li>'
  +             '<li class="dcm-option" role="option" aria-selected="false" data-val="Marina Eye Residence">Marina Eye Residence</li>'
  +             '<li class="dcm-option" role="option" aria-selected="false" data-val="Not sure yet">Not sure yet</li>'
  +           '</ul>'
  +           '<input type="hidden" name="project" id="dcmProjectInput">'
  +         '</div></div>'
  +       '<button class="dcm-submit" type="submit">Send enquiry <span class="dcm-ico" aria-hidden="true">' + ARROW + '</span></button>'
  +     '</form>'
  +     '<div class="dcm-success"><div class="dcm-check"><svg viewBox="0 0 24 24" width="28" height="28" fill="none"><path d="M5 13l4 4 10-11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
  +       '<h3>Almost there</h3><p>Your enquiry is ready in your email app &mdash; just press send and our team will be in touch shortly.</p></div>'
  +   '</div>'
  + '</div>';

  function init() {
    var style = document.createElement('style'); style.id = 'dcm-style'; style.textContent = css;
    document.head.appendChild(style);
    var holder = document.createElement('div'); holder.innerHTML = html;
    var overlay = holder.firstChild; document.body.appendChild(overlay);

    var card = overlay.querySelector('.dcm-card');
    var form = overlay.querySelector('.dcm-form');
    var success = overlay.querySelector('.dcm-success');
    var lastFocus = null;

    // ---- custom glass dropdown ----
    var combo = overlay.querySelector('.dcm-combo');
    var selBtn = combo.querySelector('.dcm-select');
    var valSpan = combo.querySelector('.dcm-select-val');
    var list = combo.querySelector('.dcm-options');
    var opts = Array.prototype.slice.call(combo.querySelectorAll('.dcm-option'));
    var hiddenInput = combo.querySelector('#dcmProjectInput');
    var activeIdx = -1;
    opts.forEach(function (o, i) { o.id = 'dcmOpt' + i; });
    function comboSetActive(i) {
      opts.forEach(function (o, idx) { o.classList.toggle('active', idx === i); });
      activeIdx = i;
      if (i >= 0) { list.setAttribute('aria-activedescendant', opts[i].id); opts[i].scrollIntoView({ block: 'nearest' }); }
      else list.removeAttribute('aria-activedescendant');
    }
    function comboOpen() {
      // open upward if there isn't room below within the card (avoids clipping)
      var cardR = card.getBoundingClientRect(), btnR = selBtn.getBoundingClientRect();
      var needed = Math.min(opts.length, 5) * 46 + 20;
      var below = cardR.bottom - btnR.bottom;
      list.classList.toggle('dcm-options--up', below < needed && (btnR.top - cardR.top) > below);
      list.classList.add('on'); selBtn.setAttribute('aria-expanded', 'true');
      var sel = opts.findIndex(function (o) { return o.getAttribute('aria-selected') === 'true'; });
      comboSetActive(sel >= 0 ? sel : 0);
    }
    function comboClose(focusBtn) {
      list.classList.remove('on'); selBtn.setAttribute('aria-expanded', 'false'); comboSetActive(-1);
      if (focusBtn) selBtn.focus();
    }
    function comboChoose(i) {
      var o = opts[i]; if (!o) return;
      opts.forEach(function (x) { x.setAttribute('aria-selected', 'false'); });
      o.setAttribute('aria-selected', 'true');
      hiddenInput.value = o.getAttribute('data-val');
      valSpan.textContent = o.textContent; selBtn.classList.remove('placeholder');
      comboClose(true);
    }
    function comboReset() {
      opts.forEach(function (x) { x.setAttribute('aria-selected', 'false'); });
      hiddenInput.value = ''; valSpan.textContent = 'Select a project'; selBtn.classList.add('placeholder');
      comboClose(false);
    }
    selBtn.addEventListener('click', function () { list.classList.contains('on') ? comboClose(true) : comboOpen(); });
    opts.forEach(function (o, i) {
      o.addEventListener('click', function () { comboChoose(i); });
      o.addEventListener('mousemove', function () { comboSetActive(i); });
    });
    selBtn.addEventListener('keydown', function (e) {
      var isOpen = list.classList.contains('on');
      if (!isOpen && (e.key === 'ArrowDown' || e.key === 'ArrowUp' || e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); comboOpen(); return; }
      if (!isOpen) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); comboSetActive(Math.min(opts.length - 1, activeIdx + 1)); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); comboSetActive(Math.max(0, activeIdx - 1)); }
      else if (e.key === 'Home') { e.preventDefault(); comboSetActive(0); }
      else if (e.key === 'End') { e.preventDefault(); comboSetActive(opts.length - 1); }
      else if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); if (activeIdx >= 0) comboChoose(activeIdx); }
      else if (e.key === 'Escape') { e.stopPropagation(); comboClose(true); }
    });
    overlay.addEventListener('click', function (e) { if (list.classList.contains('on') && !combo.contains(e.target)) comboClose(false); });

    function open() {
      lastFocus = document.activeElement;
      form.style.display = ''; success.classList.remove('on'); form.reset(); comboReset();
      overlay.classList.add('is-open'); overlay.setAttribute('aria-hidden', 'false');
      document.body.classList.add('dcm-lock');
      var f = overlay.querySelector('input:not([type=hidden])'); if (f) setTimeout(function () { f.focus(); }, 80);
    }
    function close() {
      overlay.classList.remove('is-open'); overlay.setAttribute('aria-hidden', 'true');
      document.body.classList.remove('dcm-lock');
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }
    window.__darakOpenContact = open;

    overlay.addEventListener('click', function (e) { if (e.target === overlay) close(); });
    overlay.querySelector('.dcm-close').addEventListener('click', close);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay.classList.contains('is-open')) close();
    });
    // simple focus trap
    overlay.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab') return;
      var f = overlay.querySelectorAll('button,input:not([type=hidden]),a[href]');
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.reportValidity && !form.reportValidity()) return;

      // craft the enquiry into an email and hand it to the user's mail client
      var get = function (n) { var el = form.querySelector('[name="' + n + '"]'); return el && el.value ? el.value.trim() : ''; };
      var name = get('name'), email = get('email'), phone = get('phone'), budget = get('budget'), project = get('project');
      var subject = 'New enquiry from ' + (name || 'website visitor');
      var lines = [
        'Name: ' + (name || '—'),
        'Email: ' + (email || '—'),
        'Phone: ' + (phone || '—'),
        'Budget: ' + (budget || '—'),
        'Project of interest: ' + (project || '—'),
        '',
        'Sent from the Darak Group website.'
      ];
      var mailto = 'mailto:info@darak-group.com'
        + '?subject=' + encodeURIComponent(subject)
        + '&body=' + encodeURIComponent(lines.join('\r\n'));
      window.location.href = mailto;

      form.style.display = 'none'; success.classList.add('on');
    });

    // intercept every contact link except the footer one
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a'); if (!a) return;
      if (a.closest('footer')) return;            // footer link -> real contact page
      var h = a.getAttribute('href') || '';
      if (h === '/contact/' || h === '/contact' || /\/contact\/(index\.html)?$/.test(h)) {
        e.preventDefault(); open();
      }
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

/* Darak Group — floating WhatsApp contact button (site-wide).
   On the homepage it stays hidden until the preloader animation finishes
   (the 'oh:preloaded' event); everywhere else it reveals straight away. */
(function () {
  'use strict';
  if (window.__dwaInit) return; window.__dwaInit = true;

  var PHONE = '201099890811';            // +20 10 99890811
  var HREF  = 'https://wa.me/' + PHONE + '?text=' + encodeURIComponent("Hello Darak Group, I'd like to know more about your projects.");

  var css = ''
  + '.dwa-btn{position:fixed;right:clamp(16px,3vw,28px);bottom:clamp(16px,3vw,28px);z-index:99990;'
  +   'width:60px;height:60px;border-radius:50%;display:flex;align-items:center;justify-content:center;'
  +   'background:linear-gradient(145deg,#25d366,#128c4b);color:#fff;text-decoration:none;'
  +   'box-shadow:0 12px 30px rgba(18,140,75,.4),0 4px 10px rgba(0,0,0,.18);'
  +   'opacity:0;visibility:hidden;transform:translateY(16px) scale(.85);'
  +   'transition:opacity .5s cubic-bezier(.16,1,.3,1),transform .5s cubic-bezier(.16,1,.3,1),box-shadow .3s;}'
  + '.dwa-btn.is-in{opacity:1;visibility:visible;transform:none;}'
  + '.dwa-btn:hover{transform:translateY(-3px) scale(1.05);box-shadow:0 18px 40px rgba(18,140,75,.5),0 6px 14px rgba(0,0,0,.2);}'
  + '.dwa-btn svg{width:32px;height:32px;display:block;fill:#fff;color:#fff;}'
  + '.dwa-btn svg path{fill:#fff;}'
  + '.dwa-btn::before{content:"";position:absolute;inset:0;border-radius:50%;background:#25d366;z-index:-1;'
  +   'animation:dwaPulse 2.6s ease-out infinite;}'
  + '@keyframes dwaPulse{0%{transform:scale(1);opacity:.5;}70%{transform:scale(1.6);opacity:0;}100%{opacity:0;}}'
  + '@media (prefers-reduced-motion:reduce){.dwa-btn,.dwa-btn::before{animation:none;transition:opacity .3s;}}';

  var ICON = '<svg viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path fill="#fff" d="M19.05 4.91A9.82 9.82 0 0 0 12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.91-7.02ZM12.04 20.15h-.01a8.2 8.2 0 0 1-4.18-1.15l-.3-.18-3.11.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.24-8.24a8.2 8.2 0 0 1 5.82 2.42 8.18 8.18 0 0 1 2.41 5.83c0 4.54-3.69 8.4-8.24 8.4Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.39.11-.51.11-.11.25-.29.37-.43.13-.14.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.23.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.14-1.18-.06-.11-.22-.17-.47-.29Z"/></svg>';

  function init() {
    var style = document.createElement('style'); style.id = 'dwa-style'; style.textContent = css;
    document.head.appendChild(style);

    var a = document.createElement('a');
    a.className = 'dwa-btn'; a.href = HREF; a.target = '_blank'; a.rel = 'noopener noreferrer';
    a.setAttribute('aria-label', 'Chat with us on WhatsApp');
    a.innerHTML = ICON;
    document.body.appendChild(a);

    function reveal() { requestAnimationFrame(function () { a.classList.add('is-in'); }); }

    // Homepage: a preloader is present — wait for it to finish.
    var hasPreloader = document.getElementById('ohPreloader') || document.body.classList.contains('oh-preloader-active');
    if (hasPreloader) {
      document.addEventListener('oh:preloaded', function () { setTimeout(reveal, 400); }, { once: true });
      // safety net in case the event never fires
      setTimeout(function () { if (!a.classList.contains('is-in')) reveal(); }, 9000);
    } else {
      setTimeout(reveal, 600);
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
