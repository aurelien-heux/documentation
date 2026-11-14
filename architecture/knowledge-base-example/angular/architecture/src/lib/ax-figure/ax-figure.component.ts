import { ChangeDetectionStrategy, Component, computed, input, output } from '@angular/core';
import { AxGlyphComponent } from '../icons/ax-glyph.component';
import { AX_CHANGES, AX_TYPES, AxChange, AxFigureSize, AxType } from '../notation.generated';

/**
 * ArchiMate figure: one architecture element drawn in its ArchiMate shape — layer fill, 1 px layer ink,
 * type glyph top-right, name. The type decides colour, shape and glyph.
 *
 * - static (default): role="img", name = "<name>, <type>"
 * - `clickable`: rendered as a <button>, emits `activate`; hover and pressed state layers, 2 px focus ring
 * - `selected`: 2 px primary ring · `retired`: 45 % opacity, name struck through, with the Retired chip
 *
 * The layer colour never carries status: pass `change` to show the gap chip under the figure.
 */
@Component({
  selector: 'atb-ax-figure',
  standalone: true,
  imports: [AxGlyphComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { class: 'atb-ax-figure', '[class.has-chip]': '!!change()' },
  template: `
    @if (clickable()) {
      <button type="button" [class]="boxClass()" [attr.aria-pressed]="selected() ? 'true' : null" [attr.aria-label]="label()" (click)="activate.emit()">
        <span class="ax-in"><atb-ax-glyph class="ax-glyph" [type]="type()" /><span class="ax-name">{{ name() }}</span></span>
      </button>
    } @else {
      <div [class]="boxClass()" role="img" [attr.aria-label]="label()" [attr.aria-current]="selected() ? 'true' : null">
        <div class="ax-in"><atb-ax-glyph class="ax-glyph" [type]="type()" /><span class="ax-name">{{ name() }}</span></div>
      </div>
    }
    @if (change(); as c) {
      <span class="ax-change" [class]="'ax-change ' + c"><b aria-hidden="true">{{ changes[c].glyph }}</b>{{ changes[c].label }}</span>
    }
  `,
  styles: [':host { display: inline-grid; gap: 8px; justify-items: start; } .ax-glyph { position: absolute; }'],
})
export class AxFigureComponent {
  readonly type = input.required<AxType>();
  readonly name = input.required<string>();
  readonly size = input<AxFigureSize>('m');
  readonly clickable = input(false);
  readonly selected = input(false);
  readonly retired = input(false);
  readonly change = input<AxChange | undefined>(undefined);
  readonly activate = output<void>();
  readonly changes = AX_CHANGES;

  readonly info = computed(() => AX_TYPES[this.type()]);
  readonly label = computed(() => `${this.name()}, ${this.info().name.toLowerCase()}${this.retired() ? ', retired' : ''}`);
  readonly boxClass = computed(() => {
    const i = this.info();
    return [
      'ax-box', `ax-shape-${i.shape}`, `ax-l-${i.layer}`, `ax-${this.size()}`,
      this.type() === 'and-junction' ? 'ax-and' : '',
      this.retired() ? 'ax-retired' : '', this.selected() ? 'ax-selected' : '',
    ].filter(Boolean).join(' ');
  });
}
