import { Component, signal } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { AitStateMark, AitStateMarkVariant } from './state-mark';
import { AitStateOrPending } from '../core/state';

@Component({
  imports: [AitStateMark],
  template: `<ait-state-mark [state]="state()" [variant]="variant()" [size]="size()" [label]="label()" />`,
})
class Host {
  state = signal<AitStateOrPending>('success');
  variant = signal<AitStateMarkVariant>('badge');
  size = signal<number | undefined>(undefined);
  label = signal('');
}

describe('AitStateMark', () => {
  async function render() {
    const fixture = TestBed.createComponent(Host);
    await fixture.whenStable();
    const el = fixture.nativeElement.querySelector('ait-state-mark') as HTMLElement;
    return { fixture, el, host: fixture.componentInstance };
  }

  it('is decorative without a label and named with one', async () => {
    const { fixture, el, host } = await render();
    expect(el.getAttribute('aria-hidden')).toBe('true');
    expect(el.getAttribute('role')).toBeNull();
    host.label.set('Success');
    await fixture.whenStable();
    expect(el.getAttribute('role')).toBe('img');
    expect(el.getAttribute('aria-label')).toBe('Success');
    expect(el.hasAttribute('aria-hidden')).toBe(false);
  });

  it('uses the default size of each dressing', async () => {
    const { fixture, el, host } = await render();
    const svg = () => el.querySelector('svg')!;
    expect(svg().getAttribute('height')).toBe('24');
    expect(svg().getAttribute('viewBox')).toBe('0 0 74 64');
    host.variant.set('circle');
    await fixture.whenStable();
    expect(svg().getAttribute('height')).toBe('64');
    host.variant.set('tile');
    await fixture.whenStable();
    expect(svg().getAttribute('height')).toBe('20');
    host.variant.set('tinted');
    await fixture.whenStable();
    expect(svg().getAttribute('height')).toBe('18');
    expect(svg().classList).toContain('tinted');
  });

  it('never renders below 18 px', async () => {
    const { fixture, el, host } = await render();
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => undefined);
    host.variant.set('tile');
    host.size.set(12);
    await fixture.whenStable();
    expect(el.querySelector('svg')!.getAttribute('height')).toBe('18');
    expect(warn).toHaveBeenCalled();
    warn.mockRestore();
  });

  it('shows the pen-orbit ring while pending, whatever the dressing', async () => {
    const { fixture, el, host } = await render();
    host.state.set('pending');
    await fixture.whenStable();
    expect(el.querySelector('.orbit')).not.toBeNull();
    expect(el.querySelector('svg')!.getAttribute('height')).toBe('64');
  });

  it('gives every instance its own mask id', async () => {
    @Component({ imports: [AitStateMark], template: `<ait-state-mark state="error" /><ait-state-mark state="error" />` })
    class Two {}
    const fixture = TestBed.createComponent(Two);
    await fixture.whenStable();
    const ids = [...fixture.nativeElement.querySelectorAll('mask')].map((m: Element) => m.id);
    expect(ids.length).toBe(2);
    expect(new Set(ids).size).toBe(2);
  });
});
