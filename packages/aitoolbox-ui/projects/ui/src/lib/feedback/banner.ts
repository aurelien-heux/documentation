import { booleanAttribute, ChangeDetectionStrategy, Component, inject, input, output } from '@angular/core';
import { MatIconButton } from '@angular/material/button';
import { MatIcon } from '@angular/material/icon';
import { AitIconRegistry } from '../core/icons';
import { AitState } from '../core/state';
import { AitStateMark } from '../state-mark/state-mark';

/**
 * Banner — an inline alert on the state container strip, led by the 28 px state mark (badge). Errors are announced
 * (`role="alert"`), the other states are polite (`role="status"`). Actions are projected text buttons marked `aitBannerAction`.
 *
 * ```html
 * <ait-banner state="warning" heading="Changes requested.">Revision 3 is queued as run-0150.</ait-banner>
 * ```
 */
@Component({
  selector: 'ait-banner',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [AitStateMark, MatIconButton, MatIcon],
  host: {
    '[class]': '"ait-banner ait-banner--" + state()',
    '[attr.role]': 'state() === "error" ? "alert" : "status"',
  },
  template: `
    <ait-state-mark [state]="state()" variant="badge" [size]="28" />
    <div class="text">
      @if (heading()) {
        <span class="heading">{{ heading() }}</span>
      }
      <ng-content />
    </div>
    <div class="actions"><ng-content select="[aitBannerAction]" /></div>
    @if (dismissible()) {
      <button mat-icon-button type="button" class="close" aria-label="Dismiss" (click)="dismissed.emit()">
        <mat-icon svgIcon="ait:close" />
      </button>
    }
  `,
  styles: `
    :host { display: flex; flex-wrap: wrap; align-items: center; gap: 12px; padding: 12px 16px; border-radius: 12px;
      font: var(--ait-type-body-medium); letter-spacing: var(--ait-type-body-medium-tracking); }
    :host(.ait-banner--success) { background: var(--md-sys-color-success-container); color: var(--md-sys-color-on-success-container); }
    :host(.ait-banner--info) { background: var(--md-sys-color-primary-container); color: var(--md-sys-color-on-primary-container); }
    :host(.ait-banner--warning) { background: var(--md-sys-color-warning-container); color: var(--md-sys-color-on-warning-container); }
    :host(.ait-banner--error) { background: var(--md-sys-color-error-container); color: var(--md-sys-color-on-error-container); }
    .text { flex: 1 1 320px; min-width: 0; }
    .heading { font: var(--ait-type-title-small); letter-spacing: var(--ait-type-title-small-tracking); margin-right: 4px; }
    .actions { display: flex; gap: 4px; --mat-button-text-label-text-color: currentColor; }
    .actions:empty { display: none; }
    .close { color: inherit; margin: -8px -8px -8px 0; }
  `,
})
export class AitBanner {
  readonly state = input<AitState>('info');
  readonly heading = input('');
  readonly dismissible = input(false, { transform: booleanAttribute });
  readonly dismissed = output<void>();
  constructor() {
    inject(AitIconRegistry);
  }
}
