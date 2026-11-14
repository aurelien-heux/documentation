import { ChangeDetectionStrategy, Component, computed, input, output } from '@angular/core';

export type AtbCheckStatus = 'pass' | 'warn' | 'fail';
export interface AtbCheckFinding { readonly id?: string; readonly title?: string; readonly message: string; }
export interface AtbCheck {
  readonly id: string; readonly group: string; readonly title: string;
  readonly severity: 'error' | 'warning'; readonly status: AtbCheckStatus; readonly items: readonly AtbCheckFinding[];
}

const STATUS: Record<AtbCheckStatus, { tone: string; glyph: string; word: string }> = {
  pass: { tone: 'success', glyph: '✓', word: 'Passed' }, warn: { tone: 'warning', glyph: '!', word: 'Warning' }, fail: { tone: 'error', glyph: '✕', word: 'Failed' },
};

/**
 * Check row: one rule of the validator with its result and the elements that fail it.
 * Each finding with an element id is a link (emits `open` with the id). The status word is in a visually hidden span.
 */
@Component({
  selector: 'atb-check-row',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { '[class]': '"atb-check-row " + check().status' },
  template: `
    <span class="tile" [class]="'tile t-' + s().tone" aria-hidden="true">{{ s().glyph }}</span>
    <div class="body">
      <div class="title"><b>{{ check().title }}</b><span class="id">{{ check().id }} · {{ check().severity === 'error' ? 'blocking' : 'warning' }}</span><span class="sr">{{ s().word }}</span></div>
      @if (check().items.length) {
        <ul>
          @for (f of check().items; track $index) {
            <li>
              @if (f.id) { <button type="button" class="lnk" (click)="open.emit(f.id!)">{{ f.title || f.id }}</button> · }
              {{ f.message }}
            </li>
          }
        </ul>
      }
    </div>
  `,
  styles: [`
    :host { display:flex; gap:10px; padding:10px 0; border-top:1px solid var(--md-sys-color-outline-variant); font:14px/20px var(--md-sys-typescale-plain-family, sans-serif); color:var(--md-sys-color-on-surface); }
    :host:first-of-type { border-top:0; }
    .tile { width:20px; height:20px; border-radius:4px; display:inline-grid; place-items:center; flex:none; font:700 12px/1 var(--md-sys-typescale-plain-family, sans-serif); }
    .t-success { background:var(--md-sys-color-success); color:var(--md-sys-color-on-success); }
    .t-warning { background:var(--md-sys-color-warning); color:var(--md-sys-color-on-warning); }
    .t-error { background:var(--md-sys-color-error); color:var(--md-sys-color-on-error); }
    .body { min-width:0; }
    .title { display:flex; flex-wrap:wrap; gap:2px 10px; align-items:baseline; }
    .title b { font:600 14px/20px var(--md-sys-typescale-brand-family, sans-serif); }
    .id { font:600 12px/16px var(--md-sys-typescale-brand-family, sans-serif); color:var(--md-sys-color-on-surface-variant); }
    ul { margin:6px 0 0; padding-left:18px; color:var(--md-sys-color-on-surface-variant); font-size:13px; }
    .lnk { border:0; background:none; padding:0; color:var(--md-sys-color-primary); font:inherit; cursor:pointer; text-decoration:underline; text-underline-offset:2px; }
    .lnk:focus-visible { outline:2px solid var(--md-sys-color-focus-ring); outline-offset:2px; border-radius:2px; }
    .sr { position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; }
  `],
})
export class AtbCheckRowComponent {
  readonly check = input.required<AtbCheck>();
  readonly open = output<string>();
  readonly s = computed(() => STATUS[this.check().status]);
}
