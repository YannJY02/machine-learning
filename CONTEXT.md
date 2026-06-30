# Machine Learning Course Study

This repo is a course study workspace for Hung-yi Lee's machine learning course. Its primary goal is to support learning the lectures and completing related exercises; its secondary goal is to turn that process into reusable learning assets: concept notes, runnable exercises, and review records.

## Language

**Course Study Workspace**:
A repository organized around learning a specific course and completing its related exercises.
_Avoid_: Portfolio site, general ML template

**Learning Asset**:
A reusable artifact produced from the study process, such as a note, exercise, experiment result, or review record.
_Avoid_: Dump, archive

**Course Source Reference**:
A source URL, provenance note, or local asset reference kept inside the relevant Study Unit or Homework Module instead of a separate resource registry.
_Avoid_: Link dump, detached resource registry

**Local Course Asset**:
A git-ignored official PDF, dataset, notebook, checkpoint, or other course file stored inside the relevant Study Unit or Homework Module so the learner can study without jumping back to the resource registry.
_Avoid_: Committed course archive, detached resource mirror

**Core Track**:
The primary course version used to define study order, homework selection, and the minimum study loop. This repo uses Machine Learning 2021 Spring as the core track.
_Avoid_: Only version, latest version

**Course Skeleton**:
The complete learner-facing folder structure for a Core Track, created from the official lecture order before every unit is studied. It may contain empty notes and practice folders, but only real downloaded assets are moved into it.
_Avoid_: Partial folder list, fabricated local asset

**Extension Track**:
A later course version used to add modern topics after the matching core topics are covered. This repo uses Machine Learning 2023 Spring as the GenAI extension track.
_Avoid_: Parallel main track

**Source Of Truth**:
The official course page, assignment page, or sample-code repository used to verify lecture order, homework requirements, and original materials.
_Avoid_: Random mirror

**Reference Source**:
A high-reputation open-source explanation, note, or aggregation used to support understanding after checking the source of truth.
_Avoid_: Primary source

**Dataset Reference**:
A lightweight note that records where a dataset comes from and how to download or recreate it, instead of committing the full dataset.
_Avoid_: Dataset copy

**Experiment Record**:
A concise record of a meaningful run, result, plot, mistake, or observation that supports later review.
_Avoid_: Raw log, output dump

**Concept Notes**:
Notes that explain a course concept in the learner's own words. Notes may mix Chinese and English, but technical terms should be kept in English.
_Avoid_: Raw lecture transcript

**Teaching HTML Page**:
A standalone learner-facing HTML Learning Asset for one lecture or lecture range. It is generated from the matching local slide PDF and transcripts, explains the material in practical Chinese while preserving English technical terms, and may pair self-made visualizations with original slide screenshots for stability.
_Avoid_: Marketing page, detached summary, raw slide clone

**Runnable Exercises**:
Exercise code or notebooks that can be executed, inspected, and modified. Prefer notebooks for study flow and use scripts only when code becomes reusable or needs repeated execution.
_Avoid_: Code snippets, screenshots

**Review Records**:
Records of mistakes, open questions, fixes, and follow-up decisions from study or practice.
_Avoid_: Random notes

**Study Unit**:
A lecture-first folder under `courses/ml2021-spring/units/` that follows the official course order and keeps that lecture's notes, slide references, homework modules, practice work, and review records together for learner use.
_Avoid_: Loose folder, topic dump, homework-first folder

**Study Unit Entry**:
The `README.md` inside a Study Unit. It tells the learner what this lecture contains, which local assets belong to it, which videos/source references matter, and which Homework Modules are attached.
_Avoid_: Generic index, external resource catalog

**Homework Module**:
A homework-specific subfolder inside the related Study Unit. It contains the assignment brief, runnable practice, and review record for that homework without becoming a top-level course unit.
_Avoid_: Top-level study unit, detached exercise folder

**Homework Module Entry**:
The `README.md` inside a Homework Module. It keeps the homework goal, source references, local assets, and study/practice checklist in one place.
_Avoid_: Detached assignment brief, resource pointer

**Official Starter**:
An official homework notebook that provides a runnable baseline scaffold and leaves meaningful TODOs or improvement space for the learner. It belongs in the Homework Module `practice/` folder, separate from the learner's own attempt.
_Avoid_: Answer key, detached official asset
