# Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Installation

```bash
yarn
```

## Local Development

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

Using SSH:

```bash
USE_SSH=true yarn deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.

## Content Structure and Naming Conventions

This Docusaurus project enforces a consistent structure for chapters and their topics to ensure maintainability and clear navigation.

### Chapter Directories

-   **Format:** `XX-chapter-slug/`
    -   `XX`: Two-digit chapter number (e.g., `01`, `02`, `03`).
    -   `chapter-slug`: Kebab-case, descriptive name of the chapter (e.g., `intro`, `ros2-basics`, `llm-ros2-integration`).
    -   **Example:** `docs/01-intro/`

Each chapter directory must contain an `index.md` file, which serves as the main entry point for that chapter. You can use the `_templates/chapter-index.md` template for new chapter `index.md` files.

### Topic Files

-   **Format:** `topic-Y-topic-slug.md`
    -   `Y`: Single-digit or two-digit topic number within the chapter (e.g., `1`, `2`, `10`).
    -   `topic-slug`: Kebab-case, descriptive name of the topic (e.g., `intro-to-physical-ai`, `evolution-from-ros1`).
    -   **Example:** `docs/01-intro/topic-1-intro-to-ai-native-robotics.md`

Each chapter must contain a minimum of 5 topic files. You can use the `_templates/chapter-topic.md` template for new topic files. Ensure each topic file contains detailed page-level content, not just titles.

When creating new chapters or topics, remember to update `sidebars.ts` to ensure they are correctly displayed in the Docusaurus navigation.