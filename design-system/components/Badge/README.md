# Badge
Counts and "something new" dots on icons and navigation items.
- **Small** 6 px dot, no text. **Large** 16 px high, label-small, min-width 16 px, "999+" past three digits.
- Always `error` on `on-error`: a badge is an alert, so it never takes a brand colour.
- Place at the top-right of the icon; in a navigation item the badge sits on the icon, not the label.
- **Angular Material:** `matBadge`. M2: `matBadgeColor="warn"` for alerts (never `primary` for a count that is an alert). M3: `mat.badge-overrides` — the default already lands on `error`. Full map and theme files: `angular-material.md`.
