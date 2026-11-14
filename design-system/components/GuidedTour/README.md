# GuidedTour

A sequence of steps that each point at one element of the page: the **spotlight** (a scrim with a cutout on the target) and a **step card** beside it. Decided in the Tour focus lab (canvas, Prototypes page): spotlight adopted over ring, pulse, beacon, blur, glow and spotlight + pulse. Live in the Community prototype; CSS in `brand/css/tour.css`.

## Anatomy

- **Spotlight.** A `scrim` layer at 42 % over the whole page with a cutout 6 px larger than the target on every side. The cutout keeps `radius-md` 12 (`radius-lg` 16 when the target is a navigation item). The target itself stays at full brightness and is the only thing that can be clicked; the dimmed page is inert.
- **Ring.** A 2 px `primary` border on the cutout edge, with the same 4 px `primary` 18 % glow as the focus ring, so the eye finds the exact edge of the target.
- **Step card.** `surface-container-high`, elevation-2, `radius-md` 12, 340 px wide, padding 12 × 16. First line: a tag naming the tour (`primary-container`, "New in 4.6") and "Step n of N" in body-small; then the step title in title-small and the body in body-medium `on-surface-variant` (two sentences at most); actions right-aligned as text buttons: Skip, Back (from step 2), Next or Done. A preview run by an admin adds a neutral StatusChip "Preview".
- **Placement.** The card sits 16 px to the right of the cutout, top-aligned 8 px above it; if it does not fit, 16 px to the left; otherwise 12 px below the cutout, left-aligned and kept 16 px inside the page. Never over the target.

## Behaviour

- **Anchors, not coordinates.** Every step points at a `data-anchor` id that the feature team registers on an element when it ships. The tour measures the element at runtime (after fonts load, on resize and after every render) and draws the cutout from that rectangle, so it stays on the target whatever the width, font or theme. A step whose anchor is missing from the page is skipped and reported.
- **Scroll first.** If the target is outside the viewport, it is scrolled to the centre before the spotlight appears.
- **Wide targets.** When the target is wider than 60 % of the page (a whole table, a card column) the scrim drops to 16 % so the content under it stays readable; the ring stays.
- **Motion.** The scrim fades in over 350 ms and the card rises 8 px over 400 ms, MD emphasized easing; moving to the next step replays both. Nothing loops. Under `prefers-reduced-motion` both appear without motion.
- **Lifecycle.** Started from a release card ("Try it in the app"), a Guides card, the Help menu ("Show me around this page") or a trigger set in Administration (first visit after a release, first visit to a page, after N uses). Finishing a tour marks the guide completed; Skip does not. A tour is shown once per trigger; it can always be replayed from Guides.

## Keyboard and screen reader

- The card is `role="dialog"` with `aria-label` "Guided tour", focus moves to it on each step, and Tab stays inside it; Esc = Skip. The actions are ordinary buttons in the visible order.
- The target keeps its name and role; the card body names it in words, so a screen-reader user knows what is pointed at without the spotlight. The spotlight layers are `aria-hidden`.
- Nothing under the scrim is in the Tab order while the tour runs.

## Don't

- Don't point at several elements in one step, and don't use the spotlight for anything that is not a tour (a contextual tip is an inline card; a feature announcement is a release card).
- Don't use teal: a tour is chrome, even when it presents an AI feature. The AI feature keeps its own teal inside the cutout.
- Don't add a pulse, beacon or blur: they were evaluated and not kept.
