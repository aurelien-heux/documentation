import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';

export type AtbAsdSource = 'model' | 'written' | 'thin' | 'missing';

const SOURCE: Record<AtbAsdSource, { cls: string; label: string }> = {
  model: { cls: 'model', label: 'From the model' }, written: { cls: 'ok', label: 'Written' },
  thin: { cls: 'warn', label: 'Too short' }, missing: { cls: 'err', label: 'Missing' },
};

/**
 * ASD section header: number, title (an h2, focusable from the table of contents) and the source badge.
 * Project the section body as content.
 */
@Component({
  selector: 'atb-asd-section',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { class: 'atb-asd-section', '[attr.id]': 'sectionId()', '[attr.aria-labelledby]': 'sectionId() + "-h"', role: 'region' },
  template: `
    <div class="head">
      <h2 [id]="sectionId() + '-h'" tabindex="-1"><span class="num">{{ index() }}</span>{{ title() }}</h2>
      <span [class]="'src ' + src().cls">{{ src().label }}</span>
    </div>
    <ng-content />
  `,
  styles: [`
    :host { display:block; min-width:0; scroll-margin-top:84px; }
    .head { display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-bottom:12px; padding-bottom:8px; border-bottom:1px solid var(--md-sys-color-outline-variant); }
    h2 { margin:0; font:700 18px/24px var(--md-sys-typescale-brand-family, sans-serif); display:flex; align-items:center; gap:10px; color:var(--md-sys-color-on-surface); }
    h2:focus { outline:none; } h2:focus-visible { outline:2px solid var(--md-sys-color-focus-ring); outline-offset:4px; border-radius:4px; }
    .num { width:28px; height:28px; border-radius:8px; background:var(--md-sys-color-surface-container-highest); display:grid; place-items:center; font-size:13px; flex:none; }
    .src { display:inline-flex; align-items:center; height:24px; padding:0 8px; border-radius:4px; font:600 12px/16px var(--md-sys-typescale-brand-family, sans-serif); }
    .model { background:var(--md-sys-color-secondary-container); color:var(--md-sys-color-on-secondary-container); }
    .ok { background:var(--md-sys-color-success-container); color:var(--md-sys-color-on-success-container); }
    .warn { background:var(--md-sys-color-warning-container); color:var(--md-sys-color-on-warning-container); }
    .err { background:var(--md-sys-color-error-container); color:var(--md-sys-color-on-error-container); }
  `],
})
export class AtbAsdSectionComponent {
  readonly index = input.required<number>();
  readonly title = input.required<string>();
  readonly source = input.required<AtbAsdSource>();
  readonly sectionId = input<string>('asd-section');
  readonly src = computed(() => SOURCE[this.source()]);
}
