"""
LNW Code Review Assistant - Demo Mode
AI-powered code review tool with Jira integration
"""
import streamlit as st
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="LNW Code Review Assistant",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0;
        animation: gradient-shift 3s ease infinite;
    }
    .sub-header {
        color: #666;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .result-card {
        background: linear-gradient(145deg, #f0f2f6 0%, #e6e9ef 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">🔍 LNW Code Review Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-powered code review with historical context and Jira integration</p>', unsafe_allow_html=True)

st.divider()

# Input section
col1, col2 = st.columns([2, 1])

with col1:
    git_diff_input = st.text_area(
        "📝 Git Diff",
        height=250,
        placeholder="""Paste your git diff here...

Example:
diff --git a/services/ServiceUtils.java b/services/ServiceUtils.java
index abc123..def456 100644
--- a/services/ServiceUtils.java
+++ b/services/ServiceUtils.java
@@ -45,6 +45,8 @@ public class ServiceUtils {
     public void processData(DataTO dataTO) {
+        if (dataTO == null) {
+            throw new IllegalArgumentException("DataTO cannot be null");
+        }
         dataTO.setProcessed(true);
     }""",
        help="The git diff from your pull request"
    )

with col2:
    st.markdown("### ⚙️ Options")
    jira_ticket_input = st.text_input(
        "🎫 Jira Ticket ID",
        placeholder="e.g., LNW-1234",
        help="Optional: Provide a Jira ticket ID for additional context"
    )
    
    analysis_depth = st.selectbox(
        "Analysis Depth",
        ["Standard", "Deep", "Quick Scan"],
        index=0
    )
    
    include_suggestions = st.checkbox("Include Improvement Suggestions", value=True)
    check_security = st.checkbox("Security Analysis", value=True)

st.divider()

# Submit button
submit_button = st.button("🚀 Analyze Code", type="primary", use_container_width=True)

# Process submission
if submit_button and git_diff_input:
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Simulate analysis steps
    steps = [
        "Parsing git diff...",
        "Searching for similar historical changes...",
        "Querying Jira for related tickets...",
        "Performing static code analysis...",
        "Generating recommendations..."
    ]
    
    for i, step in enumerate(steps):
        status_text.text(f"⏳ {step}")
        progress_bar.progress((i + 1) * 20)
        time.sleep(0.5)
    
    status_text.text("✅ Analysis complete!")
    time.sleep(0.3)
    status_text.empty()
    progress_bar.empty()
    
    st.success("Analysis Complete!")
    
    # Results display
    st.divider()
    
    # Metrics row
    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.metric("Files Changed", "3", delta="2 additions")
    with metric_cols[1]:
        st.metric("Lines Added", "+47", delta_color="normal")
    with metric_cols[2]:
        st.metric("Lines Removed", "-12", delta_color="inverse")
    with metric_cols[3]:
        st.metric("Code Quality", "8.5/10", delta="+0.5")
    
    st.divider()
    
    # Analysis results
    tab1, tab2, tab3 = st.tabs(["📋 Code Analysis", "🔗 Related Tickets", "💡 Suggestions"])
    
    with tab1:
        st.markdown("### Static Code Analysis")
        st.markdown("""
        <div class="result-card">
        <h4>✅ Null Safety Check</h4>
        <p>Added null check for <code>dataTO</code> parameter - Good practice!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="result-card">
        <h4>⚠️ Logging Recommendation</h4>
        <p>Consider adding debug logging before and after the <code>processData()</code> method for better traceability.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="result-card">
        <h4>✅ Exception Handling</h4>
        <p>Using <code>IllegalArgumentException</code> is appropriate for null parameter validation.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if check_security:
            st.markdown("""
            <div class="result-card">
            <h4>🔒 Security Analysis</h4>
            <p>No security vulnerabilities detected in the code changes.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Related Jira Tickets")
        
        # Simulated related tickets
        tickets = [
            {"key": "LNW-1234", "summary": "Add null safety to core utilities", "status": "In Review"},
            {"key": "LNW-1189", "summary": "ServiceUtils refactoring", "status": "Done"},
            {"key": "LNW-1156", "summary": "DataTO validation improvements", "status": "Done"},
        ]
        
        for ticket in tickets:
            status_color = "🟢" if ticket["status"] == "Done" else "🟡"
            st.markdown(f"""
            **{ticket['key']}** - {ticket['summary']}  
            {status_color} Status: {ticket['status']}
            """)
            st.divider()
    
    with tab3:
        if include_suggestions:
            st.markdown("### Improvement Suggestions")
            
            st.info("💡 **Suggestion 1**: Consider using `Objects.requireNonNull()` instead of manual null check for cleaner code.")
            
            st.code("""
// Instead of:
if (dataTO == null) {
    throw new IllegalArgumentException("DataTO cannot be null");
}

// Consider:
Objects.requireNonNull(dataTO, "DataTO cannot be null");
            """, language="java")
            
            st.info("💡 **Suggestion 2**: Add unit test for the null case scenario.")
            
            st.info("💡 **Suggestion 3**: Consider adding @NonNull annotation for compile-time checks.")

elif submit_button:
    st.warning("⚠️ Please provide a git diff to analyze.")

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Quick Stats")
    st.metric("Reviews Today", "12")
    st.metric("Avg Review Time", "2.3 min")
    st.metric("Issues Found", "23")
    
    st.divider()
    
    st.markdown("### 🔧 Settings")
    st.toggle("Dark Mode", value=False)
    st.toggle("Auto-save Results", value=True)
    
    st.divider()
    
    st.markdown("### 📚 Recent Reviews")
    st.markdown("- LNW-1234 - 2 min ago")
    st.markdown("- LNW-1189 - 15 min ago")
    st.markdown("- LNW-1156 - 1 hour ago")

# Footer
st.divider()
st.caption("LNW Code Review Assistant v1.0 | Powered by CrewAI & OpenAI | 🔒 Demo Mode")