import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { AtbAsdSectionComponent, AtbCheck, AtbCheckRowComponent, AtbDecisionChipComponent, AtbReadinessChipComponent } from '../../public-api';

@Component({ standalone: true, imports: [AtbReadinessChipComponent, AtbDecisionChipComponent, AtbCheckRowComponent, AtbAsdSectionComponent],
  template: `
    <atb-readiness-chip [readiness]="r" />
    <atb-decision-chip decision="changes-requested" />
    <atb-check-row [check]="check" (open)="opened = $event" />
    <atb-asd-section [index]="4" title="Baseline" source="model" sectionId="asd-4"><p>body</p></atb-asd-section>` })
class Host {
  r: any = 'attention'; opened = '';
  check: AtbCheck = { id: 'T6', group: 'Traceability', title: 'Every new or changed application SBB has a detailed design', severity: 'warning', status: 'warn',
    items: [{ id: 'sbb.environments.jenkins-descriptor-job', title: 'Jenkins descriptor job', message: 'no detailed design yet' }] };
}

describe('review components', () => {
  let fx: ReturnType<typeof TestBed.createComponent<Host>>;
  beforeEach(async () => { await TestBed.configureTestingModule({ imports: [Host] }).compileComponents(); fx = TestBed.createComponent(Host); fx.detectChanges(); });
  const el = () => fx.nativeElement as HTMLElement;

  it('readiness: word + tone, never colour alone', () => {
    const chip = el().querySelector('atb-readiness-chip atb-status-chip') as HTMLElement;
    expect(chip.textContent).toContain('Needs attention'); expect(chip.className).toContain('st-warning');
    expect(chip.querySelector('.tile')!.getAttribute('aria-hidden')).toBe('true');
    fx.componentInstance.r = 'blocked'; fx.detectChanges();
    expect(chip.textContent).toContain('Blocked'); expect(chip.className).toContain('st-error');
  });
  it('decision chip', () => {
    const chip = el().querySelector('atb-decision-chip atb-status-chip') as HTMLElement;
    expect(chip.textContent).toContain('Changes requested'); expect(chip.className).toContain('st-warning');
  });
  it('check row: hidden status word, finding link emits the element id', () => {
    const row = el().querySelector('atb-check-row') as HTMLElement;
    expect(row.className).toContain('warn');
    expect(row.querySelector('.sr')!.textContent).toBe('Warning');
    expect(row.textContent).toContain('T6 · warning');
    (row.querySelector('button.lnk') as HTMLButtonElement).click();
    expect(fx.componentInstance.opened).toBe('sbb.environments.jenkins-descriptor-job');
  });
  it('asd section: region labelled by its h2, number, source badge, projected body', () => {
    const s = el().querySelector('atb-asd-section') as HTMLElement;
    expect(s.getAttribute('role')).toBe('region');
    expect(s.getAttribute('aria-labelledby')).toBe('asd-4-h');
    const h = s.querySelector('h2')!;
    expect(h.id).toBe('asd-4-h'); expect(h.textContent).toContain('4'); expect(h.textContent).toContain('Baseline'); expect(h.getAttribute('tabindex')).toBe('-1');
    expect(s.querySelector('.src')!.textContent).toBe('From the model');
    expect(s.querySelector('p')!.textContent).toBe('body');
  });
});
