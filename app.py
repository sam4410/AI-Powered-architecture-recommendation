import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3
import streamlit as st
import streamlit.components.v1 as components
import warnings
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
import json
import os
import time
import threading
from io import StringIO
import contextlib
from dotenv import load_dotenv
load_dotenv(override=True)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Import your existing code (assuming it's available)
try:
    from multi_agent_architecture_recommender.crew import MultiAgentArchitectureRecommender
except ImportError:
    st.error("⚠️ CrewAI project not found. Please ensure the multi_agent_architecture_recommender package is available.")
    st.stop()

# Data Models (from your existing code)
class ArchitectureType(Enum):
    MONOLITHIC = "monolithic"
    MICROSERVICES = "microservices"
    SERVERLESS = "serverless"
    EVENT_DRIVEN = "event_driven"
    LAYERED = "layered"
    HEXAGONAL = "hexagonal"
    MODULAR_MONOLITH = "modular_monolith"

@dataclass
class RequirementContext:
    # Scale & Performance
    expected_users: int
    expected_requests_per_second: int
    data_volume_gb: float
    latency_requirements_ms: int
    peak_load_multiplier: float
    
    # Team & Organization
    team_size: int
    team_experience_level: str
    number_of_teams: int
    development_velocity_priority: str
    devops_maturity: str
    
    # Technical Constraints
    budget_constraint: str
    existing_infrastructure: List[str]
    preferred_cloud_provider: Optional[str]
    compliance_requirements: List[str]
    legacy_system_integration: bool
    
    # Business Requirements
    time_to_market: str
    scalability_needs: str
    availability_requirements: float
    multi_tenant_needs: bool
    geographic_distribution: str
    
    # Technical Preferences
    technology_stack: List[str]
    data_consistency_needs: str
    security_level: str
    integration_complexity: str
    
    def to_dict(self):
        """Convert RequirementContext to dictionary for CrewAI inputs"""
        return {
            'expected_users': self.expected_users,
            'expected_requests_per_second': self.expected_requests_per_second,
            'data_volume_gb': self.data_volume_gb,
            'latency_requirements_ms': self.latency_requirements_ms,
            'peak_load_multiplier': self.peak_load_multiplier,
            'team_size': self.team_size,
            'team_experience_level': self.team_experience_level,
            'number_of_teams': self.number_of_teams,
            'development_velocity_priority': self.development_velocity_priority,
            'devops_maturity': self.devops_maturity,
            'budget_constraint': self.budget_constraint,
            'existing_infrastructure': self.existing_infrastructure,
            'preferred_cloud_provider': self.preferred_cloud_provider,
            'compliance_requirements': self.compliance_requirements,
            'legacy_system_integration': self.legacy_system_integration,
            'time_to_market': self.time_to_market,
            'scalability_needs': self.scalability_needs,
            'availability_requirements': self.availability_requirements,
            'multi_tenant_needs': self.multi_tenant_needs,
            'geographic_distribution': self.geographic_distribution,
            'technology_stack': self.technology_stack,
            'data_consistency_needs': self.data_consistency_needs,
            'security_level': self.security_level,
            'integration_complexity': self.integration_complexity,
        }

# Streamlit Configuration
st.set_page_config(
    page_title="🏗️ AI Architecture Recommender",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .agent-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        text-align: center;
    }
    
    .step-card {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #2196f3;
        margin: 0.5rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

def create_example_requirements() -> RequirementContext:
    """Create example requirements for testing"""
    return RequirementContext(
        expected_users=750000,
        expected_requests_per_second=8000,
        data_volume_gb=250.0,
        latency_requirements_ms=150,
        peak_load_multiplier=3.0,
        team_size=18,
        team_experience_level="mixed",
        number_of_teams=4,
        development_velocity_priority="high",
        devops_maturity="medium",
        budget_constraint="medium",
        existing_infrastructure=["AWS", "PostgreSQL", "Redis"],
        preferred_cloud_provider="AWS",
        compliance_requirements=["GDPR", "SOC2"],
        legacy_system_integration=True,
        time_to_market="fast",
        scalability_needs="horizontal",
        availability_requirements=99.95,
        multi_tenant_needs=True,
        geographic_distribution="multi_region",
        technology_stack=["Python", "React", "PostgreSQL", "Redis", "Docker", "Kubernetes"],
        data_consistency_needs="eventual",
        security_level="high",
        integration_complexity="medium"
    )

def render_mermaid(mermaid_code: str):
    components.html(f"""
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
      mermaid.initialize({{ startOnLoad: true }});
    </script>
    <div class="mermaid">
        {mermaid_code}
    </div>
    """, height=800)

def display_agent_info():
    """Display information about the AI agents"""
    st.markdown("## 🤖 Meet Your Architecture Experts")
    
    agents = [
        {
            "name": "Scalability Architect",
            "role": "Senior Scalability Architect",
            "expertise": "15+ years experience building systems for millions of users. Expert in distributed systems, caching, database scaling, and performance optimization.",
            "icon": "⚡",
            "companies": "Netflix, Amazon, Google"
        },
        {
            "name": "Team Structure Analyst",
            "role": "Organizational Design Expert",
            "expertise": "Specialist in Conway's Law and team-architecture alignment. Helps organizations optimize team structures for maximum productivity.",
            "icon": "👥",
            "companies": "Various Fortune 500 consulting"
        },
        {
            "name": "Cost Optimization Analyst",
            "role": "Cloud Economics Expert",
            "expertise": "Deep knowledge of AWS, Azure, GCP pricing. Has helped companies reduce infrastructure costs by 40-70% through architectural optimizations.",
            "icon": "💰",
            "companies": "Cloud cost optimization specialist"
        },
        {
            "name": "Security and Compliance Expert",
            "role": "Security and Compliance Expert",
            "expertise": "Deep knowledge of implemetation of security and complaince as per international and industry specific regulations into technical architectures.",
            "icon": "💰",
            "companies": "ComplianceForge, StealthLabs, Netwrix"
        },
        {
            "name": "Technology Integration Specialist",
            "role": "Tools and platform Integration Specialist",
            "expertise": "Deep knowledge of AWS, Azure, GCP tools and platforms with 15+ years of experience. Has helped companies reduce integration overheads by 40-70% well designed integration plans.",
            "icon": "💰",
            "companies": "Adeptia, ScienceSoft USA Corp"
        },
        {
            "name": "Architecture Synthesis Expert",
            "role": "Chief Architecture Decision Maker",
            "expertise": "20+ years enterprise architecture experience. Synthesizes complex inputs into clear, actionable recommendations balancing technical and business needs.",
            "icon": "🎯",
            "companies": "Multiple Fortune 500 companies"
        }
    ]
    
    cols = st.columns(2)
    for i, agent in enumerate(agents):
        with cols[i % 2]:
            st.markdown(f"""
                <div class="agent-card">
                    <h4>{agent['icon']} {agent['name']}</h4>
                    <p><strong>Role:</strong> {agent['role']}</p>
                    <p><strong>Expertise:</strong> {agent['expertise']}</p>
                    <p><strong>Background:</strong> {agent['companies']}</p>
                </div>
            """, unsafe_allow_html=True)

def display_usage_steps():
    """Display usage steps"""
    st.markdown("## 📋 How to Use This Tool")
    
    steps = [
        "📊 **Input System Requirements**: Define your expected users, performance needs, and technical constraints",
        "👥 **Configure Team Context**: Specify your team size, experience level, and organizational structure",
        "💼 **Set Business Parameters**: Define budget, timeline, and compliance requirements", 
        "🚀 **Run Analysis**: Let our AI agents analyze your requirements using proven methodologies",
        "📈 **Review Recommendations**: Get detailed architecture recommendations with implementation roadmap"
    ]
    
    for i, step in enumerate(steps, 1):
        st.markdown(f"""
            <div class="step-card">
                <strong>Step {i}:</strong> {step}
            </div>
        """, unsafe_allow_html=True)

@contextlib.contextmanager
def capture_output():
    """Capture stdout and stderr for display in Streamlit"""
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    stdout_buffer = StringIO()
    stderr_buffer = StringIO()
    try:
        sys.stdout = stdout_buffer
        sys.stderr = stderr_buffer
        yield stdout_buffer, stderr_buffer
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

def run_analysis(requirements: RequirementContext):
    """Run the CrewAI analysis with the given requirements"""
    
    # Display analysis start
    st.success("🚀 Starting Architecture Analysis...")
    
    # Create progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Display key requirements summary
    with st.expander("📋 Analysis Parameters", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <h4>Scale Metrics</h4>
                    <p>👥 {requirements.expected_users:,} users</p>
                    <p>⚡ {requirements.expected_requests_per_second:,} RPS</p>
                    <p>💾 {requirements.data_volume_gb}GB data</p>
                    <p>⏱️ {requirements.latency_requirements_ms}ms latency</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <h4>Team Context</h4>
                    <p>👨‍💻 {requirements.team_size} people</p>
                    <p>🏢 {requirements.number_of_teams} teams</p>
                    <p>📊 {requirements.team_experience_level} experience</p>
                    <p>🚀 {requirements.development_velocity_priority} velocity</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <h4>Constraints</h4>
                    <p>💰 {requirements.budget_constraint} budget</p>
                    <p>☁️ {requirements.preferred_cloud_provider}</p>
                    <p>🔒 {requirements.security_level} security</p>
                    <p>🌍 {requirements.geographic_distribution}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Run the analysis
    try:
        status_text.text("Initializing AI agents...")
        progress_bar.progress(20)
        
        # Convert requirements to inputs
        inputs = requirements.to_dict()
        
        status_text.text("Starting multi-agent analysis...")
        progress_bar.progress(40)
        
        # Initialize CrewAI
        crew_instance = MultiAgentArchitectureRecommender()
        
        status_text.text("Agents are analyzing your requirements...")
        progress_bar.progress(60)
        
        # Run the crew analysis
        with capture_output() as (stdout_buffer, stderr_buffer):
            result = crew_instance.crew().kickoff(inputs=inputs)
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis completed successfully!")
        
        # Display results
        st.markdown("## 📊 Architecture Recommendation Report")
        
        # Format and display the result
        if hasattr(result, 'raw') and result.raw:
            st.markdown(result.raw)
        elif isinstance(result, str):
            st.markdown(result)
        else:
            st.write(result)
        
        # Display captured output if needed (for debugging)
        with st.expander("🔍 Analysis Logs", expanded=False):
            stdout_content = stdout_buffer.getvalue()
            stderr_content = stderr_buffer.getvalue()
            
            if stdout_content:
                st.text("Standard Output:")
                st.code(stdout_content)
            
            if stderr_content:
                st.text("Error Output:")
                st.code(stderr_content)
        
        return result
        
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
        st.error("Please check your CrewAI configuration and try again.")
        return None

def get_form_defaults():
    """Get default values for form fields, checking for pre-loaded examples"""
    if 'example_requirements' in st.session_state:
        example = st.session_state.example_requirements
        return {
            'expected_users': example.expected_users,
            'expected_rps': example.expected_requests_per_second,
            'data_volume': example.data_volume_gb,
            'latency_ms': example.latency_requirements_ms,
            'peak_load_multiplier': example.peak_load_multiplier,
            'availability': example.availability_requirements,
            'team_size': example.team_size,
            'number_of_teams': example.number_of_teams,
            'team_experience': example.team_experience_level,
            'dev_velocity': example.development_velocity_priority,
            'devops_maturity': example.devops_maturity,
            'time_to_market': example.time_to_market,
            'budget_constraint': example.budget_constraint,
            'preferred_cloud': example.preferred_cloud_provider,
            'security_level': example.security_level,
            'scalability_needs': example.scalability_needs,
            'geographic_distribution': example.geographic_distribution,
            'data_consistency': example.data_consistency_needs,
            'existing_infrastructure': example.existing_infrastructure,
            'technology_stack': example.technology_stack,
            'compliance_requirements': example.compliance_requirements,
            'integration_complexity': example.integration_complexity,
            'legacy_integration': example.legacy_system_integration,
            'multi_tenant': example.multi_tenant_needs
        }
    else:
        return {
            'expected_users': 750000,
            'expected_rps': 8000,
            'data_volume': 250.0,
            'latency_ms': 150,
            'peak_load_multiplier': 3.0,
            'availability': 99.95,
            'team_size': 18,
            'number_of_teams': 4,
            'team_experience': "mixed",
            'dev_velocity': "high",
            'devops_maturity': "medium",
            'time_to_market': "fast",
            'budget_constraint': "medium",
            'preferred_cloud': "AWS",
            'security_level': "high",
            'scalability_needs': "horizontal",
            'geographic_distribution': "multi_region",
            'data_consistency': "eventual",
            'existing_infrastructure': ["AWS", "PostgreSQL", "Redis"],
            'technology_stack': ["Python", "React", "PostgreSQL", "Redis", "Docker", "Kubernetes"],
            'compliance_requirements': ["GDPR", "SOC2"],
            'integration_complexity': "medium",
            'legacy_integration': True,
            'multi_tenant': True
        }

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🏗️ AI Architecture Recommender</h1>
            <p>Intelligent multi-agent system for architecture recommendations</p>
            <p>Powered by CrewAI • Built for Enterprise Scale</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/667eea/ffffff?text=AI+Architect", width=200)
        
        page = st.selectbox(
            "🧭 Navigation",
            ["🏠 Home", "📋 Usage Guide", "🤖 AI Agents", "⚙️ Analysis", "📊 Examples"]
        )
    
    if page == "🏠 Home":
        st.markdown("## Welcome to AI Architecture Recommender")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### 🎯 What This Tool Does
            
            Our AI-powered architecture recommender uses multiple specialized agents to analyze your system requirements and provide intelligent architecture recommendations. Each agent brings unique expertise:
            
            - **Scalability Analysis**: Performance and scale requirements
            - **Team Structure Assessment**: Conway's Law application
            - **Cost Optimization**: Total cost of ownership analysis
            - **Security and Complaince Assessment**: Applicable international regulations
            - **Integration Plan Development**: Recommending modern integration practices
            - **Synthesis & Decision**: Unified recommendations
            
            ### ✨ Key Features
            
            - 🤖 **Multi-Agent AI System**: Six specialized AI experts
            - 📊 **Comprehensive Analysis**: Scalability, team, cost, security and integration factors
            - 🎯 **Tailored Recommendations**: Specific to your context
            - 📈 **Implementation Roadmap**: Phased approach with timelines
            - 💰 **Cost Optimization**: Budget-conscious recommendations
            """)
        
        with col2:
            st.markdown("### 🚀 Quick Start")
            if st.button("Start Analysis", type="primary"):
                st.session_state.page = "⚙️ Analysis"
                st.rerun()
            
            st.markdown("### 📖 Learn More")
            if st.button("Usage Guide"):
                st.session_state.page = "📋 Usage Guide"
                st.rerun()
            
            if st.button("Meet the Agents"):
                st.session_state.page = "🤖 AI Agents"
                st.rerun()
    
    elif page == "📋 Usage Guide":
        display_usage_steps()
        
        st.markdown("## 🔧 Technical Details")
        
        with st.expander("Architecture Patterns Evaluated", expanded=False):
            patterns = [
                "**Monolithic Architecture**: Single deployable unit, simple to develop and test",
                "**Microservices Architecture**: Distributed services, independent scaling",
                "**Serverless Architecture**: Function-as-a-Service, event-driven",
                "**Event-Driven Architecture**: Asynchronous communication patterns",
                "**Modular Monolith**: Structured monolith with clear boundaries",
                "**Hybrid/Layered Approaches**: Combination strategies"
            ]
            
            for pattern in patterns:
                st.markdown(f"- {pattern}")
        
        with st.expander("Analysis Methodology", expanded=False):
            st.markdown("""
            Our analysis follows proven methodologies:
            
            1. **Conway's Law Application**: Aligning team structure with architecture
            2. **Scalability Patterns**: Performance and load analysis
            3. **Total Cost of Ownership**: Comprehensive cost modeling
            4. **Security and Threat Considerations**: Comprehensive threat analysis and solution
            5. **Integration Plan**: Detailed integration strategies
            6. **Risk Assessment**: Identifying and mitigating architectural risks
            7. **Implementation Planning**: Phased rollout strategies
            """)

    elif page == "🤖 AI Agents":
        display_agent_info()
        
        st.markdown("## 🔄 How Agents Collaborate")
        
        st.markdown("""
        The agents work in sequence, each building on the previous analysis:
        
        1. **Scalability Architect** analyzes technical performance requirements
        2. **Team Structure Analyst** evaluates organizational constraints using Conway's Law
        3. **Cost Optimization Analyst** performs comprehensive cost analysis
        4. **Security and Complaince Assessment**: Applicable international regulations
        5. **Integration Plan Development**: Recommending modern integration practices
        6. **Architecture Synthesis Expert** integrates all insights into final recommendations
        """)
        
        # Visual workflow
        st.markdown("### 🔄 Analysis Workflow")
        render_mermaid("""
        graph TD
            A[Input Requirements] --> B[Scalability Analysis]
            B --> C[Team Structure Analysis]
            C --> D[Cost Analysis]
            D --> E[Security and Compliance]
            E --> F[Integration Strategies]
            F --> G[Synthesis & Recommendations]
            G --> H[Implementation Roadmap]
        """)

    elif page == "⚙️ Analysis":
        st.markdown("## ⚙️ Configure Your Analysis")
        
        # Check if example was loaded and show notification
        if 'example_requirements' in st.session_state:
            st.success(f"✅ Example requirements loaded! You can modify the values below or run the analysis as-is.")
            if st.button("🗑️ Clear Example and Reset to Defaults"):
                del st.session_state.example_requirements
                st.rerun()
        
        # Get form defaults (either from example or hardcoded defaults)
        defaults = get_form_defaults()
        
        # Input form
        with st.form("requirements_form"):
            # Scale & Performance Section
            st.markdown("### 📊 Scale & Performance Requirements")
            col1, col2 = st.columns(2)
            
            with col1:
                expected_users = st.number_input("Expected Users", min_value=1, value=750000, step=1000)
                expected_rps = st.number_input("Requests per Second", min_value=1, value=8000, step=100)
                data_volume = st.number_input("Data Volume (GB)", min_value=0.1, value=250.0, step=10.0)
            
            with col2:
                latency_ms = st.number_input("Latency Requirement (ms)", min_value=1, value=150, step=10)
                peak_load_multiplier = st.number_input("Peak Load Multiplier", min_value=1.0, value=3.0, step=0.5)
                availability = st.number_input("Availability (%)", min_value=90.0, max_value=99.999, value=99.95, step=0.01)
            
            # Team & Organization Section
            st.markdown("### 👥 Team & Organization")
            col1, col2 = st.columns(2)
            
            with col1:
                team_size = st.number_input("Team Size", min_value=1, value=18, step=1)
                number_of_teams = st.number_input("Number of Teams", min_value=1, value=4, step=1)
                team_experience_options = ["junior", "mixed", "senior"]
                team_experience_index = team_experience_options.index(defaults['team_experience']) if defaults['team_experience'] in team_experience_options else 1
                team_experience = st.selectbox("Team Experience Level", team_experience_options, index=team_experience_index)
            
            with col2:
                dev_velocity_options = ["low", "medium", "high"]
                dev_velocity_index = dev_velocity_options.index(defaults['dev_velocity']) if defaults['dev_velocity'] in dev_velocity_options else 2
                dev_velocity = st.selectbox("Development Velocity Priority", dev_velocity_options, index=dev_velocity_index)
                
                devops_maturity_options = ["low", "medium", "high"]
                devops_maturity_index = devops_maturity_options.index(defaults['devops_maturity']) if defaults['devops_maturity'] in devops_maturity_options else 1
                devops_maturity = st.selectbox("DevOps Maturity", devops_maturity_options, index=devops_maturity_index)
                
                time_to_market_options = ["flexible", "medium", "fast"]
                time_to_market_index = time_to_market_options.index(defaults['time_to_market']) if defaults['time_to_market'] in time_to_market_options else 2
                time_to_market = st.selectbox("Time to Market", time_to_market_options, index=time_to_market_index)
            
            # Technical Constraints Section
            st.markdown("### 🔧 Technical Constraints")
            col1, col2 = st.columns(2)
            
            with col1:
                budget_constraint_options = ["low", "medium", "high"]
                budget_constraint_index = budget_constraint_options.index(defaults['budget_constraint']) if defaults['budget_constraint'] in budget_constraint_options else 1
                budget_constraint = st.selectbox("Budget Constraint", budget_constraint_options, index=budget_constraint_index)
                
                preferred_cloud_options = ["AWS", "Azure", "GCP", "Multi-cloud"]
                preferred_cloud_index = preferred_cloud_options.index(defaults['preferred_cloud']) if defaults['preferred_cloud'] in preferred_cloud_options else 0
                preferred_cloud = st.selectbox("Preferred Cloud Provider", preferred_cloud_options, index=preferred_cloud_index)
                
                security_level_options = ["standard", "high", "critical"]
                security_level_index = security_level_options.index(defaults['security_level']) if defaults['security_level'] in security_level_options else 1
                security_level = st.selectbox("Security Level", security_level_options, index=security_level_index)
            
            with col2:
                scalability_needs_options = ["vertical", "horizontal", "both"]
                scalability_needs_index = scalability_needs_options.index(defaults['scalability_needs']) if defaults['scalability_needs'] in scalability_needs_options else 1
                scalability_needs = st.selectbox("Scalability Needs", scalability_needs_options, index=scalability_needs_index)
                
                geographic_distribution_options = ["single_region", "multi_region", "global"]
                geographic_distribution_index = geographic_distribution_options.index(defaults['geographic_distribution']) if defaults['geographic_distribution'] in geographic_distribution_options else 1
                geographic_distribution = st.selectbox("Geographic Distribution", geographic_distribution_options, index=geographic_distribution_index)
                
                data_consistency_options = ["strong", "eventual", "flexible"]
                data_consistency_index = data_consistency_options.index(defaults['data_consistency']) if defaults['data_consistency'] in data_consistency_options else 1
                data_consistency = st.selectbox("Data Consistency Needs", data_consistency_options, index=data_consistency_index)
            
            # Multi-select fields
            st.markdown("### 🛠️ Technology & Compliance")
            col1, col2 = st.columns(2)
            
            with col1:
                existing_infrastructure = st.multiselect(
                    "Existing Infrastructure",
                    ["AWS", "Azure", "GCP", "On-premise", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Kubernetes", "Docker"],
                    default=defaults['existing_infrastructure']
                )
                
                technology_stack = st.multiselect(
                    "Technology Stack",
                    ["Python", "Java", "JavaScript", "TypeScript", "Go", "Rust", "React", "Vue", "Angular", "PostgreSQL", "MongoDB", "Redis", "Docker", "Kubernetes"],
                    default=defaults['technology_stack']
                )
            
            with col2:
                compliance_requirements = st.multiselect(
                    "Compliance Requirements",
                    ["GDPR", "HIPAA", "SOC2", "PCI-DSS", "ISO27001", "FedRAMP"],
                    default=defaults['compliance_requirements']
                )
                
                integration_complexity_options = ["simple", "medium", "complex"]
                integration_complexity_index = integration_complexity_options.index(defaults['integration_complexity']) if defaults['integration_complexity'] in integration_complexity_options else 1
                integration_complexity = st.selectbox("Integration Complexity", integration_complexity_options, index=integration_complexity_index)
            
            # Boolean fields
            st.markdown("### ✅ Additional Requirements")
            col1, col2 = st.columns(2)
            
            with col1:
                legacy_integration = st.checkbox("Legacy System Integration Required", value=defaults['legacy_integration'])
            
            with col2:
                multi_tenant = st.checkbox("Multi-tenant Architecture Needed", value=defaults['multi_tenant'])
            
            # Submit button
            submitted = st.form_submit_button("🚀 Start Architecture Analysis", type="primary")
            
            if submitted:
                # Clear the example from session state after use
                if 'example_requirements' in st.session_state:
                    del st.session_state.example_requirements
                
                # Create requirements object
                requirements = RequirementContext(
                    expected_users=expected_users,
                    expected_requests_per_second=expected_rps,
                    data_volume_gb=data_volume,
                    latency_requirements_ms=latency_ms,
                    peak_load_multiplier=peak_load_multiplier,
                    team_size=team_size,
                    team_experience_level=team_experience,
                    number_of_teams=number_of_teams,
                    development_velocity_priority=dev_velocity,
                    devops_maturity=devops_maturity,
                    budget_constraint=budget_constraint,
                    existing_infrastructure=existing_infrastructure,
                    preferred_cloud_provider=preferred_cloud,
                    compliance_requirements=compliance_requirements,
                    legacy_system_integration=legacy_integration,
                    time_to_market=time_to_market,
                    scalability_needs=scalability_needs,
                    availability_requirements=availability,
                    multi_tenant_needs=multi_tenant,
                    geographic_distribution=geographic_distribution,
                    technology_stack=technology_stack,
                    data_consistency_needs=data_consistency,
                    security_level=security_level,
                    integration_complexity=integration_complexity,
                )
                
                # Store in session state
                st.session_state.requirements = requirements
                
                # Run analysis
                result = run_analysis(requirements)
                
                if result:
                    st.session_state.analysis_result = result

    elif page == "📊 Examples":
        st.markdown("## 📊 Example Scenarios")
        
        examples = {
            "🏢 Enterprise SaaS Platform": create_example_requirements(),
            "🚀 Startup MVP": RequirementContext(
                expected_users=10000, expected_requests_per_second=100, data_volume_gb=10.0,
                latency_requirements_ms=200, peak_load_multiplier=2.0, team_size=5,
                team_experience_level="mixed", number_of_teams=1, development_velocity_priority="high",
                devops_maturity="low", budget_constraint="low", existing_infrastructure=["AWS"],
                preferred_cloud_provider="AWS", compliance_requirements=[], legacy_system_integration=False,
                time_to_market="fast", scalability_needs="vertical", availability_requirements=99.9,
                multi_tenant_needs=False, geographic_distribution="single_region",
                technology_stack=["Python", "React", "PostgreSQL"], data_consistency_needs="strong",
                security_level="standard", integration_complexity="simple"
            ),
            "🏭 Enterprise Monolith Migration": RequirementContext(
                expected_users=2000000, expected_requests_per_second=15000, data_volume_gb=1000.0,
                latency_requirements_ms=100, peak_load_multiplier=4.0, team_size=50,
                team_experience_level="senior", number_of_teams=8, development_velocity_priority="medium",
                devops_maturity="high", budget_constraint="high", existing_infrastructure=["On-premise", "Oracle", "Java"],
                preferred_cloud_provider="AWS", compliance_requirements=["SOC2", "ISO27001"], legacy_system_integration=True,
                time_to_market="flexible", scalability_needs="horizontal", availability_requirements=99.99,
                multi_tenant_needs=True, geographic_distribution="global",
                technology_stack=["Java", "Spring", "Oracle", "Kubernetes"], data_consistency_needs="eventual",
                security_level="critical", integration_complexity="complex"
            ),
            "🏭 Fintech Technology With High Security Needs": RequirementContext(
                expected_users=1000000, expected_requests_per_second=5000, data_volume_gb=2000.0,
                latency_requirements_ms=50, peak_load_multiplier=4.0, team_size=25,
                team_experience_level="senior", number_of_teams=4, development_velocity_priority="medium",
                devops_maturity="high", budget_constraint="high", existing_infrastructure=["AWS", "PostgreSQL", "Redis", "Kafka"],
                preferred_cloud_provider="AWS", compliance_requirements=["PCI-DSS", "SOX", "GDPR", "SOC2"], legacy_system_integration=True,
                time_to_market="medium", scalability_needs="both", availability_requirements=99.99,
                multi_tenant_needs=True, geographic_distribution="multi_region",
                technology_stack=["Java", "PostgreSQL", "Redis", "Kafka", "Kubernetes"], data_consistency_needs="strong",
                security_level="critical", integration_complexity="complex"
            )
        }
        
        for title, example in examples.items():
            with st.expander(title, expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.json({
                        "Users": f"{example.expected_users:,}",
                        "RPS": f"{example.expected_requests_per_second:,}",
                        "Data": f"{example.data_volume_gb}GB",
                        "Team": f"{example.team_size} people",
                        "Budget": example.budget_constraint,
                        "Cloud": example.preferred_cloud_provider,
                        "Security": example.security_level,
                        "Geographic": example.geographic_distribution
                    })
                
                with col2:
                    if st.button(f"Use {title}", key=f"use_{title}"):
                        st.session_state.example_requirements = example
                        st.success("Example loaded! Go to Analysis tab to run.")

if __name__ == "__main__":
    main()
