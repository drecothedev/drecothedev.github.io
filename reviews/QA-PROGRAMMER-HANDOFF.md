# QA review and Programmer handoff

Reviewed November 2, 2026. Scope: canonical Flask app in `submission/ActivityWebserver`, project2 templates and cursor script, build/export scripts, generated static preview, and Milestone 2 submission ZIP. The duplicate `ActivityWebserver 2` is documented as an older copy and was not treated as canonical.

## Findings

### P1 — Legacy build script overwrites working templates with incompatible versions

Location: `scripts/build_milestone2.py:20–50` and its subsequent template writes.

Running this script returns success but replaces the current project2 templates with older monetary templates. Those templates use the `money` filter, which the current app does not register, and fields such as `product.price` that the current data does not provide. It also removes the current shared script inclusion and Current Project navigation.

Reproduction, performed only in a temporary copy: run `python3 scripts/build_milestone2.py`, then request `/project2/products` with Flask testing enabled. Result: `TemplateAssertionError: No filter named 'money'.` In normal operation this becomes a server error. The checked-in app currently works; the failure is triggered by running the obsolete generator.

Recommended resolution: retire this one-time generator explicitly, or update it to preserve the current canonical implementation. It must not silently overwrite current source with an incompatible historical version. Preserve the authorized time estimates, Current Project page, responsive images, and spotlight.

### P2 — Static exporter cannot recreate missing output folders

Location: `scripts/export_milestone2_preview.py:10,41,45`.

The exporter writes HTML and copies assets without creating `portfolio/dist` or `portfolio/dist/assets`. In an isolated copy without generated output, the documented export command exits 1 with `FileNotFoundError` for `portfolio/dist/index.html`. A developer who deletes generated files to rebuild cannot regenerate them successfully.

Recommended resolution: create both output directories with parents before writing. Add an isolated regression check that starts without output folders, exports successfully, and verifies the generated local links and responsive image candidates.

## Verification performed

- `python3 scripts/verify_milestone2.py`: PASS. Covers 14 application routes, project2 local links/assets, six products, category filtering, shared markup, script inclusion, cart totals, invalid quantities, and a simulated NetID prefix.
- Parsed generated preview HTML: all local `href`, `src`, and `action` file paths checked resolve to existing files. This check did not validate external URLs or fragment targets.
- Compared all non-hidden source files outside `__pycache__` against `ActivityWebserver-Milestone2.zip`: no missing or differing files.
- Reproduced both findings in a temporary copy; canonical application code and generated outputs were not changed.

No fresh browser visual, keyboard, screen reader, or JavaScript runtime testing was performed. School-server deployment and the four required external browsers remain unverified in this review. Prior documentation of browser checks is not new QA evidence. Mock Add/Remove/Start controls and the shared GEMMA detail page are documented behavior, not defects. The authorized replacement of monetary fields with time estimates was preserved as the current requirement.

## Ready-to-paste prompt for the Programmer agent

You are the Programmer for this project. Resolve the two reproduced QA findings in `reviews/QA-PROGRAMMER-HANDOFF.md`.

Work in the canonical Flask app at `submission/ActivityWebserver`. Preserve Milestone 1, the authorized time-based exploration plan, Current Project page, responsive images, cursor spotlight, and documented mock controls. Do not edit `portfolio/dist` by hand or modify the old `ActivityWebserver 2` copy.

1. Make `scripts/build_milestone2.py` safe. Retire the obsolete one-time generator with an explicit explanation and no source writes, or make its output compatible with the current app. Its current successful execution followed by `/project2/products` produces `TemplateAssertionError: No filter named 'money'` because it overwrites current templates with obsolete monetary templates. Do not restore monetary fields to solve this.
2. Make `scripts/export_milestone2_preview.py` create `portfolio/dist` and `portfolio/dist/assets` before writing, so the documented export works after generated output is removed.
3. Add focused regression checks in isolated temporary copies. Verify that the legacy generator cannot silently damage the working app, and that exporting from absent output directories succeeds with valid generated local assets, including `srcset` candidates.
4. Run `python3 scripts/verify_milestone2.py` and the new regression checks. If a maintained generator is retained, verify its resulting routes and current features. If it is retired, verify that invoking it leaves source files unchanged.
5. Regenerate the preview if its inputs change. If submission source changes, refresh the Milestone 2 ZIP and confirm its contents match the canonical source. Report the exact changes, commands run, outcomes, and remaining browser/deployment checks in plain English.

Acceptance: no destructive legacy regeneration; clean static export succeeds; current route/cart checks pass; regression checks pass; generated artifacts match any changed source. Do not claim browser or school deployment validation without performing it.

## Programmer resolution

Both findings are resolved:

- P1: `scripts/build_milestone2.py` is now an explicit retirement guard. It exits nonzero with an explanation and points to the canonical Flask source, exporter, and verifier. It contains no file-writing or scaffolding code.
- P2: `scripts/export_milestone2_preview.py` creates `portfolio/dist` and its `assets` folder with `parents=True, exist_ok=True` before writing outputs.
- Added `scripts/test_build_workflows.py`. Each test uses a temporary project copy. One compares source hashes before and after invoking the retired generator, then checks that the app still works. The other begins without any output directory, checks all eight generated pages and local `href`/`src`/`action` paths plus every `srcset` candidate, confirms source was not changed, and verifies a repeat export produces identical output.
- Documented the supported workflow and retirement in `portfolio/README.md`.

Commands and results:

```text
python3 scripts/verify_milestone2.py
PASS: routes, assets, current features, categories, time calculations, invalid quantities, NetID prefix.

python3 scripts/test_build_workflows.py
PASS: 2 isolated regression tests.

python3 scripts/export_milestone2_preview.py
PASS: preview regenerated from canonical source.
```

An additional ZIP comparison confirmed that all 64 archived files exactly match the canonical application, with no extra or missing files. Submission source was unchanged, so the current ZIP was retained. User edits to homepage and Swim copy remain intact. Milestone 1 and the older `ActivityWebserver 2` copy were not modified.

No new browser visual, keyboard, screen-reader, JavaScript runtime, school-server, or four-browser validation was performed in this fix. No hosted deployment or GitHub push was performed. Existing mock controls and the authorized time-based exploration plan remain unchanged.
