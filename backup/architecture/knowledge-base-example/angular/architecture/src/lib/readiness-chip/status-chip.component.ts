import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';

export type AtbStatusTone = 'success' | 'warning' | 'error' | 'info' | 'neutral';

/**
 * AIToolbox StatusChip for the architecture feature: radius-xs, state container, 18 px tile glyph + word.
 * The word is the accessible name; the glyph is decorative (never colour alone). Used by the readiness and decision chips.
 */
@Component({
  selector: 'atb-status-chip',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { '[class]': 'cls()' },
  template: `<span class="tile" aria-hidden="true">{{ glyph() }}</span>{{ label() }}`,
  styles: [`
    :host { display:inline-flex; align-items:center; gap:6px; height:28px; padding:0 10px 0 5px; border-radius:4px; white-space:nowrap;
      font:600 12px/16px var(--md-sys-typescale-brand-family, sans-serif); }
    .tile { width:18px; height:18px; border-radius:4px; display:inline-grid; place-items:center; font:700 12px/1 var(--md-sys-typescale-plain-family, sans-serif); }
    :host.st-success { background:var(--md-sys-color-success-container); color:var(--md-sys-color-on-success-container); } :host.st-success .tile { background:var(--md-sys-color-success); color:var(--md-sys-color-on-success); }
    :host.st-warning { background:var(--md-sys-color-warning-container); color:var(--md-sys-color-on-warning-container); } :host.st-warning .tile { background:var(--md-sys-color-warning); color:var(--md-sys-color-on-warning); }
    :host.st-error { background:var(--md-sys-color-error-container); color:var(--md-sys-color-on-error-container); } :host.st-error .tile { background:var(--md-sys-color-error); color:var(--md-sys-color-on-error); }
    :host.st-info { background:var(--md-sys-color-secondary-container); color:var(--md-sys-color-on-secondary-container); } :host.st-info .tile { background:var(--md-sys-color-primary); color:var(--md-sys-color-on-primary); }
    :host.st-neutral { background:var(--md-sys-color-surface-container-highest); color:var(--md-sys-color-on-surface-variant); } :host.st-neutral .tile { background:var(--md-sys-color-outline); color:var(--md-sys-color-surface-container-lowest); }
  `],
})
export class AtbStatusChipComponent {
  readonly tone = input.required<AtbStatusTone>();
  readonly glyph = input.required<string>();
  readonly label = input.required<string>();
  readonly cls = computed(() => `atb-status-chip st-${this.tone()}`);
}
