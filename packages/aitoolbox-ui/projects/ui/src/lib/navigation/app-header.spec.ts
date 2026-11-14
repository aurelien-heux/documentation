import { Component, signal } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { AitAppHeader } from './app-header';
import { AitWindowClass } from '../core/window-class';

@Component({
  imports: [AitAppHeader],
  template: `<ait-app-header [user]="{ name: 'Aurélien Heux', role: 'platform · admin' }" [notificationCount]="count()"
    [assistant]="assistant()" (assistantToggle)="toggles = toggles + 1" />`,
})
class Host {
  count = signal(3);
  assistant = signal<'idle' | 'typing' | 'waiting'>('idle');
  toggles = 0;
}

function windowClass(cls: 'compact' | 'large') {
  return {
    windowClass: signal(cls),
    isCompact: signal(cls === 'compact'),
    navigation: signal(cls === 'compact' ? 'bar' : 'drawer'),
    drawerMode: signal('side'),
    assistantMode: signal('docked'),
    fullScreenDialogs: signal(false),
  };
}

describe('AitAppHeader', () => {
  function setup(cls: 'compact' | 'large' = 'large') {
    TestBed.configureTestingModule({ providers: [provideRouter([]), { provide: AitWindowClass, useValue: windowClass(cls) }] });
    return TestBed.createComponent(Host);
  }

  it('caps the notification badge at 9+ and 99+ and names the bell with the real count', async () => {
    const fixture = setup();
    await fixture.whenStable();
    const el: HTMLElement = fixture.nativeElement;
    expect(el.querySelector('.badge')!.textContent!.trim()).toBe('3');
    fixture.componentInstance.count.set(42);
    await fixture.whenStable();
    expect(el.querySelector('.badge')!.textContent!.trim()).toBe('9+');
    expect(el.querySelector('.bell')!.getAttribute('aria-label')).toBe('Notifications, 42 unread');
    fixture.componentInstance.count.set(120);
    await fixture.whenStable();
    expect(el.querySelector('.badge')!.textContent!.trim()).toBe('99+');
    fixture.componentInstance.count.set(0);
    await fixture.whenStable();
    expect(el.querySelector('.badge')).toBeNull();
  });

  it('starts the user chip name with the visible name and derives the initials', async () => {
    const fixture = setup();
    await fixture.whenStable();
    const user = fixture.nativeElement.querySelector('.user') as HTMLElement;
    expect(user.getAttribute('aria-label')).toBe('Aurélien Heux, platform · admin, account menu');
    expect(user.querySelector('.avatar')!.textContent!.trim()).toBe('AH');
  });

  it('carries the assistant state in the button name and toggles with ⌘J / Ctrl+J', async () => {
    const fixture = setup();
    fixture.componentInstance.assistant.set('waiting');
    await fixture.whenStable();
    const button = fixture.nativeElement.querySelector('.assistant') as HTMLElement;
    expect(button.getAttribute('aria-label')).toBe('Open assistant, answer ready');
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'j', ctrlKey: true }));
    expect(fixture.componentInstance.toggles).toBe(1);
  });

  it('drops the search field and the assistant button on phones', async () => {
    const fixture = setup('compact');
    await fixture.whenStable();
    const el: HTMLElement = fixture.nativeElement;
    expect(el.querySelector('ait-search-ask')).toBeNull();
    expect(el.querySelector('.assistant')).toBeNull();
    expect(el.querySelector('[aria-label="Open navigation"]')).not.toBeNull();
  });
});
