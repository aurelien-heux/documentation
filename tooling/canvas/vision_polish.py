"""Cross-cutting polish applied to the assembled production vision (after the parts are merged, before the markup check):
accessibility structure (h1, skip link, named action columns, scrollable diagrams), keyboard layers (Escape closes the top
layer and returns focus, focus moves into a dialog, arrow keys in tablists), floors (11 px text, 24 px targets), reduced
motion, and the removal of duplicate entry points (header assistant icon, cookie item)."""
import re
import vision_theme

A11Y_CSS = r"""
.sr-only{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.skip{position:absolute;left:16px;top:-48px;z-index:40;height:40px;padding:0 16px;border-radius:16px;background:#35307E;color:#FFFFFF;font:600 14px/40px Manrope,system-ui,sans-serif;text-decoration:none}.skip:focus{top:12px;outline:2px solid #FFFFFF;outline-offset:2px}
.simframe button:not(.lnk):not(.ib),.simframe [role="button"]{min-height:24px;min-width:24px}
.simframe .sw-con .no{color:#A9A4AE}
.simframe button.lnk{min-height:24px}
.simframe .chip{min-height:24px}
.simsep{width:1px;height:20px;background:#CAC4CF;margin:0 4px}
.dd-pic:focus-visible,.gd-wrap:focus-visible,.ad-tscroll:focus-visible{outline:2px solid #35307E;outline-offset:-2px}
@media (prefers-reduced-motion: reduce){.simframe *,.simframe *::before,.simframe *::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}
"""

LAYER_JS = r"""
  // ---- keyboard layers: Escape closes the top layer and returns focus to its opener; focus enters a dialog; arrows move in tablists
  layerState() {
    var s = this.state, sw = s.sw || {}, as = s.as || {};
    if (sw.confirm) return { k: 'swConfirm', close: { sw: Object.assign({}, sw, { confirm: false }) } };
    if (sw.dlg) return { k: 'swDlg', close: { sw: Object.assign({}, sw, { dlg: false }) } };
    if (as.menu) return { k: 'asMenu', close: { as: Object.assign({}, as, { menu: false }) } };
    if (s.panel) return { k: 'panel', close: { panel: false } };
    if (s.menu) return { k: 'menu', close: { menu: false } };
    if (s.help) return { k: 'help', close: { help: false } };
    if (s.video) return { k: 'video', close: { video: null } };
    if (s.newIdea) return { k: 'newIdea', close: { newIdea: false } };
    if (s.micro) return { k: 'micro', close: { micro: false } };
    if (s.navOpen && (this._simW || 1440) < 1200) return { k: 'nav', close: { navOpen: false } };
    return null;
  }
  layerBind() {
    var self = this; if (this._layerBound || typeof document === 'undefined') return; this._layerBound = true;
    document.addEventListener('pointerdown', function (e) { var t = e.target && e.target.closest ? e.target.closest('[aria-expanded],[aria-haspopup],button,a') : null; if (t) self._lastTrigger = t; }, true);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { var L = self.layerState(); if (L) { e.preventDefault(); self.setState(L.close); self._returnFocus = true; } return; }
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft' || e.key === 'Home' || e.key === 'End') {
        var el = document.activeElement, list = el && el.closest ? el.closest('[role="tablist"],[role="radiogroup"],.seg') : null; if (!list) return;
        var items = Array.prototype.filter.call(list.querySelectorAll('[role="tab"],[role="radio"],button'), function (b) { return !b.disabled && b.offsetWidth > 0; }); var i = items.indexOf(el); if (i < 0) return;
        e.preventDefault(); var n = e.key === 'Home' ? 0 : e.key === 'End' ? items.length - 1 : (i + (e.key === 'ArrowRight' ? 1 : items.length - 1)) % items.length; items[n].focus();
        if (list.getAttribute('role') === 'tablist') items[n].click();
      }
    });
  }
  layerSync() {
    if (typeof document === 'undefined') return;
    var L = this.layerState(), k = L ? L.k : null;
    if (k && k !== this._layerK) {
      var dlg = document.querySelector('#cl-root [role="dialog"], #cl-root [role="alertdialog"], #cl-root [role="menu"]');
      if (dlg) { var f = dlg.querySelector('input:not([type=hidden]),select,textarea,button,[href],[tabindex="0"]'); try { (f || dlg).focus({ preventScroll: true }); } catch (e) {} }
    } else if (!k && this._layerK && this._returnFocus) { var t = this._lastTrigger; if (t && document.body.contains(t)) try { t.focus({ preventScroll: true }); } catch (e) {} }
    if (!k) this._returnFocus = false;
    this._layerK = k;
    var m = document.getElementById('main-content'); if (m && this._skipTo) { this._skipTo = false; try { m.focus({ preventScroll: true }); } catch (e) {} }
  }
"""


def polish(out):
    # one h1 per screen: the header's context title
    out, n = re.subn(r'<span class="hf" style="([^"]*)">\{\{hdrFeature\}\}</span>', r'<h1 class="hf" style="margin: 0; \1">{{hdrFeature}}</h1>', out)
    assert n == 1, n
    # skip link + main landmark target
    out, n = re.subn(r'(<div class="simframe"[^>]*>)', r'\1<a class="skip" href="#main-content">Skip to content</a>', out)
    assert n == 1
    out, n = re.subn(r'<main class="cl-main \{\{mainPaneCls\}\}"', '<main id="main-content" tabindex="-1" class="cl-main {{mainPaneCls}}"', out)
    assert n == 1
    # empty action headers get a name
    out = out.replace('<th class="th"></th>', '<th class="th"><span class="sr-only">Actions</span></th>').replace('<th class="th" style="text-align: right"></th>', '<th class="th" style="text-align: right"><span class="sr-only">Actions</span></th>')
    # scrollable pictures are reachable
    out = out.replace('<div class="dd-pic">', '<div class="dd-pic" tabindex="0" aria-label="Diagram, scrolls sideways">')
    # radios: aria-checked only
    out = out.replace('role="radio" aria-checked="{{n.on}}" aria-pressed="{{n.on}}"', 'role="radio" aria-checked="{{n.on}}"').replace('role="radio" aria-checked="{{m.on}}" aria-pressed="{{m.on}}"', 'role="radio" aria-checked="{{m.on}}"')
    # one entry point to the assistant in the header; no cookie item in the navigation
    out, n = re.subn(r'<button type="button" class="ib hdr-asst" aria-label="Open assistant"[^>]*>.*?</button>', '', out, flags=re.S)
    assert n == 1, n
    out, n = re.subn(r'<a href="#cookies"[^>]*>.*?</a>', '', out, flags=re.S)
    assert n >= 6, n
    # text floor 11 px
    out = re.sub(r'font-size:\s*(9|10)px', 'font-size: 11px', out)
    out = re.sub(r'(font:\s*\d{3}\s+)(9|10)px', r'\g<1>11px', out)
    # section titles as real headings
    out = re.sub(r'<div class="h2"([^>]*)>((?:(?!</?div\b).)*?)</div>', r'<h2 class="h2"\1>\2</h2>', out, flags=re.S)
    out = re.sub(r'<div class="h3"([^>]*)>((?:(?!</?div\b).)*?)</div>', r'<h3 class="h3"\1>\2</h3>', out, flags=re.S)
    # CSS additions and the layer helper
    out = out.replace('</style>', A11Y_CSS + '</style>', 1)
    out = out.replace('  componentDidMount() {\n    var self = this; this.simSync(); this.measure();', '  componentDidMount() {\n    var self = this; this.simSync(); this.measure(); this.layerBind();', 1)
    assert 'this.layerBind();' in out
    out = out.replace('  componentDidUpdate() {\n    this.simSync(); this.measure(); this.qaFocusSync();', '  componentDidUpdate() {\n    this.simSync(); this.measure(); this.qaFocusSync(); this.layerSync();', 1)
    assert 'this.layerSync();' in out
    out = out.replace('  componentWillUnmount() { if (this._swT) clearInterval(this._swT); }', LAYER_JS + '  componentWillUnmount() { if (this._swT) clearInterval(this._swT); }', 1)
    assert 'layerState() {' in out
    out = vision_theme.apply(out)
    return out
