# Handoff: ML2021 Study Workspace

Generated: 2026-06-30

## Next Session Goal

Continue working from the new canonical project path:

```text
/Users/yann.jy/Developer/AI/machine learning
```

The old Desktop path is only a compatibility symlink for existing Codex threads:

```text
/Users/yann.jy/Desktop/AI/machine learning -> /Users/yann.jy/Developer/AI/machine learning
```

Open new Codex threads from the canonical `Developer` path.

## Current Project Purpose

This repo is a learning workspace for Hung-yi Lee's Machine Learning 2021 Spring course. The goal is to support lecture study, homework practice, group discussion, and reusable learning assets.

Notes may mix Chinese and English. Technical terms should stay in English.

## Important Paths

- Project root: `/Users/yann.jy/Developer/AI/machine learning`
- Core course track: `courses/ml2021-spring/`
- Current active unit: `courses/ml2021-spring/units/001-regression/`
- Resource registry: `resources/`
- Official ML2021 resource manifest: `resources/2021-spring/manifest.json`
- PDF catalog: `resources/2021-spring/catalog.md`
- Exercise asset catalog: `resources/2021-spring/datasets.md`
- Resource sync script: `scripts/sync_ml2021_resources.py`

## Current Filesystem State

Large local resources now live inside the project under ignored directories:

```text
resources/2021-spring/datasets/
resources/2021-spring/downloads/
resources/2021-spring/upstream/
```

These are real directories, not symlinks. They are ignored by `.gitignore`.

The previous `~/LocalOnly` resource folder was removed after moving these directories back into the project.

## Git / GitHub State

The GitHub repo `YannJY02/machine-learning` was deleted at the user's request.

Local `.git` history is preserved. The local `origin` remote was removed, so `git remote -v` is currently empty.

Recent local commits:

```text
74e3471 Ignore local mirror symlinks
564c855 Restructure ML2021 study track
6ca8f28 Add ML2021 exercise asset sync
e56473a Add ML2021 PDF resource sync
a6d587e Add resource registry and first study unit
5e17239 Define study workspace structure
e4fbb15 Initialize agent skill setup
```

Before publishing again, create a new GitHub repo and set a new `origin`.

## Course / Resource Decisions

- Core track: Machine Learning 2021 Spring.
- Official source of truth: `https://speech.ee.ntu.edu.tw/~hylee/ml/2021-spring.php`
- Official/sample GitHub reference used locally: `ga642381/ML2021-Spring`
- PDF-only policy for courseware downloads: no PPT/PPTX.
- Official PDFs are indexed and downloaded under `resources/2021-spring/downloads/`.
- Exercise datasets/assets were parsed from upstream notebooks and downloaded when publicly accessible through Google Drive.
- Some assets remain missing because public Google Drive mirrors were inaccessible; see `resources/2021-spring/datasets.md`.

## Current Study Structure

Main course entry:

```text
courses/ml2021-spring/
|-- README.md
|-- progress.md
`-- units/
    `-- 001-regression/
        |-- notes.md
        |-- assignment.md
        |-- practice/
        `-- review.md
```

Unit 001 is active. It covers Regression / HW1.

## Local Resource Snapshot

At last verification:

- Project size: about `1.5G`
- `datasets/`: about `1.4G`
- `downloads/`: about `75M`
- `upstream/`: about `46M`
- Desktop compatibility path: `0B` symlink

HW1 verified assets:

```text
resources/2021-spring/datasets/hw01/covid.train.csv
resources/2021-spring/datasets/hw01/covid.test.csv
resources/2021-spring/downloads/homework/hw1-regression/slides/HW01.pdf
```

## Suggested Skills

- `$ask-matt`: route the next workflow if unsure.
- `$grill-with-docs`: refine the learning/repo structure or study process while preserving decisions in docs.
- `$handoff`: create a fresh handoff when switching threads again.
- `$implement`: use for concrete repo edits after the next task is clear.

## Good Next Moves

1. Start a new Codex thread from `/Users/yann.jy/Developer/AI/machine learning`.
2. Ask it to read this handoff plus `AGENTS.md`, `README.md`, `CONTEXT.md`, and `courses/ml2021-spring/progress.md`.
3. Decide whether to publish a new GitHub repo now or keep working locally until the learning structure is more stable.
4. Continue Unit 001 by creating the first HW1 notebook/script under `courses/ml2021-spring/units/001-regression/practice/`.

## Guardrails

- Do not commit `resources/2021-spring/datasets/`, `downloads/`, or `upstream/`.
- Do not use low-signal homework solution repos before making an independent attempt.
- Keep new project work on the canonical `Developer` path, not the Desktop symlink.
- Keep large generated outputs, checkpoints, and logs out of Git.
