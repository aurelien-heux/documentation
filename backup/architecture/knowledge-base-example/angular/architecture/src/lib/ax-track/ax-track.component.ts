import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';

export interface AxPlateau { readonly tag: string; readonly title: string; readonly short: string; }

/** Plateau track: one cell per plateau (B · T1 · T), filled when the element belongs to it. */
@Component({
  selector: 'atb-ax-track',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { class: 'ax-track', '[attr.aria-label]': 'label()', role: 'img' },
  template: `
    @for (p of plateaus(); track p.tag) {
      <span [class.on]="member().includes(p.tag)" [attr.title]="p.title">{{ p.short }}</span>
    }
  `,
})
export class AxTrackComponent {
  readonly plateaus = input.required<readonly AxPlateau[]>();
  readonly member = input<readonly string[]>([]);
  readonly label = computed(() => {
    const names = this.plateaus().filter(p => this.member().includes(p.tag)).map(p => p.title);
    return names.length ? `In ${names.join(', ')}` : 'In no plateau';
  });
}
