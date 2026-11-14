// Generates the four options of the colour decision lab.
import {Hct, argbFromHex, hexFromArgb, TonalPalette, SchemeTonalSpot, MaterialDynamicColors as M} from '../lab3/node_modules/@material/material-color-utilities/index.js';
import fs from 'fs';
const here = new URL('.', import.meta.url).pathname;
const cur = JSON.parse(fs.readFileSync(here + 'cur.json'));
const A = {}; for (const t of cur) A[t.name] = [t.light.toUpperCase(), t.dark.toUpperCase()];
const U = h => h.toUpperCase();
const pal = (hex, chroma) => { const c = Hct.fromInt(argbFromHex(hex)); return TonalPalette.fromHueAndChroma(c.hue, chroma ?? c.chroma); };
const T = (p, t) => U(hexFromArgb(p.tone(t)));
// role family at given tones: [role, on, container, onContainer] light / dark
const fam = (p, name, lt = 30, pins = {}) => ({
  [name]: [pins.role || T(p, lt), T(p, 80)],
  ['on-' + name]: ['#FFFFFF', T(p, 20)],
  [name + '-container']: [pins.container || T(p, 90), T(p, 30)],
  ['on-' + name + '-container']: [T(p, 10), T(p, 90)],
});

const NEUTRAL = ['surface', 'on-surface', 'on-surface-variant', 'surface-dim', 'surface-bright', 'surface-container-lowest', 'surface-container-low', 'surface-container', 'surface-container-high', 'surface-container-highest', 'outline', 'outline-variant', 'inverse-surface', 'inverse-on-surface', 'scrim', 'shadow'];
const pick = (src, keys) => Object.fromEntries(keys.map(k => [k, src[k]]));
const BRAND_A = { 'logo-box': A['logo-box'], 'on-logo-box': A['on-logo-box'], 'logo-cursor': A['logo-cursor'], 'logo-ai': [A['ai'][0], A['ai'][1]] };

// ---------- A · current 4.7 ----------
const optA = { ...A };

// ---------- B · Tidy: same colours, fewer tokens ----------
const optB = {};
for (const k of Object.keys(A)) {
  if (['run-icon', 'run-outline', 'run-text', 'nav-active', 'focus-ring', 'ai-strong', 'surface-variant', 'logo-box', 'on-logo-box', 'logo-cursor'].includes(k)) continue;
  optB[k] = A[k];
}
optB['secondary-container'] = [A['nav-active'][0], A['secondary-container'][1]];  // light #D4D0F9: ends the duplicate with primary-container and replaces nav-active
optB['ai'] = [A['ai-strong'][0], A['ai'][1]];                                      // MD3 tones: t40 light (was ai-strong), t80 dark
optB['on-ai'] = ['#FFFFFF', A['on-ai'][1]];

// ---------- C · Sweep palette: the three Sweep colours as seeds ----------
const P = pal('#39235F'), S = pal('#DED7EB'), L = pal('#DCEAB4'), E = pal(A['error'][0]),
  G = pal(A['success'][0]), W = pal(A['warning'][1]), I = pal(A['ai'][0]);
const optC = {
  ...fam(P, 'primary', 20, { role: '#39235F' }),
  ...fam(S, 'secondary', 30, { container: '#DED7EB' }),
  ...fam(L, 'tertiary', 30, { container: '#DCEAB4' }),
  ...pick(A, ['error', 'on-error', 'error-container', 'on-error-container']),
  ...pick(A, NEUTRAL),
  'nav-container': A['nav-container'],
  'inverse-primary': [T(P, 80), T(P, 30)],
  ...fam(I, 'ai', 30),
  ...fam(G, 'success', 30),
  ...fam(W, 'warning', 30),
};

// ---------- D · Material 3 as generated from the seed ----------
const seed = Hct.fromInt(argbFromHex('#39235F'));
const sl = new SchemeTonalSpot(seed, false, 0), sd = new SchemeTonalSpot(seed, true, 0);
const kebab = s => s.replace(/[A-Z]/g, m => '-' + m.toLowerCase());
const roles = ['primary', 'onPrimary', 'primaryContainer', 'onPrimaryContainer', 'secondary', 'onSecondary', 'secondaryContainer', 'onSecondaryContainer', 'tertiary', 'onTertiary', 'tertiaryContainer', 'onTertiaryContainer', 'error', 'onError', 'errorContainer', 'onErrorContainer', 'surface', 'onSurface', 'onSurfaceVariant', 'surfaceDim', 'surfaceBright', 'surfaceContainerLowest', 'surfaceContainerLow', 'surfaceContainer', 'surfaceContainerHigh', 'surfaceContainerHighest', 'outline', 'outlineVariant', 'inverseSurface', 'inverseOnSurface', 'inversePrimary', 'scrim', 'shadow'];
const optD = {};
for (const r of roles) optD[kebab(r)] = [U(hexFromArgb(M[r].getArgb(sl))), U(hexFromArgb(M[r].getArgb(sd)))];
const md3fam = (hex, name) => { const p = pal(hex, Math.max(36, Hct.fromInt(argbFromHex(hex)).chroma)); return { [name]: [T(p, 40), T(p, 80)], ['on-' + name]: [T(p, 100), T(p, 20)], [name + '-container']: [T(p, 90), T(p, 30)], ['on-' + name + '-container']: [T(p, 10), T(p, 90)] }; };
Object.assign(optD, md3fam(A['ai'][0], 'ai'), md3fam(A['success'][0], 'success'), md3fam(A['warning'][0], 'warning'));

// ---------- slots: how each option paints the specimen ----------
const slots = (o, rules) => {
  const g = k => o[k] || (() => { throw new Error('missing ' + k); })();
  const r = {};
  const base = ['primary', 'on-primary', 'primary-container', 'on-primary-container', 'secondary-container', 'on-secondary-container', 'tertiary', 'error', 'error-container', 'on-error-container', 'surface', 'on-surface', 'on-surface-variant', 'surface-container-lowest', 'surface-container-low', 'surface-container', 'surface-container-high', 'surface-container-highest', 'outline', 'outline-variant', 'inverse-surface', 'inverse-on-surface', 'inverse-primary', 'ai-container', 'on-ai-container', 'success-container', 'on-success-container', 'warning-container', 'on-warning-container'];
  for (const k of base) r[k] = g(k);
  for (const [k, v] of Object.entries(rules)) r[k] = Array.isArray(v) ? v : (typeof v === 'string' ? g(v) : v);
  return r;
};
const N = ['transparent', 'transparent'];
const S_A = slots(optA, { 'nav-bg': 'nav-container', 'nav-pill': 'nav-active', 'nav-bar': 'primary', 'run-bg': 'run', 'run-fg': 'on-run', 'run-icon': 'run-icon', 'run-edge': 'run-outline', 'rowrun-fg': 'run-text', 'rowrun-disc': 'run', 'rowrun-glyph': 'on-run', focus: 'focus-ring', 'ai-mark': 'ai-strong', dots: 'tertiary', 'logo-box': 'logo-box', 'on-logo-box': 'on-logo-box', 'logo-cursor': 'logo-cursor', 'logo-ai': 'ai', 'search-bg': [A['surface-container-lowest'][0], A['surface-container-high'][1]] });
const S_B = slots(optB, { 'nav-bg': 'nav-container', 'nav-pill': 'secondary-container', 'nav-bar': 'primary', 'run-bg': 'run', 'run-fg': 'on-run', 'run-icon': 'on-run', 'run-edge': 'on-run', 'rowrun-fg': 'primary', 'rowrun-disc': 'run', 'rowrun-glyph': 'on-run', focus: 'primary', 'ai-mark': 'ai', dots: 'tertiary', 'logo-box': BRAND_A['logo-box'], 'on-logo-box': BRAND_A['on-logo-box'], 'logo-cursor': BRAND_A['logo-cursor'], 'logo-ai': BRAND_A['logo-ai'], 'search-bg': [optB['surface-container-lowest'][0], optB['surface-container-high'][1]] });
const S_C = slots(optC, { 'nav-bg': 'nav-container', 'nav-pill': 'secondary-container', 'nav-bar': 'primary', 'run-bg': 'tertiary-container', 'run-fg': 'on-tertiary-container', 'run-icon': 'on-tertiary-container', 'run-edge': N, 'rowrun-fg': 'primary', 'rowrun-disc': 'tertiary-container', 'rowrun-glyph': 'on-tertiary-container', focus: 'primary', 'ai-mark': 'ai', dots: 'tertiary', 'logo-box': BRAND_A['logo-box'], 'on-logo-box': BRAND_A['on-logo-box'], 'logo-cursor': BRAND_A['logo-cursor'], 'logo-ai': BRAND_A['logo-ai'], 'search-bg': [optC['surface-container-lowest'][0], optC['surface-container-high'][1]] });
const S_D = slots(optD, { 'nav-bg': [optD['surface-container'][0], optD['surface-container'][1]], 'nav-pill': 'secondary-container', 'nav-bar': N, 'run-bg': 'tertiary-container', 'run-fg': 'on-tertiary-container', 'run-icon': 'on-tertiary-container', 'run-edge': N, 'rowrun-fg': 'primary', 'rowrun-disc': 'tertiary-container', 'rowrun-glyph': 'on-tertiary-container', focus: 'primary', 'ai-mark': 'ai', dots: 'tertiary', 'logo-box': BRAND_A['logo-box'], 'on-logo-box': BRAND_A['on-logo-box'], 'logo-cursor': BRAND_A['logo-cursor'], 'logo-ai': BRAND_A['logo-ai'], 'search-bg': [optD['surface-container-highest'][0], optD['surface-container-highest'][1]] });

const out = {
  A: { tokens: optA, brand: {}, slots: S_A },
  B: { tokens: optB, brand: BRAND_A, slots: S_B },
  C: { tokens: optC, brand: BRAND_A, slots: S_C },
  D: { tokens: optD, brand: BRAND_A, slots: S_D },
};
fs.writeFileSync(here + 'options.json', JSON.stringify(out, null, 1));
for (const k of 'ABCD') console.log(k, Object.keys(out[k].tokens).length, 'ui tokens', Object.keys(out[k].brand).length, 'brand');
const show = ['primary', 'primary-container', 'secondary', 'secondary-container', 'tertiary', 'tertiary-container', 'on-tertiary-container', 'error', 'surface', 'surface-container', 'inverse-primary', 'ai', 'ai-container', 'success', 'success-container', 'warning', 'warning-container'];
for (const s of show) console.log(s.padEnd(24), 'ABCD'.split('').map(k => (out[k].tokens[s] || ['—', '—']).join('/')).join('  '));
