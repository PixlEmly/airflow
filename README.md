# exhaust enclosure — review package

**Status: discussion concept, 8 November 2026. Not a fabrication or validated acoustic/airflow design.**

This project investigates an enclosed, bottom-discharge sound baffle box along the dyno-room exterior wall, constrained by an existing tree and soffit. Option 4 is the provisional selection. Three alternating half-depth baffles and a one-inch interior lining allowance are modeled. A separate six-inch roof silencer route is included.

## Start here

1. Read [design brief](docs/DESIGN-BRIEF.md) and [airflow/acoustic assessment](docs/AIRFLOW-AND-ACOUSTICS.md).
2. Open [current Blender model](models/XLR8-all-options-toggle.blend), authored using Blender 5.1.1. Option 4 is visible; options 1, 2, 3 and 5 remain hidden. This is the authoritative editable model.
3. For a portable mesh preview, use [Option 4 GLB](models/option-4-lined-review.glb). It contains the visible concept only; option toggles and source scan collections require Blender.
4. See [lined cutaway](drawings/option-4-lined-baffles-cutaway.png), [current exterior](drawings/current-exterior.png), and [dimensioned section schematic](drawings/option-4-section.svg). Cutaways hide the outer wall for explanation; the actual enclosure face is closed.
5. Read [agent handoff and conversation history](docs/CHAT-HANDOFF.md), [review plan](docs/REVIEW-PLAN.md), and root [AGENTS.md](AGENTS.md) before changing the model.

## Contents

| Folder | Purpose |
|---|---|
| models | Current editable scene and portable Option 4 export |
| drawings | Current review images and a vector section schematic |
| calculations | Current lining dimensions and machine-readable screening calculations |
| references | Both wall/tree scans with textures, roof scan/fragments, registration data, user sketches and product reference images |
| docs | Requirements, provenance, design decisions, review questions and handoff |
| tools | Portable export, calculation and package-validation scripts |
| history | Superseded exterior studies, pre-lining calculations and original one-off scripts |

Original scripts are archival provenance, NOT a supported one-command rebuild pipeline. Many require earlier intermediate models and paths not included here; use the current model as the starting point. Do not run historical generators over the current model.

## Verification and limitations

The current model is packaged with textures; see `models/model-audit.json` for resource and visibility checks. `MANIFEST.json` records SHA-256 hashes and sizes. `python tools/calculate_airflow.py` regenerates the screening tables; `python tools/validate_package.py` checks the manifest and required deliverables. Blender exports can be refreshed with `blender -b --python tools/export_review.py`.

No measured fan static pressure, verified fan curve, noise spectrum, required attenuation, final lining product, structural design, thermal review or surveyed clearance is supplied. The 9,900 CFM allowance is a user-provided conservative total, not a measured flow. References and images are included for project review; no blanket redistribution license is asserted for third-party materials.

This package was assembled locally. It has not been pushed to GitHub. Repository remote: https://github.com/PixlEmly/airflow
