# Agent Instructions

This repo is for studying Hung-yi Lee's machine learning course and doing related exercises.

## Study writing conventions

Use English for folder and file names. Notes may mix Chinese and English, but technical terms should be kept in English.
Organize study units under `courses/ml2021-spring/units/` by course progress first, then add lightweight topic indexes only after enough material exists.
Prefer official course pages and widely verified open-source references before creating a study unit from scratch.
Use Machine Learning 2021 Spring as the core track. Use Machine Learning 2023 Spring as a GenAI extension after the matching core topics are covered.
Keep local course assets inside the learner-facing course tree: lecture PDFs and transcripts under the matching study unit, homework PDFs/notebooks/data under the matching homework module, and prep tutorials under `courses/ml2021-spring/prep/`. These assets must stay out of git unless they are small learner-authored notes, indexes, or curated experiment records.
When generating a lesson teaching HTML page, place the standalone `lesson-<lecture-range>-<topic>.html` file in the matching study unit directory. Keep supporting slide screenshots or other PDF-derived teaching images under `teaching-assets/<html-slug>/` in the same study unit; treat those images as local course assets unless explicitly curated as learner-authored material.
Teaching HTML should be based on the local official slide PDF and matching transcripts, preserve the lecture's knowledge points and caveats, explain in practical learner-facing Chinese while keeping English technical terms, and connect concepts with a clear logic. Use concise self-made visualizations for explanation, and add original PDF slide screenshots when they help verify or stabilize the visual explanation.

## Data and output policy

Keep only small sample data, download notes, and curated experiment records in git. Do not commit large datasets, checkpoints, generated output batches, or long logs.

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues; external PRs are not a triage request surface. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the default five-label triage vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

This repo uses a single-context domain-doc layout. See `docs/agents/domain.md`.

## Study unit shape

Use this minimum loop for each unit:

```text
courses/ml2021-spring/units/001-topic-name/
|-- README.md
|-- notes.md
|-- slides/
|-- teaching-assets/
|   `-- lesson-lecture-range-topic/
|-- homework/
|   `-- hw-name/
|       |-- README.md
|       |-- assignment.pdf
|       |-- data/
|       |-- practice/
|       `-- review.md
|-- practice/
|-- lesson-lecture-range-topic.html
`-- review.md
```
