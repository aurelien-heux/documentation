# TimePicker
Input-mode time picker, 328 px: two 96×80 px fields in display-large, the active one in `primary-container`, AM/PM segmented in `tertiary-container` when selected.
- A dial mode exists for touch; the input mode is the default on desktop and in 24 h locales (then no AM/PM).
- Schedules and maintenance windows always show the timezone next to the field.
- **Angular Material:** M2 (≤ 18): no Angular component — this TimePicker is a custom dial/input. M3 (19+): `mat-timepicker` with `matTimepicker` on a `matInput`; `surface-container-high` container via `mat.timepicker-overrides`. Full map and theme files: `angular-material.md`.
