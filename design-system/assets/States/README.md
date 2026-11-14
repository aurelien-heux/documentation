# States

The state marks: the logo's construction with the state in the badge instead of "AI". The toolbox never changes — deep-violet `primary` (lavender tone 80 in dark) with its `>_` — and the corner badge (same corner and cut-out as the AI badge) carries the state role and a symbol: ✓ success, i info (`primary`), ! warning, ✕ error. Light and dark files; colours are fixed in each file.

Three dressings, chosen by size only:

| File | Container | Size | Note |
|---|---|---|---|
| `state-<state>-badge-<theme>.svg` (A) | Snackbar | 24 px | Leading, on the inverse surface (dark file in light theme). |
| | Inline alert in a popin, page banner | 24–28 px | On the state container strip. |
| | Popin / dialog header | 32–40 px | Next to the title of a state-driven popin (destructive confirm, warning). |
| `state-<state>-circle-<theme>.svg` (B) | Table-, panel- or popin-level empty / error state | 56–64 px | Inside the container's frame with title, cause and a Retry button. |
| | Page / workspace empty state | 72–96 px | The only place the mark is a hero. |
| `state-<state>-tile-<theme>.svg` (C, filled) | Table row status column, list row, menu item | 18–20 px | Leads the message; a text "Retry" follows a failed row. |
| `state-<state>-tile-tinted-<theme>.svg` (C, tinted) | Status chip, dropdown option, inline alert | 18–20 px | Inside a container that already has the state tint; the option stays selectable unless the state is error. |
| `state-pending-<theme>.svg` | Any B slot while a request is pending | 56–96 px | Pen-orbit ring around the plain mark; in A and C slots use the 24 / 18 px pen orbit from `loading-states/`. When the request resolves, swap in place (no layout shift) for the state: warning after a timeout ("Still loading…", keep waiting), error with Retry on failure. |

Also: loading is not a state and shows no badge; never below 18 px (use an 8 px dot); never recolour outside the four roles; never as the app logo; no entrance animation — a state mark appears with its container.
