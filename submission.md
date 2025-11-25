# StudyGuardian: Your AI-Powered Study Companion

## Problem Statement
Studying for exams or learning new topics can be overwhelming. Students often struggle with organizing their study schedules, finding relevant and concise resources, and testing their knowledge effectively. Manually creating a study plan, searching for materials across the web, and creating practice quizzes takes valuable time away from actual learning. Furthermore, maintaining focus and tracking progress across different subjects can be difficult without a structured system, leading to inefficient study sessions and lower retention.

## Solution Statement
**StudyGuardian** is an intelligent multi-agent system designed to streamline the study process. It acts as a personal tutor that plans, retrieves, and tests knowledge automatically.
*   **Planning**: The **Planner Agent** analyzes the user's goal and creates a structured, step-by-step study plan, breaking down complex topics into manageable tasks.
*   **Resource Gathering**: The **Retriever Agent** automatically finds relevant study materials from the web or processes local documents (PDFs), saving hours of research time.
*   **Active Recall**: The **Quiz Agent** generates custom multiple-choice quizzes based on the retrieved content, ensuring the user actively engages with the material.
*   **Context Awareness**: The system remembers previous interactions, allowing users to ask follow-up questions and get explanations for specific concepts or quiz answers.

## Architecture
StudyGuardian is built as a modular multi-agent system using the **Google Agent Development Kit** principles. It is not a monolithic script but a coordinated team of specialized agents.

### Core Components
*   **StudyOrchestrator**: The central brain that manages the workflow. It receives user input, maintains the state, and coordinates the hand-offs between agents. It also manages the **MemoryBank** to persist context across turns.

### Specialized Agents
1.  **Planner Agent (`planner.py`)**:
    *   **Role**: Content Strategist & Scheduler.
    *   **Function**: Analyzes the user's request and context to generate a logical 3-step study plan. It is context-aware and can switch modes to explain concepts if the user asks follow-up questions.
    *   **Tools**: `GeminiClient` for reasoning.

2.  **Retriever Agent (`retriever.py`)**:
    *   **Role**: Research Assistant.
    *   **Function**: Fetches information relevant to the study plan. It can search the web (via Google Search API) or read local files provided by the user. If external tools are unavailable, it uses its internal LLM knowledge base as a fallback.
    *   **Tools**: `PDFReaderTool`, `SearchTool`, `GeminiClient`.

3.  **Quiz Agent (`quiz_agent.py`)**:
    *   **Role**: Examiner.
    *   **Function**: Synthesizes the retrieved information to create targeted multiple-choice questions (MCQs) that test the user's understanding.
    *   **Tools**: `GeminiClient`.

### Essential Tools and Utilities
*   **GeminiClient**: A custom REST-based client implemented to interact directly with Google's Gemini 2.0 Flash model, ensuring access to the latest capabilities even in restricted environments.
*   **PDFReaderTool**: Allows the system to ingest local textbooks or notes (PDF format) to generate quizzes specifically from the user's own material.
*   **MemoryBank**: A JSON-based storage system that persists study sessions and conversation history, enabling the agents to "remember" context like previous quiz questions.
*   **AgentLogger**: A centralized observability tool that logs every agent action and system event to `study_guardian.log` for debugging and performance tracking.

## Value Statement
StudyGuardian transforms the chaotic process of studying into a structured, guided experience. By automating the planning and quiz generation, it allows students to focus 100% of their energy on learning. The ability to instantly generate a quiz from a textbook chapter (via PDF) or get a study plan for any topic makes it an invaluable tool for continuous learning.

If I had more time, I would implement a **Feedback Agent** that grades the user's quiz answers in real-time and updates a "Weak Areas" database to customize future study plans.
