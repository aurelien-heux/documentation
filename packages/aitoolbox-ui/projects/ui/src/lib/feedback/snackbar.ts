import { ChangeDetectionStrategy, Component, inject, Injectable } from '@angular/core';
import { MatButton, MatIconButton } from '@angular/material/button';
import { MatIcon } from '@angular/material/icon';
import { MAT_SNACK_BAR_DATA, MatSnackBar, MatSnackBarRef } from '@angular/material/snack-bar';
import { AitIconRegistry } from '../core/icons';
import { AitState } from '../core/state';
import { AitStateMark } from '../state-mark/state-mark';

export interface AitSnackBarOptions {
  /** Leading 24 px state mark. Omit for a neutral confirmation. */
  state?: AitState;
  /** One optional action, in inverse-primary. */
  action?: string;
  /** 4–10 s; defaults to 6 s, or no auto-dismiss when there is an action the user must be able to reach. */
  duration?: number;
  /** Show a close icon button. */
  closable?: boolean;
}

interface AitSnackBarData extends AitSnackBarOptions {
  message: string;
}

/** Content of the AIToolbox snackbar. Opened through AitSnackBar; not used directly. */
@Component({
  selector: 'ait-snack-bar',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [AitStateMark, MatButton, MatIconButton, MatIcon],
  host: { class: 'ait-snack-bar' },
  template: `
    @if (data.state) {
      <span class="ait-on-inverse mark"><ait-state-mark [state]="data.state" variant="badge" [size]="24" /></span>
    }
    <span class="message">{{ data.message }}</span>
    @if (data.action) {
      <button mat-button type="button" (click)="ref.dismissWithAction()">{{ data.action }}</button>
    }
    @if (data.closable) {
      <button mat-icon-button type="button" aria-label="Close" class="close" (click)="ref.dismiss()"><mat-icon svgIcon="ait:close" /></button>
    }
  `,
  styles: `
    :host { display: flex; align-items: center; gap: 12px; min-height: 40px; color: var(--md-sys-color-inverse-on-surface);
      font: var(--ait-type-body-medium); letter-spacing: var(--ait-type-body-medium-tracking); }
    .mark { display: inline-flex; }
    .message { flex: 1; }
    button { --mat-button-text-label-text-color: var(--md-sys-color-inverse-primary); flex: none; }
    .close { color: var(--md-sys-color-inverse-on-surface); }
  `,
})
export class AitSnackBarContent {
  protected readonly data = inject<AitSnackBarData>(MAT_SNACK_BAR_DATA);
  protected readonly ref = inject(MatSnackBarRef<AitSnackBarContent>);
  constructor() {
    inject(AitIconRegistry);
  }
}

/**
 * Snackbar with the design-system anatomy: inverse surface, 24 px state mark, one action. Never for an error that needs
 * a decision (use a dialog), never stacked (opening one replaces the previous).
 *
 * ```ts
 * inject(AitSnackBar).open('Design approved · implement Run requested', { state: 'success', action: 'View design' });
 * ```
 */
@Injectable({ providedIn: 'root' })
export class AitSnackBar {
  private readonly snackBar = inject(MatSnackBar);

  open(message: string, options: AitSnackBarOptions = {}): MatSnackBarRef<AitSnackBarContent> {
    const duration = options.duration ?? (options.action ? 10000 : 6000);
    return this.snackBar.openFromComponent(AitSnackBarContent, {
      data: { message, ...options } satisfies AitSnackBarData,
      duration,
      panelClass: 'ait-snackbar-panel',
      politeness: options.state === 'error' ? 'assertive' : 'polite',
    });
  }

  dismiss(): void {
    this.snackBar.dismiss();
  }
}
