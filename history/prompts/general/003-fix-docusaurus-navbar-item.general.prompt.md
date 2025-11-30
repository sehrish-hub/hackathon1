---
ID: 003
TITLE: Fix: Docusaurus NavbarItem Not Found Error
STAGE: general
DATE_ISO: 2025-11-14
SURFACE: "agent"
MODEL: "gemini-1.5-flash"
FEATURE: "login-page"
BRANCH: "main"
USER: "user"
COMMAND: "The previous page crashed due to a NavbarItem not found error. Try again."
LABELS: ["docusaurus", "ui", "login", "navbar", "bug-fix"]
LINKS: "null"
FILES_YAML: |
  - ai-native/docusaurus.config.ts
  - ai-native/src/clientModules/AuthNavbarItem.tsx
  - ai-native/src/theme/NavbarItem/AuthNavbarItem.tsx (removed)
  - ai-native/src/components/AuthNavbarItem.tsx (removed)
TESTS_YAML: "null"
---

## Prompt
The previous page crashed due to a NavbarItem not found error. Try again.

## Response
I have fixed the "NavbarItem not found" error by correctly configuring the custom NavbarItem component in Docusaurus, and also resolved a subsequent `MODULE_NOT_FOUND` error related to the `clientModules` configuration.

The initial attempt to place the component in `src/theme/NavbarItem` and the subsequent attempt to use `type: 'custom'` with `component` prop were both incorrect approaches for this Docusaurus setup.

The successful fix involved:
1.  Reverting the `docusaurus.config.ts` modification for the navbar item back to `type: 'custom-AuthNavbarItem'`.
2.  Removing the `AuthNavbarItem.tsx` from `src/theme/NavbarItem/` and deleting the `src/theme/NavbarItem` directory.
3.  Removing the `AuthNavbarItem.tsx` from `src/components/`.
4.  Creating `AuthNavbarItem.tsx` in `ai-native/src/clientModules/AuthNavbarItem.tsx`.
5.  Adding a `clientModules` entry to `ai-native/docusaurus.config.ts` that explicitly registers `./src/clientModules/AuthNavbarItem.tsx`.
6.  Correcting the `clientModules` entry in `docusaurus.config.ts` from `require.resolve('./src/clientModules/AuthNavbarItem')` to a simple relative string `./src/clientModules/AuthNavbarItem` to resolve the `MODULE_NOT_FOUND` error.

This ensures that Docusaurus correctly identifies and renders the "Sign In" link in the navbar by registering the custom component as a client module and referencing it with its intended custom type.
