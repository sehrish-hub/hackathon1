# Task Plan: Setup Book Introduction

**Branch**: `002-setup-book-introduction` | **Date**: 2025-11-12 | **Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Phase 1: Setup

- [X] T001 Remove all default content from `ai-native/docs`.
- [X] T002 Create a new directory `ai-native/docs/01-intro`.
- [X] T003 Create a new directory `ai-native/docs/01-intro/diagrams`.
- [X] T004 Create a new directory `ai-native/docs/01-intro/examples`.

## Phase 2: User Story 1 - Setup initial book content

- [X] T005 [US1] Create the main chapter file `ai-native/docs/01-intro/index.md`.
- [X] T006 [US1] Add the frontmatter and metadata to `ai-native/docs/01-intro/index.md`.
- [X] T007 [US1] Add the content for "Topic 1: What is Physical AI?" to `ai-native/docs/01-intro/index.md`.
- [X] T008 [US1] Add the content for "Topic 2: Embodied Intelligence Principles" to `ai-native/docs/01-intro/index.md`.
- [X] T009 [US1] Add the content for "Topic 3: The Three Pillars Framework" to `ai-native/docs/01-intro/index.md`.
- [X] T010 [US1] Create the "Embodiment Spectrum" diagram in `ai-native/docs/01-intro/diagrams/embodiment-spectrum.mmd`.
- [X] T011 [US1] Create the "Three Pillars of Physical AI" diagram in `ai-native/docs/01-intro/diagrams/three-pillars.mmd`.
- [X] T012 [US1] Create the "Perception-Decision-Action Loop" diagram in `ai-native/docs/01-intro/diagrams/perception-decision-action.mmd`.
- [X] T013 [US1] Create the "Humanoid Robot Landscape 2025" table in `ai-native/docs/01-intro/diagrams/humanoid-landscape-2025.md`.
- [X] T014 [US1] Create the "Embodiment Simulation Pseudocode" example in `ai-native/docs/01-intro/examples/embodied-vs-pure-ai.py`.
- [X] T015 [US1] Create the "Three Pillars in ROS 2" example in `ai-native/docs/01-intro/examples/three-pillars-ros2.py`.
- [X] T016 [US1] Create a `README.md` file in `ai-native/docs/01-intro/` to serve as a navigation guide.

## Phase 3: Polish & Verification

- [ ] T017 Build the Docusaurus site to ensure there are no errors.
- [ ] T018 Verify that the new chapter is rendered correctly.

## Dependencies

- User Story 1 (Phase 2) depends on the successful completion of the Setup phase (Phase 1).
- The Polish & Verification phase (Phase 3) depends on the successful completion of Phase 2.

## Parallel Execution

- T010, T011, T012, T013, T014, T015 can be executed in parallel after T005.

## Implementation Strategy

The strategy is to first clean the existing project, then create the new content, and finally verify the changes by building the site. This ensures a clean and testable implementation. The MVP is the successful rendering of the new introduction chapter.
