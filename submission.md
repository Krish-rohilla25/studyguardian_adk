# StudyGuardian: Your AI-Powered Study Companion

### Problem Statement
Studying for exams or learning new topics can be overwhelming. Students often struggle with organizing their study schedules, finding relevant and concise resources, and testing their knowledge effectively. Manually creating a study plan, searching for materials across the web, and creating practice quizzes takes valuable time away from actual learning. Furthermore, maintaining focus and tracking progress across different subjects can be difficult without a structured system, leading to inefficient study sessions and lower retention.

### Why agents?
Agents are the right solution for this problem because studying is a multi-step, dynamic process that requires distinct cognitive capabilities. A single script cannot easily handle the diverse tasks of planning a schedule, researching disparate sources, and generating pedagogical content simultaneously.
*   **Specialization**: By using specialized agents (Planner, Retriever, Quiz), we can optimize each step—the Planner focuses on pedagogy, while the Retriever focuses on search accuracy.
*   **Adaptability**: Agents can react to user input dynamically. If a user asks for clarification, the Planner Agent can switch context from "planning" to "tutoring" without breaking the system.
*   **Automation**: Agents automate the repetitive "grunt work" of finding resources and writing questions, allowing the student to focus purely on cognitive absorption.

### What you created
StudyGuardian is a modular multi-agent system built using the **Google Agent Development Kit** principles. It is not a monolithic application but a coordinated team of specialized agents orchestrated to act as a personal tutor.

**Architecture Overview**:
*   **StudyOrchestrator**: The central brain that manages the workflow. It receives user input, maintains the state, and coordinates the hand-offs between agents. It also manages the **MemoryBank** to persist context across turns.

**The Agent Team**:
1.  **Planner Agent**: Acts as the Content Strategist. It analyzes the user's goal and context to generate a logical 3-step study plan. It is context-aware and can switch modes to explain concepts if the user asks follow-up questions.
2.  **Retriever Agent**: Acts as the Research Assistant. It fetches information relevant to the study plan. It can search the web (via Google Search API) or read local files (`.pdf`) provided by the user. It uses an internal LLM fallback if external tools are unavailable.
3.  **Quiz Agent**: Acts as the Examiner. It synthesizes the retrieved information to create targeted multiple-choice questions (MCQs) that test the user's understanding.

### Demo
The solution is an interactive Command Line Interface (CLI) that guides the user through a study session.
1.  **Start**: User runs `python app/main.py`.
2.  **Input**: User asks "Teach me about Photosynthesis" or "Create a quiz from notes.pdf".
3.  **Process**:
    *   The **Planner** displays a formatted study schedule.
    *   The **Retriever** confirms it has found resources (web or PDF).
    *   The **Quiz Agent** presents 3 MCQs.
4.  **Interaction**: The user can answer the questions or ask follow-up questions like "Explain why B is correct", and the system uses its memory to provide context-aware answers.

### The Build
I built StudyGuardian using a Python-based agentic architecture.
*   **Gemini 2.0 Flash**: The core intelligence powering the agents. I implemented a custom `GeminiClient` to interact with the REST API, ensuring access to the latest model capabilities.
*   **LangChain & Pypdf**: Used for tool abstractions and PDF text extraction.
*   **MemoryBank**: A custom JSON-based storage system I built to persist study sessions and conversation history, enabling the agents to "remember" context.
*   **AgentLogger**: A centralized observability tool I created to log every agent action to `study_guardian.log` for debugging and performance tracking.

### If I had more time, this is what I'd do
I would implement a **Feedback Agent** that grades the user's quiz answers in real-time and updates a "Weak Areas" database. This would allow the system to customize future study plans based on the user's actual performance, creating a truly adaptive learning loop. I would also add a frontend interface to make the tool more accessible to non-technical students.
