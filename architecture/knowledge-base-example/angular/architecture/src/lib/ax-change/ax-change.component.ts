import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';
import { AX_CHANGES, AxChange } from '../notation.generated';

/** Change chip: what happens to a building block between two plateaus (glyph + word on the state containers). */
@Component({
  selector: 'atb-ax-change',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { '[class]': 'cls()' },
  template: `<b aria-hidden="true">{{ info().glyph }}</b>{{ info().label }}`,
})
export class AxChangeComponent {
  readonly change = input.required<AxChange>();
  readonly info = computed(() => AX_CHANGES[this.change()]);
  readonly cls = computed(() => `ax-change ${this.change()}`);
}
