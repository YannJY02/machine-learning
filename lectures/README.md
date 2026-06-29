# Lectures

Organize study units by course progress. Use one lecture folder by default, and split by topic only when a lecture is too broad to study as one unit.

Each study unit should leave the minimum study loop:

```text
lecture-001-topic-name/
|-- notes.md
|-- exercise/
`-- review.md
```

- `notes.md`: concept notes in the learner's own words. Chinese and English may be mixed; technical terms should stay in English.
- `exercise/`: runnable exercises, preferably notebooks first and scripts only when code becomes reusable.
- `review.md`: mistakes, open questions, fixes, experiment records, and follow-up decisions.

Keep only small sample data, dataset references, and curated experiment records in git. Do not commit large datasets, checkpoints, generated output batches, or long logs.
