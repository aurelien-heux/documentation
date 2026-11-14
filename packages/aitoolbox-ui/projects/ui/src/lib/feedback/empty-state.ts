import { ChangeDetectionStrategy, Component, computed, input, numberAttribute } from '@angular/core';
import { AitStateOrPending } from '../core/state';
import { AitStateMark } from '../state-mark/state-mark';

/**
 * Empty or error state of a page, panel or table: the circle state mark (56–96 px), a title, the cause and the way out.
 * While the request is pending the same slot shows the pending ring, so nothing moves when it resolves.
 *
 * ```html
 * <ait-empty-state state="error" title="Runs could not load" cause="The run service did not answer in 10 s.">
 *   <button mat-flat-button (click)="retry()">Retry</button>
 * </ait-empty-state>
 * ```
 */
@Component({
  selector: 'ait-empty-state',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [AitStateMark],
  host: {
    class: 'ait-empty-state',
    '[attr.role]': 'state() === "error" ? "alert" : "status"',
    '[attr.aria-busy]': 'state() === "pending" ? "true" : null',
  },
  template: `
    <ait-state-mark [state]="state()" variant="circle" [size]="size()" />
    <h2 class="title">{{ title() }}</h2>
    @if (cause()) {
      <p class="cause">{{ cause() }}</p>
    }
    <div class="actions"><ng-content /></div>
  `,
  styles: `
    :host { display: flex; flex-direction: column; align-items: center; text-align: center; gap: 8px; padding: 48px 24px; }
    .title { margin: 8px 0 0; font: var(--ait-type-title-medium); letter-spacing: var(--ait-type-title-medium-tracking); color: var(--md-sys-color-on-surface); }
    .cause { margin: 0; max-width: 480px; font: var(--ait-type-body-medium); letter-spacing: var(--ait-type-body-medium-tracking); color: var(--md-sys-color-on-surface-variant); }
    .actions { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin-top: 8px; }
    .actions:empty { display: none; }
  `,
})
export class AitEmptyState {
  readonly state = input<AitStateOrPending>('info');
  readonly title = input.required<string>();
  readonly cause = input('');
  /** 56–64 inside a table or panel, 72–96 for a whole page. */
  readonly size = input(64, { transform: numberAttribute });
  protected readonly isPending = computed(() => this.state() === 'pending');
}
