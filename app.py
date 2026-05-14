import streamlit as st

st.set_page_config(
    page_title="PhantomOps AI",
    page_icon="🚀",
    layout="wide"
)

# =========================
# STYLING
# =========================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0b1120;
        color: white;
    }

    .hero {
        background: linear-gradient(135deg, #111827, #1f2937);
        padding: 60px;
        border-radius: 20px;
        margin-bottom: 40px;
    }

    .hero-title {
        font-size: 60px;
        font-weight: bold;
        color: white;
    }

    .hero-subtitle {
        font-size: 24px;
        color: #cbd5e1;
        margin-top: 15px;
    }

    .card {
        background-color: #111827;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #374151;
        margin-bottom: 20px;
    }

    .metric-card {
        background-color: #111827;
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        border: 1px solid #374151;
    }

    .service-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .footer {
        text-align: center;
        margin-top: 50px;
        color: #9ca3af;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# HERO
# =========================

st.markdown(
    """
    <div class="hero">

        <div class="hero-title">
            PhantomOps AI
        </div>

        <div class="hero-subtitle">
            Autonomous AI Operations Infrastructure For Modern Businesses
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# INTRO
# =========================

left, right = st.columns([2, 1])

with left:

    st.markdown(
        """
        ## We Build AI Business Systems

        PhantomOps AI helps businesses automate:

        - CRM workflows
        - lead generation
        - proposal automation
        - AI inbox intelligence
        - autonomous followups
        - analytics dashboards
        - Telegram/WhatsApp automation
        - AI-powered operational systems

        We specialize in building scalable AI infrastructure
        that saves time, increases efficiency, and drives revenue.
        """
    )

with right:

    st.info(
        """
        ### Quick Stats

        ✅ Autonomous Runtime

        ✅ AI CRM Systems

        ✅ Live Marketplace Intelligence

        ✅ Proposal Automation

        ✅ Revenue Analytics

        ✅ AI Workflow Systems
        """
    )

# =========================
# SERVICES
# =========================

st.header("Services")

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown(
        """
        <div class="card">

        <div class="service-title">
            AI Workflow Automation
        </div>

        Build autonomous workflows for:
        <ul>
            <li>operations</li>
            <li>lead management</li>
            <li>CRM systems</li>
            <li>internal automation</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        """
        <div class="card">

        <div class="service-title">
            CRM Intelligence Systems
        </div>

        AI-powered CRM systems with:
        <ul>
            <li>analytics</li>
            <li>opportunity tracking</li>
            <li>customer intelligence</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )

with c3:

    st.markdown(
        """
        <div class="card">

        <div class="service-title">
            AI Lead Generation
        </div>

        Automated:
        <ul>
            <li>lead discovery</li>
            <li>outreach systems</li>
            <li>proposal generation</li>
            <li>acquisition pipelines</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# WHY US
# =========================

st.header("Why PhantomOps AI")

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.markdown(
        """
        <div class="metric-card">
            <h2>24/7</h2>
            Autonomous Runtime
        </div>
        """,
        unsafe_allow_html=True
    )

with m2:

    st.markdown(
        """
        <div class="metric-card">
            <h2>AI</h2>
            Commercial Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:

    st.markdown(
        """
        <div class="metric-card">
            <h2>CRM</h2>
            Revenue Operations
        </div>
        """,
        unsafe_allow_html=True
    )

with m4:

    st.markdown(
        """
        <div class="metric-card">
            <h2>Automation</h2>
            AI Infrastructure
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# INDUSTRIES
# =========================

st.header("Industries We Serve")

st.markdown(
    """
    - Healthcare & Clinics  
    - Hospitals  
    - Real Estate  
    - Agencies  
    - Startups  
    - SaaS Companies  
    - Coaching Businesses  
    - Educational Institutions  
    - E-commerce Brands  
    - Service Businesses  
    """
)

# =========================
# CAPABILITIES
# =========================

st.header("AI Capabilities")

st.success(
    """
    ✔ Live Marketplace Monitoring

    ✔ AI Proposal Generation

    ✔ Autonomous Followup Systems

    ✔ AI Revenue Analytics

    ✔ Telegram Intelligence

    ✔ Continuous Runtime Operations
    """
)

# =========================
# PRICING
# =========================

st.header("Starting Packages")

p1, p2, p3 = st.columns(3)

with p1:

    st.markdown(
        """
        <div class="card">

        <h2>Starter</h2>

        <h1>₹15K+</h1>

        <ul>
            <li>Basic AI automation</li>
            <li>Telegram workflows</li>
            <li>CRM integrations</li>
            <li>Email automation</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )

with p2:

    st.markdown(
        """
        <div class="card">

        <h2>Business</h2>

        <h1>₹50K+</h1>

        <ul>
            <li>AI lead systems</li>
            <li>Proposal automation</li>
            <li>CRM dashboards</li>
            <li>Analytics engine</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )

with p3:

    st.markdown(
        """
        <div class="card">

        <h2>Enterprise</h2>

        <h1>Custom</h1>

        <ul>
            <li>Autonomous AI systems</li>
            <li>Revenue operations</li>
            <li>Healthcare automation</li>
            <li>Custom infrastructure</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# CONTACT
# =========================

st.header("Request A Consultation")

with st.form("contact_form"):

    name = st.text_input("Your Name")

    email = st.text_input("Email")

    company = st.text_input("Company")

    need = st.text_area(
        "What would you like to automate?"
    )

    submitted = st.form_submit_button(
        "Submit Request"
    )

    if submitted:

        st.success(
            "Consultation request submitted successfully."
        )

        st.write(
            {
                "name": name,
                "email": email,
                "company": company,
                "need": need
            }
        )

# =========================
# FOOTER
# =========================

st.markdown(
    """
    <div class="footer">

    PhantomOps AI © 2026<br>
    Autonomous AI Operations Infrastructure

    </div>
    """,
    unsafe_allow_html=True
)