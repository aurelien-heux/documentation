/* AIToolbox · standalone runtime for exported canvas boards (.dc.html → .html).
   Implements the subset the boards use: {{dotted.holes}}, <sc-if>, <sc-for>, on* handlers, controlled inputs,
   a DCLogic base class with state / setState / forceUpdate and componentDidMount / DidUpdate / WillUnmount.
   Rendering builds a detached tree and morphs it into the page, so focus, scroll and CSS animations survive. */
(function () {
  'use strict';

  function DCLogic(props) { this.props = props || {}; this.state = {}; }
  DCLogic.prototype.setState = function (patch, cb) {
    var p = typeof patch === 'function' ? patch(this.state, this.props) : patch;
    if (p) this.state = Object.assign({}, this.state, p);
    schedule(this, cb);
  };
  DCLogic.prototype.forceUpdate = function (cb) { schedule(this, cb); };
  DCLogic.prototype.renderVals = function () { return {}; };
  window.DCLogic = DCLogic;

  var pending = null, callbacks = [];
  function schedule(inst, cb) {
    if (cb) callbacks.push(cb);
    if (pending) return;
    pending = Promise.resolve().then(function () {
      pending = null;
      render(inst);
      var cbs = callbacks; callbacks = [];
      cbs.forEach(function (f) { try { f(); } catch (e) { console.error(e); } });
      if (inst.componentDidUpdate) try { inst.componentDidUpdate(); } catch (e) { console.error(e); }
    });
  }

  /* ---------- holes ---------- */
  var HOLE = /\{\{\s*([^{}]+?)\s*\}\}/g;
  function lookup(expr, scope) {
    expr = expr.trim();
    if (expr === 'true') return true;
    if (expr === 'false') return false;
    if (expr === 'null') return null;
    if (/^-?\d+(\.\d+)?$/.test(expr)) return Number(expr);
    if (/^(['"]).*\1$/.test(expr)) return expr.slice(1, -1);
    var parts = expr.split('.'), v;
    for (var s = scope; s; s = s.__parent) {
      if (Object.prototype.hasOwnProperty.call(s, parts[0])) { v = s[parts[0]]; break; }
    }
    for (var i = 1; i < parts.length && v != null; i++) v = v[parts[i]];
    return v;
  }
  function single(str) { var m = /^\s*\{\{\s*([^{}]+?)\s*\}\}\s*$/.exec(str); return m ? m[1] : null; }
  function interp(str, scope) {
    return str.replace(HOLE, function (_, e) { var v = lookup(e, scope); return v == null || typeof v === 'function' ? '' : String(v); });
  }
  function truthy(v) { return Array.isArray(v) ? v.length > 0 : !!v; }

  /* ---------- events ---------- */
  var SPECIAL = { doubleclick: 'dblclick', focus: 'focusin', blur: 'focusout' };
  function eventType(attr, el) {
    var name = attr.slice(2).toLowerCase(), capture = false;
    if (/capture$/.test(name)) { capture = true; name = name.slice(0, -7); }
    if (name === 'change') {
      var tag = el.tagName, t = (el.getAttribute('type') || '').toLowerCase();
      name = (tag === 'SELECT' || t === 'checkbox' || t === 'radio' || t === 'file') ? 'change' : 'input';
    }
    name = SPECIAL[name] || name;
    return { type: name, capture: capture, key: name + (capture ? ':c' : '') };
  }
  function bindAll(el) {
    var h = el.__dcH || {};
    el.__dcBound = el.__dcBound || {};
    Object.keys(h).forEach(function (k) {
      if (el.__dcBound[k]) return;
      var spec = h[k];
      el.__dcBound[k] = true;
      el.addEventListener(spec.type, function (e) { var cur = el.__dcH && el.__dcH[k]; if (cur && cur.fn) cur.fn(e); }, spec.capture);
    });
  }

  /* ---------- build ---------- */
  var BOOL = { checked: 1, disabled: 1, selected: 1, hidden: 1, open: 1, readonly: 1, required: 1, multiple: 1, autofocus: 1 };
  function build(node, scope, out) {
    if (node.nodeType === 3) {
      var t = node.data;
      out.appendChild(document.createTextNode(t.indexOf('{{') >= 0 ? interp(t, scope) : t));
      return;
    }
    if (node.nodeType !== 1) return;
    if (node.tagName === 'TEMPLATE' && node.hasAttribute('data-sc')) {
      var kind = node.getAttribute('data-sc');
      if (kind === 'if') {
        var ex = single(node.getAttribute('value') || '');
        if (truthy(ex ? lookup(ex, scope) : false)) buildChildren(node.content, scope, out);
      } else {
        var le = single(node.getAttribute('list') || ''), as = node.getAttribute('as') || 'item';
        var list = le ? lookup(le, scope) : null;
        if (list && list.length) for (var i = 0; i < list.length; i++) {
          var s2 = { __parent: scope }; s2[as] = list[i]; s2[as + 'Index'] = i;
          buildChildren(node.content, s2, out);
        }
      }
      return;
    }
    var el = node.cloneNode(false);
    var attrs = Array.prototype.slice.call(node.attributes), handlers = null, valueProp;
    attrs.forEach(function (a) {
      var name = a.name, v = a.value;
      if (/^hint-placeholder/.test(name)) { el.removeAttribute(name); return; }
      if (/^on[a-z]/i.test(name)) {
        el.removeAttribute(name);
        var ex = single(v); if (!ex) return;
        var fn = lookup(ex, scope), spec = eventType(name, el);
        handlers = handlers || {}; handlers[spec.key] = { type: spec.type, capture: spec.capture, fn: typeof fn === 'function' ? fn : null };
        return;
      }
      if (v.indexOf('{{') < 0) { if (name === 'value') valueProp = v; return; }
      var one = single(v);
      if (one) {
        var val = lookup(one, scope);
        if (typeof val === 'boolean' && !/^(aria-|data-)/.test(name)) {
          if (val) el.setAttribute(name, ''); else el.removeAttribute(name);
          if (name === 'value') valueProp = String(val);
          return;
        }
        var sv = val == null || typeof val === 'function' ? '' : String(val);
        if (BOOL[name] && (sv === '' || sv === 'false')) { el.removeAttribute(name); return; }
        el.setAttribute(name, sv);
        if (name === 'value') valueProp = sv;
        return;
      }
      var iv = interp(v, scope); el.setAttribute(name, iv); if (name === 'value') valueProp = iv;
    });
    if (handlers) el.__dcH = handlers;
    if (valueProp !== undefined) el.__dcValue = valueProp;
    if (node.tagName === 'TEXTAREA') { el.__dcValue = valueProp !== undefined ? valueProp : interp(node.textContent, scope); }
    else buildChildren(node, scope, el);
    out.appendChild(el);
  }
  function buildChildren(parent, scope, out) {
    var kids = parent.childNodes;
    for (var i = 0; i < kids.length; i++) build(kids[i], scope, out);
  }

  /* ---------- morph ---------- */
  function syncProps(live, next) {
    live.__dcH = next.__dcH; bindAll(live);
    if (next.__dcValue !== undefined && 'value' in live && live.value !== next.__dcValue) {
      if (live.tagName === 'SELECT') live.__dcSelect = next.__dcValue; else live.value = next.__dcValue;
    }
    if (live.tagName === 'INPUT' && (live.type === 'checkbox' || live.type === 'radio')) live.checked = next.hasAttribute('checked');
  }
  function morphAttrs(live, next) {
    var i, a;
    for (i = live.attributes.length - 1; i >= 0; i--) { a = live.attributes[i]; if (!next.hasAttribute(a.name)) live.removeAttribute(a.name); }
    for (i = 0; i < next.attributes.length; i++) { a = next.attributes[i]; if (live.getAttribute(a.name) !== a.value) live.setAttribute(a.name, a.value); }
  }
  function same(a, b) { return a.nodeType === b.nodeType && (a.nodeType !== 1 || (a.tagName === b.tagName && a.namespaceURI === b.namespaceURI)); }
  function morphChildren(live, next) {
    var lk = live.childNodes, nk = Array.prototype.slice.call(next.childNodes), i;
    for (i = 0; i < nk.length; i++) {
      var l = lk[i], n = nk[i];
      if (!l) { live.appendChild(adopt(n)); continue; }
      if (!same(l, n)) { live.replaceChild(adopt(n), l); continue; }
      if (n.nodeType === 3) { if (l.data !== n.data) l.data = n.data; continue; }
      morphAttrs(l, n);
      if (l.tagName !== 'TEXTAREA') morphChildren(l, n);
      syncProps(l, n);
      if (l.tagName === 'SELECT' && l.__dcSelect !== undefined) { l.value = l.__dcSelect; l.__dcSelect = undefined; }
    }
    while (lk.length > nk.length) live.removeChild(live.lastChild);
  }
  function adopt(n) {
    // first insertion: bind handlers and set values on the whole subtree
    (function walk(el) {
      if (el.nodeType !== 1) return;
      if (el.__dcH) bindAll(el);
      for (var c = el.firstChild; c; c = c.nextSibling) walk(c);
      if (el.__dcValue !== undefined && 'value' in el) el.value = el.__dcValue;
    })(n);
    return n;
  }

  /* ---------- mount ---------- */
  var tpl, root;
  function render(inst) {
    var vals;
    try { vals = inst.renderVals() || {}; } catch (e) { console.error('renderVals failed', e); return; }
    var frag = document.createElement('div');
    buildChildren(tpl.content, vals, frag);
    morphChildren(root, frag);
  }
  function mount() {
    var src = document.getElementById('dc-template');
    tpl = document.createElement('template');
    tpl.innerHTML = src.textContent;
    root = document.getElementById('dc-root');
    var code = document.getElementById('dc-logic').textContent;
    var Component;
    try { Component = new Function('DCLogic', code + '\n;return typeof Component !== "undefined" ? Component : null;')(DCLogic); }
    catch (e) { console.error('board script failed', e); }
    var inst = Component ? new Component({}) : new DCLogic({});
    window.__dcInstance = inst;
    render(inst);
    if (inst.componentDidMount) try { inst.componentDidMount(); } catch (e) { console.error(e); }
    window.addEventListener('beforeunload', function () { if (inst.componentWillUnmount) inst.componentWillUnmount(); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();
})();
