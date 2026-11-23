import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';
import { AtbStatusChipComponent, AtbStatusTone } from './status-chip.component';

export type AtbReadiness = 'ready' | 'attention' | 'blocked';

const READINESS: Record<AtbReadiness, { tone: AtbStatusTone; glyph: string; label: string }> = {
  ready: { tone: 'success', glyph: '✓', label: 'Ready for the board' },
  attention: { tone: 'warning', glyph: '!', label: 'Needs attention' },
  blocked: { tone: 'error', glyph: '✕', label: 'Blocked' },
};

/** Readiness chip: whether an ARB submission can go to the board. */
@Component({
  selector: 'atb-readiness-chip',
  standalone: true,
  imports: [AtbStatusChipComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `<atb-status-chip [tone]="info().tone" [glyph]="info().glyph" [label]="info().label" />`,
})
export class AtbReadinessChipComponent {
  readonly readiness = input.required<AtbReadiness>();
  readonly info = computed(() => READINESS[this.readiness()]);
}
