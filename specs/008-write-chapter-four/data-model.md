# Data Model: Chapter Four

**Date**: 2025-11-13

## Key Entities

### Chapter

- **Description**: Represents a chapter in the book.
- **Attributes**:
  - `title`: The title of the chapter.
  - `content`: The content of the chapter in Markdown format.
  - `diagrams`: A list of diagrams used in the chapter.
  - `examples`: A list of code examples used in the chapter.

## Relationships

- A `Book` has many `Chapters`.
- A `Chapter` has many `Diagrams`.
- A `Chapter` has many `Examples`.
