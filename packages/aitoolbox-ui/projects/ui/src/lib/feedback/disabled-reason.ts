import { Directive, inject, input } from '@angular/core';
import { MatTooltip } from '@angular/material/tooltip';

/**
 * Disabled reason (Tooltip E) — why an action is unavailable and how to unlock it, two lines at most, ending with the way
 * out. Pair it with Material's `disabledInteractive` so the button stays focusable and keyboard users get the reason:
 *
 * ```html
 * <button mat-flat-button disabled disabledInteractive aitDisabledReason="Choose a variant for every decision first.">
 *   Approve design
 * </button>
 * ```
 * The reason is also the button's accessible description (MatTooltip registers it with aria-describedby).
 */
@Directive({
  selector: '[aitDisabledReason]',
  hostDirectives: [{ directive: MatTooltip, inputs: ['matTooltip: aitDisabledReason', 'matTooltipPosition: aitDisabledReasonPosition'] }],
})
export class AitDisabledReason {
  readonly aitDisabledReason = input.required<string>();
  readonly aitDisabledReasonPosition = input<'above' | 'below' | 'left' | 'right' | 'before' | 'after'>('above');

  constructor() {
    // Design-system timing: 500 ms show delay on hover (immediate on keyboard focus is Material's default), 150 ms hide.
    const tooltip = inject(MatTooltip);
    tooltip.showDelay = 500;
    tooltip.hideDelay = 150;
  }
}

