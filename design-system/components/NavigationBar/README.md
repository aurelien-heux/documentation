# NavigationBar
Phone bottom navigation, 80 px, 3–5 destinations on `nav-container` (violet tint in light; `class="dt-nav"` on the `mat-toolbar`).
- Active destination: 64×32 px `secondary-container` pill behind the icon, label in `on-surface` at weight 600; inactive icons and labels in `on-surface-variant`.
- Destinations: Sweep · Envs · Docs · Community · Assistant (feature marks at 24 px, the Chatbot mark for Assistant), the rail's destinations plus the Assistant; Administration and Cookie policy are in the modal drawer from the top-bar menu, Settings in the avatar menu.
- Badges sit on the icon. On tablet and desktop the same destinations move to the NavigationRail.
- **Responsive:** Compact only (under 600 px): 3–5 destinations, the rest in the modal drawer opened from the top-bar menu. From 600 px the destinations move to the NavigationRail; a phone in landscape (height under 480 px) also takes the rail.
- **Keyboard and screen reader:** the active destination has `aria-current="page"` and a 3 px `primary` bar on top of its pill; labels always visible; it replaces the drawer at 320 CSS px and 200 % zoom.
- **Angular Material:** No Angular Material equivalent — a bottom `mat-toolbar` with `mat-button`s, or `mat-tab-nav-bar` with icons. The active pill is a class on `secondary-container` in both. Full map and theme files: `angular-material.md`.
