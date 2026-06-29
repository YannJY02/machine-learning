# Machine Learning Course Study

This repo is a course study workspace for Hung-yi Lee's machine learning course. Its primary goal is to support learning the lectures and completing related exercises; its secondary goal is to turn that process into reusable learning assets: concept notes, runnable exercises, and review records.

## Language

**Course Study Workspace**:
A repository organized around learning a specific course and completing its related exercises.
_Avoid_: Portfolio site, general ML template

**Learning Asset**:
A reusable artifact produced from the study process, such as a note, exercise, experiment result, or review record.
_Avoid_: Dump, archive

**Resource Registry**:
A curated list of upstream course pages, open-source repositories, and reference materials used to seed study units.
_Avoid_: Link dump, database

**Local Resource Mirror**:
A git-ignored local copy of official downloadable course files, exercise assets, datasets, or upstream repositories generated from a resource manifest.
_Avoid_: Committed course archive

**Core Track**:
The primary course version used to define study order, homework selection, and the minimum study loop. This repo uses Machine Learning 2021 Spring as the core track.
_Avoid_: Only version, latest version

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

**Runnable Exercises**:
Exercise code or notebooks that can be executed, inspected, and modified. Prefer notebooks for study flow and use scripts only when code becomes reusable or needs repeated execution.
_Avoid_: Code snippets, screenshots

**Review Records**:
Records of mistakes, open questions, fixes, and follow-up decisions from study or practice.
_Avoid_: Random notes

**Study Unit**:
A lecture or topic folder that reaches the minimum study loop: concept notes, runnable exercises, and review records. Use a course lecture as the default unit, split by topic only when a lecture is too broad, and organize units by course progress before adding topic indexes.
_Avoid_: Loose folder, topic dump
