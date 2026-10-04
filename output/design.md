# Problem 10 — Storefront design

## Visual changes

- Added a restrained Yale-inspired palette using deep Yale blue, lighter blue-gray surfaces, warm gold for the chat accent and focus indicator, and a paper-colored background. This makes the storefront feel coherent while keeping product imagery dominant.
- Refined navigation with a sticky translucent bar, clearer brand lockup, and stronger primary-account action. Shoppers keep their place while browsing without losing the main navigation.
- Improved product cards with quieter borders, clearer text spacing, subtle lift on hover, and restrained shadows. Product names, descriptions, and prices are easier to scan without decorative effects competing with the products.
- Refined product detail presentation with an offset image surface, stronger information spacing, and a full-width action area. The large image and factual product data remain the focus.
- Improved filters, forms, and chat surfaces with consistent borders, radii, colors, and spacing. The chat widget remains visually distinct but does not cover the product content unnecessarily.
- Added visible keyboard focus rings with high-contrast gold and support for `prefers-reduced-motion`. This makes navigation, filters, forms, and chat controls easier to use without a mouse.
- Added mobile refinements for compact navigation, two-column product browsing, filter wrapping, detail-page spacing, and chat width.

## Verification

The existing product-card links, detail routes, login/create-account forms, search/filter controls, and chat widget were preserved. The TypeScript/Vite production build succeeds after the styling layer is loaded from `src/design.css`.
