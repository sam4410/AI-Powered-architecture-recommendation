# AI-Powered-architecture-recommendation
Architecture Recommendation from an Agentic AI system based on Key Requirement Parameters

# 🚀 Setup Instructions for AI Architecture Recommender

## Prerequisites

1. **Python 3.8+** installed on your system
2. **Your existing CrewAI project** structure should be maintained
3. **Required Python packages** (see installation below)

## Project Structure

Your project should maintain this structure:

```
your_project/
├── multi_agent_architecture_recommender/
│   ├── __init__.py
│   ├── crew.py                    # Your existing crew definition
│   └── config/
│       ├── agents.yaml           # Your agent configurations
│       └── tasks.yaml            # Your task definitions
├── app.py                        # The Streamlit app (save the code here)
├── requirements.txt              # Dependencies
└── README.md
```

### 2. Environment Setup

Create a `.env` file in your project root:

```env
# OpenAI API Key (required for CrewAI)
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Other API keys if using different models
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here

# CrewAI Settings
CREWAI_TELEMETRY_OPT_OUT=true
```

### 3. Verify CrewAI Project Structure

Ensure your `config/agents.yaml` file exists and contains:

```yaml
scalability_architect:
  role: >
    Senior Scalability Architect
  goal: >
    Analyze scalability and performance requirements to recommend optimal architecture patterns
  backstory: >
    You are a senior scalability architect with 15+ years of experience 
    building systems that serve millions of users...

team_structure_analyst:
  role: >
    Team Structure Analyst
  goal: >
    Evaluate team structure and organizational constraints using Conway's Law principles
  backstory: >
    You are an expert in organizational design and software architecture alignment...

cost_optimization_analyst:
  role: >
    Cost Optimization Analyst
  goal: >
    Analyze cost implications of different architecture patterns
  backstory: >
    You are a cloud economics expert with deep knowledge of AWS, Azure, and GCP...

architecture_synthesis_expert:
  role: >
    Chief Architecture Decision Maker
  goal: >
    Synthesize insights from all experts to recommend optimal architecture
  backstory: >
    You are a distinguished enterprise architect with 20+ years of experience...
```

### 4. Run the Application

```bash
# Navigate to your project directory
cd your_project

# Run the Streamlit app
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 🔧 Configuration Options

### Streamlit Configuration

Create a `.streamlit/config.toml` file for custom settings:

```toml
[server]
port = 8501
address = "localhost"

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[browser]
gatherUsageStats = false
```

### CrewAI Model Configuration

You can customize the AI models used in your `crew.py`:

```python
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class MultiAgentArchitectureRecommender():
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    @agent
    def scalability_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['scalability_architect'],
            verbose=True,
            allow_delegation=False,
            # Optional: specify different models
            # llm="gpt-4-turbo-preview"  # or "claude-3-opus", etc.
        )
```

## 🎯 Usage Tips

### 1. **Start with Examples**
- Use the "Examples" tab to test with pre-configured scenarios
- This helps verify your setup is working correctly

### 2. **Monitor Performance**
- The analysis can take 2-5 minutes depending on complexity
- Watch the progress bar and status updates
- Check the logs in the expandable section if issues occur

### 3. **Customize for Your Needs**
- Modify the input form fields based on your specific requirements
- Add or remove technology stack options
- Adjust the example scenarios to match your use cases

### 4. **Error Troubleshooting**
- Ensure all API keys are properly set in `.env`
- Check that your CrewAI project structure matches expectations
- Verify all required packages are installed

## 🚨 Common Issues & Solutions

### Issue: "CrewAI project not found"
**Solution**: Ensure the import path matches your project structure:
```python
from multi_agent_architecture_recommender.crew import MultiAgentArchitectureRecommender
```

### Issue: API Rate Limits
**Solution**: Add delays or use different models:
- Implement exponential backoff
- Use different API providers
- Reduce concurrent agent operations

### Issue: Long Analysis Times
**Solution**: Optimize your CrewAI configuration:
- Use faster models for non-critical agents
- Implement timeout handling
- Cache frequently used results

### Issue: Memory Issues
**Solution**: 
- Use lighter models for development
- Implement result streaming
- Clear session state periodically

## 🔐 Security Considerations

1. **API Keys**: Never commit `.env` files to version control
2. **User Input**: The app validates and sanitizes user inputs
3. **Rate Limiting**: Consider implementing rate limiting for production use
4. **Access Control**: Add authentication for enterprise deployments

## 📈 Performance Optimization

### For Production Deployment:

1. **Caching**: Implement Streamlit caching for expensive operations
2. **Async Processing**: Use background tasks for long-running analyses
3. **Database Storage**: Store analysis results for reuse
4. **Load Balancing**: Use multiple instances for high traffic

### Example Caching Implementation:

```python
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def cached_analysis(requirements_hash):
    # Run analysis only if not cached
    return run_analysis(requirements)
```

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Cloud Deployment
- **Streamlit Cloud**: URL: https://ai-powered-architecture-recommendation-zaoqdewv3vn5ljyv6ojqn8.streamlit.app/
- **Heroku**: Easy deployment with buildpacks
- **AWS/GCP/Azure**: Container-based deployment

## 📞 Support

If you encounter issues:
1. Check the error logs in the Streamlit app
2. Verify your CrewAI configuration
3. Ensure all dependencies are properly installed
4. Check API key validity and quotas

## 🎉 Next Steps

Once you have the basic setup working:
1. Customize the UI colors and branding
2. Add more example scenarios
3. Implement result export functionality
4. Add user authentication if needed
5. Deploy to your preferred platform
