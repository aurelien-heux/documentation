import { booleanAttribute, ChangeDetectionStrategy, Component, input, numberAttribute } from '@angular/core';
import { aitUid } from '../core/state';

/**
 * Brand loader "Constructor" — app-level waits only (boot, workspace switch), never inside a screen. The AI tag comes
 * in, construction guides appear, a teal pen draws the toolbox in one trip and the night box becomes solid; 4.8 s loop.
 * `once` plays one time and stays on the logo (splash). 96 px for splash and workspace boot, 40 px minimum.
 * Under reduced motion it shows the finished logo; the label carries the state.
 */
@Component({
  selector: 'ait-brand-loader',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { class: 'ait-brand-loader', role: 'status' },
  template: `
    <svg class="ait-loader" [class.ait-once]="once()" viewBox="-4 2 76 64" [attr.height]="size()" [attr.width]="size() * 76 / 64" focusable="false" aria-hidden="true">
      <defs>
        <mask [attr.id]="uid + '-hole'" maskUnits="userSpaceOnUse" x="-4" y="2" width="76" height="64">
          <rect x="-4" y="2" width="76" height="64" fill="#fff" /><rect x="37" y="3" width="36" height="24" rx="7" fill="#000" />
        </mask>
        <clipPath [attr.id]="uid + '-tag'"><rect x="39.5" y="5.5" width="31" height="19" rx="5" /></clipPath>
      </defs>
      <g class="o guide ai-stroke" opacity="0" fill="none">
        <rect x="4" y="22" width="56" height="36" stroke-width=".8" stroke-dasharray="2 2" />
        <path d="M-2 22h62M-2 58h62M4 16v48M60 16v48M21 11h22M21 11v12M43 11v12" stroke-width=".8" stroke-dasharray="2 2" />
        <path d="M4 20v4M60 20v4M2 22h4M2 58h4" stroke-width="1.2" />
      </g>
      <g [attr.mask]="'url(#' + uid + '-hole)'">
        <rect class="fill box" x="4" y="22" width="56" height="36" rx="10" />
        <path class="fill box-stroke" d="M21 23v-6a6 6 0 0 1 6-6h10a6 6 0 0 1 6 6v6" fill="none" stroke-width="6" stroke-linecap="round" />
        <path class="fill chev" d="M17.5 33l8 7-8 7" fill="none" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round" />
        <path class="blink cursor" d="M33.5 47h13" fill="none" stroke-width="5.5" stroke-linecap="round" />
      </g>
      <path class="o ln-box ai-stroke" pathLength="100" stroke-dasharray="100" d="M44 22H14a10 10 0 0 0-10 10v16a10 10 0 0 0 10 10h36a10 10 0 0 0 10-10V32a10 10 0 0 0-10-10H44" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
      <path class="o ln-handle ai-stroke" pathLength="100" stroke-dasharray="100" d="M43 23v-6a6 6 0 0 0-6-6H27a6 6 0 0 0-6 6v6" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
      <path class="o ln-chev ai-stroke" pathLength="100" stroke-dasharray="100" d="M17.5 33l8 7-8 7" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
      <path class="o ln-cur ai-stroke" pathLength="100" stroke-dasharray="100" d="M33.5 47h13" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
      <circle class="pen ai-fill" r="2.6" />
      <g class="badge-in"><g class="badge-pulse">
        <rect class="ai-fill" x="39.5" y="5.5" width="31" height="19" rx="5" />
        <g [attr.clip-path]="'url(#' + uid + '-tag)'">
          <g class="la"><path class="on-ai" d="M48.567 20.04 51.647 9.96H54.489L57.569 20.04H55.609L54.958 17.94H51.164L50.527 20.04ZM54.412 16.162 53.047 11.745 51.703 16.162Z" /></g>
          <g class="li"><path class="on-ai" d="M58.689 20.04V9.96H60.593V20.04Z" /></g>
          <g class="sheen" opacity="0"><rect x="34" y="2" width="6" height="28" fill="#FFFFFF" transform="skewX(-20)" /></g>
        </g>
      </g></g>
    </svg>
    @if (label()) {
      <span class="label">{{ label() }}</span>
    } @else {
      <span class="ait-visually-hidden">Loading</span>
    }
  `,
  styles: `
    :host { display: inline-flex; flex-direction: column; align-items: center; gap: 12px; }
    .label { font: var(--ait-type-title-small); letter-spacing: .1px; color: var(--md-sys-color-on-surface-variant); }
    .box { fill: var(--md-sys-color-logo-box); } .box-stroke { stroke: var(--md-sys-color-logo-box); }
    .chev { stroke: var(--md-sys-color-on-logo-box); } .cursor { stroke: var(--md-sys-color-logo-cursor); }
    .ai-stroke { stroke: var(--md-sys-color-ai); } .ai-fill { fill: var(--md-sys-color-ai); } .on-ai { fill: var(--md-sys-color-on-ai); }
    @keyframes badge-in { 0% { transform: scale(0); opacity: 0 } 4% { transform: scale(1.12); opacity: 1 } 6.5% { transform: scale(.96); opacity: 1 } 8%, 100% { transform: scale(1); opacity: 1 } }
    @keyframes la { 0%, 6% { transform: translateY(8px); opacity: 0 } 10% { transform: translateY(-1px); opacity: 1 } 11.5%, 100% { transform: translateY(0); opacity: 1 } }
    @keyframes li { 0%, 8.5% { transform: translateY(8px); opacity: 0 } 12.5% { transform: translateY(-1px); opacity: 1 } 14%, 100% { transform: translateY(0); opacity: 1 } }
    @keyframes sheen { 0%, 14% { transform: translateX(0); opacity: 0 } 14.5% { opacity: .6 } 18.5% { transform: translateX(40px); opacity: .6 } 19%, 100% { transform: translateX(40px); opacity: 0 } }
    @keyframes badge-pulse { 0%, 68% { transform: scale(1) } 71% { transform: scale(1.08) } 75%, 100% { transform: scale(1) } }
    @keyframes pen { 0%, 18% { offset-distance: 0%; opacity: 0 } 18.5% { opacity: 1 } 65.5% { opacity: 1 } 66%, 100% { offset-distance: 100%; opacity: 0 } }
    @keyframes ln-box { 0%, 19.77% { stroke-dashoffset: 100; opacity: 0 } 19.87% { opacity: 1 } 46%, 68% { stroke-dashoffset: 0; opacity: 1 } 74%, 100% { stroke-dashoffset: 0; opacity: 0 } }
    @keyframes ln-handle { 0%, 46.23% { stroke-dashoffset: 100; opacity: 0 } 46.33% { opacity: 1 } 52.65%, 68% { stroke-dashoffset: 0; opacity: 1 } 74%, 100% { stroke-dashoffset: 0; opacity: 0 } }
    @keyframes ln-chev { 0%, 54.32% { stroke-dashoffset: 100; opacity: 0 } 54.42% { opacity: 1 } 57.66%, 68% { stroke-dashoffset: 0; opacity: 1 } 74%, 100% { stroke-dashoffset: 0; opacity: 0 } }
    @keyframes ln-cur { 0%, 60.17% { stroke-dashoffset: 100; opacity: 0 } 60.27% { opacity: 1 } 62.22%, 68% { stroke-dashoffset: 0; opacity: 1 } 74%, 100% { stroke-dashoffset: 0; opacity: 0 } }
    @keyframes fill { 0%, 68% { opacity: 0 } 73%, 100% { opacity: 1 } }
    @keyframes blink { 0%, 73% { opacity: 0 } 75% { opacity: 1 } 81% { opacity: 0 } 85% { opacity: 1 } 91% { opacity: 0 } 93%, 100% { opacity: 1 } }
    @keyframes guide { 0%, 14% { opacity: 0 } 18%, 64% { opacity: .55 } 69%, 100% { opacity: 0 } }
    .badge-in { transform-origin: 55px 15px; animation: badge-in 4.8s cubic-bezier(.34,1.4,.64,1) infinite; }
    .badge-pulse { transform-origin: 55px 15px; animation: badge-pulse 4.8s cubic-bezier(.2,0,0,1) infinite; }
    .la { animation: la 4.8s cubic-bezier(.2,0,0,1) infinite; }
    .li { animation: li 4.8s cubic-bezier(.2,0,0,1) infinite; }
    .sheen { animation: sheen 4.8s cubic-bezier(.2,0,0,1) infinite; }
    .pen { offset-path: path("M55 24.5L44 22H14a10 10 0 0 0-10 10v16a10 10 0 0 0 10 10h36a10 10 0 0 0 10-10V32a10 10 0 0 0-10-10H44L43 23v-6a6 6 0 0 0-6-6H27a6 6 0 0 0-6 6v6L17.5 33l8 7-8 7L33.5 47h13L55 24.5"); offset-rotate: 0deg; animation: pen 4.8s linear infinite; }
    .ln-box { animation: ln-box 4.8s linear infinite; } .ln-handle { animation: ln-handle 4.8s linear infinite; }
    .ln-chev { animation: ln-chev 4.8s linear infinite; } .ln-cur { animation: ln-cur 4.8s linear infinite; }
    .fill { animation: fill 4.8s linear infinite; } .blink { animation: blink 4.8s linear infinite; } .guide { animation: guide 4.8s linear infinite; }
    .ait-once * { animation-iteration-count: 1 !important; animation-fill-mode: forwards !important; }
    @media (prefers-reduced-motion: reduce) {
      .ait-loader * { animation: none !important; }
      .o { opacity: 0; } .pen { opacity: 0; } .fill, .blink { opacity: 1; } .badge-in { transform: none; opacity: 1; } .sheen { opacity: 0; }
    }
  `,
})
export class AitBrandLoader {
  /** Height in px: 96 for splash and workspace boot, 40 minimum. */
  readonly size = input(96, { transform: numberAttribute });
  /** Play one time and stay on the logo. */
  readonly once = input(false, { transform: booleanAttribute });
  /** Visible label under the loader, e.g. "Preparing your toolbox…". */
  readonly label = input('');
  protected readonly uid = aitUid('ait-ldr');
}
