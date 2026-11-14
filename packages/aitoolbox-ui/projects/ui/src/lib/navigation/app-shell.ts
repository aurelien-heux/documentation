import { NgTemplateOutlet } from '@angular/common';
import { ChangeDetectionStrategy, Component, computed, effect, forwardRef, inject, input, linkedSignal, signal } from '@angular/core';
import { MatIconButton } from '@angular/material/button';
import { MatDivider } from '@angular/material/divider';
import { MatIcon } from '@angular/material/icon';
import { MatListItem, MatListItemIcon, MatListItemMeta, MatListItemTitle, MatNavList } from '@angular/material/list';
import { MatMenu, MatMenuItem, MatMenuTrigger } from '@angular/material/menu';
import { MatSidenav, MatSidenavContainer, MatSidenavContent } from '@angular/material/sidenav';
import { MatTooltip } from '@angular/material/tooltip';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { AitIconRegistry } from '../core/icons';
import { AitWindowClass } from '../core/window-class';
import { AIT_SHELL, AitShellApi } from './shell-token';

/** One destination of the navigation. */
export interface AitNavItem {
  label: string;
  /** Registered SVG icon (`ait:runs`, `myset:deploy`) — or use `fontIcon` with a Material Symbols ligature. */
  icon?: string;
  fontIcon?: string;
  /** Router destination; `exact` matches the URL exactly. */
  route?: string | unknown[];
  exact?: boolean;
  /** Plain link when the destination is outside the app. */
  href?: string;
  /** Active state for `href` items (router items compute it). */
  active?: boolean;
  /** Trailing count in the drawer (label-medium). */
  count?: number | string;
  /** Unread or alert count: an error badge on the icon. */
  badge?: number;
  /** Starts a new group with an inset divider and this label. */
  section?: string;
  /** Show in the bottom NavigationBar on phones (3–5 destinations). */
  bar?: boolean;
}

export interface AitLegalLink {
  label: string;
  href: string;
}

const DEFAULT_LEGAL: AitLegalLink[] = [
  { label: 'Privacy', href: '/legal/privacy' },
  { label: 'Cookies', href: '/legal/cookies' },
  { label: 'Terms', href: '/legal/terms' },
];

/**
 * App shell — header, navigation and page area, following the window class:
 * - from 1200 px a standard 300 px NavigationDrawer that pushes the page; its menu button folds it to the 80 px rail;
 * - 600–1199 px the NavigationRail, whose menu button opens the drawer over the page (scrim);
 * - under 600 px the bottom NavigationBar (items with `bar: true`), the drawer opens from the header menu.
 *
 * ```html
 * <ait-app-shell [items]="nav" version="v4.5">
 *   <ait-app-header aitShellHeader [user]="me" />
 *   <router-outlet />
 * </ait-app-shell>
 * ```
 * Needs the router (`provideRouter`) for `route` items.
 */
@Component({
  selector: 'ait-app-shell',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [
    NgTemplateOutlet, RouterLink, RouterLinkActive, MatSidenavContainer, MatSidenav, MatSidenavContent, MatNavList, MatListItem,
    MatListItemIcon, MatListItemTitle, MatListItemMeta, MatIcon, MatIconButton, MatDivider, MatMenu, MatMenuItem, MatMenuTrigger, MatTooltip,
  ],
  providers: [{ provide: AIT_SHELL, useExisting: forwardRef(() => AitAppShell) }],
  host: { class: 'ait-app-shell', '[class]': '"ait-app-shell--" + layout()' },
  templateUrl: './app-shell.html',
  styleUrl: './app-shell.scss',
})
export class AitAppShell implements AitShellApi {
  private readonly windowClass = inject(AitWindowClass);

  readonly items = input.required<AitNavItem[]>();
  /** Destinations pinned to the bottom of the drawer and rail (Settings). */
  readonly bottomItems = input<AitNavItem[]>([]);
  readonly legalLinks = input<AitLegalLink[]>(DEFAULT_LEGAL);
  /** Shown in the drawer footer and under the rail, e.g. "v4.5". */
  readonly version = input('');
  /** Start folded to the rail at Large widths (the choice should be remembered per user). */
  readonly collapsed = input(false);

  /** Large+: the user folded the drawer to the rail. */
  protected readonly folded = linkedSignal(() => this.collapsed());
  /** Over-mode drawer open (rail menu, header menu). */
  protected readonly overlayOpen = signal(false);

  protected readonly nav = this.windowClass.navigation;
  /** drawer · rail · bar — what is on screen. */
  protected readonly layout = computed(() => (this.nav() === 'drawer' && this.folded() ? 'rail' : this.nav()));
  protected readonly drawerMode = computed(() => (this.nav() === 'drawer' && !this.folded() ? 'side' : 'over'));
  protected readonly drawerOpened = computed(() => (this.drawerMode() === 'side' ? true : this.overlayOpen()));
  protected readonly barItems = computed(() => {
    const flagged = this.items().filter((i) => i.bar);
    return (flagged.length ? flagged : this.items()).slice(0, 5);
  });

  constructor() {
    inject(AitIconRegistry);
    // Leaving a window class closes a drawer that was open over the page.
    effect(() => {
      this.nav();
      this.overlayOpen.set(false);
    });
  }

  openDrawer(): void {
    if (this.drawerMode() === 'side') return;
    this.overlayOpen.set(true);
  }

  closeDrawer(): void {
    this.overlayOpen.set(false);
  }

  /** Menu button: at Large, folds or unfolds; below, opens or closes the drawer over the page. */
  protected toggleFromMenu(): void {
    if (this.nav() === 'drawer') {
      this.folded.update((v) => !v);
      this.overlayOpen.set(false);
    } else {
      this.overlayOpen.update((v) => !v);
    }
  }

  protected onOpenedChange(open: boolean): void {
    if (this.drawerMode() === 'over') this.overlayOpen.set(open);
  }

  protected onNavigate(): void {
    if (this.drawerMode() === 'over') this.overlayOpen.set(false);
  }

  protected badgeText(n?: number): string {
    return !n || n <= 0 ? '' : n <= 9 ? String(n) : n <= 99 ? '9+' : '99+';
  }
}
