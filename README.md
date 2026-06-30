# Machine Learning Course Study

This repo is a course study workspace for Hung-yi Lee's machine learning course.

The primary goal is to support learning the lectures and completing related exercises. The secondary goal is to turn that process into reusable learning assets: concept notes, runnable exercises, and review records.

## Structure

- `courses/`: active course tracks and study units.
- `discussions/`: group discussion records and follow-ups.
- `CONTEXT.md`: glossary for the repo's study language.

## Study Unit

Each study unit should leave the minimum study loop:

```text
courses/ml2021-spring/units/001-topic-name/
|-- README.md
|-- notes.md
|-- slides/
|-- homework/
|   `-- hw-name/
|       |-- README.md
|       |-- assignment.pdf
|       |-- data/
|       |-- practice/
|       `-- review.md
|-- practice/
`-- review.md
```

## Data Policy

Keep only small sample data, dataset references, and curated experiment records in git. Do not commit large datasets, checkpoints, generated output batches, or long logs.
