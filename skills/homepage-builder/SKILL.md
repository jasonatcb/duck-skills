---
name: homepage-builder
description: >-
  Create or refactor custom Zensical homepage templates (`homepage_xxx.html`) that extend `main.html` and fully override the content block with a custom landing page layout. Use this whenever the user mentions creating a new homepage variant, a custom landing page, a dashboard-style page, or a page that needs to replace the default MkDocs content with a hero + cards + bento layout. Also trigger when the user provides raw HTML/CSS/JS that needs to be wrapped in the proper Jinja2 block structure for Zensical, or when they want to extract/refactor an existing homepage into a reusable pattern. This skill is NOT for editing content within MkDocs markdown pages — it's specifically for custom full-page overrides in `overrides/`.
version: 1.0.0
last_updated: 2026-05-31
---

# Homepage Builder: Zensical Custom Templates

## Why This Architecture Exists

The Zensical homepage (`index.md`) uses a custom template (`homepage_ec.html`) that completely replaces the default MkDocs content area. This is different from a regular documentation page — there's no table of contents, no breadcrumbs, no "last updated" footer. Instead, the full page is a branded landing experience.

The key insight: **we extend `main.html`, not `base.html`**. `main.html` is our project's override that layers on SEO metadata (OG tags, Schema.org JSON-LD, Twitter cards) and the SPA router bypass script. Extending `base.html` directly would lose all of this.

## File Locations

| What | Where |
|------|-------|
| Custom templates | `overrides/homepage_xxx.html` |
| Base override | `overrides/main.html` (extends `base.html`, adds SEO + SPA bypass) |
| Config | `zensical.toml` (site-wide settings, nav) |
| Activate template | `docs/index.md` frontmatter: `template: homepage_xxx.html` |

## Jinja2 Block Contract

These are the only blocks you should touch. Never override `{% block scripts %}`.

```jinja2
{% extends "main.html" %}

{% block extrahead %}
  {{ super() }}
  {# Material Symbols font + ALL CSS go here #}
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet">
  <style>
    /* ALL CSS in one <style> block inside extrahead */
  </style>
{% endblock %}

{% block content %}
  {# ALL page HTML + inline JS go here #}
  {# NO {{ super() }} — we fully replace the content area #}
{% endblock %}
```

### Rules
1. `{% block extrahead %}` — MUST call `{{ super() }}` first. This preserves SEO tags from `main.html`.
2. `{% block content %}` — MUST NOT call `{{ super() }}`. We want a blank slate for the full-page layout.
3. `{% block scripts %}` — MUST NOT be overridden. This inherits the SPA bypass script from `main.html`.

## CSS Architecture

### Material Design 3 Token System
Define all colors as CSS custom properties in `:root` inside the `<style>` block. Use the naming convention from Material Design 3:

```css
:root {
  --primary: #003d9b;
  --on-primary: #ffffff;
  --primary-container: #0052cc;
  --secondary: #006e2f;
  --surface: #f7f9fb;
  --surface-container-low: #f2f4f6;
  --surface-container-lowest: #ffffff;
  --on-surface: #191c1e;
  --on-surface-variant: #434654;
  --outline: #737685;
  --outline-variant: #c3c6d6;
  --mx: 1280px;       /* max-width for content */
  --px: 32px;         /* horizontal padding */
}
```

The exact hue values matter less than the pattern — use colors appropriate for the brand/section the homepage is targeting.

### Spacing System
```css
.ec-sect {
  padding-left: var(--px);
  padding-right: var(--px);
}
.ec-sect + .ec-sect { margin-top: 64px; }
.mt-16 { margin-top: 64px; }
.mb-16 { margin-bottom: 64px; }
```

Every section uses the `ec-sect` class. Vertical rhythm is handled by the sibling selector (no manual margins on individual sections). The `.mt-16`/`.mb-16` utilities are for exceptions.

### Zero-Invention Principle
**Before creating new class names, check if an equivalent already exists in `homepage_ec.html`.** If a section has the same visual structure (hero, card grid, resource list), reuse the exact same classes. Only invent new classes for genuinely new visual structures.

For example, `homepage_resources.html` reuses `.ec-hero`, `.ec-card`, `.ec-grid-4`, `.ec-section-hd`, `.ec-resources`, `.ec-res-grid`, `.ec-res-item` from the EC page — no new classes needed for those. The highlight section was genuinely new, so `.ec-highlight` was created.

### Section Naming Convention
Use the `ec-` prefix for ALL custom classes to avoid colliding with MkDocs/Material classes:
- `.ec-hero` — hero banner (solid `var(--primary-container)` bg — keep consistent across pages)
- `.ec-card` — feature/info cards
- `.ec-card.large` — card that spans 2 columns in the grid (`grid-column: span 2` at 768+)
- `.ec-grid-4` — 4-column responsive card grid
- `.ec-bento` / `.ec-bento-main` / `.ec-bento-side` — two-column bento layout
- `.ec-bento-slide` / `.ec-bento-content` / `.ec-bento-img` — carousel slide components
- `.ec-section-hd` — section header with title + link
- `.ec-resources` / `.ec-res-grid` / `.ec-res-item` — resource link section
- `.ec-res-divider` / `.ec-res-border` — mobile divider / desktop border for resource items
- `.ec-testimonial` / `.ec-support` — sidebar panels
- `.ec-highlight` — dark-background featured highlight section (白皮書 style, uses `#001848` in light mode, `var(--primary-container)` in dark mode)

### New Section: Highlight
For a featured content section with a dark background, book mockup, and CTAs:

```css
.ec-highlight {
  border-radius: 0.75rem;
  overflow: hidden;
  background: #001848;
  padding: 48px;
  display: flex;
  flex-direction: column;
  gap: 48px;
}
@media (min-width: 768px) {
  .ec-highlight {
    flex-direction: row;
    align-items: center;
  }
}
.ec-highlight-content { flex: 1; color: #fff; }
.ec-highlight-badge { /* green pill badge */ }
.ec-highlight-content h2 { /* 32px bold heading */ }
.ec-highlight-content p { /* 18px with primary-fixed-dim color */ }
.ec-highlight-actions { /* flex, gap 16px */ }
.ec-highlight-actions .btn-primary { /* primary-container bg, white text */ }
.ec-highlight-actions .btn-outline { /* transparent bg, white border */ }
.ec-highlight-image { flex: 1; max-width: 400px; }
.ec-highlight-mockup { /* 3:4 aspect ratio, rotate 3deg, unrotate on hover */ }
```

In dark mode, override the background:
```css
[data-md-color-scheme="slate"] .ec-highlight {
  background: var(--primary-container);
}
[data-md-color-scheme="slate"] .ec-highlight-actions .btn-primary {
  background: var(--primary);
}
```

### Responsive Breakpoints
Always use these two breakpoints consistently:

```css
/* Mobile-first: single column by default */

@media (min-width: 768px) {
  /* Tablet+: 2-column grids, horizontal layouts */
}

@media (min-width: 1024px) {
  /* Desktop: 4-column grids, bento side-by-side */
}
```

### Mobile Navigation Requirement

When the top nav is hidden below `lg` (`display: none` at < 1024px), you **must** provide a hamburger menu (`lg:hidden` button) that toggles a slide-down dropdown containing all nav links. Pattern:

- Hamburger button placed in the header's right-side container, visible only below `lg`
- Toggle script swaps `menu` / `close` icon and toggles a `hidden` class on the nav panel
- Mobile nav panel sits between `</header>` and `<main>` in the DOM so it pushes content down naturally
- Current page link gets a distinct background (`bg-surface-container`) to indicate active state
- All links preserve exact `href` from the desktop nav

See `homepage.html` for the reference implementation.

### Touch Targets

All interactive elements (links, buttons, cards) must have a minimum touch target of 44×44px on mobile. This is especially important for:
- Nav items in the mobile dropdown
- FAQ / tag pill buttons
- Carousel dot indicators
- "查看更多" / CTA links

### Horizontal Overflow

Every homepage must include this guard to prevent content from breaking out on narrow viewports:
```css
img, video, iframe { max-width: 100%; height: auto; }
.ec-sect { overflow-x: hidden; }
```

### Card Pattern
Cards should follow this structure:
```css
.ec-card {
  background: var(--surface-container-lowest);
  padding: 24px;
  border-radius: 0.75rem;
  border: 1px solid var(--outline-variant);
  transition: all 0.3s ease;
  cursor: pointer;
}
.ec-card:hover {
  box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
  border-color: var(--primary);
  transform: translateY(-8px);
}
.ec-card-icon {
  width: 48px; height: 48px;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  transition: transform 0.3s ease;
}
.ec-card:hover .ec-card-icon {
  transform: scale(1.1);
}
```

Use `color-mix()` for icon background tints:
```css
.ec-card-icon {
  background: color-mix(in srgb, var(--primary) 10%, transparent);
  color: var(--primary);
}
```

## Dark Mode

Zensical uses `[data-md-color-scheme="slate"]` for dark mode. Always include this block at the end of your `<style>`:

```css
[data-md-color-scheme="slate"] {
  --on-surface: #e3e3e3;
  --on-surface-variant: #b0b0b0;
  --surface-container-lowest: #1e1e1e;
  --surface-container-low: #2a2a2a;
  --outline-variant: #3e3e3e;
  --primary: #a6c1ff;
  --primary-container: #0040a2;
}
/* Elements that use --primary as a background with white text need a dark-mode fallback */
[data-md-color-scheme="slate"] .ec-support {
  background: #0040a2;
}
```

This overrides the page-scoped `:root` variables so text, backgrounds, and accent colors all invert properly. Every new homepage must include a dark mode strategy — never leave hardcoded `#fff` backgrounds that would be invisible in dark mode.

## JavaScript Patterns

If your page includes interactive elements (carousels, accordions, etc.), use an IIFE (Immediately Invoked Function Expression) at the bottom of `{% block content %}`:

```html
<script>
  (function() {
    /* all JS here, no globals leaked */
  })();
</script>
```

### Carousel pattern (copy from homepage_ec.html reference)
If you need a slide-based carousel:
1. Track container with `display: flex; transition: transform 0.5s ease`
2. Slides at `flex: 0 0 100%`
3. Dots as nav with `data-index` attributes
4. Auto-rotate via `setInterval(5000)` with pause-on-hover
5. Timer resets on manual dot click

## SPA Router Bypass

The `main.html` base override includes a `bypassSpaRouter` script that forces full-page reloads when clicking the logo ("主頁" link or `.md-logo` class). You MUST NOT override `{% block scripts %}` — this ensures the bypass is inherited automatically.

## Workflow: Creating a New Homepage

1. **Read the reference** — First read `references/homepage_ec.html` to understand the full pattern before writing anything
2. **Understand the sections** — Ask the user what sections/content they want (hero, card grid, bento layout, resource links, call-to-action panels, etc.)
3. **Draft the file** — Create `overrides/homepage_xxx.html` following the block contract above
4. **Apply the CSS architecture** — Theme colors → spacing → responsive → dark mode
5. **Verify the checklist:**
   - [ ] Extends `main.html`, not `base.html`
   - [ ] `extrahead` calls `{{ super() }}`
   - [ ] `content` does NOT call `{{ super() }}`
   - [ ] `scripts` is NOT overridden
   - [ ] No hardcoded `#fff` backgrounds (use `var(--surface-container-lowest)`)
   - [ ] Dark mode override block present (`[data-md-color-scheme="slate"]`)
   - [ ] Responsive breakpoints at 768px and 1024px
   - [ ] Mobile nav hamburger menu provided for screens < 1024px
   - [ ] Touch targets meet 44×44px minimum
   - [ ] Horizontal overflow guard in place
   - [ ] All custom classes use `ec-` prefix
   - [ ] Section spacing uses `.ec-sect + .ec-sect`
   - [ ] Buttons that need `position: relative; z-index` use a value < 2 (below the header z-index)
   - [ ] Material Symbols font loaded in `extrahead`
   - [ ] User can navigate to this page via nav (register in `zensical.toml`)

## Registration

To make the new homepage active:
1. The page's markdown file (e.g., `docs/resources/index.md`) must have frontmatter:
   ```yaml
   ---
   template: homepage_resources.html
   ---
   ```
2. The nav entry in `zensical.toml` should point to that markdown file normally.

## Common Pitfalls

- **Invented new CSS classes for existing UI patterns** → first version of `homepage_resources.html` created `.ec-rhero`, `.ec-rcard`, `.ec-rgrid`, `.ec-rext` instead of reusing `.ec-hero`, `.ec-card`, `.ec-grid-4`, `.ec-resources`. Always refactor to reuse before creating new.
- **Inconsistent hero background color across pages** → EC uses solid `var(--primary-container)`; don't use a gradient unless there's a brand reason. Keep hero backgrounds consistent across all homepage variants.
- **Added unused `:root` variables** → only define CSS vars that are actually referenced in the template's CSS or content.
- **Forgot `{{ super() }}` in extrahead** → loses OG tags, JSON-LD, Twitter cards
- **Added `{{ super() }}` in content** → renders the default page content above the custom layout
- **Extended `base.html` instead of `main.html`** → loses the SPA bypass and SEO
- **Hardcoded `#fff`** → invisible text/backgrounds in dark mode
- **`z-index` >= 2** on hero content → steals clicks from the sticky header (dark mode toggle, search)
- **Forgot responsive breakpoints** → layout breaks on mobile
