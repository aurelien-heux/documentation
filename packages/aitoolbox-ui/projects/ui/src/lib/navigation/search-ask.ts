import { ChangeDetectionStrategy, Component, ElementRef, inject, input, model, output, viewChild } from '@angular/core';
import { MatIcon } from '@angular/material/icon';
import { MatTooltip } from '@angular/material/tooltip';
import { AitIconRegistry } from '../core/icons';
import { aitUid } from '../core/state';
import { AitChatbotMark } from '../brand/logo';

/**
 * Search-or-ask field of the app header: 44 px, radius 16, on surface-container-lowest (light) / -high (dark).
 * Enter searches; the Ask chip (ai-container + Chatbot mark) sends the text to the assistant. ⌘K / Ctrl+K focuses it.
 * `compactAsk` shows the Ask chip as an icon (Medium and Expanded windows).
 */
@Component({
  selector: 'ait-search-ask',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [MatIcon, MatTooltip, AitChatbotMark],
  host: {
    class: 'ait-search-ask',
    role: 'search',
    '(document:keydown)': 'onDocumentKey($event)',
  },
  template: `
    <mat-icon svgIcon="ait:search" class="lead" aria-hidden="true" />
    <label [attr.for]="uid" class="ait-visually-hidden">{{ placeholder() }}</label>
    <input #field [id]="uid" type="search" [placeholder]="placeholder()" [value]="query()" autocomplete="off"
      (input)="query.set(field.value)" (keydown.enter)="search.emit(field.value)" />
    <kbd class="shortcut" aria-hidden="true">{{ shortcut }}</kbd>
    <button type="button" class="ask" [class.ask--icon]="compactAsk()" [attr.aria-label]="compactAsk() ? 'Ask the assistant' : null"
      [matTooltip]="askDisabledReason() || (compactAsk() ? 'Ask the assistant' : '')" [attr.aria-disabled]="askDisabledReason() ? 'true' : null"
      (click)="onAsk()">
      <ait-chatbot-mark [size]="24" />
      @if (!compactAsk()) { <span>Ask</span> }
    </button>
  `,
  styles: `
    :host { display: flex; align-items: center; gap: 10px; height: 44px; padding: 0 6px 0 14px; box-sizing: border-box; border-radius: 16px;
      background: light-dark(var(--md-sys-color-surface-container-lowest), var(--md-sys-color-surface-container-high)); color: var(--md-sys-color-on-surface-variant); min-width: 0; }
    :host:focus-within { box-shadow: inset 0 0 0 2px var(--md-sys-color-primary); }
    .lead { width: 22px; height: 22px; flex: none; }
    input { flex: 1; min-width: 0; height: 100%; border: 0; outline: none; background: transparent; color: var(--md-sys-color-on-surface);
      font: var(--ait-type-body-medium); letter-spacing: var(--ait-type-body-medium-tracking); }
    input::placeholder { color: var(--md-sys-color-on-surface-variant); }
    input::-webkit-search-cancel-button { display: none; }
    .shortcut { font-family: var(--ait-font-body); font-weight: 600; font-size: 11px; line-height: 16px; padding: 0 6px; border-radius: 4px;
      border: 1px solid var(--md-sys-color-outline-variant); color: var(--md-sys-color-on-surface-variant); }
    .ask { display: inline-flex; align-items: center; gap: 4px; height: 32px; padding: 0 12px 0 4px; border: 0; border-radius: 12px; cursor: pointer;
      background: var(--md-sys-color-ai-container); color: var(--md-sys-color-on-ai-container); font: var(--ait-type-label-medium); letter-spacing: .5px; flex: none; }
    .ask:hover { box-shadow: inset 0 0 0 100px color-mix(in srgb, var(--md-sys-color-on-ai-container) 6%, transparent); }
    .ask--icon { width: 36px; padding: 0; justify-content: center; }
    .ask[aria-disabled='true'] { opacity: .5; cursor: not-allowed; }
  `,
})
export class AitSearchAsk {
  readonly placeholder = input('Search, or ask the assistant…');
  /** Ask chip as a 36 px icon (Medium and Expanded windows). */
  readonly compactAsk = input(false);
  /** When set, the Ask chip is disabled with this reason (Tooltip E). */
  readonly askDisabledReason = input('');
  readonly query = model('');
  readonly search = output<string>();
  readonly ask = output<string>();

  protected readonly uid = aitUid('ait-search');
  protected readonly shortcut = typeof navigator !== 'undefined' && /Mac|iP(hone|ad)/.test(navigator.platform) ? '⌘K' : 'Ctrl K';
  private readonly field = viewChild.required<ElementRef<HTMLInputElement>>('field');

  constructor() {
    inject(AitIconRegistry);
  }

  /** Moves focus into the field. */
  focus(): void {
    this.field().nativeElement.focus();
  }

  protected onAsk(): void {
    if (!this.askDisabledReason()) this.ask.emit(this.field().nativeElement.value);
  }

  protected onDocumentKey(e: KeyboardEvent): void {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      this.focus();
    }
  }
}
