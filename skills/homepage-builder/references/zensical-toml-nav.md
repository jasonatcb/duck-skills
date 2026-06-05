# Registering a Custom Homepage in zensical.toml

To activate a custom homepage template, you need:

## 1. Frontmatter in the Markdown file

The page's markdown file (e.g., `docs/ec/index.md`) must specify the custom template:

```yaml
---
title: 品牌官網
template: homepage_ec.html
---
```

## 2. Nav entry in zensical.toml

The nav entry points to the markdown file normally — Zensical reads the `template` field from the page's frontmatter at render time:

```toml
 nav = [ 
    { "主頁" = "index.md" },
    { "品牌官網" = [
        { "品牌官網" = "ec/index.md" },
        ...
    ]},
]
```

The `template` field in frontmatter automatically overrides which template Zensical uses to render that page.
