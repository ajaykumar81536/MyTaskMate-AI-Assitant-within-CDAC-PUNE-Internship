
# MyTaskMate: Your Intelligent Personal Assistant 🤖✨



MyTaskMate is a modern, all-in-one productivity hub that acts as your personal assistant. It's designed to understand your documents, manage your tasks, and find information for you, all through a single, conversational interface.

-----

### 🤔 The Problem It Solves

In today's fast-paced world, our digital lives are scattered. We have important information in PDFs, Word documents, and emails, while our to-do lists and calendars are in separate apps. This disorganization leads to wasted time and missed deadlines. MyTaskMate solves this by unifying your entire workflow into one smart, central place.

-----

### ✨ Core Features

  * **Universal Document Reader 📂:** Upload and chat with almost any file, including **PDFs, Word documents, images (with OCR), Excel sheets, and CSVs**. Instantly get summaries or find specific information.
  * **Intelligent Task Manager ✅:** Create, view, and reschedule tasks using natural language. The assistant understands commands like, *"remind me to finish the report by next Friday."*
  * **Smart Calendar Integration 🗓️:** Connects to your Google Calendar to schedule events and check your availability, acting as a true scheduling assistant.
  * **Accurate Web Search 🌐:** Asks a question, and if the answer isn't in your documents, the assistant will search the web in real-time to provide the most up-to-date information.
  * **Proactive Suggestions 💡:** Learns from your habits to proactively suggest tasks or actions, helping you stay one step ahead.

-----

### 🏛️ System Architecture

MyTaskMate is not a single AI; it's a team of AI specialists managed by a smart supervisor.

  * **The Supervisor (The Manager):** Built with **LangGraph**, this is the main AI brain. It uses a fast, local Ollama model (`phi3:mini`) to analyze your request and delegate it to the correct specialist agent.
  * **The Specialist Agents (The Team):**
      * **Document Agent:** An expert at reading and understanding your files.
      * **Task Agent:** An expert at managing your to-do list in the database.
      * **Calendar Agent:** An expert at interacting with Google Calendar.
      * **Web Agent:** An expert at searching the internet.

This multi-agent design makes the system highly efficient, scalable, and specialized.

-----

### 🛠️ Tech Stack

| Component             | Technology                                       |
| --------------------- | ------------------------------------------------ |
| **Framework** | Python & Reflex (for UI and backend)             |
| **AI Core** | LangChain & LangGraph                            |
| **Local LLMs** | Ollama (`phi3:mini` for routing)                 |
| **Database** | PostgreSQL                                       |
| **Document Processing** | PyMuPDF, python-docx, Pillow, Pytesseract, openpyxl |
| **Web Search** | Tavily API                                       |
| **Calendar** | Google Calendar API                              |

-----

### 🚀 Getting Started

Follow these steps to set up and run the project on your local machine.

#### 1\. Clone the Repository

```bash
git clone https://github.com/ajaykumar81536/MyTaskMate-AI-Assitant-within-CDAC-PUNE-Internship
```

#### 2\. Set Up Environment Variables

  * Create a file named `.env` in the root of the project.
  * Add your API keys and database URL to this file. Use the `.env.example` file as a template.
    ```
    TAVILY_API_KEY="your_tavily_key"
    POSTGRES_URL="your_database_url"
    # ... and other credentials
    ```
  * Place your `credentials.json` file for Google Calendar in the root directory.

#### 3\. Create a Virtual Environment and Install Dependencies

```bash
# Create the virtual environment
python -m venv .venv

# Activate it (Windows)
.venv\Scripts\activate

# Install all required packages
pip install -r requirements.txt
```

#### 4\. Run the Application

```bash
reflex run
```

The application will be running at `http://localhost:3000`.

-----
