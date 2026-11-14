// Generates projects/ui/styles/tokens.css and projects/ui/src/lib/core/tokens.ts from the design-system tokens.json.
// Run with `npm run tokens` (also runs before `npm run build:lib`). Never edit the generated files by hand.
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const lib = resolve(root, 'projects/ui');
const t = JSON.parse(readFileSync(resolve(lib, 'tokens/tokens.json'), 'utf8'));

const families = {
  ui: "'BNPP Type', 'Open Sans', system-ui, sans-serif",
  body: "'Open Sans', system-ui, sans-serif",
  plain: "'Open Sans', system-ui, sans-serif",
};

const lines = [];
const out = (s = '') => lines.push(s);
out(`/* AIToolbox — generated from tokens.json (v${t.version ?? '?'}) by tools/build-tokens.mjs. Do not edit by hand. */`);
out('/* Colours use light-dark(): they follow `color-scheme`, which the theme files set (html.light / html.dark, or the system setting). */');
out('');
out('@font-face {');
out("  font-family: 'BNPP Type';");
out("  src: url('../fonts/BNPPType-Regular.woff2') format('woff2');");
out('  font-weight: 500;');
out('  font-style: normal;');
out('  font-display: swap;');
out('}');
out('');
out(':root {');
for (const tok of t.color.tokens) {
  const v = typeof tok.value === 'string' ? { light: tok.value, dark: tok.value } : tok.value;
  const light = v.light;
  const dark = v.dark ?? v.light;
  out(`  --md-sys-color-${tok.name}: ${light === dark ? light : `light-dark(${light}, ${dark})`};`);
}
out('');
out(`  --md-ref-typeface-brand: ${families.ui};`);
out(`  --md-ref-typeface-plain: ${families.body};`);
out('  --ait-font-ui: var(--md-ref-typeface-brand);');
out('  --ait-font-body: var(--md-ref-typeface-plain);');
for (const group of t.type.groups) {
  for (const s of group.styles) {
    const fam = group.family === 'ui' ? 'var(--ait-font-ui)' : 'var(--ait-font-body)';
    out(`  --ait-type-${s.name}: ${s.fontWeight} ${s.fontSize}/${s.lineHeight} ${fam};`);
    out(`  --ait-type-${s.name}-tracking: ${s.letterSpacing ?? '0px'};`);
  }
}
out('');
for (const fam of ['spacing', 'radius', 'shadow', 'breakpoint']) {
  for (const tok of t[fam].tokens) out(`  --ait-${tok.name}: ${tok.value};`);
}
out('');
out('  --md-sys-state-hover-opacity: 0.06;');
out('  --md-sys-state-focus-opacity: 0;');
out('  --md-sys-state-pressed-opacity: 0.1;');
out('  --md-sys-state-dragged-opacity: 0.14;');
out('  --ait-state-layer: var(--md-sys-color-primary);');
out('  --ait-ease-emphasized: cubic-bezier(0.2, 0, 0, 1);');
out('  --ait-duration-short: 150ms;');
out('  --ait-duration-medium: 300ms;');
out('  --ait-duration-long: 500ms;');
out('');
const lay = Object.fromEntries(t.layout.tokens.map((x) => [x.name, x.value]));
out(`  --ait-page-margin: ${lay['layout-margin-compact']};`);
out(`  --ait-grid-columns: ${lay['layout-columns-compact']};`);
out(`  --ait-grid-gutter: ${lay['layout-gutter-compact'] ?? '16px'};`);
out('}');
const bps = Object.fromEntries(t.breakpoint.tokens.map((x) => [x.name.replace('breakpoint-', ''), x.value]));
for (const cls of ['medium', 'expanded', 'large', 'extra-large']) {
  out(`@media (min-width: ${bps[cls]}) {`);
  out(`  :root { --ait-page-margin: ${lay[`layout-margin-${cls}`]}; --ait-grid-columns: ${lay[`layout-columns-${cls}`]}; --ait-grid-gutter: ${lay[`layout-gutter-${cls}`] ?? '24px'}; }`);
  out('}');
}
out('');
out('/* Type utility classes (one per style of the scale). */');
for (const group of t.type.groups) {
  for (const s of group.styles) {
    out(`.ait-${s.name} { font: var(--ait-type-${s.name}); letter-spacing: var(--ait-type-${s.name}-tracking); }`);
  }
}
writeFileSync(resolve(lib, 'styles/tokens.css'), lines.join('\n') + '\n');
// Same content as a Sass partial, so the theme entry files can @use it (and the build rebases the font URL).
writeFileSync(resolve(lib, 'styles/_tokens.scss'), lines.join('\n') + '\n');

// TypeScript mirror, for code that needs a value (charts, canvas, tests).
const colors = {};
for (const tok of t.color.tokens) {
  const v = typeof tok.value === 'string' ? { light: tok.value, dark: tok.value } : tok.value;
  colors[tok.name] = { light: v.light, dark: v.dark ?? v.light };
}
const ts = `// Generated from tokens.json by tools/build-tokens.mjs. Do not edit by hand.
/** AIToolbox colour roles, light and dark. In templates and styles use the CSS custom properties (\`var(--md-sys-color-<role>)\`) instead. */
export const AIT_COLORS = ${JSON.stringify(colors, null, 2)} as const;
export type AitColorRole = keyof typeof AIT_COLORS;
/** Version of the design-system token set this library was built from. */
export const AIT_TOKENS_VERSION = '${t.version ?? 'unknown'}';
`;
writeFileSync(resolve(lib, 'src/lib/core/tokens.ts'), ts);
console.log(`tokens.css: ${t.color.tokens.length} colours, ${t.type.groups.reduce((n, g) => n + g.styles.length, 0)} type styles`);
