/*
 * @aitoolbox/architecture — ArchiMate notation and ARB review components of the AIToolbox design system.
 * Styles: import 'src/styles/archimate.css' after css/tokens.css (or use the theme bridge in styles/_theme.scss).
 */
export * from './lib/notation.generated';
export { AxGlyphComponent } from './lib/icons/ax-glyph.component';
export { AxIconRegistry, IconRegistryLike } from './lib/icons/ax-icon-registry';
export { AxTileComponent } from './lib/ax-tile/ax-tile.component';
export { AxFigureComponent } from './lib/ax-figure/ax-figure.component';
export { AxChangeComponent } from './lib/ax-change/ax-change.component';
export { AxTrackComponent, AxPlateau } from './lib/ax-track/ax-track.component';
export { AxRelationshipComponent, AxMarker, marker } from './lib/ax-relationship/ax-relationship.component';
export { AtbStatusChipComponent, AtbStatusTone } from './lib/readiness-chip/status-chip.component';
export { AtbReadinessChipComponent, AtbReadiness } from './lib/readiness-chip/readiness-chip.component';
export { AtbDecisionChipComponent, AtbDecision, ATB_DECISIONS } from './lib/decision-chip/decision-chip.component';
export { AtbCheckRowComponent, AtbCheck, AtbCheckFinding, AtbCheckStatus } from './lib/check-row/check-row.component';
export { AtbAsdSectionComponent, AtbAsdSource } from './lib/asd-section/asd-section.component';
