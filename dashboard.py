"""
AI Code Review Dashboard
Streamlit-based analytics and management interface
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

# Page config
st.set_page_config(
    page_title="AI Code Review Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Load mock data
def load_stats():
    """Load statistics from file or generate mock data"""
    stats_file = Path("data/stats.json")
    
    if stats_file.exists():
        with open(stats_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Mock data for demo
    return {
        "total_mrs": 12,
        "total_comments": 47,
        "time_saved_hours": 4.5,
        "avg_score": 7.2,
        "ai_provider": "Gemini 2.5 Flash",
        "webhook_status": "Connected",
        "daily_activity": [
            {"date": "2025-11-18", "mrs": 2, "comments": 8},
            {"date": "2025-11-19", "mrs": 3, "comments": 12},
            {"date": "2025-11-20", "mrs": 4, "comments": 15},
            {"date": "2025-11-21", "mrs": 3, "comments": 12}
        ],
        "team_stats": [
            {"developer": "john_dev", "mrs": 5, "avg_score": 8.2, "time_saved": 2.5},
            {"developer": "maria_dev", "mrs": 7, "avg_score": 6.5, "time_saved": 3.2},
            {"developer": "alex_senior", "mrs": 3, "avg_score": 9.1, "time_saved": 1.8}
        ],
        "issue_types": [
            {"type": "Security", "count": 18},
            {"type": "Code Style", "count": 12},
            {"type": "Performance", "count": 8},
            {"type": "Best Practices", "count": 9}
        ]
    }

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 AI Code Review")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["📊 Analytics", "⚙️ Settings", "👥 Team Performance", "🧠 Learning"]
    )
    
    st.markdown("---")
    st.markdown("### System Status")
    st.success("✅ AI: Online")
    st.success("✅ GitLab: Connected")
    st.info("💡 Gemini 2.5 Flash")
    
    st.markdown("---")
    st.markdown("**ForteBank Hackathon 2025**")

# Main content
if page == "📊 Analytics":
    st.markdown('<p class="main-header">📊 Analytics Dashboard</p>', unsafe_allow_html=True)
    
    stats = load_stats()
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total MRs Analyzed",
            value=stats["total_mrs"],
            delta="+3 this week"
        )
    
    with col2:
        st.metric(
            label="AI Comments Posted",
            value=stats["total_comments"],
            delta="+12 today"
        )
    
    with col3:
        st.metric(
            label="Time Saved",
            value=f"{stats['time_saved_hours']}h",
            delta="+1.2h"
        )
    
    with col4:
        st.metric(
            label="Avg Code Score",
            value=f"{stats['avg_score']}/10",
            delta="+0.3"
        )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Daily Activity")
        df_activity = pd.DataFrame(stats["daily_activity"])
        fig_activity = px.line(
            df_activity,
            x="date",
            y="mrs",
            markers=True,
            title="Merge Requests Analyzed Per Day"
        )
        fig_activity.update_layout(
            xaxis_title="Date",
            yaxis_title="Number of MRs",
            hovermode="x unified"
        )
        st.plotly_chart(fig_activity, use_container_width=True)
    
    with col2:
        st.subheader("🔍 Issue Types Distribution")
        df_issues = pd.DataFrame(stats["issue_types"])
        fig_issues = px.pie(
            df_issues,
            values="count",
            names="type",
            title="Issues Found by Category",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_issues, use_container_width=True)
    
    st.markdown("---")
    
    # Recent activity
    st.subheader("🕒 Recent Activity")
    
    recent_data = [
        {"time": "2 hours ago", "mr": "#12", "developer": "@maria_dev", "score": "6.5/10", "status": "🟡 Needs Fixes"},
        {"time": "5 hours ago", "mr": "#11", "developer": "@john_dev", "score": "8.2/10", "status": "🟢 Approved"},
        {"time": "1 day ago", "mr": "#10", "developer": "@alex_senior", "score": "9.1/10", "status": "🟢 Approved"}
    ]
    
    df_recent = pd.DataFrame(recent_data)
    st.dataframe(df_recent, use_container_width=True, hide_index=True)

elif page == "⚙️ Settings":
    st.markdown('<p class="main-header">⚙️ Settings</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🤖 AI Configuration", "🔗 Integrations", "📋 Review Rules"])
    
    with tab1:
        st.subheader("AI Model Settings")
        
        provider = st.selectbox(
            "AI Provider",
            ["Gemini 2.5 Flash", "OpenAI GPT-4", "Claude 3.5 Sonnet"],
            help="Select the AI model to use for code review"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            auto_review = st.toggle("Auto Review on MR", value=True)
            auto_label = st.toggle("Auto Label MRs", value=True)
            
        with col2:
            min_score = st.slider("Min Score for Approval", 0.0, 10.0, 7.0, 0.1)
            max_length = st.number_input("Max Code Length", value=50000, step=5000)
        
        st.markdown("---")
        
        st.subheader("Custom Prompt Template")
        custom_prompt = st.text_area(
            "Additional Instructions",
            placeholder="e.g., Focus on banking security requirements...",
            height=150
        )
        
        if st.button("💾 Save Settings", type="primary"):
            st.success("✅ Settings saved successfully!")
    
    with tab2:
        st.subheader("GitLab Integration")
        
        gitlab_url = st.text_input("GitLab URL", value="https://gitlab.com")
        webhook_url = st.text_input(
            "Webhook URL",
            value="https://shelia-gallic-overchildishly.ngrok-free.dev/webhook/gitlab",
            disabled=True
        )
        
        st.success("✅ Connected to GitLab")
        
        st.markdown("---")
        
        st.subheader("Webhook Status")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Webhooks Received", "47")
            st.metric("Successful", "45", delta="+2")
        
        with col2:
            st.metric("Failed", "2", delta_color="inverse")
            st.metric("Avg Response Time", "350ms")
    
    with tab3:
        st.subheader("Project Review Rules")
        
        st.markdown("""
        Define custom rules for your project that AI will follow during code review.
        These rules are stored in `.codereview-rules.yaml` in your repository.
        """)
        
        project_name = st.text_input("Project Name", placeholder="e.g., payment-service")
        tech_stack = st.multiselect(
            "Tech Stack",
            ["Python", "FastAPI", "PostgreSQL", "React", "Docker", "Redis"],
            default=["Python", "FastAPI"]
        )
        
        st.markdown("**Security Rules**")
        sec1 = st.checkbox("No hardcoded secrets", value=True)
        sec2 = st.checkbox("SQL injection protection", value=True)
        sec3 = st.checkbox("Input validation required", value=True)
        
        st.markdown("**Banking Requirements**")
        bank1 = st.checkbox("Transaction logging", value=True)
        bank2 = st.checkbox("Error handling with rollback", value=True)
        bank3 = st.checkbox("PCI DSS compliance checks", value=True)
        
        if st.button("📝 Generate .codereview-rules.yaml", type="primary"):
            yaml_content = f"""project_context:
  name: "{project_name}"
  tech_stack: {tech_stack}

security_rules:
  - "No hardcoded secrets"
  - "SQL injection protection required"
  - "All inputs must be validated"

banking_requirements:
  - "Log all transactions"
  - "Implement error handling with rollback"
  - "Follow PCI DSS compliance standards"
"""
            st.code(yaml_content, language="yaml")
            st.success("✅ Copy this to your GitLab repository!")

elif page == "👥 Team Performance":
    st.markdown('<p class="main-header">👥 Team Performance</p>', unsafe_allow_html=True)
    
    stats = load_stats()
    
    # Team stats table
    st.subheader("Developer Statistics")
    
    df_team = pd.DataFrame(stats["team_stats"])
    df_team["rank"] = df_team["avg_score"].rank(ascending=False, method="dense").astype(int)
    df_team = df_team.sort_values("avg_score", ascending=False)
    
    # Format display
    df_team["Developer"] = df_team["developer"].apply(lambda x: f"@{x}")
    df_team["MRs"] = df_team["mrs"]
    df_team["Avg Score"] = df_team["avg_score"].apply(lambda x: f"{x}/10")
    df_team["Time Saved"] = df_team["time_saved"].apply(lambda x: f"{x}h")
    df_team["Rank"] = df_team["rank"].apply(lambda x: f"🏆 {x}" if x == 1 else f"#{x}")
    
    st.dataframe(
        df_team[["Rank", "Developer", "MRs", "Avg Score", "Time Saved"]],
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Score Distribution")
        fig_scores = go.Figure(data=[
            go.Bar(
                x=df_team["developer"],
                y=df_team["avg_score"],
                marker_color=df_team["avg_score"].apply(
                    lambda x: '#2ecc71' if x >= 8 else '#f39c12' if x >= 6 else '#e74c3c'
                )
            )
        ])
        fig_scores.update_layout(
            xaxis_title="Developer",
            yaxis_title="Average Score",
            yaxis_range=[0, 10]
        )
        st.plotly_chart(fig_scores, use_container_width=True)
    
    with col2:
        st.subheader("⏱️ Time Saved by Developer")
        fig_time = px.bar(
            df_team,
            x="developer",
            y="time_saved",
            color="time_saved",
            color_continuous_scale="Blues"
        )
        fig_time.update_layout(
            xaxis_title="Developer",
            yaxis_title="Hours Saved",
            showlegend=False
        )
        st.plotly_chart(fig_time, use_container_width=True)
    
    st.markdown("---")
    
    # ROI Calculation
    st.subheader("💰 Return on Investment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        senior_rate = st.number_input("Senior Hourly Rate (₸)", value=15000, step=1000)
    
    with col2:
        total_saved = stats["time_saved_hours"]
        st.metric("Total Hours Saved", f"{total_saved}h")
    
    with col3:
        roi = total_saved * senior_rate
        st.metric("Money Saved", f"₸{roi:,.0f}")
    
    st.info(f"💡 **Monthly Projection**: If this trend continues, you'll save ~₸{roi * 6.67:,.0f} per month!")

elif page == "🧠 Learning":
    st.markdown('<p class="main-header">🧠 AI Learning System</p>', unsafe_allow_html=True)
    
    st.markdown("""
    The AI learns from senior developer feedback to improve recommendations over time.
    When a senior marks an AI comment as incorrect, the system adapts.
    """)
    
    st.markdown("---")
    
    # Feedback stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Feedback", "23")
    
    with col2:
        st.metric("👍 Positive", "19", delta="83%")
    
    with col3:
        st.metric("👎 Negative", "4", delta="-17%", delta_color="inverse")
    
    st.markdown("---")
    
    # Recent feedback
    st.subheader("📝 Recent Feedback")
    
    feedback_data = [
        {
            "date": "2025-11-21 10:30",
            "mr": "#12",
            "senior": "@alex_senior",
            "feedback": "👎 Negative",
            "reason": "ORM is used, prepared statements comment not relevant",
            "status": "✅ Learned"
        },
        {
            "date": "2025-11-21 09:15",
            "mr": "#11",
            "senior": "@john_dev",
            "feedback": "👍 Positive",
            "reason": "Good catch on SQL injection vulnerability",
            "status": "✅ Reinforced"
        },
        {
            "date": "2025-11-20 16:45",
            "mr": "#10",
            "senior": "@maria_dev",
            "feedback": "👎 Negative",
            "reason": "This pattern is standard in our codebase",
            "status": "✅ Learned"
        }
    ]
    
    df_feedback = pd.DataFrame(feedback_data)
    st.dataframe(df_feedback, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Learning rules
    st.subheader("📚 Learned Rules")
    
    with st.expander("🔒 Security Patterns"):
        st.markdown("""
        - **Use ORM instead of raw SQL** - Learned from @alex_senior feedback
        - **JWT token validation** - Standard practice in auth service
        - **API key rotation** - Required for production deployments
        """)
    
    with st.expander("🏗️ Architecture Patterns"):
        st.markdown("""
        - **Service layer pattern** - Used across all microservices
        - **Repository pattern** - Standard for data access
        - **Dependency injection** - FastAPI native approach
        """)
    
    with st.expander("🏦 Banking Specific"):
        st.markdown("""
        - **Transaction logging** - PCI DSS requirement
        - **Audit trail** - Mandatory for all money operations
        - **Double-entry accounting** - Standard practice
        """)
    
    st.markdown("---")
    
    st.info("💡 **Tip**: The more feedback you provide, the better AI becomes at understanding your codebase!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🤖 AI Code Review Assistant | ForteBank Hackathon 2025</p>
    <p>Powered by Gemini 2.5 Flash | Made with ❤️ for developers</p>
</div>
""", unsafe_allow_html=True)
