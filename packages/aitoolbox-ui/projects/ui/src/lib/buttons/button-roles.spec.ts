import { Component, signal } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { AitDanger, AitRun, AitRunRegistry, AitRunText, AitTonal } from './button-roles';

@Component({
  imports: [AitRun, AitRunText, AitTonal, AitDanger],
  template: `
    <button aitRun>Run</button>
    @if (second()) { <button aitRun>Deploy</button> }
    <button aitRunText>Re-run</button>
    <button aitTonal>Filter</button>
    <button aitDanger>Delete</button>
  `,
})
class Host {
  second = signal(false);
}

describe('button roles', () => {
  it('apply the theme classes', async () => {
    const fixture = TestBed.createComponent(Host);
    await fixture.whenStable();
    const [run, runText, tonal, danger] = fixture.nativeElement.querySelectorAll('button');
    expect(run.classList).toContain('dt-run');
    expect(runText.classList).toContain('dt-run-text');
    expect(tonal.classList).toContain('dt-tonal');
    expect(danger.classList).toContain('dt-danger');
  });

  it('warn when a second Run button appears, and forget removed ones', async () => {
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => undefined);
    const fixture = TestBed.createComponent(Host);
    await fixture.whenStable();
    const registry = TestBed.inject(AitRunRegistry);
    expect(registry.count).toBe(1);
    expect(warn).not.toHaveBeenCalled();
    fixture.componentInstance.second.set(true);
    await fixture.whenStable();
    expect(registry.count).toBe(2);
    expect(warn).toHaveBeenCalledWith(expect.stringContaining('one per screen'), expect.anything());
    fixture.componentInstance.second.set(false);
    await fixture.whenStable();
    expect(registry.count).toBe(1);
    warn.mockRestore();
  });

  it('warn when the Run button is placed in a dialog', async () => {
    @Component({ imports: [AitRun], template: `<div role="dialog"><button aitRun>Run</button></div>` })
    class InDialog {}
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => undefined);
    const fixture = TestBed.createComponent(InDialog);
    await fixture.whenStable();
    expect(warn).toHaveBeenCalledWith(expect.stringContaining('never used inside a dialog'), expect.anything());
    warn.mockRestore();
  });
});
