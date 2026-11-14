import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AitSnackBar } from './snackbar';
import { AitEmptyState } from './empty-state';
import { AitBanner } from './banner';
import { AitStatusChip } from '../status-chip/status-chip';
import { AitGuideLine, AitPenOrbit } from '../progress/progress';

describe('AitSnackBar', () => {
  it('opens the design-system snackbar with the inverse panel and a longer duration when there is an action', () => {
    const openFromComponent = vi.fn();
    TestBed.configureTestingModule({ providers: [{ provide: MatSnackBar, useValue: { openFromComponent, dismiss: vi.fn() } }] });
    const snack = TestBed.inject(AitSnackBar);
    snack.open('Saved');
    expect(openFromComponent.mock.calls[0][1]).toMatchObject({ duration: 6000, panelClass: 'ait-snackbar-panel', politeness: 'polite' });
    snack.open('Deleted', { action: 'Undo', state: 'success' });
    expect(openFromComponent.mock.calls[1][1]).toMatchObject({ duration: 10000, data: { message: 'Deleted', action: 'Undo', state: 'success' } });
    snack.open('Failed', { state: 'error' });
    expect(openFromComponent.mock.calls[2][1].politeness).toBe('assertive');
  });
});

describe('feedback containers', () => {
  it('announce errors and keep other states polite', async () => {
    @Component({
      imports: [AitEmptyState, AitBanner],
      template: `
        <ait-empty-state state="error" title="Runs could not load" />
        <ait-empty-state state="pending" title="Loading" />
        <ait-banner state="warning">Changes requested</ait-banner>
        <ait-banner state="error">Down</ait-banner>`,
    })
    class Host {}
    const fixture = TestBed.createComponent(Host);
    await fixture.whenStable();
    const [errorState, pendingState] = fixture.nativeElement.querySelectorAll('ait-empty-state');
    const [warning, error] = fixture.nativeElement.querySelectorAll('ait-banner');
    expect(errorState.getAttribute('role')).toBe('alert');
    expect(pendingState.getAttribute('role')).toBe('status');
    expect(pendingState.getAttribute('aria-busy')).toBe('true');
    expect(warning.getAttribute('role')).toBe('status');
    expect(error.getAttribute('role')).toBe('alert');
  });

  it('status chips never rely on colour alone', async () => {
    @Component({ imports: [AitStatusChip], template: `<ait-status-chip state="error">Failed</ait-status-chip><ait-status-chip state="unknown">No data</ait-status-chip>` })
    class Host {}
    const fixture = TestBed.createComponent(Host);
    await fixture.whenStable();
    const [failed, unknown] = fixture.nativeElement.querySelectorAll('ait-status-chip');
    expect(failed.textContent).toContain('Failed');
    expect(failed.querySelector('ait-state-mark')).not.toBeNull();
    expect(failed.querySelector('.dt-chip-error')).not.toBeNull();
    expect(unknown.querySelector('.ait-status-chip__dot')).not.toBeNull();
  });

  it('progress indicators expose progressbar semantics', async () => {
    @Component({ imports: [AitPenOrbit, AitGuideLine], template: `<ait-pen-orbit /><ait-guide-line [value]="140" label="Rollout" />` })
    class Host {}
    const fixture = TestBed.createComponent(Host);
    await fixture.whenStable();
    const orbit = fixture.nativeElement.querySelector('ait-pen-orbit');
    const line = fixture.nativeElement.querySelector('ait-guide-line');
    expect(orbit.getAttribute('role')).toBe('progressbar');
    expect(orbit.hasAttribute('aria-valuenow')).toBe(false);
    expect(line.getAttribute('aria-valuenow')).toBe('140');
    expect((line.querySelector('.bar') as HTMLElement).style.width).toBe('100%');
  });
});
