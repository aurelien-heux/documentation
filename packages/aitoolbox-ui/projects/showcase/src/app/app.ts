import { Component, inject, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AitAppHeader, AitAppShell, AitNavItem, AitSnackBar, AitUserMenuAction } from '@aitoolbox/ui';
import { DOCUMENT } from '@angular/common';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, AitAppShell, AitAppHeader],
  template: `
    <ait-app-shell [items]="nav" [bottomItems]="bottom" version="v4.5">
      <ait-app-header [user]="{ name: 'Aurélien Heux', role: 'platform · admin' }" [notificationCount]="3"
        [assistantOpen]="assistantOpen()" [assistant]="assistantOpen() ? 'idle' : 'waiting'"
        (assistantToggle)="assistantOpen.set(!assistantOpen())" (userMenuAction)="onUserMenu($event)"
        (search)="snack.open('Search: ' + $event)" (ask)="snack.open('Sent to the assistant', { state: 'info' })" />
      <router-outlet />
    </ait-app-shell>
  `,
})
export class App {
  protected readonly snack = inject(AitSnackBar);
  private readonly document = inject(DOCUMENT);
  protected readonly assistantOpen = signal(false);

  protected readonly nav: AitNavItem[] = [
    { label: 'Catalog', icon: 'ait:grid', href: '#catalog' },
    { label: 'Documentation', icon: 'ait:book', href: '#docs' },
    { label: 'Design System', icon: 'ait:swatch', route: '/components', bar: true },
    { label: 'Environments', icon: 'ait:environments', href: '#environments', badge: 2, bar: true },
    { label: 'Work items', icon: 'ait:tasks', href: '#work-items', section: 'Delivery' },
    { label: 'Runs', icon: 'ait:play', route: '/runs', count: 4, bar: true },
  ];
  protected readonly bottom: AitNavItem[] = [{ label: 'Settings', icon: 'ait:settings', href: '#settings' }];

  protected onUserMenu(action: AitUserMenuAction): void {
    if (action === 'theme') {
      const root = this.document.documentElement;
      const dark = !root.classList.contains('dark');
      root.classList.toggle('dark', dark);
      root.classList.toggle('light', !dark);
    }
  }
}
