
import streamlit as st
import pandas as pd
from textwrap import dedent

from dashboard.agent_bridge import run_customer_workflow
from utils.integration_errors import IntegrationError


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Customer Intelligence Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# HTML RENDERING
# =====================================================

def render_html(content):
    st.markdown(
        dedent(content).strip(),
        unsafe_allow_html=True
    )


# =====================================================
# ANIMATED DESIGN
# =====================================================

render_html("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,.18), transparent 30%),
        radial-gradient(circle at 90% 80%, rgba(139,92,246,.15), transparent 30%),
        linear-gradient(135deg, #070b18, #10172d, #11102b);
    background-size: 200% 200%;
    animation: backgroundFlow 16s ease infinite;
}

@keyframes backgroundFlow {
    0% { background-position: 0% 0%; }
    50% { background-position: 100% 100%; }
    100% { background-position: 0% 0%; }
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(22px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes floating {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

.main-hero {
    position: relative;
    overflow: hidden;
    padding: 45px;
    border-radius: 24px;
    margin-bottom: 30px;
    background: linear-gradient(115deg, #172554, #3730a3, #6d28d9, #312e81);
    background-size: 300% 300%;
    border: 1px solid rgba(196,181,253,.4);
    animation: backgroundFlow 12s ease infinite, fadeUp 1s ease both;
}

.main-hero::after {
    content: "";
    position: absolute;
    width: 200px;
    height: 200px;
    top: -80px;
    right: 8%;
    border-radius: 50%;
    background: rgba(255,255,255,.13);
    filter: blur(5px);
    animation: floating 5s ease-in-out infinite;
    pointer-events: none;
}

.hero-tag {
    color: #ddd6fe;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 3px;
}

.main-hero h1 {
    color: white !important;
    font-size: 40px;
    font-weight: 850;
}

.main-hero p {
    color: #e0e7ff !important;
    font-size: 16px;
    line-height: 1.8;
}

.feature-card {
    min-height: 205px;
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(145deg, rgba(30,41,75,.9), rgba(17,24,48,.9));
    border: 1px solid rgba(129,140,248,.3);
    transition: all .35s ease;
    animation: fadeUp 1s ease both;
}

.feature-card:hover {
    transform: translateY(-8px);
    border-color: #a78bfa;
    box-shadow: 0 15px 35px rgba(99,102,241,.3);
}

.feature-icon {
    font-size: 36px;
    animation: floating 4s ease-in-out infinite;
}

.feature-card h3 {
    color: #c4b5fd !important;
    font-size: 20px;
}

.feature-card p {
    color: #cbd5e1 !important;
    font-size: 14px;
    line-height: 1.8;
}

.workflow-card {
    padding: 25px;
    border-radius: 20px;
    background: rgba(30,41,75,.7);
    border: 1px solid rgba(129,140,248,.3);
    animation: fadeUp 1s ease both;
}

.workflow-step {
    color: #c4b5fd;
    font-size: 16px;
    font-weight: 700;
}

[data-testid="stSidebar"] {
    background: #0b1020;
    border-right: 1px solid rgba(129,140,248,.25);
}

[data-testid="stMetric"] {
    background: rgba(30,41,75,.75);
    padding: 18px;
    border-radius: 16px;
    border: 1px solid rgba(129,140,248,.25);
    transition: transform .3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
}

.stButton button,
.stDownloadButton button {
    border-radius: 12px;
    background: linear-gradient(110deg,#4338ca,#7c3aed);
    border: 1px solid #8b5cf6;
    color: white;
    font-weight: 700;
}

@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation: none !important;
        transition: none !important;
    }
}

</style>
""")


# =====================================================
# DEMO DATA
# =====================================================

def create_demo_data():

    return pd.DataFrame({
        "customer_id": [
            "C001", "C002", "C003", "C004",
            "C005", "C006", "C007", "C008",
            "C009", "C010", "C011", "C012"
        ],
        "tenure": [2, 12, 36, 5, 48, 8, 60, 18, 4, 30, 54, 10],
        "monthly_charges": [95, 75, 45, 100, 55, 88, 40, 72, 105, 60, 48, 92],
        "contract": [
            "Month-to-month", "One year", "Two year",
            "Month-to-month", "Two year", "Month-to-month",
            "Two year", "One year", "Month-to-month",
            "One year", "Two year", "Month-to-month"
        ],
        "support_calls": [5, 2, 0, 6, 1, 4, 0, 2, 7, 1, 0, 5],
        "churn_probability": [
            .91, .48, .12, .87, .08, .73,
            .05, .38, .95, .25, .09, .78
        ]
    })


def mark_demo_dashboard_loaded():
    st.session_state["demo_dashboard_loaded"] = True


# =====================================================
# SIDEBAR NAVIGATION
# Keep the radio's selected page managed by its widget.
# =====================================================

st.sidebar.markdown("# 🧠 Customer AI")
st.sidebar.caption("INTELLIGENCE PLATFORM")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    ["Executive Dashboard", "Customer Analytics"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### PLATFORM MODULES")
st.sidebar.markdown("""
✦ Machine Learning

✦ Advanced RAG

✦ Agentic AI

✦ Customer Analytics
""")

st.sidebar.markdown("---")
st.sidebar.caption("Customer Intelligence | Capstone Project")


# =====================================================
# EXECUTIVE DASHBOARD
# =====================================================

if page == "Executive Dashboard":

    render_html("""
    <div class="main-hero">
        <div class="hero-tag">✦ NEXT-GENERATION AI ANALYTICS</div>
        <h1>Customer Intelligence Platform</h1>
        <p>
            Predict churn. Understand customers.
            Generate evidence-based retention strategies.
        </p>
    </div>
    """)

    st.markdown("## ✨ Platform Intelligence")

    st.write(
        "An integrated customer intelligence platform "
        "combining machine learning, advanced retrieval "
        "and coordinated AI agents."
    )

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        render_html("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3>Churn Prediction</h3>
            <p>Identify customers with potential churn risk using machine learning predictions.</p>
        </div>
        """)

    with col2:
        render_html("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <h3>Advanced RAG</h3>
            <p>Retrieve relevant business knowledge and supporting evidence using hybrid retrieval.</p>
        </div>
        """)

    with col3:
        render_html("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>Agentic AI</h3>
            <p>Coordinate customer analysis, retention recommendations and evidence verification.</p>
        </div>
        """)

    st.markdown("---")
    st.markdown("## ⚡ Intelligence Workflow")

    render_html("""
    <div class="workflow-card">
        <p class="workflow-step">01 &nbsp; Customer Data</p>
        <p style="color:#818cf8;">↓</p>
        <p class="workflow-step">02 &nbsp; Churn Prediction</p>
        <p style="color:#818cf8;">↓</p>
        <p class="workflow-step">03 &nbsp; Advanced Knowledge Retrieval</p>
        <p style="color:#818cf8;">↓</p>
        <p class="workflow-step">04 &nbsp; Agentic AI Processing</p>
        <p style="color:#818cf8;">↓</p>
        <p class="workflow-step">05 &nbsp; Verified Retention Insights</p>
    </div>
    """)

    st.markdown("---")
    st.info("Select **Customer Analytics** from the sidebar to explore the dashboard.")


# =====================================================
# CUSTOMER ANALYTICS
# =====================================================

elif page == "Customer Analytics":

    render_html("""
    <div class="main-hero">
        <div class="hero-tag">✦ CUSTOMER ANALYTICS WORKSPACE</div>
        <h1>Customer Risk Intelligence</h1>
        <p>Explore customer records, churn risk and customer profiles.</p>
    </div>
    """)

    uploaded_file = st.file_uploader(
        "Upload customer CSV",
        type=["csv"]
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("Dataset uploaded successfully.")
            is_demo_data = False
        except Exception as error:
            st.error(f"CSV reading error: {error}")
            st.stop()

    else:
        if not st.session_state.get("demo_dashboard_loaded", False):
            st.info("Upload a CSV or load synthetic demo records.")
            st.button(
                "Load Demo Dashboard",
                width="stretch",
                on_click=mark_demo_dashboard_loaded
            )
            st.stop()

        df = create_demo_data()
        is_demo_data = True
        st.warning("Synthetic demo data is being displayed.")

    if df.empty:
        st.warning("The dataset is empty.")
        st.stop()

    # FIND CHURN PROBABILITY COLUMN

    candidates = [
        "churn_probability",
        "churn probability",
        "churn_score",
        "churn score",
        "probability"
    ]

    probability_column = next(
        (column for column in candidates if column in df.columns),
        None
    )

    df = df.copy()

    if probability_column is not None:
        df[probability_column] = pd.to_numeric(
            df[probability_column],
            errors="coerce"
        )
        valid_probabilities = df[probability_column].dropna()
        if not valid_probabilities.empty and valid_probabilities.max() > 1:
            df[probability_column] = df[probability_column] / 100
        df[probability_column] = df[probability_column].clip(0, 1)
    else:
        st.warning(
            "No churn probability column was found. Customer records remain "
            "available, but churn metrics and ML-dependent workflow stages "
            "will be unavailable."
        )

    # RISK CATEGORIES

    def risk_category(value):
        if pd.isna(value):
            return "Unknown"
        if value >= .70:
            return "High"
        if value >= .40:
            return "Medium"
        return "Low"

    if probability_column is None:
        df["Risk Level"] = "Unknown"
    else:
        df["Risk Level"] = df[probability_column].apply(risk_category)

    # METRICS

    st.markdown("## 📊 Customer Overview")

    total = len(df)
    high = int((df["Risk Level"] == "High").sum())
    medium = int((df["Risk Level"] == "Medium").sum())
    low = int((df["Risk Level"] == "Low").sum())

    average = (
        df[probability_column].mean() * 100
        if probability_column is not None
        and df[probability_column].notna().any()
        else None
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Customers", total)
    c2.metric("High Risk", high)
    c3.metric("Medium Risk", medium)
    c4.metric(
        "Average Churn Score",
        f"{average:.1f}%" if average is not None else "Unavailable"
    )

    # FILTERS

    st.markdown("---")
    st.markdown("## 🔎 Customer Filters")

    f1, f2 = st.columns(2)

    risk_options = ["High", "Medium", "Low", "Unknown"]

    with f1:
        selected_risks = st.multiselect(
            "Risk category",
            risk_options,
            default=risk_options
        )

    with f2:
        search = st.text_input("Search customer ID")

    customer_column = next(
        (
            column for column in [
                "customer_id", "customerid", "customer id", "id"
            ]
            if column in df.columns
        ),
        None
    )

    if customer_column is None:
        df["customer_id"] = [
            f"CUST-{i + 1:04d}" for i in range(len(df))
        ]
        customer_column = "customer_id"

    filtered = df[
        df["Risk Level"].isin(selected_risks)
    ].copy()

    filtered = filtered[
        filtered[customer_column].astype(str).str.contains(
            search,
            case=False,
            na=False
        )
    ]

    # RISK DISTRIBUTION

    st.markdown("---")
    st.markdown("## 📈 Churn Risk Distribution")

    chart1, chart2 = st.columns(2)

    with chart1:
        risk_counts = (
            df["Risk Level"]
            .value_counts()
            .reindex(["High", "Medium", "Low"], fill_value=0)
        )
        st.bar_chart(risk_counts)

    with chart2:
        st.markdown("### Risk percentages")

        for name, count in risk_counts.items():
            percentage = count / total
            st.write(f"**{name}: {percentage * 100:.1f}%**")
            st.progress(float(percentage))

    # CUSTOMER TABLE

    st.markdown("---")
    st.markdown("## 👥 Customer Explorer")

    st.caption(f"Showing {len(filtered)} of {total} customers.")

    st.dataframe(
        filtered,
        width="stretch",
        hide_index=True
    )

    # CUSTOMER PROFILE

    st.markdown("---")
    st.markdown("## 🔍 Individual Customer Profile")

    if not filtered.empty:

        selected_customer = st.selectbox(
            "Select customer",
            filtered[customer_column].astype(str).tolist()
        )

        profile = filtered[
            filtered[customer_column].astype(str) == selected_customer
        ].iloc[0]

        p1, p2 = st.columns(2)

        with p1:
            st.markdown("### Customer details")
            st.metric("Customer ID", selected_customer)
            st.write(
                profile.drop(
                    labels=["Risk Level", customer_column],
                    errors="ignore"
                ).to_dict()
            )

        with p2:
            has_prediction = (
                probability_column is not None
                and pd.notna(profile[probability_column])
            )
            st.metric(
                "Churn Probability",
                (
                    f"{profile[probability_column] * 100:.1f}%"
                    if has_prediction
                    else "Unavailable"
                )
            )
            st.metric("Risk Category", profile["Risk Level"])

        st.markdown("### Evidence-grounded agent workflow")
        if is_demo_data and probability_column is not None:
            st.warning(
                "Demo only: the displayed probability is synthetic. "
                "No ML model has run for this record."
            )
            prediction_source = "synthetic_demo"
        elif has_prediction:
            st.caption(
                "The probability is read from the uploaded CSV. "
                "No ML model is invoked by this dashboard."
            )
            prediction_source = "uploaded_csv"
        else:
            st.warning(
                "No valid ML prediction is available for this customer. "
                "The agent workflow will report this missing prerequisite."
            )
            prediction_source = "unavailable"

        if st.button(
            "Run customer workflow",
            key="run_customer_agent_workflow",
            width="content"
        ):
            customer_data = profile.drop(
                labels=["Risk Level"],
                errors="ignore"
            ).to_dict()
            prediction_result = (
                {
                    "churn_probability": float(profile[probability_column]),
                    "source": prediction_source,
                }
                if has_prediction
                else None
            )
            try:
                workflow = run_customer_workflow(
                    customer_data,
                    prediction_result
                )
            except IntegrationError as error:
                st.error(
                    "The customer workflow failed "
                    f"({type(error).__name__}). No result is being shown."
                )
            else:
                st.write(f"**Workflow status:** {workflow['workflow_status']}")
                st.write(f"**Customer ID:** {selected_customer}")
                if prediction_result is not None:
                    st.write(
                        "**Churn probability:** "
                        f"{prediction_result['churn_probability']:.1%}"
                    )
                else:
                    st.write("**Churn probability:** unavailable")
                st.write(f"**Risk category:** {profile['Risk Level']}")

                if workflow["workflow_status"] in {
                    "missing_customer_data",
                    "missing_ml_prediction",
                }:
                    st.warning(workflow["message"])
                else:
                    analysis = workflow["analysis"]
                    st.write(
                        "**Analysis status:** "
                        f"{analysis['analysis_status']}"
                    )
                    st.caption(analysis["message"])

                    if workflow["retrieved_evidence"]:
                        st.markdown("#### Retrieved evidence")
                        for item in workflow["retrieved_evidence"]:
                            with st.container(border=True):
                                st.write(f"**Source:** {item['source_id']}")
                                st.write(item["text"])
                                metadata = item.get("metadata")
                                if metadata:
                                    st.json(metadata)
                    elif workflow["retrieval_status"] == "unavailable":
                        st.warning(
                            "No RAG retriever is integrated. "
                            "Recommendations are blocked."
                        )
                    else:
                        st.warning(
                            "The configured retriever returned no valid "
                            "evidence. Recommendations are blocked."
                        )

                    if workflow["recommendations"]:
                        st.markdown("#### Recommendations")
                        for item in workflow["recommendations"]:
                            st.write(f"- {item['recommendation']}")
                            st.caption(
                                "Sources: "
                                + ", ".join(item["source_ids"])
                            )
                        st.info(
                            "Source IDs and exact evidence quotations were "
                            "validated. Semantic entailment is not configured; "
                            "human review is still required."
                        )
                    else:
                        st.info(
                            "No recommendations were generated. A verified "
                            "strategy generator and sufficient evidence are "
                            "required."
                        )

                    st.write(
                        "**Verification status:** "
                        f"{workflow['verification']['verification_status']}"
                    )
                    if workflow["verification"]["rejected_recommendations"]:
                        st.warning("One or more recommendations were rejected.")
                        st.json(
                            workflow["verification"][
                                "rejected_recommendations"
                            ]
                        )

    else:
        st.info("No customers match the selected filters.")

    # EXPORT

    st.markdown("---")
    st.markdown("## 📥 Export")

    st.download_button(
        "Download Customer Report",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="customer_intelligence_report.csv",
        mime="text/csv",
        width="stretch"
    )

    st.caption(
        "Risk thresholds are illustrative. Synthetic demo data "
        "does not represent actual customer predictions."
    )


# =====================================================
# FOOTER
# =====================================================

st.markdown("---")
st.caption(
    "Customer Intelligence Platform | "
    "Agentic RAG-Based Customer Churn Intelligence and Retention System"
)
