import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';
import { MatChip, MatChipAvatar } from '@angular/material/chips';
import { AitHealth } from '../core/state';
import { AitStateMark } from '../state-mark/state-mark';

/**
 * StatusChip — health on a `*-container` fill, led by the 18 px tinted tile glyph, never colour alone.
 * Built on `mat-chip` with the `dt-chip-*` classes of the theme files; not interactive.
 *
 * ```html
 * <ait-status-chip state="success">Healthy</ait-status-chip>
 * <ait-status-chip state="unknown">No data</ait-status-chip>
 * ```
 */
@Component({
  selector: 'ait-status-chip',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [MatChip, MatChipAvatar, AitStateMark],
  host: { class: 'ait-status-chip' },
  template: `
    <mat-chip [class]="chipClass()" [disableRipple]="true" [highlighted]="false">
      @if (state() === 'unknown') {
        <span matChipAvatar class="ait-status-chip__dot" aria-hidden="true"></span>
      } @else {
        <ait-state-mark matChipAvatar [state]="$any(state())" variant="tinted" [size]="18" />
      }
      <ng-content />
    </mat-chip>
  `,
  styles: `
    :host { display: inline-flex; vertical-align: middle; }
    /* Higher specificity than the M2 theme's chip tokens (html .mat-mdc-standard-chip…), so M2 and M3 render alike. */
    :host .mat-mdc-standard-chip.ait-sc {
      --mat-chip-container-height: 24px;
      --mat-chip-container-shape-radius: 4px;
      --mat-chip-with-avatar-avatar-size: 18px;
      --mat-chip-with-avatar-avatar-shape-radius: 4px;
      --mat-chip-label-text-font: var(--ait-font-ui);
      --mat-chip-label-text-size: 12px;
      --mat-chip-label-text-weight: 500;
      --mat-chip-label-text-tracking: 0.5px;
      --mat-chip-outline-width: 0;
      --mat-chip-elevated-container-color: var(--_ctr);
      --mat-chip-label-text-color: var(--_on-ctr);
      --mat-chip-elevated-disabled-container-color: var(--_ctr);
      cursor: default;
    }
    :host .ait-sc.dt-chip-success { --_ctr: var(--md-sys-color-success-container); --_on-ctr: var(--md-sys-color-on-success-container); }
    :host .ait-sc.dt-chip-warning { --_ctr: var(--md-sys-color-warning-container); --_on-ctr: var(--md-sys-color-on-warning-container); }
    :host .ait-sc.dt-chip-error { --_ctr: var(--md-sys-color-error-container); --_on-ctr: var(--md-sys-color-on-error-container); }
    :host .ait-sc.dt-chip-info { --_ctr: var(--md-sys-color-primary-container); --_on-ctr: var(--md-sys-color-on-primary-container); }
    :host .ait-sc.dt-chip-unknown { --_ctr: var(--md-sys-color-surface-container-highest); --_on-ctr: var(--md-sys-color-on-surface-variant); }
    .ait-status-chip__dot { width: 6px !important; height: 6px !important; border-radius: 9999px; background: var(--md-sys-color-outline); margin: 0 4px 0 6px; }
  `,
})
export class AitStatusChip {
  /** success · warning · error · info, or unknown (outline dot on surface-container-highest). */
  readonly state = input.required<AitHealth>();
  protected readonly chipClass = computed(() => `ait-sc dt-chip-${this.state()}`);
}

/** Log level word in a Trace or log view: only the word is coloured (Open Sans 600). */
@Component({
  selector: 'ait-log-level',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { '[class]': '"ait-log-level ait-log-level--" + level()' },
  template: `{{ level() }}`,
  styles: `
    :host { font-family: var(--ait-font-body); font-weight: 600; font-size: 12px; line-height: 16px; letter-spacing: 0.4px; }
    :host(.ait-log-level--INFO) { color: var(--md-sys-color-success); }
    :host(.ait-log-level--WARN) { color: var(--md-sys-color-warning); }
    :host(.ait-log-level--ERR) { color: var(--md-sys-color-error); }
    :host(.ait-log-level--DEBUG) { color: var(--md-sys-color-on-surface-variant); }
  `,
})
export class AitLogLevel {
  readonly level = input.required<'DEBUG' | 'INFO' | 'WARN' | 'ERR'>();
}
