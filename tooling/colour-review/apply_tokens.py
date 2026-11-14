import json, re
R = '/tmp/claude-0/-home-claude/7965e1dc-e9df-573c-8252-b3af265ef67c/scratchpad/ds5/project/'
t = json.load(open(R + 'tokens.json'))
old = {k['name']: k for k in t['color']['tokens']}

REMOVED = ['run', 'on-run', 'run-icon', 'run-outline', 'run-text', 'nav-active', 'focus-ring', 'ai-strong', 'surface-variant']
BRAND = ['logo-box', 'on-logo-box', 'logo-cursor']
NEW = {  # name: (light, dark, usage or None to keep)
 'primary': ('#39235f', '#c4c0ff', 'The Sweep purple #39235F in light, the lavender #C4C0FF in dark (kept from 4.x). Filled buttons, links, active tab and navigation bar, focused field border, switches on, the keyboard focus ring (2 px with a 2 px gap: 12.7 : 1 light, 10.9 : 1 dark), the “Toolbox” of the wordmark. Text on it: on-primary.'),
 'secondary': ('#484454', '#cac3d7', 'From the Sweep pale purple #DED7EB (hue 296, the hue of the neutrals), tone 30 in light. Secondary icons and text accents; rarely a fill.'),
 'on-secondary': ('#ffffff', '#322e3d', None),
 'secondary-container': ('#ded7eb', '#484454', 'The Sweep pale purple #DED7EB in light: tonal buttons, filter and selected chips, segmented selection, environment badges, avatars and the active navigation pill (with a 3 px primary bar, because the pill is 1.1 : 1 on the band). Text on it: on-secondary-container.'),
 'on-secondary-container': ('#1d1a28', '#e6dff3', 'Text and icons on secondary-container (12.2 : 1 light, 7.3 : 1 dark).'),
 'tertiary': ('#404b23', '#bfcc99', 'From the Sweep lime #DCEAB4: olive in light (tone 30, 8.9 : 1 on the page), pale lime in dark. Running dots and deploy states, never a fill. The neon green stays in the logo only.'),
 'on-tertiary': ('#ffffff', '#2a340f', 'Text on tertiary.'),
 'tertiary-container': ('#dceab4', '#dceab4', 'The Sweep lime #DCEAB4 in both themes (pinned in dark): the Run action (Run, Deploy, Apply, New run; one per screen, a tonal button, never in a dialog), the disc behind the play icon of row Re-run actions, “Deploying…” chips. Text on it: on-tertiary-container.'),
 'on-tertiary-container': ('#151f00', '#151f00', 'Label and play icon on tertiary-container (the Run button): deep olive, 13.4 : 1 on lime in both themes.'),
 'ai': ('#004f50', '#80d5d4', 'AI-powered features, Material tones: deep teal in light (tone 30, 8.9 : 1), light teal in dark. AI marks drawn as lines or dots (working dots, pen orbit, guide track, sparkle icon). Fills use ai-container. Never chrome, navigation or non-AI buttons.'),
 'on-ai': ('#ffffff', '#003737', 'Text on ai.'),
 'success': ('#0b5314', '#91d888', 'Healthy / passing (tone 30 in light). Status dots, INFO log level. Status is never told by colour alone: success chips carry the check glyph and a word.'),
 'warning': ('#5c4300', '#fcbc00', 'Degraded / attention (tone 30 in light). WARN log level. Always with a glyph and a word.'),
}
BRAND_USAGE = {
 'logo-box': 'Brand token (logo family, not a UI role): the toolbox box and handle of the mark, the favicon and app-icon tiles, the brand loader and the state marks. Night #0D0B14 on light backgrounds, lavender on dark.',
 'on-logo-box': 'Brand token: the > chevron of the prompt on logo-box.',
 'logo-cursor': 'Brand token: the cursor of the prompt on logo-box, full neon on the night box, emerald on the lavender box. The neon is used nowhere else.',
 'logo-ai': 'Brand token: the AI badge of the mark and the teal of the brand loader, the light teal #80D5D4 in both themes.',
 'on-logo-ai': 'Brand token: the “AI” letters on logo-ai.',
}
toks = []
for k in t['color']['tokens']:
    n = k['name']
    if n in REMOVED or n in BRAND: continue
    if n in NEW:
        l, d, u = NEW[n]
        k = dict(k, value={'light': l, 'dark': d}, usage=u or k['usage'])
    toks.append(k)
for n in BRAND:
    toks.append(dict(old[n], usage=BRAND_USAGE[n]))
toks.append({'name': 'logo-ai', 'value': {'light': '#80d5d4', 'dark': '#80d5d4'}, 'usage': BRAND_USAGE['logo-ai']})
toks.append({'name': 'on-logo-ai', 'value': {'light': '#003737', 'dark': '#003737'}, 'usage': BRAND_USAGE['on-logo-ai']})
t['color']['tokens'] = toks
t['version'] = '5.0.0'
t['meta']['scheme'] = ('Palettes from the three Sweep colours (v5.0, colour review option C): primary from the Sweep purple #39235F (hue 303), '
  'secondary from the pale purple #DED7EB (hue 296, the hue of the night neutrals), tertiary from the lime #DCEAB4 (hue 125); neutrals from #0D0B14 (hue 296). '
  'One tone rule: light roles at tone 30 (primary at 20, the Sweep purple itself), dark roles at 80, containers 90 / 30, text on containers 10 / 90. '
  'Kept from 4.x: the whole dark primary family on the lavender #C4C0FF (hue 288), the light primary-container #E3DFFF, the error family, the neutrals and nav-container. '
  'Pinned: tertiary-container is the lime in both themes, so the Run button stays lime in dark. Shape ceiling 16 px. '
  'History: v4.2–4.5 tuned the light surfaces, containers and the navigation band; v4.6 moved Run to the Sweep lime; v4.7 moved the light primary to #39235F. '
  'v5.0 removes run, on-run, run-icon, run-outline, run-text (Run = tertiary-container), nav-active (= secondary-container), focus-ring (= primary), ai-strong (= ai) and the legacy surface-variant; '
  'logo-box, on-logo-box, logo-cursor, logo-ai and on-logo-ai form the brand group (logo only).')
json.dump(t, open(R + 'tokens.json', 'w'), indent=2, ensure_ascii=False)
print(len(toks), 'colour tokens')

# ---- tokens.css: rewrite colour lines in the light and dark blocks
css = open(R + 'tokens.css').read().split('\n')
css[0] = css[0].replace('4.7.0', '5.0.0')
names = [k['name'] for k in toks]
val = {k['name']: k['value'] for k in toks}
use = {k['name']: k['usage'] for k in toks}
out = []; block = None; inserted = False
for ln in css:
    if ln.startswith(':root, [data-theme="light"]'): block = 'light'
    elif ln.startswith('[data-theme="dark"]'): block = 'dark'
    elif ln.startswith('}'):
        if block in ('light', 'dark'):
            ex = ['logo-ai', 'on-logo-ai']
            for n in ex:
                out.append(f'  --{n}: {val[n][block]};' + (f' /* {use[n]} */' if block == 'light' else ''))
        block = None
    m = re.match(r'  --([a-z0-9-]+): ', ln)
    if block in ('light', 'dark') and m and (m.group(1) in val or m.group(1) in REMOVED):
        n = m.group(1)
        if n in REMOVED: continue
        out.append(f'  --{n}: {val[n][block]};' + (f' /* {use[n]} */' if block == 'light' else ''))
        continue
    out.append(ln)
out.append('/* Deprecated aliases from 4.x, kept for migration only: remove in 5.1. */')
out.append(':root { --run: var(--tertiary-container); --on-run: var(--on-tertiary-container); --run-icon: var(--on-tertiary-container); --run-outline: transparent; --run-text: var(--primary); --nav-active: var(--secondary-container); --focus-ring: var(--primary); --ai-strong: var(--ai); --surface-variant: var(--surface-container-highest); }')
open(R + 'tokens.css', 'w').write('\n'.join(out))
print('css lines', len(out))
