import { NgTemplateOutlet } from '@angular/common';
import { ChangeDetectionStrategy, Component, computed, input, isDevMode, numberAttribute } from '@angular/core';
import { AIT_STATE_LABELS, AitStateOrPending, aitUid } from '../core/state';

/**
 * How the state mark is dressed, chosen by size:
 * - `badge` (A) alone on a surface, 24–40 px: snackbars, dialog headers, inline alerts, banners.
 * - `circle` (B) 56–96 px: empty states, table-, panel- or dialog-level errors.
 * - `tile` (C, filled) 18–20 px: table status columns, list rows, menu items.
 * - `tinted` (C, tinted) 18–20 px: inside a chip or alert that already carries the state container.
 * `pending` is not a dressing: set `state="pending"` and the mark shows the pen-orbit ring around the plain toolbox.
 */
export type AitStateMarkVariant = 'badge' | 'circle' | 'tile' | 'tinted';

const DEFAULT_SIZE: Record<AitStateMarkVariant, number> = { badge: 24, circle: 64, tile: 20, tinted: 18 };

/**
 * StateMark — the feedback icon of the system: the logo's construction with the state in the corner badge.
 * Decorative by default (`aria-hidden`), because the word next to it carries the state; give it a `label` when it stands alone.
 *
 * ```html
 * <ait-state-mark state="error" variant="tile" /> Failed
 * <ait-state-mark state="warning" variant="badge" [size]="32" label="Warning" />
 * ```
 */
@Component({
  selector: 'ait-state-mark',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: 'ait-state-mark',
    '[class]': '"ait-sm-" + state()',
    '[attr.role]': 'label() ? "img" : null',
    '[attr.aria-label]': 'label() || null',
    '[attr.aria-hidden]': 'label() ? null : "true"',
    '[style.height.px]': 'resolvedSize()',
  },
  template: `
    @switch (shape()) {
      @case ('badge') {
        <svg viewBox="0 0 74 64" [attr.height]="resolvedSize()" [attr.width]="resolvedSize() * 74 / 64" focusable="false">
          <mask [attr.id]="uid + '-m'" maskUnits="userSpaceOnUse" x="0" y="0" width="74" height="64">
            <rect width="74" height="64" fill="#fff" /><rect x="44.5" y="0.5" width="29" height="29" rx="8.5" fill="#000" />
          </mask>
          <g [attr.mask]="'url(#' + uid + '-m)'">
            <path d="M21 23v-6a6 6 0 0 1 6-6h10a6 6 0 0 1 6 6v6" fill="none" class="box-stroke" stroke-width="6" stroke-linecap="round" />
            <rect x="4" y="22" width="56" height="36" rx="10" class="box-fill" />
            <path d="M17.5 33l8 7-8 7" fill="none" class="chev" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M33.5 47h13" fill="none" class="cursor" stroke-width="5.5" stroke-linecap="round" />
          </g>
          <rect x="47" y="3" width="24" height="24" rx="6" class="badge-fill" />
          <ng-container *ngTemplateOutlet="badgeSymbol" />
        </svg>
      }
      @case ('circle') {
        <svg viewBox="0 0 100 100" [attr.height]="resolvedSize()" [attr.width]="resolvedSize()" focusable="false">
          <circle cx="50" cy="50" r="48" class="disc" />
          <g transform="translate(17.62 22) scale(0.875)">
            <mask [attr.id]="uid + '-m'" maskUnits="userSpaceOnUse" x="0" y="0" width="74" height="64">
              <rect width="74" height="64" fill="#fff" /><rect x="44.5" y="0.5" width="29" height="29" rx="8.5" fill="#000" />
            </mask>
            <g [attr.mask]="'url(#' + uid + '-m)'">
              <path d="M21 23v-6a6 6 0 0 1 6-6h10a6 6 0 0 1 6 6v6" fill="none" class="rev-stroke" stroke-width="6" stroke-linecap="round" />
              <rect x="4" y="22" width="56" height="36" rx="10" class="rev-fill" />
              <path d="M17.5 33l8 7-8 7" fill="none" class="role-stroke" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M33.5 47h13" fill="none" class="role-stroke" stroke-width="5.5" stroke-linecap="round" />
            </g>
            <rect x="47" y="3" width="24" height="24" rx="6" class="ctr-fill" />
            <ng-container *ngTemplateOutlet="badgeSymbol; context: { $implicit: 'on-ctr' }" />
          </g>
        </svg>
      }
      @case ('pending') {
        <svg viewBox="0 0 100 100" [attr.height]="resolvedSize()" [attr.width]="resolvedSize()" focusable="false" class="ait-motion">
          <circle cx="50" cy="50" r="48" fill="none" class="track" stroke-width="4" />
          <g class="orbit">
            <circle cx="50" cy="50" r="48" fill="none" class="arc" stroke-width="4" stroke-linecap="round" stroke-dasharray="156.8 144.8" transform="rotate(-90 50 50)" />
            <circle cx="43.98" cy="97.62" r="4" class="pen" />
          </g>
          <g transform="translate(22 22) scale(0.875)">
            <path d="M21 23v-6a6 6 0 0 1 6-6h10a6 6 0 0 1 6 6v6" fill="none" class="box-stroke" stroke-width="6" stroke-linecap="round" />
            <rect x="4" y="22" width="56" height="36" rx="10" class="box-fill" />
            <path d="M17.5 33l8 7-8 7" fill="none" class="chev" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M33.5 47h13" fill="none" class="cursor" stroke-width="5.5" stroke-linecap="round" />
          </g>
        </svg>
      }
      @default {
        <svg viewBox="0 0 64 64" [attr.height]="resolvedSize()" [attr.width]="resolvedSize()" focusable="false" [class.tinted]="shape() === 'tinted'">
          <rect width="64" height="64" rx="14" class="tile" />
          <path d="M17 23l10 9-10 9" fill="none" class="tile-ink" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" />
          @switch (state()) {
            @case ('success') { <path d="M35 33l5 5 10-10" fill="none" class="tile-ink" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" /> }
            @case ('info') { <path d="M42 31v10" fill="none" class="tile-ink" stroke-width="7" stroke-linecap="round" /><circle cx="42" cy="21" r="4" class="tile-dot" /> }
            @case ('warning') { <path d="M42 23v10" fill="none" class="tile-ink" stroke-width="7" stroke-linecap="round" /><circle cx="42" cy="43" r="4" class="tile-dot" /> }
            @case ('error') { <path d="M35 25l14 14M49 25L35 39" fill="none" class="tile-ink" stroke-width="7" stroke-linecap="round" /> }
          }
        </svg>
      }
    }

    <ng-template #badgeSymbol let-ink>
      <svg:g [attr.class]="ink === 'on-ctr' ? 'sym on-ctr' : 'sym'">
        @switch (state()) {
          @case ('success') { <svg:path d="M52 15.5l4.5 4.5 9.5-9.5" fill="none" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" /> }
          @case ('info') { <svg:path d="M59 13.5v7.5" fill="none" stroke-width="3.5" stroke-linecap="round" /><svg:circle cx="59" cy="8.5" r="2.2" /> }
          @case ('warning') { <svg:path d="M59 8v7.5" fill="none" stroke-width="3.5" stroke-linecap="round" /><svg:circle cx="59" cy="21" r="2.2" /> }
          @case ('error') { <svg:path d="M54 10l10 10M64 10L54 20" fill="none" stroke-width="3.5" stroke-linecap="round" /> }
        }
      </svg:g>
    </ng-template>
  `,
  imports: [NgTemplateOutlet],
  styles: `
    :host { display: inline-flex; flex: none; line-height: 0; vertical-align: middle; }
    :host(.ait-sm-success) { --_role: var(--md-sys-color-success); --_on: var(--md-sys-color-on-success); --_ctr: var(--md-sys-color-success-container); --_on-ctr: var(--md-sys-color-on-success-container); }
    :host(.ait-sm-info) { --_role: var(--md-sys-color-primary); --_on: var(--md-sys-color-on-primary); --_ctr: var(--md-sys-color-primary-container); --_on-ctr: var(--md-sys-color-on-primary-container); }
    :host(.ait-sm-warning) { --_role: var(--md-sys-color-warning); --_on: var(--md-sys-color-on-warning); --_ctr: var(--md-sys-color-warning-container); --_on-ctr: var(--md-sys-color-on-warning-container); }
    :host(.ait-sm-error) { --_role: var(--md-sys-color-error); --_on: var(--md-sys-color-on-error); --_ctr: var(--md-sys-color-error-container); --_on-ctr: var(--md-sys-color-on-error-container); }
    .box-fill { fill: var(--md-sys-color-logo-box); }
    .box-stroke { stroke: var(--md-sys-color-logo-box); }
    .chev { stroke: var(--md-sys-color-on-logo-box); }
    .cursor { stroke: var(--md-sys-color-logo-cursor); }
    .badge-fill { fill: var(--_role); }
    .sym { stroke: var(--_on); fill: var(--_on); }
    .sym.on-ctr { stroke: var(--_on-ctr); fill: var(--_on-ctr); }
    .sym path { fill: none; }
    .disc { fill: var(--_role); }
    .rev-fill { fill: var(--_on); }
    .rev-stroke { stroke: var(--_on); }
    .role-stroke { stroke: var(--_role); }
    .ctr-fill { fill: var(--_ctr); }
    .tile { fill: var(--_role); }
    .tile-ink { stroke: var(--_on); }
    .tile-dot { fill: var(--_on); }
    .tinted .tile { fill: var(--_ctr); }
    .tinted .tile-ink { stroke: var(--_on-ctr); }
    .tinted .tile-dot { fill: var(--_on-ctr); }
    .track { stroke: var(--md-sys-color-primary-container); }
    .arc { stroke: var(--md-sys-color-logo-box); }
    .pen { fill: var(--md-sys-color-ai); }
    .orbit { transform-origin: 50px 50px; animation: ait-orbit 1.4s linear infinite; }
    @keyframes ait-orbit { to { transform: rotate(360deg); } }
    @media (prefers-reduced-motion: reduce) { .orbit { animation: none; } }
  `,
})
export class AitStateMark {
  /** success · info · warning · error, or pending while a request runs. */
  readonly state = input.required<AitStateOrPending>();
  /** Dressing, chosen by size (see AitStateMarkVariant). Ignored while pending. */
  readonly variant = input<AitStateMarkVariant>('badge');
  /** Height in px. Defaults: badge 24, circle 64, tile 20, tinted 18, pending 64. Never below 18. */
  readonly size = input<number | undefined, unknown>(undefined, { transform: (v: unknown) => (v == null || v === '' ? undefined : numberAttribute(v)) });
  /** Accessible name. Leave empty when a visible word next to the mark already says the state. */
  readonly label = input<string>('');

  protected readonly uid = aitUid('ait-sm');
  protected readonly shape = computed(() => (this.state() === 'pending' ? 'pending' : this.variant()));
  protected readonly resolvedSize = computed(() => {
    const shape = this.shape();
    const size = this.size() ?? (shape === 'pending' ? 64 : DEFAULT_SIZE[shape as AitStateMarkVariant]);
    if (isDevMode() && size < 18) {
      console.warn(`[ait-state-mark] ${size} px is below the 18 px minimum; use an 8 px dot instead.`);
    }
    return Math.max(size, 18);
  });

  /** Default word for the state, for callers that need it. */
  static labelFor(state: AitStateOrPending): string {
    return AIT_STATE_LABELS[state];
  }
}

