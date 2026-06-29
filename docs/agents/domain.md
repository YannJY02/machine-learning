# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before Exploring, Read These

- **`CONTEXT.md`** at the repo root.
- **`docs/adr/`** for decisions that touch the area being worked on.

If any of these files don't exist, proceed silently. Don't flag their absence or suggest creating them upfront. Create them lazily only when terms or decisions actually get resolved.

## File Structure

Single-context repo:

```text
/
|-- CONTEXT.md
|-- docs/
|   `-- adr/
`-- exercises/
```

## Use The Glossary's Vocabulary

When output names a domain concept in an issue title, refactor proposal, hypothesis, or test name, use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept isn't in the glossary yet, either reconsider the language or note the gap for domain modeling.

## Flag ADR Conflicts

If output contradicts an existing ADR, surface it explicitly rather than silently overriding it.
