# AIToolbox colour system review (decision open)

Date: 2026-11-14 · Baseline: tokens 4.7 · Lab: board `ColourLab.dc.html` on the AIToolbox labs canvas (https://claude.ai/artifact/DTSkQfZZJTHTrpBSQxmZVg) and the phone-friendly Colour Decision Lab page (https://claude.ai/artifact/2mZGPYmS98tgzvpEb8jjgd).

Status: **decided 2026-11-14 — option C, with the dark lavender primary kept.** Applied as tokens 5.0.0, adjusted in 5.0.1 (purple Run label, calmer Discussion panel) (design system, both Angular theme files, the three canvases, component rules, domain reference DEC-DS-09).

### What was applied (tokens 5.0)

- Primary: light #39235F (Sweep purple); the whole dark primary family stays on the lavender #C4C0FF (#2A2473 / #413C8A / #E3DFFF); light primary-container stays #E3DFFF.
- Secondary from the pale purple: secondary-container #DED7EB / #484454, secondary #484454 / #CAC3D7.
- Tertiary from the lime: tertiary #404B23 / #BFCC99; tertiary-container #DCEAB4 in both themes (pinned: the lime Run is kept in dark), on-tertiary-container the Sweep purple #39235F in both themes (10.4:1; changed from olive #151F00 in 5.0.1 at the user’s request).
- ai on Material tones: #004F50 / #80D5D4, on-ai #FFFFFF / #003737. success #0B5314 and warning #5C4300 in light (tone 30).
- Removed: run, on-run, run-icon, run-outline, run-text, nav-active, focus-ring, ai-strong, surface-variant (deprecated aliases in tokens.css until 5.1). Brand group: logo-box, on-logo-box, logo-cursor, logo-ai, on-logo-ai.
- Answers to the open points: dark Run stays lime (one pin); running dots follow tertiary (olive / pale lime), the neon stays in the logo; the active nav pill is carried by its 3 px bar; the Run label is the Sweep purple #39235F (5.0.1).
- Not recoloured: brand marks and logo files (they keep their own colours), the historical labs (Run button rounds, hover, purples trial, accessibility plan) and the colour lab itself.

## Findings on tokens 4.7

| # | Finding | Evidence |
|---|---|---|
| 01 | Two purples for one brand | Light primary #39235F on hue 303 (Sweep); every other purple role and the dark theme on hue 288. |
| 02 | Five greens, five meanings | tertiary neon #00F29E (running), success #1B5F1F (healthy), run lime #DCEAB4 (action), logo cursor, feature marks #00A56B / dots #008857 (not tokens). |
| 03 | Six tokens for one button | run, on-run, run-icon, run-outline, run-text; four of them are #39235F in light; the edge exists in light only. |
| 04 | Same value, different names | primary-container = secondary-container (light #E3DFFF), focus-ring = primary, run-icon = on-run, surface-bright = surface (light), surface-dim = surface (dark). |
| 05 | Navigation has its own pair | nav-container + nav-active outside Material; the pill is 1.2 : 1 on the band, hence the 3 px bar. |
| 06 | No single tone rule | Light roles: primary 20, tertiary/error 30, secondary/success/warning 35, ai 80 with ai-strong 40. |
| 07 | AI upside down | ai is the pale teal in both themes; lines and dots need ai-strong. |
| 08 | Brand inside the UI scheme | logo-box, on-logo-box, logo-cursor listed with UI roles; legacy surface-variant still exported. |
| 09 | Values outside the tokens | theme.m2.scss: 44 hex values not in tokens; canvas boards: 268 distinct hex values, 197 not tokens (2,931 uses); feature-marks package still #35307E. |
| 10 | Exceptions kept for contrast | Light accents at tone 30 instead of 40, dark inverse-primary at 30: deliberate, to state as one rule. |

Totals: 58 colour tokens, 24 outside Material 3, 11 exceptions, 9 hue families.

## Options

| | A · Keep 4.7 | B · Tidy | C · Sweep palette | D · Material 3 as generated |
|---|---|---|---|---|
| Idea | Nothing moves | Same colours, duplicates and one-off tokens folded into Material roles | The three Sweep colours seed the scheme: #39235F primary, #DED7EB secondary, #DCEAB4 tertiary | Tonal-spot scheme from #39235F, nothing pinned |
| UI colour tokens | 58 | 48 (+4 brand) | 46 (+4 brand) | 45 (+4 brand) |
| Outside Material 3 | 24 | 15 | 13 | 12 |
| Exceptions | 11 | 5 | 2 (3 with the lime Run kept in dark) | 0 |
| Run button | run · on-run · run-icon · run-outline | run · on-run | tertiary-container · on-tertiary-container | tertiary-container (pink) |
| Navigation | nav-container + nav-active | nav-container, pill = secondary-container | nav-container, pill = secondary-container (pale purple) | surface-container, no band |
| Light primary | #39235F | #39235F | #39235F | #69548D (tone 40) |
| Lowest text contrast (checked pairs) | 7.2 : 1 | 7.2 : 1 | 7.2 : 1 | 5.0 : 1 |
| Visual change | None | Small | Medium | Large |

B details: run-icon/run-outline → on-run (edge in both themes), run-text → primary, nav-active → secondary-container (#D4D0F9 light), focus-ring → primary, ai-strong → ai (ai = #006A6A light / #80D5D4 dark), logo tokens and the teal badge (`logo-ai`) to a brand group, surface-variant removed. Two purple hues remain.

C details: primary palette hue 303 in both themes (dark primary #D4BBFF, containers #EBDCFF / #513B78); secondary from #DED7EB (hue 296, the neutrals' hue) = light secondary-container; tertiary from the lime: Run = tertiary-container (light: lime with an olive #151F00 label instead of the Sweep purple; dark by rule: olive #404B23 with a lime label, 2.0 : 1 against the page); running dots = tertiary (olive / pale lime), the neon stays only in the logo; one tone rule (light roles 30, primary 20, dark 80, containers 90/30, on-containers 10/90); neutrals unchanged; nav-container kept.

## Recommendation

C, with today's lime Run kept in dark (one pin: tertiary-container dark = #DCEAB4; Run then 14.5 : 1 against the dark page, label 13.4 : 1). It removes the special cases instead of renaming them, keeps the Sweep identity, and every checked text pair stays at 7.2 : 1 or more. B is the fallback if nothing on screen may move; D shows the cost of going fully generic.

## To settle if C is chosen

1. Dark Run: olive container (rule) or lime as today (one pin). Recommended: lime.
2. Running dots: olive / pale lime (rule) or keep the neon (one extra token).
3. Active nav pill: pale purple on the band is 1.1 : 1; the 3 px bar carries the state.
4. Run label in light becomes olive #151F00 instead of the Sweep purple (or pin on-tertiary-container to #39235F).

Applying a choice = tokens 5.0, both Angular theme files, canvas recolour, assets (working dots, feature marks), component rules and the domain reference, in one pass.
