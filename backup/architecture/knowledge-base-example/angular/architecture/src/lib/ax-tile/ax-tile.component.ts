import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';
import { AxGlyphComponent } from '../icons/ax-glyph.component';
import { AX_TYPES, AxType } from '../notation.generated';

/**
 * Type tile: the 20 px (32 px large) type mark before an element name in lists, tables and chips.
 * Layer fill, layer-ink glyph. Decorative: aria-hidden; the type name belongs to the row (title attribute helps on hover).
 * `type` undefined → the neutral tile (DD files, ADRs) with the given `neutralGlyph` ('code' | 'document').
 */
@Component({
  selector: 'atb-ax-tile',
  standalone: true,
  imports: [AxGlyphComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: 'ax-tile',
    '[class.lg]': 'large()',
    '[class.ax-neutral]': '!type()',
    '[class]': 'layerClass()',
    '[attr.title]': 'typeName()',
    'aria-hidden': 'true',
  },
  template: `
    @if (type(); as t) {
      <atb-ax-glyph [type]="t" />
    } @else {
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
        @if (neutralGlyph() === 'document') {
          <path d="M6 3.5h9l3.5 3.5v13.5H6z"/><path d="M9 11h6M9 14.5h6M9 18h4"/>
        } @else {
          <path d="M8 7 3.5 12 8 17M16 7l4.5 5-4.5 5M13.5 5l-3 14"/>
        }
      </svg>
    }
  `,
  styles: [':host atb-ax-glyph, :host svg { width: 16px; height: 16px; } :host.lg atb-ax-glyph, :host.lg svg { width: 24px; height: 24px; }'],
})
export class AxTileComponent {
  readonly type = input<AxType | undefined>(undefined);
  readonly large = input(false);
  readonly neutralGlyph = input<'code' | 'document'>('code');
  readonly typeName = computed(() => (this.type() ? AX_TYPES[this.type()!].name : this.neutralGlyph() === 'document' ? 'Decision record' : 'Detailed design'));
  readonly layerClass = computed(() => {
    const t = this.type();
    return ['ax-tile', this.large() ? 'lg' : '', t ? `ax-l-${AX_TYPES[t].layer}` : 'ax-neutral'].filter(Boolean).join(' ');
  });
}
