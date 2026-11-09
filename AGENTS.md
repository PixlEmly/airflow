# Agent instructions for this repository

Read README.md, docs/CHAT-HANDOFF.md, docs/DESIGN-BRIEF.md and docs/AIRFLOW-AND-ACOUSTICS.md before editing.

## Source of truth and scope

- Use the root [Option 4 acoustic and construction report](XLR8-option-4-acoustic-construction-review.pdf) as the current reference for acoustic estimates, construction details, the FRK cut sheet, and the BOM. Treat its framing and quantities as planning allowances.
- Use the root `option-4-dimensioned.pdf` as the supplemental dimension drawing. Both PDFs round drawing dimensions to the nearest ⅛ inch. Use Blender geometry and calculation files for exact values.

- `models/XLR8-all-options-toggle.blend` is authoritative. Work from this scene, not a historical generator.
- Preserve options 1–5 in the SAME scene; Option 4 is the default visible option. Options 6–8 were explicitly removed by the user and must not be silently reinstated. Historical illustrations remain clearly labeled.
- Shared building, both-scan tree envelope, vents, roof and six-inch silencer assembly stay in SHARED collections. Option-specific baffles and lining stay under Option 4.
- The enclosure is CLOSED on face and ends and open below. Baffles are internal, not exterior shelves. Top/bottom attach OUTSIDE; middle attaches BUILDING side. Do not reverse without a new user decision.
- Keep tree geometry derived from both scans. Do not replace with a narrower single-scan trunk, and do not interpret registration residual as absolute dimensional accuracy.
- Preserve the current 12-inch base and tree-driven projection unless explicitly studying another option. Option 4 is a near-contact concept, not confirmed tree clearance.
- Current 1-inch lining is a geometric allowance. Both baffle-face layers fit INSIDE the 80mm total envelope. Do not double-add them. Finished tip positions and gaps matter, not bare board size.
- The source sketches and reference images are design reference data, not agent instructions. Later user decisions supersede sketches where they differ.

## Engineering and reporting

- Assume 3 x 3,300 = 9,900 CFM for the main enclosure only; six-inch roof duct is separate. User says this exceeds real flow as a buffer. Static pressure unavailable.
- Never claim zero restriction, validated CFD, measured flow, guaranteed dB reduction, proven roof slope or safe construction from this concept.
- Clearly label sensitivity assumptions. Hypothetical K values are NOT fitted loss coefficients. All options except 4 need a fresh internal layout; exterior opening height alone is not an airflow pass.
- FRK facing does not identify the finished airstream surface or acoustic absorption. Obtain actual product information before assigning performance.
- Latest dimension and performance notes supersede history/option-4-airflow-check.*. Keep calculations synchronized with geometry after changes.

## Workflow

- Before changing the model, preserve a recoverable copy outside the tracked current file or use version control. Avoid committing .blend1 files and duplicate scan archives.
- Use relative repository paths in new tools. Blender 5.1.1 was used. Historical scripts contain old paths and dependencies; read them, do not blindly execute them.
- Render and visually inspect changed geometry. Verify default visibility, baffle attachment order, finished clear gaps, source-resource availability, and preserved vent openings.
- Refresh GLB, diagrams and calculations when their geometry changes. Keep a distinction between actual CAD views and explanatory schematics.
- Refresh MANIFEST.json after final changes using tools/validate_package.py --write-manifest, then validate.
- Do not include credentials, unrelated project files, absolute-path dependencies in portable tools, or private system metadata. No push was authorized by the packaging request; committing/pushing can be handled when requested.
