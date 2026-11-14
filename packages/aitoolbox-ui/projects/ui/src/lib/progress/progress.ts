import { ChangeDetectionStrategy, Component, computed, input, numberAttribute } from '@angular/core';

const clamp = (v: number) => Math.min(100, Math.max(0, v));
const optionalNumber = (v: unknown) => (v == null || v === '' ? undefined : numberAttribute(v));

/**
 * Pen orbit — the circular indicator of the Constructor family (skin of `mat-progress-spinner`): a violet arc with
 * the teal pen at its head on a faint primary-container track. 48 px in content, 24 px inline, 18 px inside a button.
 * Indeterminate by default; give `value` (0–100) for a determinate arc.
 */
@Component({
  selector: 'ait-pen-orbit',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: 'ait-pen-orbit',
    role: 'progressbar',
    '[attr.aria-label]': 'label()',
    '[attr.aria-valuenow]': 'value() ?? null',
    '[attr.aria-valuemin]': 'value() == null ? null : 0',
    '[attr.aria-valuemax]': 'value() == null ? null : 100',
    '[style.width.px]': 'size()',
    '[style.height.px]': 'size()',
  },
  template: `
    <svg viewBox="0 0 48 48" [attr.width]="size()" [attr.height]="size()" focusable="false" aria-hidden="true">
      <circle cx="24" cy="24" r="20" fill="none" class="track" [attr.stroke-width]="stroke()" />
      <g [class.spin]="value() == null" [attr.transform]="value() == null ? null : 'rotate(' + (headAngle() - 90) + ' 24 24)'">
        <circle cx="24" cy="24" r="20" fill="none" class="arc" [attr.stroke-width]="stroke()" stroke-linecap="round"
          [attr.stroke-dasharray]="dash()" [attr.transform]="'rotate(' + (-headAngle()) + ' 24 24)'" />
        <circle cx="44" cy="24" [attr.r]="pen()" class="pen" />
      </g>
    </svg>
  `,
  styles: `
    :host { display: inline-flex; flex: none; vertical-align: middle; }
    .track { stroke: var(--md-sys-color-primary-container); }
    .arc { stroke: var(--md-sys-color-primary); }
    .pen { fill: var(--md-sys-color-ai-strong); }
    .spin { transform-origin: 24px 24px; animation: ait-po 1.4s linear infinite; }
    @keyframes ait-po { from { transform: rotate(-90deg); } to { transform: rotate(270deg); } }
    @media (prefers-reduced-motion: reduce) { .spin { animation: none; } }
  `,
})
export class AitPenOrbit {
  /** 48 (content) · 24 (inline) · 18 (inside a button). */
  readonly size = input(48, { transform: numberAttribute });
  /** 0–100 for a determinate arc; leave unset for indeterminate. */
  readonly value = input<number | undefined, unknown>(undefined, { transform: optionalNumber });
  readonly label = input('Loading');

  protected readonly stroke = computed(() => (this.size() <= 24 ? 5 : 4));
  protected readonly pen = computed(() => (this.size() <= 24 ? 4.5 : 3.6));
  /** Arc length in degrees: 190° while indeterminate, the value otherwise. */
  protected readonly sweep = computed(() => (this.value() == null ? 190 : (clamp(this.value()!) / 100) * 360));
  protected readonly headAngle = computed(() => this.sweep());
  protected readonly dash = computed(() => {
    const c = 2 * Math.PI * 20;
    const len = (this.sweep() / 360) * c;
    return `${len} ${c}`;
  });
}

/**
 * Guide line — the linear indicator (skin of `mat-progress-bar`): a dashed teal construction guide, the violet bar
 * runs along it with the pen on its leading edge. Indeterminate by default; `value` (0–100) for determinate.
 */
@Component({
  selector: 'ait-guide-line',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: 'ait-guide-line',
    role: 'progressbar',
    '[attr.aria-label]': 'label()',
    '[attr.aria-valuenow]': 'value() ?? null',
    '[attr.aria-valuemin]': 'value() == null ? null : 0',
    '[attr.aria-valuemax]': 'value() == null ? null : 100',
    '[class.ait-guide-line--indeterminate]': 'value() == null',
  },
  template: `
    <span class="guide"></span>
    <span class="bar" [style.width.%]="value() == null ? 30 : clamped()"><span class="pen"></span></span>
  `,
  styles: `
    :host { position: relative; display: block; height: 8px; overflow: hidden; }
    .guide { position: absolute; left: 0; right: 0; top: 3.25px; height: 1.5px; opacity: .7;
      background: repeating-linear-gradient(90deg, var(--md-sys-color-ai-strong) 0 2px, transparent 2px 5px); }
    .bar { position: absolute; left: 0; top: 2px; height: 4px; border-radius: 2px; background: var(--md-sys-color-primary); transition: width 300ms cubic-bezier(.2,0,0,1); }
    .pen { position: absolute; right: -3.5px; top: -1.5px; width: 7px; height: 7px; border-radius: 9999px; background: var(--md-sys-color-ai-strong); }
    :host(.ait-guide-line--indeterminate) .bar { animation: ait-gl 1.8s cubic-bezier(.2,0,0,1) infinite; }
    @keyframes ait-gl { 0% { transform: translateX(-100%); } 100% { transform: translateX(350%); } }
    @media (prefers-reduced-motion: reduce) { :host(.ait-guide-line--indeterminate) .bar { animation: none; } .bar { transition: none; } }
  `,
})
export class AitGuideLine {
  readonly value = input<number | undefined, unknown>(undefined, { transform: optionalNumber });
  readonly label = input('Loading');
  protected readonly clamped = computed(() => clamp(this.value() ?? 0));
}

/**
 * Working dots — three dots on a 1.4 s rhythm. The colour says who works: `run` (green, a command executes) or
 * `ai` (teal, a model is thinking). Inline after a log line or a chat message.
 */
@Component({
  selector: 'ait-working-dots',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { class: 'ait-working-dots', role: 'img', '[attr.aria-label]': 'label()', '[class.ait-working-dots--ai]': 'kind() === "ai"' },
  template: `<span></span><span></span><span></span>`,
  styles: `
    :host { display: inline-flex; align-items: center; gap: 3px; height: 8px; vertical-align: middle; --_dot: var(--md-sys-color-tertiary); }
    :host(.ait-working-dots--ai) { --_dot: var(--md-sys-color-ai-strong); }
    span { width: 6px; height: 6px; border-radius: 9999px; background: var(--_dot); animation: ait-dot 1.4s ease-in-out infinite; }
    span:nth-child(2) { animation-delay: .16s; } span:nth-child(3) { animation-delay: .32s; }
    @keyframes ait-dot { 0%, 80%, 100% { transform: scale(.6); opacity: .4; } 40% { transform: scale(1); opacity: 1; } }
    @media (prefers-reduced-motion: reduce) { span { animation: none; opacity: 1; transform: none; } }
  `,
})
export class AitWorkingDots {
  readonly kind = input<'run' | 'ai'>('run');
  readonly label = input('Working');
}

/**
 * Constructor determinate — long operations with a known value (install, deploy, migration): the pen draws the box in
 * proportion to progress and at 100 % the toolbox fills. 64–96 px in dialogs and empty states.
 */
@Component({
  selector: 'ait-constructor-progress',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: 'ait-constructor-progress',
    role: 'progressbar',
    'aria-valuemin': '0',
    'aria-valuemax': '100',
    '[attr.aria-valuenow]': 'clamped()',
    '[attr.aria-label]': 'label()',
  },
  template: `
    <svg viewBox="-4 2 76 64" [attr.height]="size()" [attr.width]="size() * 76 / 64" focusable="false" aria-hidden="true" [class.done]="clamped() >= 100">
      <rect x="4" y="22" width="56" height="36" rx="10" fill="none" class="guide" stroke-width="1" stroke-dasharray="2 2" opacity=".45" />
      <path d="M21 23v-6a6 6 0 0 1 6-6h10a6 6 0 0 1 6 6v6" fill="none" class="guide" stroke-width="1" stroke-dasharray="2 2" opacity=".6" />
      <g class="solid">
        <rect x="4" y="22" width="56" height="36" rx="10" class="box" />
        <path d="M21 23v-6a6 6 0 0 1 6-6h10a6 6 0 0 1 6 6v6" fill="none" class="box-stroke" stroke-width="6" stroke-linecap="round" />
        <path d="M17.5 33l8 7-8 7" fill="none" class="chev" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round" />
        <path d="M33.5 47h13" fill="none" class="cursor" stroke-width="5.5" stroke-linecap="round" />
      </g>
      <path class="line" pathLength="100" stroke-dasharray="100" [attr.stroke-dashoffset]="100 - clamped()"
        d="M44 22H14a10 10 0 0 0-10 10v16a10 10 0 0 0 10 10h36a10 10 0 0 0 10-10V32a10 10 0 0 0-10-10H44"
        fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
      <circle class="pen" r="2.6" [style.offset-distance.%]="clamped()" />
      @if (clamped() < 100) {
        <text x="32" y="43" text-anchor="middle" class="pct">{{ clamped() }}%</text>
      }
    </svg>
  `,
  styles: `
    :host { display: inline-flex; flex: none; }
    svg { overflow: visible; }
    .guide, .line { stroke: var(--md-sys-color-ai-strong); }
    .pen { fill: var(--md-sys-color-ai-strong); offset-path: path("M44 22H14a10 10 0 0 0-10 10v16a10 10 0 0 0 10 10h36a10 10 0 0 0 10-10V32a10 10 0 0 0-10-10H44"); offset-rotate: 0deg; }
    .solid { opacity: 0; transition: opacity 300ms; }
    .box { fill: var(--md-sys-color-logo-box); } .box-stroke { stroke: var(--md-sys-color-logo-box); }
    .chev { stroke: var(--md-sys-color-on-logo-box); } .cursor { stroke: var(--md-sys-color-logo-cursor); }
    .done .solid { opacity: 1; } .done .pen, .done .line { opacity: 0; }
    .pct { font-family: var(--ait-font-body); font-weight: 600; font-size: 11px; fill: var(--md-sys-color-ai-strong); }
    @media (prefers-reduced-motion: reduce) { .solid { transition: none; } }
  `,
})
export class AitConstructorProgress {
  readonly value = input.required({ transform: numberAttribute });
  /** Height in px, 64–96. */
  readonly size = input(72, { transform: numberAttribute });
  readonly label = input('Progress');
  protected readonly clamped = computed(() => Math.round(clamp(this.value())));
}
