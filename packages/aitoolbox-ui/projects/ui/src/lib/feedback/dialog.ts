import { ChangeDetectionStrategy, Component, inject, Injectable, input } from '@angular/core';
import { MatButton } from '@angular/material/button';
import { MAT_DIALOG_DATA, MatDialog, MatDialogActions, MatDialogClose, MatDialogContent, MatDialogTitle } from '@angular/material/dialog';
import { map, Observable } from 'rxjs';
import { AitState } from '../core/state';
import { AitWindowClass } from '../core/window-class';
import { AitStateMark } from '../state-mark/state-mark';
import { AitDanger } from '../buttons/button-roles';

/**
 * Dialog title with the optional 32 px state mark of a state-driven popin (destructive confirm, warning).
 * `<h2 mat-dialog-title aitDialogTitle state="warning">Cancel run-0147?</h2>`
 */
@Component({
  selector: '[aitDialogTitle]',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [AitStateMark],
  host: { class: 'ait-dialog-title' },
  template: `
    @if (state()) {
      <ait-state-mark [state]="state()!" variant="badge" [size]="32" />
    }
    <span><ng-content /></span>
  `,
  styles: `:host { display: flex !important; align-items: center; gap: 12px; }`,
})
export class AitDialogTitle {
  readonly state = input<AitState | undefined>(undefined);
}

export interface AitConfirmOptions {
  title: string;
  /** One or two sentences: what happens, and what is kept. */
  message: string;
  confirmLabel: string;
  dismissLabel?: string;
  /** Destructive confirm: a text button in error, never a filled red. */
  destructive?: boolean;
  /** 32 px state mark next to the title. Defaults to `warning` for destructive confirms. */
  state?: AitState;
}

@Component({
  selector: 'ait-confirm-dialog',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [MatDialogTitle, MatDialogContent, MatDialogActions, MatDialogClose, MatButton, AitDialogTitle, AitDanger],
  template: `
    <h2 mat-dialog-title aitDialogTitle [state]="data.state ?? (data.destructive ? 'warning' : undefined)">{{ data.title }}</h2>
    <mat-dialog-content><p class="message">{{ data.message }}</p></mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button type="button" [mat-dialog-close]="false" cdkFocusInitial>{{ data.dismissLabel ?? 'Cancel' }}</button>
      @if (data.destructive) {
        <button mat-button aitDanger type="button" [mat-dialog-close]="true">{{ data.confirmLabel }}</button>
      } @else {
        <button mat-flat-button type="button" [mat-dialog-close]="true">{{ data.confirmLabel }}</button>
      }
    </mat-dialog-actions>
  `,
  styles: `.message { margin: 0; color: var(--md-sys-color-on-surface-variant); }`,
})
export class AitConfirmDialog {
  protected readonly data = inject<AitConfirmOptions>(MAT_DIALOG_DATA);
}

/**
 * Confirmation dialogs with the design-system rules: 280–560 px, headline-small title, text dismiss, filled primary
 * confirm, text-in-error confirm when destructive; focus starts on the dismiss button.
 *
 * ```ts
 * this.confirm.open({ title: 'Cancel run-0147?', message: '…', confirmLabel: 'Cancel Run', destructive: true })
 *   .subscribe(ok => ok && this.cancel());
 * ```
 */
@Injectable({ providedIn: 'root' })
export class AitConfirm {
  private readonly dialog = inject(MatDialog);
  private readonly windowClass = inject(AitWindowClass);

  open(options: AitConfirmOptions): Observable<boolean> {
    return this.dialog
      .open(AitConfirmDialog, {
        data: options,
        width: '560px',
        maxWidth: this.windowClass.isCompact() ? 'calc(100vw - 32px)' : '560px',
        minWidth: '280px',
        autoFocus: 'first-tabbable',
        role: options.destructive ? 'alertdialog' : 'dialog',
      })
      .afterClosed()
      .pipe(map((v) => v === true));
  }
}
