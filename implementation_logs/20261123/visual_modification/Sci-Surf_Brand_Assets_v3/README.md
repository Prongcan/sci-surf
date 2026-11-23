# Sci-Surf Brand Assets — v3 (production-oriented)

The 1938×601 transparent Sci-Surf wordmark is the **single master** for both themes.
Both logo files have the **exact same size, alpha channel, glyph outline, and visible arrangement**.
Dark mode is derived by recoloring only the black/neutral `SCI-` region to white;
`Surf` blue, the orange accent, the sweeping underline, and pixel positions are unchanged.

## Ready-to-copy directory

`frontend/public/` contains the exact Vite target tree, including two brand logos, `favicon.svg`, `.ico` and small PNGs. Copy its contents into your repository `frontend/public/`.

The full execution plan is in `Frontend_Branding_Migration_Plan_v3.md`.

## Assets to copy

| File | Target in Vite `frontend/public/` | Purpose |
| --- | --- | --- |
| `logo/sci-surf-logo-light.png` | `brand/sci-surf-logo-light.png` | Light header; transparent RGBA, 1938×601 |
| `logo/sci-surf-logo-dark.png` | `brand/sci-surf-logo-dark.png` | Dark header; transparent RGBA, 1938×601 |
| `favicon/favicon.svg` | `favicon.svg` | New vector browser favicon |
| `favicon/favicon.ico` | `favicon.ico` *(optional)* | Fallback for browsers needing ICO |
| `favicon/favicon-16x16.png` | `favicon-16x16.png` *(optional)* | 16px raster fallback |
| `favicon/favicon-32x32.png` | `favicon-32x32.png` *(optional)* | 32px raster fallback |

Additional 48/64/180/256px raster icons and previews are provided for verification / optional use.

## CSS usage

```tsx
<Link to="/" className="flex items-center" aria-label="Sci-Surf home">
  <img src="/brand/sci-surf-logo-light.png" alt="Sci-Surf"
       className="block h-10 w-auto object-contain md:h-11 dark:hidden" />
  <img src="/brand/sci-surf-logo-dark.png" alt="" aria-hidden="true"
       className="hidden h-10 w-auto object-contain md:h-11 dark:block" />
</Link>
```

Raster aspect ratio `1938 / 601 = 3.2246`, so `h-10` (40px) displays ~129px wide,
and `md:h-11` (44px) displays ~142px wide, as in the migration plan.
Do not force width and height separately. Keep Header height unchanged.

## Color tokens

- Primary: `#0A6FFF`
- Hover: **`#005DD9` only**
- Brand soft: `#E6F2FF`
- Orange accent: `#FF8A00`

## Browser favicon

Use the SVG path in `index.html` (existing Vite href usually works unchanged):

```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
```

The favicon has its own compact S/wave icon with a tightly cropped viewBox. It is a real SVG with paths,
not a PNG embedded inside an SVG. Its 16×16 and 32×32 renderings are included.

## QA proofs

See `previews/` for light/dark header mockups and actual favicon 16×16/32×32 inspection views.
The output has been programmatically checked for identical theme alpha masks,
correct raster mode, correct aspect ratio, and vector SVG syntax.

*Note: this package provides visual assets and guidance, not a code change in the repository.*
