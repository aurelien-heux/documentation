import { ChangeDetectionStrategy, Component, computed, input, numberAttribute } from '@angular/core';
import { aitUid } from '../core/state';

/**
 * - `horizontal` default lockup (clear space included) · `stacked` square slots and splash screens
 * - `mark` the toolbox prompt with the AI badge, from 24 px · `mark-plain` without the badge, under 24 px
 * - `wordmark` "AIToolbox", outlined (never retyped)
 */
export type AitLogoVariant = 'horizontal' | 'stacked' | 'mark' | 'mark-plain' | 'wordmark';

/**
 * Logo — the toolbox-prompt mark and its lockups, drawn from the design-system files with the logo tokens, so it is the
 * night box on light grounds and the lavender box on dark grounds without picking a file.
 * Under 32 px use the favicon (assets/logos/favicon-*.svg) instead of the mark.
 */
@Component({
  selector: 'ait-logo',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { class: 'ait-logo', role: 'img', '[attr.aria-label]': 'label()' },
  templateUrl: './logo.html',
  styles: `:host { display: inline-flex; flex: none; line-height: 0; }`,
})
export class AitLogo {
  readonly variant = input<AitLogoVariant>('horizontal');
  /** Rendered height in px. Defaults: horizontal 44, stacked 96, mark 32, mark-plain 24, wordmark 24. */
  readonly size = input<number | undefined, unknown>(undefined, { transform: (v: unknown) => (v == null || v === '' ? undefined : numberAttribute(v)) });
  readonly label = input('AIToolbox');
  protected readonly uid = aitUid('ait-logo');
  protected readonly height = computed(() => {
    const d: Record<AitLogoVariant, number> = { horizontal: 44, stacked: 96, mark: 32, 'mark-plain': 24, wordmark: 24 };
    return this.size() ?? d[this.variant()];
  });
}

/**
 * Chatbot mark — the assistant's avatar, the `{ >_ }` brace box drawn as one outline. Never the brand mark, never below
 * 24 px: 24 in a message, 32 in the assistant header, 48 in a launcher.
 */
@Component({
  selector: 'ait-chatbot-mark',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: 'ait-chatbot-mark',
    '[attr.role]': 'label() ? "img" : null',
    '[attr.aria-label]': 'label() || null',
    '[attr.aria-hidden]': 'label() ? null : "true"',
  },
  template: `
    <svg viewBox="0 0 64 64" [attr.width]="px()" [attr.height]="px()" focusable="false" aria-hidden="true">
      <path d="M26 56h-3a9 9 0 0 1-9-9v-4l-5-4 5-4v-4a9 9 0 0 1 9-9h2l7-5 7 5h2a9 9 0 0 1 9 9v4l5 4-5 4v4a9 9 0 0 1-9 9h-3" fill="none" class="line" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" />
      <path d="M26 37l6 5-6 5" fill="none" class="line" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" />
      <path d="M35 49h5" fill="none" class="cursor" stroke-width="4.5" stroke-linecap="round" />
    </svg>
  `,
  styles: `
    :host { display: inline-flex; flex: none; line-height: 0; }
    .line { stroke: var(--md-sys-color-primary); }
    .cursor { stroke: light-dark(#008857, #00f29e); }
  `,
})
export class AitChatbotMark {
  readonly size = input(24, { transform: numberAttribute });
  /** Accessible name; empty when a visible label sits next to it. */
  readonly label = input('');
  protected readonly px = computed(() => Math.max(24, this.size()));
}
