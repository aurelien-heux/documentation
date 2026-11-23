import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';
import { AtbStatusChipComponent, AtbStatusTone } from '../readiness-chip/status-chip.component';

export type AtbDecision = 'approved' | 'approved-with-conditions' | 'changes-requested' | 'rejected' | 'pending' | 'not-required';

export const ATB_DECISIONS: Record<AtbDecision, { tone: AtbStatusTone; glyph: string; label: string }> = {
  approved: { tone: 'success', glyph: '✓', label: 'Approved' },
  'approved-with-conditions': { tone: 'success', glyph: '✓', label: 'Approved with conditions' },
  'changes-requested': { tone: 'warning', glyph: '!', label: 'Changes requested' },
  rejected: { tone: 'error', glyph: '✕', label: 'Rejected' },
  pending: { tone: 'info', glyph: 'i', label: 'Pending' },
  'not-required': { tone: 'neutral', glyph: '–', label: 'Not required' },
};

/** Reviewer decision chip: a board member's decision, recorded as a Checkpoint (never by an agent, INV-12). */
@Component({
  selector: 'atb-decision-chip',
  standalone: true,
  imports: [AtbStatusChipComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `<atb-status-chip [tone]="info().tone" [glyph]="info().glyph" [label]="info().label" />`,
})
export class AtbDecisionChipComponent {
  readonly decision = input.required<AtbDecision>();
  readonly info = computed(() => ATB_DECISIONS[this.decision()]);
}
