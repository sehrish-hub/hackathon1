# Data Model: Book Chapter and Topic Structure

## Entities

### Chapter
- **Description**: A major section of the book, containing multiple topics.
- **Attributes**:
    - `id`: Unique identifier for the chapter (e.g., `01-intro`, `02-ros2-basics`).
    - `title`: Display title of the chapter.
    - `sidebar_label`: Label used in Docusaurus sidebar navigation.
    - `slug`: URL slug for the chapter's main page.
    - `topics`: A collection of `Topic` entities associated with this chapter.

### Topic
- **Description**: A sub-section within a chapter, represented by a single `.md` file with detailed content.
- **Attributes**:
    - `id`: Unique identifier for the topic (e.g., `topic-1-intro-to-physical-ai`).
    - `title`: Display title of the topic.
    - `file_path`: Relative path to the `.md` file containing the topic's content (e.g., `01-intro/topic-1-intro-to-physical-ai.md`).
    - `content`: The detailed page-level markdown content of the topic.
    - `parent_chapter_id`: Reference to the `id` of the `Chapter` it belongs to.

## Relationships

- A `Chapter` **has many** `Topics` (one-to-many relationship).
- A `Topic` **belongs to** one `Chapter`.

## Constraints & Validation

- Each `Chapter` MUST contain a minimum of 5 and a maximum of 6 `Topics` (as per FR-001).
- Each `Topic` MUST be represented by a unique `.md` file within its chapter's directory (as per FR-002).
- The `content` attribute of each `Topic` MUST not be empty and MUST contain detailed page-level information (as per FR-003).
