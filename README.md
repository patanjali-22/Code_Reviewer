# LNW Code Review Assistant

An AI-powered code review tool that leverages **CrewAI agents** and **LLMs** to automatically analyze pull requests with historical context and Jira integration.

## ✨ Features

- 🔍 **Similarity Search** - Find historically similar code changes using vector embeddings
- 📋 **Jira Integration** - Fetch related ticket context including parent/child relationships
- 🧠 **AI Code Analysis** - GPT-powered static code review (null checks, logging, performance, readability)
- 📝 **Smart Summaries** - Human-readable explanations of review findings

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit UI (main.py)                   │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               CodeReviewEngine (review_engine.py)           │
│                    Orchestrates workflow                    │
└─────────────────────────────┬───────────────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           ▼                  ▼                  ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ AIAgentFactory  │  │ ReviewTaskBuilder│  │ OpenAIAnalyzer  │
│ (agent_defs.py) │  │ (task_defs.py)  │  │ (openai_client) │
└────────┬────────┘  └────────┬────────┘  └─────────────────┘
         │                    │
         ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│               CodeReviewTools (agent_tools.py)              │
│         find_similar_code_changes | fetch_ticket_context    │
└─────────────────────────────┬───────────────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           ▼                  ▼                  ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   DiffParser    │  │  JiraApiClient  │  │BitbucketClient  │
│ (diff_analyzer) │  │ (jira_client)   │  │(bitbucket_client│
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

## 📁 Project Structure

```
Code_Reviewer/
├── main.py                 # Streamlit web interface
├── review_engine.py        # Main orchestrator
├── agent_definitions.py    # AI agent factory
├── task_definitions.py     # Agent task builders
├── agent_tools.py          # LangChain tools for agents
├── openai_client.py        # OpenAI API wrapper
├── jira_client.py          # Jira REST API client
├── diff_analyzer.py        # Git diff parsing utilities
├── pr_data_utils.py        # PR data helpers
├── bitbucket_client.py     # Bitbucket API client
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   Update `.env` with your API keys:
   ```env
   OPENAI_API_KEY=your_openai_key
   ```

3. **Initialize vector database:**
   ```bash
   python create_database.py
   ```

4. **Run the application:**
   ```bash
   streamlit run main.py
   ```

## 🐳 Docker Deployment

### Quick Start with Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t lnw-code-reviewer .
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key lnw-code-reviewer
```

### Environment Variables for Docker

Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key
JIRA_TOKEN=your_jira_token
```

Then run:
```bash
docker-compose --env-file .env up -d
```

Access the application at: `http://localhost:8501`

## ⚙️ Configuration

| File | Settings |
|------|----------|
| `jira_client.py` | `JiraConfig` - Jira URL and auth token |
| `openai_client.py` | `OpenAIAnalyzer.API_KEY` - OpenAI key |
| `bitbucket_client.py` | `BitbucketConfig` - Bitbucket workspace/repo |
| `agent_tools.py` | `OPENAI_KEY`, `VECTOR_DB_PATH` |

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **CrewAI** | Multi-agent orchestration |
| **LangChain** | LLM tooling & embeddings |
| **ChromaDB** | Vector similarity search |
| **OpenAI GPT** | Code analysis |
| **Streamlit** | Web interface |
| **Jira REST API** | Ticket integration |

## 📄 License

For LNW internal use only.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Contact

For questions or support, reach out to the LNW Engineering Team.
