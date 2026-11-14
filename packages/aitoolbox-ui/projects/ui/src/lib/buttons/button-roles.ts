import { afterNextRender, DestroyRef, Directive, ElementRef, inject, Injectable, isDevMode } from '@angular/core';

/** Counts the Run buttons on screen so a second one is reported in development (INV-DS-02). */
@Injectable({ providedIn: 'root' })
export class AitRunRegistry {
  private readonly active = new Set<HTMLElement>();
  add(el: HTMLElement): void {
    this.active.add(el);
    if (isDevMode() && this.active.size > 1) {
      console.warn(`[aitRun] ${this.active.size} Run buttons on screen: the design system allows one per screen. Use aitRunText for repeated row actions.`, [...this.active]);
    }
  }
  delete(el: HTMLElement): void {
    this.active.delete(el);
  }
  get count(): number {
    return this.active.size;
  }
}

/**
 * Run — the ONE action per screen that starts work (Run, Deploy, Apply, New run): the night "terminal" button with the
 * neon play icon. Use on a filled Material button, with a leading icon:
 *
 * ```html
 * <button mat-flat-button aitRun><mat-icon svgIcon="ait:play" />Request Run</button>
 * ```
 * Never inside a dialog (confirm there with a filled primary button). Development builds warn on both mistakes.
 */
@Directive({
  selector: '[aitRun]',
  host: { class: 'dt-run' },
})
export class AitRun {
  constructor() {
    const el = inject(ElementRef<HTMLElement>).nativeElement as HTMLElement;
    const registry = inject(AitRunRegistry);
    registry.add(el);
    inject(DestroyRef).onDestroy(() => registry.delete(el));
    afterNextRender(() => {
      if (isDevMode() && el.closest('mat-dialog-container, .mat-mdc-dialog-container, [role="dialog"], [role="alertdialog"]')) {
        console.warn('[aitRun] The Run button is never used inside a dialog: confirm with a filled primary button.', el);
      }
    });
  }
}

/** Repeated run actions (table rows, cards): a text button in on-surface with the tertiary play icon, never filled. */
@Directive({ selector: '[aitRunText]', host: { class: 'dt-run-text' } })
export class AitRunText {}

/** Tonal button (secondary-container) beside a filled one. Works on M2 and M3: `<button mat-flat-button aitTonal>`. */
@Directive({ selector: '[aitTonal]', host: { class: 'dt-tonal' } })
export class AitTonal {}

/** Destructive action: a text button in error, never a filled red. `<button mat-button aitDanger>Delete</button>` */
@Directive({ selector: '[aitDanger]', host: { class: 'dt-danger' } })
export class AitDanger {}

/** AI-powered features only (teal), always with the sparkle icon: buttons, chips, cards. */
@Directive({ selector: '[aitAi]', host: { class: 'dt-ai' } })
export class AitAi {}
