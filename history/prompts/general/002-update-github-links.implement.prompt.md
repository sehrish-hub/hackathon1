---
id: 002
title: Update GitHub Links
stage: implement
date: 2025-11-14
surface: agent
model: gemini-1.5-flash-latest
feature: general
branch: 002-setup-book-introduction
user: sehri
command: read_file, replace
labels: ["github", "links", "docusaurus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ai-native/docusaurus.config.ts
tests:
  - No automated tests were added for this configuration change.
---

## Prompt

ab aisy krn k ye jo gitub ka logo h ospr user click kry tu mera github ka page khuly ye vala https://github.com/sehrish-hub/hackathon1

## Response snapshot

Updated the GitHub links in 'ai-native/docusaurus.config.ts' (both in the navbar and footer configurations) to point to 'https://github.com/sehrish-hub/hackathon1'.

## Outcome

- ✅ Impact: GitHub links on the website now correctly point to the specified repository.
- 🧪 Tests: Manual verification of the links in the deployed site.
- 📁 Files: `ai-native/docusaurus.config.ts` updated.
- 🔁 Next prompts: Continue with further website customization or development.
- 🧠 Reflection: Successfully located and updated Docusaurus configuration for external links.

## Evaluation notes (flywheel)

- Failure modes observed: Initial search for "github" in components was not fruitful, requiring investigation of `docusaurus.config.ts`.
- Graders run and results (PASS/FAIL): N/A (Manual verification)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add a more prominent GitHub icon in the navbar.
