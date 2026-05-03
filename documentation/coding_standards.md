# Coding Standards and Engineering Practices

This document outlines the professional standards and development workflows adopted for the COMP3011 Search Engine Tool project to ensure high-quality, maintainable, and robust software.

**Note** - This content is AI generated through Google Gemini by giving it the coursework spec. Tweaks to this content have been made by myself however.

---

## 1. Python Style and Formatting
To achieve "Publication-quality code", the following standards are strictly enforced:

*   **PEP 8 Compliance**: All code follows the official Python style guide (PEP 8) for naming conventions and layout.
*   **Type Hinting**: All functions and class methods must include type hints for parameters and return values (e.g., `def index_word(word: str) -> bool:`).
*   **Naming Conventions**: 
    *   `snake_case` for functions and variables.
    *   `PascalCase` for classes.
    *   `UPPER_CASE` for constants (e.g., `POLITENESS_WINDOW = 6`).

---

## 2. Documentation Standards
Clear communication is a core assessment.

*   **Docstrings**: Every module, class, and function must have a Google-style docstring explaining:
    *   Purpose of the code.
    *   Arguments (types and descriptions).
    *   Returns (types and descriptions).
    *   Exceptions raised.
*   **In-line Comments**: Used sparingly to explain "why" a specific logic was implemented, rather than "what" the code is doing.
*   **README Mastery**: The root `README.md` acts as a professional landing page with architecture overviews and design rationales.

---

## 3. Engineering & Architecture
*   **Modular Design**: Logic is separated into `crawler.py`, `indexer.py`, and `search.py` to ensure high cohesion and low coupling.
*   **Defensive Programming**: 
    *   Network requests are wrapped in `try-except` blocks to handle timeouts and connection errors.
    *   Validation checks are performed on user inputs in the CLI.
*   **Algorithm Optimization**: Implement TF-IDF ranking for the `find` command and use efficient data structures (hash maps/dictionaries) for $O(1)$ index lookups.

---

## 4. Requirement-Specific Constraints
These items are non-negotiable for grade eligibility:

*   **Politeness Window**: A mandatory delay of at least 6 seconds is enforced between every HTTP request.
*   **Case Insensitivity**: All tokens are normalized to lowercase before indexing and searching.
*   **Persistence**: The `build` command must serialize the index to the `data/` directory, and `load` must successfully reconstruct it.

---

## 5. Quality Assurance (Testing)
To reach the "Excellent" band, a professional-grade test suite is required:

*   **Unit Tests**: Testing individual components in isolation (e.g., the cleaning of a string).
*   **Integration Tests**: Testing the end-to-end flow from crawling to searching.
*   **Coverage Goal**: Aim for >85% code coverage, including tests for edge cases like empty queries or non-existent words.

---

## 6. Version Control Workflow
*   **Semantic Commits**: Use descriptive prefixes (e.g., `feat:`, `fix:`, `docs:`, `test:`).
*   **Iterative Progression**: Commits must be regular and incremental, showing the evolution of the project from the first line of code.
*   **Kanban Integration**: Tasks are tracked via GitHub Projects, with commits linked to specific feature cards.
*   **Pull Requests**: Work will be done in development branches, and pull requests will be used to merge code into main. GitHub Copilot will be used to review all pull requests before going into main. It will look to check code functionality, but also ensure all code followed the coding standards outlined in this document.

---

## 7. GenAI Ethical Usage & Audit
*   **Transparent Declaration**: All AI assistance throughout this project will be declared in the `gen_ai.md` file in this directory.
*   **Critical Evaluation**: AI suggestions won't be blindly accepted, and I will use critical thinking to ensure any gen AI contribution is valid.