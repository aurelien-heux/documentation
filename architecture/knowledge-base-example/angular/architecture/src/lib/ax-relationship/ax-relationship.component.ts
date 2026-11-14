import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';
import { AX_RELATIONSHIPS, AxRelationship } from '../notation.generated';

/** One end marker of a relationship line, as SVG data (no innerHTML: Angular's sanitizer strips SVG markup). */
export interface AxMarker { readonly kind: 'fill' | 'open' | 'line'; readonly d: string; }

/** Marker geometry at one end of a line of the given width (same drawing as the design-system catalog). */
export function marker(kind: string, end: 's' | 't', width: number): AxMarker | null {
  const x = end === 's' ? 4 : width - 4, d = end === 's' ? 1 : -1;
  switch (kind) {
    case 'diamond': return { kind: 'fill', d: `M${x} 12 l${6 * d} -4 l${6 * d} 4 l${-6 * d} 4z` };
    case 'odiamond': return { kind: 'open', d: `M${x} 12 l${6 * d} -4 l${6 * d} 4 l${-6 * d} 4z` };
    case 'dot': return { kind: 'fill', d: `M${x + 3 * d} 9 a3 3 0 1 0 0.001 0z` };
    case 'arrow': return { kind: 'fill', d: `M${x} 12 l${10 * d} -5 v10z` };
    case 'triangle': return { kind: 'open', d: `M${x} 12 l${11 * d} -6 v12z` };
    case 'open': return { kind: 'line', d: `M${x + 10 * d} 6 L${x} 12 L${x + 10 * d} 18` };
    case 'small': return { kind: 'line', d: `M${x + 7 * d} 8 L${x} 12 L${x + 7 * d} 16` };
    default: return null;
  }
}

/**
 * Relationship line: an ArchiMate relationship drawn as a horizontal SVG sample (legends, tables, relationship lists).
 * Line style and end markers follow the type. `highlight` = 2.2 px primary (the selected element's relationships).
 */
@Component({
  selector: 'atb-ax-relationship',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { class: 'atb-ax-relationship' },
  template: `
    <svg [class]="cls()" [attr.width]="width()" height="24" [attr.viewBox]="'0 0 ' + width() + ' 24'" role="img" [attr.aria-label]="label()">
      <line x1="6" y1="12" [attr.x2]="width() - 6" y2="12" [attr.stroke-dasharray]="dash()" />
      @for (m of markers(); track $index) {
        <path [class]="m.kind === 'fill' ? 'mk-fill' : m.kind === 'open' ? 'mk-open' : 'line'" [attr.d]="m.d" />
      }
    </svg>
    @if (showName()) { <span class="name">{{ info().name }}</span> }
  `,
  styles: [':host { display: inline-flex; align-items: center; gap: 12px; } .name { font: 600 14px/20px var(--md-sys-typescale-brand-family, sans-serif); }'],
})
export class AxRelationshipComponent {
  readonly type = input.required<AxRelationship>();
  readonly highlight = input(false);
  readonly showName = input(true);
  readonly width = input(150);
  readonly info = computed(() => AX_RELATIONSHIPS[this.type()]);
  readonly label = computed(() => `${this.info().name}, ${this.info().line} line`);
  readonly cls = computed(() => `ax-rel ${this.type()}${this.highlight() ? ' hi' : ''}`);
  readonly dash = computed(() => (this.info().line === 'dotted' ? '2 3' : this.info().line === 'dashed' ? '6 4' : null));
  readonly markers = computed(() => [marker(this.info().source, 's', this.width()), marker(this.info().target, 't', this.width())].filter((m): m is AxMarker => !!m));
}
