// AIToolbox — Material 3 window size classes for Angular (CDK BreakpointObserver).
// The CDK Breakpoints constants (600 / 960 / 1280 / 1920) do not match Material 3: use these queries instead.
import { BreakpointObserver } from '@angular/cdk/layout';
import { computed, inject, Injectable } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { map } from 'rxjs';

export const AIT_BREAKPOINTS = { medium: 600, expanded: 840, large: 1200, extraLarge: 1600 } as const;

export const AitWindow = {
  Compact: '(max-width: 599.98px)',
  Medium: '(min-width: 600px) and (max-width: 839.98px)',
  Expanded: '(min-width: 840px) and (max-width: 1199.98px)',
  Large: '(min-width: 1200px) and (max-width: 1599.98px)',
  ExtraLarge: '(min-width: 1600px)',
  ShortHeight: '(max-height: 479.98px)',
} as const;

export type AitSizeClass = 'compact' | 'medium' | 'expanded' | 'large' | 'extra-large';
export type AitNavigation = 'bar' | 'rail' | 'drawer';
export type AitAssistantMode = 'full-screen' | 'in-place' | 'docked';

/** Current window class and the shell decisions that follow from it (signals). */
@Injectable({ providedIn: 'root' })
export class AitWindowClass {
  private readonly observer = inject(BreakpointObserver);
  private readonly state = toSignal(this.observer.observe(Object.values(AitWindow)).pipe(map(() => ({
    cls: this.observer.isMatched(AitWindow.ExtraLarge) ? 'extra-large' as const
       : this.observer.isMatched(AitWindow.Large) ? 'large' as const
       : this.observer.isMatched(AitWindow.Expanded) ? 'expanded' as const
       : this.observer.isMatched(AitWindow.Medium) ? 'medium' as const : 'compact' as const,
    short: this.observer.isMatched(AitWindow.ShortHeight),
  }))), { requireSync: true });

  readonly windowClass = computed<AitSizeClass>(() => this.state().cls);
  readonly isCompact = computed(() => this.state().cls === 'compact');
  /** bottom NavigationBar under 600 px (rail on a phone in landscape), rail 600–1199 px, drawer from 1200 px. */
  readonly navigation = computed<AitNavigation>(() => {
    const c = this.state().cls;
    if (c === 'compact') return this.state().short ? 'rail' : 'bar';
    return c === 'medium' || c === 'expanded' ? 'rail' : 'drawer';
  });
  /** mat-sidenav mode for the drawer: side from 1200 px, over below. */
  readonly drawerMode = computed<'side' | 'over'>(() => (this.navigation() === 'drawer' ? 'side' : 'over'));
  readonly assistantMode = computed<AitAssistantMode>(() => {
    const c = this.state().cls;
    return c === 'compact' ? 'full-screen' : c === 'medium' || c === 'expanded' ? 'in-place' : 'docked';
  });
  /** forms in dialogs open full screen under 600 px or on a short screen. */
  readonly fullScreenDialogs = computed(() => this.state().cls === 'compact' || this.state().short);
}
