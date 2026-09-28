# Instructions for AI Agents

> **You are Claude Code, or any other AI assistant working in the Serenity-UAV repository. Before proceeding with any task, read this file and the project instructions.**

## Authoritative Source

The **canonical project instructions and standards are in [`AGENTS.md`](AGENTS.md)** (root directory). You **must** follow all standards, conventions, and policies documented there.

**Every design specification, code change, commit message, and piece of documentation must comply with the standards in `AGENTS.md`.**

## Authenticity

- **No Reference, citation, standard, or other resource will ever be fabricated.**
- Every resource will be properly cited, whether or not it's required by copyright or license
- All work done by AI will be distinguished from that done by a human user
- Human contributers will be referenced by their GitHub usernames, unless otherwise specified in a the project's governing documents.
- Each AI system and model will be cited for its own contribution (i.e. Gemini must be distinguished from Grok, from Claude, and Haiku 4.5 needs a separate citation from Opus 4.8)
- **Every design decision, algorithm, or geometry technique that draws on an external reference must be cited in the relevant source file docstring and commit message.**
- **Derivative files must carry the full attribution chain back to upstream sources.**

## Scope-Specific Guidance

For work within a specific subsystem, also consult the **federated `AGENTS.md` file in that folder**. These provide additional detail and workflows tailored to that subsystem:

**Subordinate files are authoritative for their scope.** If a subordinate file contradicts the root file, follow the subordinate.

## Critical Standards You Must Follow

### Code and Commit Quality

- All code shall be clean and syntactically correct
- 4-space indenting throughout
- Verbose comments in strict conformity to each language
- Use secure coding practices — avoid command injection, XSS, SQL injection, OWASP top 10 vulnerabilities
- All code must pass strict linting rules

### Documentation

- Every design specification with any effect beyond cosmetic appearance must be vetted against applicable industry standards
- All standards citations use `[REF-ID §section.subsection.paragraph]` format from `REFERENCES.md`
- No fabricated, unverifiable, or incorrectly attributed references are permitted
- All measurements: **imperial-primary with metric in parentheses** (e.g., 10 in (254 mm))
    - Use **lbm** for mass, **lbf** for force, **kt** for airspeed

### Design Philosophy

- All designs are for **actual physical builds**, not hypothetical work
- Every component will be fabricated or procured
- Account for real weights, balance, power, space, and component capabilities
- Do not leave values as "TBD"
- Failover capability is a first-class requirement

### Fabrication Standards

- **Material:** CF-PETG (0.15 mm layer height, 4 perimeters, ≥40% infill for load-bearing)
- **Shell walls:** hollowed to 2.0 mm while maintaining a **watertight mesh** with no voids or holes
- All load-bearing mating surfaces: minimum 2-wall contact annulus + positive-stop shoulder
- **Mesh validation:** Run after every 3D model modification; report all findings to `TODO.md`

### STL and SCAD

- All models must be clean and watertight; ready to slice for printing
- Any regenerated primary-component STL must be re-baked before publishing
- After SCAD changes, verify Z-range and bore-diameter in console output before committing

### File Management

- Prefer editing existing files over creating new ones
- Do not add features, refactor, or introduce abstractions beyond what the task requires
- Keep `PROJECT_INDEX.md` up to date when adding active files
- Move archived files to `archives/` and update `ARCHIVE_INDEX.md`
- When adding a standards citation, update `REFERENCES.md` with a validated URL and specific section/paragraph

### Git Commits

- **Create NEW commits** rather than amending existing ones (unless explicitly requested)
- Never skip hooks (`--no-verify`) or bypass signing (`--no-gpg-sign`)
- Never force-push to main/master
- Use HEREDOC syntax for commit messages with multi-line bodies:

  ```sh
  git commit -m "$(cat <<'EOF'
  Commit message here.

  Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
  EOF
  )"
  ```

### Coordinate System (Hull Frame)

## Before You Act

1. **Read `AGENTS.md`** in full before starting any task
2. **Check for subordinate AGENTS.md** in the target folder
3. **Verify all standards citations** against `REFERENCES.md` before using them
4. **Check `TODO.md`** for context on ongoing work
5. **Review git history** for recent commits and patterns

## When Adding New Work

1. Add tracking items to `TODO.md` as subtasks in the appropriate section
2. Update `PROJECT_INDEX.md` when adding new active files
3. Update `REFERENCES.md` when adding standards citations
4. Cite applicable standards using REF-IDs
5. Include commit messages explaining the **why**, not just the **what**

## Conflict Resolution

**If you encounter conflicting guidance:**

1. Root AGENTS.md (project-wide) > Subordinate AGENTS.md (scope-specific)
1.1. The subordinate AGENTS.md guidance is authoritative unless excluded by the root AGENTS.md.
1.2 All conflicts between Root and Subordinate AGENTS.md **shall** be immediately be brought to the user's attention for adjudication.  No work will procede until adjudication is received.  
2. REFERENCES.md (verified standards) > comments or assumptions
3. Actual code/model state > documentation (if they diverge, update the docs to match reality and investigate why they diverged)

## Questions?

If the task is unclear or you lack required information, **ask the user explicitly** before proceeding. Do not guess or invent details.

---

**Last updated:** 2026-06-30  
**Authoritative file:** [`AGENTS.md`](AGENTS.md)

## Standards Vetting Policy

- **Every design specification with any effect beyond cosmetic appearance must be vetted against applicable industry standards and/or regulations before implementation.**  Standards citations shall be recorded in `REFERENCES.md`, which catalogs every applicable standard with:
    - Standard designation and full title
    - Validated URL for official access (verified against the issuing body)
    - Specific chapter, section, and paragraph applied
    - Every repository location where the standard is cited

- **All citations throughout the codebase** — in code comments, documentation, schematics, and build guides — shall reference the `REFERENCES.md` REF-ID (e.g., `[REF-FCC-001 §15.247(b)(3)(ii)]`) and shall include chapter, section, and paragraph to enable auditing.

- **No fabricated, unverifiable, or incorrectly attributed references are permitted.**  Any citation that cannot be traced to a specific published document with a validated URL must be removed or corrected.  Removed or superseded citations are documented in the "Removed / Superseded Citations" section of `REFERENCES.md`.

- **Applicable standards bodies for this project:** FAA (airworthiness, registration, operations), FCC (radio frequency), NIST (cybersecurity and information security), DoD/DLA (MIL-STD bus protocols), ISO (data bus protocols), IEC (component safety), VDE (isolator certification), IEEE (networking standards), ISA/IEC 62443 (OT/ICS cybersecurity),
  AUVSI/ASTM F38 (UAS design guidelines), and ICAO (international aviation rules).

## Engineering Requirements

- **Weight, balance, power, space, and component capabilities must always be accounted for.**

  Size fasteners, walls, and structural members for real loads. Quote actual masses and CG shifts
  when adding or removing geometry. Do not leave these as "TBD."

- **All measurements shall be expressed imperial-primary with metric in parentheses: e.g. 10 in (254 mm), 2.5 lbm (1.13 kg), 4.8 lbf (21.4 N).**
    - Use **lbm** for mass (pounds-mass) and **lbf** for force (pounds-force); never write bare "lb" where the distinction matters.
    - Metric equivalents use **kg** for mass and **N** for force.
    - Thrust, lift, and aerodynamic loads are forces → lbf / (N).  Component weights and payload capacity are masses → lbm / (kg).
    - **Airspeed and wind speed are expressed in knots (kt)** with m/s in parentheses where needed for calculation.  Never use mph or km/h for airspeed.

## Coding Standards

- All code shall be clean and syntactically correct.  **Secure coding practices shall be used throughout.**

- All code and documentation shall be written in accordance with **strict linting rules and all linting standards shall be observed.**

- All code shall use 4 space indenting, whether or not required by the language.

- All code shall use verbose commenting, in strict conformity to each language.  In the case of a language that doesn't allow inline comments, such as kicad files, comments shall be included in an accompanying Markdown file.

- Commenting in KiCad files using ; or # is strictly prohibited. All comments for kiCad files must be either in a Markdown file or comment blocks such as: ( comment 1 "hello world" )

## Licensing and Attribution

- All work is **published under CC BY 4.0**.
- The author of this project is Steve Griffing, PE(CSE), CISSP-ISSEP, CPP.  The avionics boards are marked with his personally owned LLC name, but he retains personal copyright.

- Every design decision, algorithm, or geometry technique that draws on an external reference
  **must be cited** in the relevant source file docstring or commit message.

- Derivative files must carry the full attribution chain back to upstream sources.

## Workflow Notes

- **When adding a standards citation:** look up the standard in `REFERENCES.md` by REF-ID; if it is not yet in the catalog, add it to `REFERENCES.md` with a validated URL and the specific section cited, then use the REF-ID in the code or doc.
  Never invent or guess a section number — if the section cannot be verified, mark it as "requires verification" in `REFERENCES.md` and add a TODO §0.x item.

- Run Blender scripts with `blender --background --python <script>.py` — the machine supports headless execution.
- Any time that an assistant creates a todo list to accomplish a task for the build, the steps shall be added as sup-tasks in the appropriate paragraph of the root repository TODO.md wbs, conforming to proper style, so that unresolved issues can be picked up in future sessons.

- The AI assistant shall update PROJECT_INDEX.md, which lists the directory structure and all folders and files in the active project, whenever new active files are added to the repository.  When filess are archived, their names shall be moved from PROJECT_INDEX.md to ARCHIVE_INDEX.md, which describes the file tree of the archive.

## Word Usage and Documentation Style

This section applies to all documents in this repository, human- and AI-authored alike.

### Voice

- Use **active voice** for all directions and authoritative specification documents.
- Use **passive voice** for all descriptive as-built documents.

### Mandatory word usage

| Word | Meaning | Example |
|---|---|---|
| **shall** | The action is prescribed as mandatory. | "You shall obey the law." |
| **will** | One thing follows another; no mandatory action is demanded. | "Friday will come after Thursday." |
| **should** | Preferred but not mandatory. | "You may do it that way, but you should do it this way." |
| **may** | A permissible action by an entity (AI or human). | |
| **could** | Used only to describe the physical or performance limits of objects. | |

### Call-out boxes

- A call-out box labeled **WARNING** shall prominently accompany any directive, instruction, or checklist item that, if not followed, creates a hazard to life or bodily injury.
- A call-out box labeled **CAUTION** shall accompany directives, instructions, and checklist items that, if not followed carefully, create a hazard to objects.
- A call-out box labeled **NOTE** will accompany other items that need emphasis but do not present hazardous conditions.

### Reference

The shall/should/may definitions and the WARNING/CAUTION/NOTE call-out
convention above follow CNAF M-3710.7, *NATOPS General Flight and Operating
Instructions*, issued by Commander, Naval Air Forces (CNAF)
(<https://www.secnav.navy.mil/doni/SECNAV%20Manuals1/3710.7%20(CNAF).pdf>).
The will/could definitions and the active-voice/passive-voice distinction
above are this project's own convention, not drawn from that source.
