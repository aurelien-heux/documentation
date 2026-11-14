import { inject, Injectable } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { AX_GLYPHS, AX_SVG_ATTRS, AX_TYPES, AxType } from '../notation.generated';

/**
 * Registers every ArchiMate glyph with Angular Material's MatIconRegistry under the namespace `ax`,
 * so `<mat-icon svgIcon="ax:business-object">` works wherever mat-icon is already used.
 * MatIconRegistry is typed loosely to keep @angular/material an optional peer: pass the registry instance.
 */
export interface IconRegistryLike {
  addSvgIconLiteralInNamespace(namespace: string, iconName: string, literal: unknown): unknown;
}

@Injectable({ providedIn: 'root' })
export class AxIconRegistry {
  private readonly sanitizer = inject(DomSanitizer);
  private registered = false;

  /** Call once at app start: `inject(AxIconRegistry).registerWith(inject(MatIconRegistry))`. */
  registerWith(registry: IconRegistryLike): void {
    if (this.registered) return;
    for (const type of Object.keys(AX_TYPES) as AxType[]) {
      const inner = AX_GLYPHS[AX_TYPES[type].glyph] ?? '';
      registry.addSvgIconLiteralInNamespace('ax', type, this.sanitizer.bypassSecurityTrustHtml(`<svg ${AX_SVG_ATTRS}>${inner}</svg>`));
    }
    this.registered = true;
  }

  /** `<use href="archimate-sprite.svg#ax-<type>">` for templates that prefer the sprite (assets/archimate-sprite.svg). */
  spriteRef(type: AxType, spriteUrl = 'archimate-sprite.svg'): string {
    return `${spriteUrl}#ax-${type}`;
  }
}
