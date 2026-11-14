import { ChangeDetectionStrategy, Component, computed, inject, input, output, viewChild } from '@angular/core';
import { MatIconButton } from '@angular/material/button';
import { MatIcon } from '@angular/material/icon';
import { MatMenu, MatMenuItem, MatMenuTrigger } from '@angular/material/menu';
import { MatDivider } from '@angular/material/divider';
import { MatTooltip } from '@angular/material/tooltip';
import { RouterLink } from '@angular/router';
import { AitIconRegistry } from '../core/icons';
import { AitWindowClass } from '../core/window-class';
import { AitChatbotMark, AitLogo } from '../brand/logo';
import { AitWorkingDots } from '../progress/progress';
import { AitSearchAsk } from './search-ask';
import { AIT_SHELL } from './shell-token';

export interface AitUser {
  name: string;
  /** Shown under the name from 1200 px, e.g. "platform · admin". */
  role?: string;
  /** Two letters for the avatar; derived from the name when omitted. */
  initials?: string;
}

export type AitUserMenuAction = 'account' | 'notifications' | 'tokens' | 'theme' | 'sign-out';
/** idle · typing (an answer is being written while the block is closed) · waiting (a reply waits to be read). */
export type AitAssistantState = 'idle' | 'typing' | 'waiting';

/**
 * App header (TopAppBar) of the AIToolbox shell, on nav-container like the drawer. Left to right: logo · search-or-ask
 * field centred · assistant · notifications · help · user chip. Follows the window class:
 * under 600 px 56 px with menu · mark · search icon · bell · avatar; 600–1199 px search flexes, Ask as an icon, avatar
 * only (help from 840 px); from 1200 px 600 px search, labelled Ask, user chip with name and role.
 * ⌘J / Ctrl+J toggles the assistant.
 */
@Component({
  selector: 'ait-app-header',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [MatIconButton, MatIcon, MatMenu, MatMenuItem, MatMenuTrigger, MatDivider, MatTooltip, RouterLink, AitLogo, AitChatbotMark, AitWorkingDots, AitSearchAsk],
  host: {
    class: 'ait-app-header dt-nav',
    role: 'banner',
    '[class.ait-app-header--compact]': 'compact()',
    '(document:keydown)': 'onDocumentKey($event)',
  },
  template: `
    <div class="start">
      @if (compact()) {
        <button mat-icon-button type="button" aria-label="Open navigation" (click)="openNavigation()"><mat-icon svgIcon="ait:menu" /></button>
        <a [routerLink]="homeLink()" class="home" aria-label="AIToolbox home"><ait-logo variant="mark" [size]="28" label="" /></a>
      } @else {
        <a [routerLink]="homeLink()" class="home"><ait-logo variant="horizontal" [size]="44" label="AIToolbox home" /></a>
      }
    </div>

    @if (!compact()) {
      <ait-search-ask class="search" [compactAsk]="!wide()" [placeholder]="searchPlaceholder()" [askDisabledReason]="askDisabledReason()"
        (search)="search.emit($event)" (ask)="ask.emit($event)" />
    }

    <div class="end">
      @if (compact()) {
        <button mat-icon-button type="button" aria-label="Search" (click)="searchOpen.emit()"><mat-icon svgIcon="ait:search" /></button>
      } @else {
        <button mat-icon-button type="button" class="assistant" [class.assistant--open]="assistantOpen()" [attr.aria-expanded]="assistantOpen()"
          [attr.aria-label]="assistantLabel()" [matTooltip]="(assistantOpen() ? 'Close' : 'Open') + ' assistant ' + shortcutJ" (click)="assistantToggle.emit()">
          <ait-chatbot-mark [size]="24" />
          @if (assistant() === 'typing') { <ait-working-dots kind="ai" class="assistant__dots" label="" aria-hidden="true" /> }
          @if (assistant() === 'waiting') { <span class="assistant__dot" aria-hidden="true"></span> }
        </button>
      }
      <button mat-icon-button type="button" class="bell" [attr.aria-label]="bellLabel()" matTooltip="Notifications" (click)="notificationsClick.emit()">
        <svg viewBox="0 0 64 64" width="24" height="24" aria-hidden="true" focusable="false">
          <circle cx="32" cy="8" r="3.6" class="bell__body" />
          <path d="M32 9C22 9 17 17 17 27V38L12 46Q11 48.5 13.5 48.5H50.5Q53 48.5 52 46L47 38V27C47 17 42 9 32 9Z" class="bell__body" />
          <circle cx="32" cy="53.5" r="5" class="bell__clapper" />
        </svg>
        @if (badge()) { <span class="badge" aria-hidden="true">{{ badge() }}</span> }
      </button>
      @if (showHelp()) {
        <button mat-icon-button type="button" aria-label="Help" matTooltip="Help" (click)="helpClick.emit()"><mat-icon svgIcon="ait:help" /></button>
      }
      @if (!compact()) { <span class="divider" aria-hidden="true"></span> }
      <button type="button" class="user" [matMenuTriggerFor]="userMenu" aria-haspopup="menu" [attr.aria-label]="userLabel()">
        <span class="avatar">{{ initials() }}</span>
        @if (wide()) {
          <span class="user__text"><span class="user__name">{{ user().name }}</span>
            @if (user().role) { <span class="user__role">{{ user().role }}</span> }</span>
          <mat-icon svgIcon="ait:chevron-down" class="user__chev" />
        }
      </button>
      <mat-menu #userMenu="matMenu" xPosition="before">
        <button mat-menu-item (click)="userMenuAction.emit('account')"><mat-icon svgIcon="ait:person" />Account</button>
        <button mat-menu-item (click)="userMenuAction.emit('notifications')"><mat-icon svgIcon="ait:bell" />Notification preferences</button>
        <button mat-menu-item (click)="userMenuAction.emit('tokens')"><mat-icon svgIcon="ait:key" />API tokens</button>
        <button mat-menu-item (click)="userMenuAction.emit('theme')"><mat-icon svgIcon="ait:palette" />Theme</button>
        @if (!showHelp()) {
          <button mat-menu-item (click)="helpClick.emit()"><mat-icon svgIcon="ait:help" />Help</button>
        }
        <mat-divider />
        <button mat-menu-item (click)="userMenuAction.emit('sign-out')"><mat-icon svgIcon="ait:logout" />Sign out</button>
      </mat-menu>
    </div>
  `,
  styles: `
    :host { display: grid; grid-template-columns: minmax(max-content, 1fr) minmax(240px, 600px) minmax(max-content, 1fr); align-items: center; gap: 12px; height: 64px; padding: 0 8px 0 12px;
      box-sizing: border-box; background: var(--md-sys-color-nav-container); color: var(--md-sys-color-on-surface); position: relative; z-index: 3; }
    :host(.ait-app-header--compact) { grid-template-columns: 1fr auto; height: 56px; padding: 0 4px; }
    .start { display: flex; align-items: center; gap: 4px; justify-self: start; min-width: 0; }
    .home { display: inline-flex; border-radius: 8px; }
    .search { min-width: 0; }
    .end { display: flex; align-items: center; justify-self: end; gap: 0; }
    button[mat-icon-button] { color: var(--md-sys-color-on-surface-variant); position: relative; }
    .assistant--open { background: var(--md-sys-color-nav-active); }
    .assistant__dots { position: absolute; bottom: 2px; left: 50%; transform: translateX(-50%) scale(.6); }
    .assistant__dot { position: absolute; top: 8px; right: 8px; width: 8px; height: 8px; border-radius: 9999px; background: var(--md-sys-color-tertiary); box-shadow: 0 0 0 2px var(--md-sys-color-nav-container); }
    .bell__body { fill: var(--md-sys-color-primary); }
    .bell__clapper { fill: var(--md-sys-color-ai); }
    .badge { position: absolute; top: 4px; left: 22px; min-width: 16px; height: 16px; padding: 0 4px; box-sizing: border-box; border-radius: 9999px;
      background: var(--md-sys-color-error); color: var(--md-sys-color-on-error); font-family: var(--ait-font-body); font-weight: 600; font-size: 11px; line-height: 16px;
      text-align: center; box-shadow: 0 0 0 2px var(--md-sys-color-nav-container); }
    .divider { width: 1px; height: 24px; background: var(--md-sys-color-outline-variant); margin: 0 6px; }
    .user { display: inline-flex; align-items: center; gap: 8px; height: 48px; padding: 0 8px 0 4px; border: 0; border-radius: 16px; background: transparent; color: inherit; cursor: pointer; text-align: left; }
    .user:hover { background: color-mix(in srgb, var(--md-sys-color-primary) 6%, transparent); }
    .avatar { width: 32px; height: 32px; border-radius: 9999px; background: var(--md-sys-color-nav-active); color: var(--md-sys-color-on-secondary-container);
      display: inline-flex; align-items: center; justify-content: center; font: var(--ait-type-label-large); flex: none; }
    .user__text { display: flex; flex-direction: column; line-height: 1.15; }
    .user__name { font: var(--ait-type-title-small); letter-spacing: .1px; }
    .user__role { font: var(--ait-type-body-small); color: var(--md-sys-color-on-surface-variant); }
    .user__chev { width: 18px; height: 18px; color: var(--md-sys-color-on-surface-variant); }
  `,
})
export class AitAppHeader {
  private readonly windowClass = inject(AitWindowClass);
  private readonly shell = inject(AIT_SHELL, { optional: true });
  private readonly searchField = viewChild(AitSearchAsk);

  readonly user = input.required<AitUser>();
  readonly notificationCount = input(0);
  readonly assistant = input<AitAssistantState>('idle');
  readonly assistantOpen = input(false);
  readonly searchPlaceholder = input('Search, or ask the assistant…');
  readonly askDisabledReason = input('');
  readonly homeLink = input<string | unknown[]>('/');

  readonly search = output<string>();
  readonly ask = output<string>();
  /** Compact windows: the search icon was pressed (open the full-screen search view). */
  readonly searchOpen = output<void>();
  readonly assistantToggle = output<void>();
  readonly notificationsClick = output<void>();
  readonly helpClick = output<void>();
  readonly userMenuAction = output<AitUserMenuAction>();
  /** Compact windows: the menu button was pressed. The AppShell opens its drawer by itself. */
  readonly menuClick = output<void>();

  protected readonly compact = this.windowClass.isCompact;
  protected readonly wide = computed(() => ['large', 'extra-large'].includes(this.windowClass.windowClass()));
  protected readonly showHelp = computed(() => !['compact', 'medium'].includes(this.windowClass.windowClass()));
  protected readonly shortcutJ = typeof navigator !== 'undefined' && /Mac|iP(hone|ad)/.test(navigator.platform) ? '⌘J' : 'Ctrl+J';
  protected readonly initials = computed(() => {
    const u = this.user();
    return (u.initials ?? u.name.split(/\s+/).map((p) => p[0]).join('').slice(0, 2)).toUpperCase();
  });
  protected readonly badge = computed(() => {
    const n = this.notificationCount();
    return n <= 0 ? '' : n <= 9 ? String(n) : n <= 99 ? '9+' : '99+';
  });
  protected readonly bellLabel = computed(() => (this.notificationCount() > 0 ? `Notifications, ${this.notificationCount()} unread` : 'Notifications'));
  protected readonly assistantLabel = computed(() => {
    const base = this.assistantOpen() ? 'Close assistant' : 'Open assistant';
    return this.assistant() === 'waiting' ? `${base}, answer ready` : this.assistant() === 'typing' ? `${base}, writing an answer` : base;
  });
  protected readonly userLabel = computed(() => `${this.user().name}${this.user().role ? ', ' + this.user().role : ''}, account menu`);

  constructor() {
    inject(AitIconRegistry);
  }

  /** Moves focus into the search field (also bound to ⌘K / Ctrl+K). */
  focusSearch(): void {
    this.searchField()?.focus();
  }

  protected openNavigation(): void {
    this.menuClick.emit();
    this.shell?.openDrawer();
  }

  protected onDocumentKey(e: KeyboardEvent): void {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'j') {
      e.preventDefault();
      this.assistantToggle.emit();
    }
  }
}
