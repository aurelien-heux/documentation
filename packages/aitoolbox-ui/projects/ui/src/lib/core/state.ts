/** The four feedback states of the design system. Loading is not a state: it is `pending`. */
export type AitState = 'success' | 'info' | 'warning' | 'error';
/** A state, or `pending` while a request has not resolved yet. */
export type AitStateOrPending = AitState | 'pending';
/** Health shown by a StatusChip: the four states plus `unknown`. */
export type AitHealth = AitState | 'unknown';

/** Default words for each state, used as accessible names when no label is given. */
export const AIT_STATE_LABELS: Record<AitStateOrPending | 'unknown', string> = {
  success: 'Success',
  info: 'Info',
  warning: 'Warning',
  error: 'Error',
  pending: 'Loading',
  unknown: 'Unknown',
};

let nextUid = 0;
/** Unique id prefix for SVG masks and ARIA relations, stable for the life of one component. */
export function aitUid(prefix = 'ait'): string {
  nextUid += 1;
  return `${prefix}-${nextUid}`;
}
