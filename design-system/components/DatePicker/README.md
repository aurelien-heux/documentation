# DatePicker
Modal date picker, 328 px, radius-lg (16 px), `surface-container-high`, elevation-3.
- Header: label-medium supporting text, the selected date in headline-large, an edit icon to switch to text input.
- 40 px day cells; today outlined in `primary`, the selection filled `primary`. Text buttons Cancel / OK.
- For ranges use the full-screen range picker; for a single date in a dense form use a docked picker under the field.
- **Angular Material:** `mat-datepicker` with `mat-datepicker-toggle` in a `mat-form-field`. M2: selected day `primary`; M3: `mat.datepicker-overrides` pins the 16 px container (`calendar-container-shape`) in both theme files. Full map and theme files: `angular-material.md`.
