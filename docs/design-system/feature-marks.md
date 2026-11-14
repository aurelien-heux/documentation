# Feature marks · Sweep, Docs, Environments, Chatbot, Notifications

Marks for the AIToolbox features, separate from the product logo. One folder per feature, then `light/` and `dark/`, like the rest of the brand package. Open `index.html` for a live preview (with a button to play the once versions again).

- `light/` — colours for **light backgrounds**: the Sweep purple (primary #39235F), teal (ai 50 #278383), green (tertiary 60 #00A56B).
- `dark/` — colours for **dark backgrounds**: lavender (primary 70 #A6A2F8), light teal (ai 80 #80D5D4), neon green (tertiary #00F29E).
- Chatbot keeps its validated colours: the Sweep purple #39235F with a #008857 cursor on light, lavender #C4C0FF with a neon #00F29E cursor on dark.

Colours are fixed in each file (no automatic switching), so you choose the file that matches the surface. All backgrounds are transparent except the GIFs.

Each mark comes in three versions — they are **different animations**, not the same one at two speeds:

| Version | What it does | When |
|---|---|---|
| **static** (`<feature>.svg`) | No motion. | Navigation, lists, documents, anywhere by default. |
| **once** (`<feature>-once.svg` / `.gif`) | An **entrance**: the mark builds itself from nothing, plays **one time** and stays on the static mark. Never repeats. | When the feature opens, a page loads, an action completes. |
| **loop** (`<feature>-loop.svg` / `.gif`) | A **working** motion on the mark already in place; repeats until you remove it. Each cycle starts and ends on the static mark. | While something is in progress. |

| Feature | Once — entrance, plays one time | Loop — working, repeats |
|---|---|---|
| **Sweep** · agentic SDLC pipeline · broom & sparkle | 1.8 s: the broom drops in from the top right, sweeps across and settles; the two sparkles pop where it passed | 2.8 s: the sparkles fade, the broom winds up and sweeps, the sparkles pop back |
| **Docs** · documentation · shelf | 1.5 s: the books slide up onto the shelf in turn; the last lands upright, then leans | 3.0 s: the first two books lift in turn; the leaning one straightens and falls back |
| **Environments** · environment management · promotion | 1.8 s: the path draws, each node pops as it is reached, the check draws on prod | 2.8 s: a release token travels dev → staging → prod; nodes pulse; the check redraws |
| **Chatbot** · assistant · brace box `{ >_ }` | 1.4 s: the bubble pops out of its tail, the prompt fades in, the cursor blinks once | 2.8 s (typing): the prompt gives way to three bouncing dots, then comes back |
| **Notifications** · notification centre · bell | 1.6 s: the bell drops in and swings to rest; the green unread dot pops last | 2.6 s (new notification): the bell rings, the clapper follows, then the dot pulses |

## Files — in `<feature>/light/` and `<feature>/dark/`

| File | Use |
|---|---|
| `<feature>.svg` | Static mark, 64 × 64 viewBox. Apps, web, PowerPoint. |
| `<feature>-once.svg` | Entrance, plays one time and holds the static mark (CSS `animation-iteration-count: 1`). |
| `<feature>-loop.svg` | Working loop (CSS `infinite`). |
| `<feature>-lockup.svg` | Mark + "AIToolbox" label + feature name; text outlined (Manrope 700 / 800), no font needed. |
| `<feature>-<size>.png` | Static mark, transparent: 16, 24, 32, 48, 64, 128, 256, 512 px (Chatbot from 24 px). Google Slides, older Office, wikis, tool avatars, email. |
| `<feature>-lockup@2x.png` | Lockup at 2×, transparent: title slides, document headers, release notes. |
| `<feature>-once.gif` | 256 px on the surface colour, **no loop flag**: plays one time and stops on the mark (browsers, PowerPoint, Confluence, email). |
| `<feature>-loop.gif` | 256 px on the surface colour, loops forever. |

Some viewers replay every GIF regardless of its loop flag (macOS Quick Look, Slack, Teams previews); there the once GIF repeats too. Use the static PNG in those places, or the loop GIF on purpose.

## Motion

- CSS inside the SVG: transform, opacity and stroke-dashoffset only; easing `cubic-bezier(.2, 0, 0, 1)` (MD emphasized). Under `prefers-reduced-motion: reduce` the static mark shows. Tools that ignore CSS animation (PowerPoint) also show the static mark.
- At most one looping mark per screen. Don't chain once into loop on the same element; swap the file when work starts.

```html
<img src="sweep/light/sweep.svg" width="24" height="24" alt="">                        <!-- navigation -->
<img src="sweep/light/sweep-once.svg" width="64" height="64" alt="Sweep">               <!-- feature opened -->
<img src="sweep/light/sweep-loop.svg" width="40" height="40" alt="Sweep running">      <!-- in progress -->
<picture>
  <source srcset="docs/dark/docs.svg" media="(prefers-color-scheme: dark)">
  <img src="docs/light/docs.svg" width="32" height="32" alt="Docs">
</picture>
```

```js
img.src = img.src.split('?')[0] + '?r=' + Date.now();   // play a "once" file again
```

## Rules

- The marks identify the features (navigation drawer and rail items, feature headers, empty states, the docs site, release notes). The AIToolbox logo stays the product brand; never place the two marks side by side as equals.
- In the app header the bell is drawn without its dot (`bell_icon`): an `error` count badge sits on it instead (1–9, 9+ … 99+); the loop runs once when a new notification arrives.
- Sizes: 16 px minimum (Chatbot: 24 px minimum — bubble avatar 24, assistant panel header 32, launcher 48); 24 px in navigation; 32–48 px in headers; 64 px and up for empty states and splash.
- Never recolour: pick the `light/` or `dark/` file for the background; on colour or photos, place the mark on a `surface` tile.
- Lockup: use the supplied files, don't retype.
