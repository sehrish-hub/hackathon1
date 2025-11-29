# Research for Chapter Topic Structure Feature

## Naming Convention for Chapter and Topic Files

### Decision:
Adopt the existing naming convention observed in the `docs/01-intro/` and `docs/02-ros2-basics/` directories.

### Rationale:
Consistency with existing project structure is paramount for maintainability, ease of navigation, and integration with Docusaurus. Deviating from the established pattern would introduce unnecessary complexity and potential issues with routing and sidebar generation.

### Alternatives Considered:
-   **Fully numerical (e.g., `docs/01/`, `docs/01-01.md`):** Rejected as it lacks descriptive names, making content harder to identify at a glance.
-   **Descriptive only (e.g., `docs/introduction/`, `docs/introduction-to-physical-ai.md`):** Rejected because the numerical prefix (e.g., `01-` for chapters, `topic-1-` for topics) is crucial for maintaining a clear, sortable order in the documentation sidebar and file system, especially as the book grows.

### Enforced Naming Convention:

-   **Chapter Directories:** `XX-chapter-slug/`
    -   `XX`: Two-digit chapter number (e.g., `01`, `02`, `03`).
    -   `chapter-slug`: Kebab-case, descriptive name of the chapter (e.g., `intro`, `ros2-basics`, `llm-ros2-integration`).
    -   *Example:* `docs/01-intro/`

-   **Chapter Index Files:** `index.md`
    -   Each chapter directory will contain an `index.md` file, serving as the main entry point for that chapter.
    -   *Example:* `docs/01-intro/index.md`

-   **Topic Files:** `topic-Y-topic-slug.md`
    -   `Y`: Single-digit or two-digit topic number within the chapter (e.g., `1`, `2`, `10`).
    -   `topic-slug`: Kebab-case, descriptive name of the topic (e.g., `intro-to-physical-ai`, `evolution-from-ros1`).
    -   *Example:* `docs/01-intro/topic-1-intro-to-ai-native-robotics.md`

This convention ensures that files are logically grouped, easily identifiable, and maintain a consistent order within the Docusaurus sidebar.