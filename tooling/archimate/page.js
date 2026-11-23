(() => {
  const root = document.documentElement;
  const store = { get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
  // theme
  const themeBtns = document.querySelectorAll('[data-theme-set]');
  const setTheme = (t) => {
    if (t === 'system') root.removeAttribute('data-theme'); else root.setAttribute('data-theme', t);
    themeBtns.forEach(b => b.setAttribute('aria-checked', String(b.dataset.themeSet === t)));
    store.set('ax-theme', t);
  };
  themeBtns.forEach(b => b.addEventListener('click', () => setTheme(b.dataset.themeSet)));
  const saved = store.get('ax-theme'); if (saved && saved !== 'system') setTheme(saved);
  // radio groups: arrow keys
  document.querySelectorAll('[role="radiogroup"]').forEach(g => g.addEventListener('keydown', e => {
    if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) return;
    const bs = [...g.querySelectorAll('[role="radio"]')]; const i = bs.indexOf(document.activeElement); if (i < 0) return;
    const n = bs[(i + (e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? bs.length - 1 : 1)) % bs.length]; n.focus(); n.click(); e.preventDefault();
  }));
  // renderer switch per kind
  document.querySelectorAll('.kind').forEach(k => {
    k.querySelectorAll('[data-set-r]').forEach(b => b.addEventListener('click', () => {
      k.dataset.r = b.dataset.setR;
      k.querySelectorAll('[data-set-r]').forEach(x => x.setAttribute('aria-checked', String(x === b)));
    }));
    const fit = k.querySelector('.fit'), body = k.querySelector('.dg-body');
    fit.addEventListener('click', () => {
      const on = body.classList.toggle('fit');
      fit.setAttribute('aria-pressed', String(on)); fit.textContent = on ? 'Fit width' : 'Actual size';
    });
  });
  // copy
  const snack = document.getElementById('snack'); let tt;
  const say = m => { snack.textContent = m; snack.hidden = false; clearTimeout(tt); tt = setTimeout(() => { snack.hidden = true; }, 2500); };
  document.querySelectorAll('[data-copy]').forEach(b => b.addEventListener('click', async () => {
    const t = b.parentElement.querySelector('code').textContent;
    try { await navigator.clipboard.writeText(t); say('Copied'); } catch (e) { say('Copy is blocked here: select the text and copy it'); }
  }));
  // element filter
  const q = document.getElementById('q'), chips = document.querySelectorAll('.chips [data-f]'), empty = document.getElementById('empty');
  let f = 'all';
  const apply = () => {
    const s = (q.value || '').trim().toLowerCase(); let shown = 0; const seen = {};
    document.querySelectorAll('table.els tbody tr').forEach(tr => {
      if (tr.classList.contains('lay')) return;
      const ok = (f === 'all' || (f === 'model' ? tr.dataset.model === 'true' : tr.dataset.layer === f)) && (!s || tr.dataset.q.includes(s));
      tr.hidden = !ok; if (ok) { shown++; seen[tr.dataset.layer] = true; }
    });
    document.querySelectorAll('table.els tr.lay').forEach(tr => { tr.hidden = !seen[tr.dataset.layer]; });
    empty.hidden = shown > 0;
  };
  chips.forEach(c => c.addEventListener('click', () => { f = c.dataset.f; chips.forEach(x => x.setAttribute('aria-pressed', String(x === c))); apply(); }));
  q.addEventListener('input', apply);
})();
