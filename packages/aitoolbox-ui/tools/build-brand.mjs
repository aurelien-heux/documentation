// Generates projects/ui/src/lib/brand/logo.html from the design-system logo files (assets/logos/*-light.svg).
// The fixed light colours become token-driven styles, so one template serves light and dark:
// logo-box / on-logo-box / logo-cursor for the toolbox, ai / on-ai for the badge, on-surface / primary for the wordmark.
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const lib = resolve(root, 'projects/ui');
const variants = {
  horizontal: 'logo-horizontal-light.svg',
  stacked: 'logo-stacked-light.svg',
  mark: 'mark-light.svg',
  'mark-plain': 'mark-plain-light.svg',
  wordmark: 'wordmark-light.svg',
};
const colour = {
  '#0D0B14': 'var(--md-sys-color-logo-box)',
  '#FFFFFF': 'var(--md-sys-color-on-logo-box)',
  '#00F29E': 'var(--md-sys-color-logo-cursor)',
  '#80D5D4': 'var(--md-sys-color-ai)',
  '#003737': 'var(--md-sys-color-on-ai)',
  '#1C1B1E': 'var(--md-sys-color-on-surface)',
  '#1D1A27': 'var(--md-sys-color-on-surface)',
  '#35307E': 'var(--md-sys-color-primary)',
};

const cases = [];
for (const [name, file] of Object.entries(variants)) {
  let s = readFileSync(resolve(lib, 'assets/logos', file), 'utf8').trim();
  const viewBox = /viewBox="([^"]+)"/.exec(s)[1];
  s = s.replace(/<title[^>]*>.*?<\/title>/s, '');
  s = s.replace(/^<svg[^>]*>/, '').replace(/<\/svg>$/, '');
  s = s.replace(/(fill|stroke)="(#[0-9A-Fa-f]{6})"/g, (m, attr, hex) => {
    const v = colour[hex.toUpperCase()];
    if (!v) throw new Error(`${file}: unmapped colour ${hex}`);
    return `style="${attr}: ${v}"`;
  });
  // Unique mask ids per instance.
  s = s.replace(/id="(bm\d+)"/g, `[attr.id]="uid + '-m'"`).replace(/mask="url\(#bm\d+\)"/g, `[attr.mask]="'url(#' + uid + '-m)'"`);
  const [, , w, h] = viewBox.split(/\s+/).map(Number);
  cases.push(`  @case ('${name}') {
    <svg viewBox="${viewBox}" [attr.height]="height()" [attr.width]="height() * ${(w / h).toFixed(5)}" focusable="false" aria-hidden="true">${s}</svg>
  }`);
}
const html = `<!-- Generated from assets/logos by tools/build-brand.mjs. Do not edit by hand. -->
@switch (variant()) {
${cases.join('\n')}
}
`;
writeFileSync(resolve(lib, 'src/lib/brand/logo.html'), html);
console.log(`logo.html: ${cases.length} variants`);
