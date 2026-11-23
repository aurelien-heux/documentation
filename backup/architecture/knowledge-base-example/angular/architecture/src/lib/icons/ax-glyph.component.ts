import { ChangeDetectionStrategy, Component, computed, inject, input } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { AX_GLYPHS, AX_SVG_ATTRS, AX_TYPES, AxType } from '../notation.generated';

/**
 * The 24 × 24 glyph of an ArchiMate type, drawn in currentColor. Decorative: the host is aria-hidden,
 * the type name is given by the component around it (tile, figure, table column).
 * Inline SVG from the generated notation; no icon font and no network request.
 */
@Component({
  selector: 'atb-ax-glyph',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { 'aria-hidden': 'true', class: 'atb-ax-glyph', '[innerHTML]': 'svg()' },
  template: '',
  styles: [':host { display: inline-block; width: 1em; height: 1em; line-height: 0; } :host ::ng-deep svg { width: 100%; height: 100%; display: block; }'],
})
export class AxGlyphComponent {
  readonly type = input.required<AxType>();
  private readonly sanitizer = inject(DomSanitizer);
  readonly svg = computed<SafeHtml>(() => {
    const info = AX_TYPES[this.type()];
    const inner = info ? AX_GLYPHS[info.glyph] ?? '' : '';
    // The markup comes from the generated notation file (build-time constant), never from user input.
    return this.sanitizer.bypassSecurityTrustHtml(`<svg ${AX_SVG_ATTRS}>${inner}</svg>`);
  });
}
