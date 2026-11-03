# Milestone 2 submission review

Implemented November 2, 2026 against the supplied Milestone 2 specification. Personal programming projects serve as the product collection. Per Andre’s requested revision, prices are replaced with estimated code-exploration minutes. Estimates describe an initial code tour, not a full code review; they vary by reader.

## Required routes and files

| Route | Template | Result |
| --- | --- | --- |
| `/project2` | `templates/project2/index.html` | Independent copy of the Milestone 1 homepage, restyled in monochrome glass |
| `/project2/products` | `templates/project2/products.html` | Six projects, category navigation, pictures, names, estimated exploration times, detail links |
| `/project2/details` | `templates/project2/details.html` | GEMMA detail page (legacy URL), image, description, exploration estimate, Add to exploration list, platform, language, backend, voice workflow |
| `/project2/cart` | `templates/project2/cart.html` | Two items, images, minutes per session, session counts, Update/Remove, row times, total exploration time, Start exploring |

The existing `/project` homepage and its stylesheet/assets remain unchanged. The activity landing page now links to both milestones. The duplicate `ActivityWebserver 2` folder was left unchanged; use the canonical `submission/ActivityWebserver` folder and the Milestone 2 ZIP.

## Structure and behavior

- Shared `base.html`, `header.html`, and `footer.html` maintain consistent navigation and footer across all four Milestone 2 pages.
- One stylesheet: `static/css/project2/styles.css`. Images and resume are independently copied to `static/img/project2` and `static/files/project2`.
- All local assets use Flask `url_for`; navigation also uses `url_for`. A simulated `/~sampleid` URL prefix passes.
- Catalog uses CSS Grid, with three cards per desktop row and one card per mobile row. No layout tables.
- Per Andre’s subsequent request, catalog and cart cards now link to project-specific detail pages. The original shared GEMMA mock-up has been replaced while its legacy URL remains valid.
- Quantities submit a GET form to Flask. `app.py` computes integer row minutes and total exploration time and passes template variables to `cart.html`. Core navigation and calculations do not require JavaScript.
- Add, Remove, and Start exploring intentionally do nothing, as appropriate for mock-ups. No purchases, payments, authentication, or cart persistence are implemented.
- Default exploration plan: GEMMA 30 min + Jess 45 min = 75 min.
- Two GEMMA sessions and one Jess session: 60 + 45 = 105 min.
- Quantities must be whole numbers from 1 to 99; invalid input resets to 1 and displays an error.
- Monochrome original project artwork is used for projects without provided screenshots; GEMMA and Sxmpler retain actual screenshots with a grayscale CSS treatment.
- Glass effects use CSS gradients, translucent fills, shadows, borders, and backdrop blur. Reduced-motion and reduced-transparency alternatives are included.

## Verification

`python3 scripts/verify_milestone2.py` checks all course routes, local links/assets, product/category counts, shared layouts, one deferred spotlight script and no inline event handlers, cart calculations, invalid quantities, and deployment URL prefixes.

Browser QA: desktop 1440px and mobile 390px. Confirmed three-column desktop and one-column mobile catalog, all six images loaded, working quantity form, no horizontal overflow on catalog, details, and cart. Homepage was also visually reviewed.

Brave, Firefox, Chrome, and Edge were not individually tested. School deployment is not completed or verified.

## Run and submit

1. Use `submission/ActivityWebserver` as the complete app folder. From there, run `python3 -m flask --app app run` (install `requirements.txt` in your normal course environment if needed).
2. Visit `/project2` and verify the pages in the four required browsers.
3. Upload `ActivityWebserver-Milestone2.zip` at https://cob-flaskweb.unr.edu.
4. Confirm `https://cob-flaskweb.unr.edu/~yourNetID/project2`, its navigation, images, and cart quantity updates.

The private Sites URL is a static visual preview. Its catalog category links work via pre-rendered pages; its cart controls display sample values. Use the Flask ZIP for the actual course submission and quantity recalculation.

## Requested time-based revision

GEMMA: 30 min; Jess: 45 min; Sxmpler: 20 min; Swift Is My Life: 15 min; Worder: 10 min; Yen to USD: 5 min. These are editorial estimates, not measured completion times. Catalog, shared details page, and cart now use minutes throughout. Tax, shipping, and monetary totals were removed. This is a deliberate portfolio adaptation requested by Andre; the original course PDF specified prices, tax, and shipping, so this version does not literally implement those monetary fields.

## Current Project page

Added `/project2/current-project` with `templates/project2/current.html` for Swim. Shared navigation includes Current Project on every Milestone 2 page. Swim is marked in development; the description is based on Andre’s supplied explanation; no repository URL has been assumed. The page uses cyan, violet, and rose CSS glows over the existing dark glass theme. Desktop 1440px and mobile 390px were visually checked without horizontal overflow. The cursor spotlight now uses a deferred external JavaScript file, as authorized by Andre. Static preview path: `current-project.html`.

## Authorized JavaScript enhancement

Andre approved JavaScript moving forward. Every Milestone 2 page now includes `static/js/project2/spotlight.js` via `url_for` with `defer`. The small decorative glow tracks the mouse; regular pages use white and Current Project uses its cyan/violet/rose palette. Pointer events pass through it. Touch and reduced-motion preferences disable it. Pointer leave, browser blur, hidden documents, and Tab navigation hide it. Browser checks verified pointer tracking and both color variants; script checks covered batching, exit, touch, and preference changes.

## Performance pass

- Replaced oversized JPEG screenshots with 180px, 360px, and 720px monochrome WebP variants. All six variants total 36,334 bytes, versus 335,930 bytes for the two old JPEGs (89.2% smaller). M1 originals are preserved.
- Responsive `srcset`/`sizes`, explicit image dimensions, asynchronous decoding, and lazy loading below the fold reduce unnecessary downloads and layout movement. The details screenshot is prioritized.
- Removed redundant grayscale GPU filters and backdrop blur on static glass panels, while retaining gradients, borders, highlights, and header glass. The moving spotlight no longer needs a blur filter.
- Mouse listeners are registered only for eligible devices. Pointer movement remains batched to one paint per animation frame, without a continuous JavaScript loop.
- Decorative animation pauses offscreen and in hidden tabs, and is static on smaller screens.
- Static export removes HTML comments and redundant whitespace outside preformatted code.
- Complete static files measured 722,564 → 418,118 bytes, including the unchanged resume PDF: a 42.1% file-size reduction. This is not a network-speed or Core Web Vitals benchmark.
- Route, asset, responsive-image, and cart-calculation verification passed; browser review confirmed the optimized screenshot and cursor effect. No runtime framework, external fonts, or new runtime dependencies were added.

To regenerate images, run `scripts/optimize_project_images.py` with the bundled Pillow-enabled Python runtime. Flask itself does not need Pillow. Then run `python3 scripts/export_milestone2_preview.py` to refresh the hosted files.

## School-server startup compatibility

Milestone 2 routes and project data now live directly in `app.py`. Startup no longer relies on importing a sibling `project2.py` file. Local checks pass for normal app imports, package-style imports, and importing `app.py` by absolute path from an unrelated working directory. This removes a potential import-path failure, but the truncated school-server log did not include its final exception, so the original server failure is not yet confirmed.

## Project navigation improvement

Each of the six projects now opens its matching detail page. A shared data-driven template supplies the name, description, image, exploration minutes, technical information, code-tour suggestions, and correct GitHub repository. Unknown IDs return 404. Static exports include five additional detail HTML files. Route and isolated-export tests verify all six destinations. Browser checks confirmed the Jess card opens Jess and the long Swift Is My Life title fits at 1440px and 390px. School-server deployment and the four external browsers remain unverified.
