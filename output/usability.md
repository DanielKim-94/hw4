# Problem 9 — Usability improvements

## 1. Product filtering and price sorting

The Products page now filters by the real `catalogue.garment_type` values and sorts by price low-to-high or high-to-low. This helps shoppers narrow a large catalogue and compare prices without introducing attributes that are not in the database.

## 2. Chat waiting state

Chat submission is guarded by `chatBusy`, disables the send control while a request is running, and changes the visible message to “Checking the collection…”. This reduces duplicate submissions and gives shoppers immediate feedback while the agent works. This is an additional accessible/explicit treatment of the existing request guard.

## 3. Typo and similar-term search

Catalogue search normalizes common apparel terms such as “hoodies” and “sweatshirts” to the database’s related hoodie terminology, while preserving database-backed matches. A search for `hoodies` returns real hoodie records from the catalogue.

## 4. Database-backed alternatives

The registered `alternatives_for_unavailable` tool compares real catalogue records by `garment_type`, shared colors, and shared search tags. It returns each alternative with a factual reason such as “same garment type” or “shared colors or search tags.” Unknown products return `unknown_product`; no alternative is invented.

## Verification

- Schema inspection confirmed filtering uses only `garment_type` and sorting uses `price`; inventory remains size/quantity data.
- `search_catalogue("hoodies")` returned 8 real matches.
- `alternative_products("Basic Hoodie Big Yale")` returned real alternatives with reasons.
- `alternative_products("not-real")` returned `unknown_product`.
- The frontend production build was run from `HW 4` successfully.
