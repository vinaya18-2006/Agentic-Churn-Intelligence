
import streamlit as st
import pandas as pd


# --------------------------------------------------
# DEMO DATA
# --------------------------------------------------

def create_demo_data():

    data = {
        "Customer ID": [
            f"CUST{i:03d}" for i in range(1, 13)
        ],
        "Tenure": [
            2, 5, 12, 24, 36, 8,
            18, 3, 48, 30, 6, 42
        ],
        "Monthly Charges": [
            85, 75, 55, 45, 60, 90,
            50, 95, 40, 65, 88, 42
        ],
        "Contract": [
            "Month-to-month",
            "Month-to-month",
            "One year",
            "Two year",
            "Two year",
            "Month-to-month",
            "One year",
            "Month-to-month",
            "Two year",
            "One year",
            "Month-to-month",
            "Two year"
        ],
        "Churn Probability": [
            0.92, 0.84, 0.35, 0.12,
            0.18, 0.78, 0.42, 0.95,
            0.08, 0.32, 0.72, 0.15
        ]
    }

    df = pd.DataFrame(data)

    df["Risk Level"] = df["Churn Probability"].apply(
        lambda x: (
            "High" if x >= 0.70
            else "Medium" if x >= 0.40
            else "Low"
        )
    )

    return df


# --------------------------------------------------
# COLUMN DETECTION
# --------------------------------------------------

def find_column(df, possible_names):

    for column in df.columns:

        normalized = (
            column.lower()
            .strip()
            .replace("_", " ")
        )

        if normalized in possible_names:
            return column

    return None


# --------------------------------------------------
# CUSTOMER DASHBOARD CSS
# --------------------------------------------------

def inject_customer_css():

    st.markdown("""
    <style>

    /* Hero */

    .customer-hero {
        position: relative;
        overflow: hidden;
        padding: 38px;
        border-radius: 22px;

        background: linear-gradient(
            115deg,
            #172554,
            #4338ca,
            #6d28d9,
            #312e81
        );

        background-size: 300% 300%;

        animation: customerGradient 12s ease infinite;

        border: 1px solid rgba(196,181,253,0.3);
        box-shadow: 0 10px 35px rgba(79,70,229,0.18);
    }

    @keyframes customerGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes customerFade {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes customerFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }

    .customer-hero h1 {
        color: white;
        font-size: 36px;
        font-weight: 850;
        animation: customerFade 1s ease both;
    }

    .customer-hero p {
        color: #ddd6fe;
        font-size: 15px;
    }

    .customer-hero .tag {
        color: #c4b5fd;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 3px;
    }

    /* KPI cards */

    [data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            rgba(30,41,75,0.9),
            rgba(17,24,48,0.9)
        );

        border: 1px solid rgba(129,140,248,0.3);
        border-radius: 17px;
        padding: 20px;

        animation: customerFade 0.8s ease both;

        transition: all 0.35s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: #a78bfa;
        box-shadow: 0 15px 35px rgba(99,102,241,0.3);
    }

    [data-testid="stMetricValue"] {
        color: #c4b5fd;
        font-weight: 800;
    }

    /* Buttons */

    .stButton button,
    .stDownloadButton button {
        border-radius: 12px;
        background: linear-gradient(110deg,#4338ca,#7c3aed);
        border: 1px solid #8b5cf6;
        color: white;
        font-weight: 700;
        transition: all 0.3s ease;
    }

    .stButton button:hover,
    .stDownloadButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(124,58,237,0.4);
    }

    /* Tables and charts */

    [data-testid="stDataFrame"],
    [data-testid="stPlotlyChart"],
    [data-testid="stVegaLiteChart"] {
        border-radius: 16px;
        animation: customerFade 0.8s ease both;
    }

    /* Section headings */

    h2, h3 {
        animation: customerFade 0.7s ease both;
    }

    /* Alerts */

    [data-testid="stAlert"] {
        border-radius: 14px;
        animation: customerFade 0.6s ease both;
    }

    /* Reduced motion */

    @media (prefers-reduced-motion: reduce) {
        *,
        *::before,
        *::after {
            animation: none !important;
            transition: none !important;
        }
    }

    </style>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# MAIN CUSTOMER VIEW
# --------------------------------------------------

def render_customer_view():

    inject_customer_css()

    # HERO

    st.markdown("""
    <div class="customer-hero">

        <div class="tag">
            ✦ CUSTOMER INTELLIGENCE CENTER
        </div>

        <h1>Customer Analytics</h1>

        <p>
            Discover customer behaviour, explore churn risk
            and understand customer intelligence.
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # DATA UPLOAD

    st.markdown("## 📂 Customer Data Workspace")

    uploaded_file = st.file_uploader(
        "Upload customer dataset",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:
            df = pd.read_csv(uploaded_file)
            st.success("Dataset uploaded successfully.")

        except Exception as error:
            st.error(f"Unable to read the file: {error}")
            return

    else:

        st.info(
            "Demo mode: Synthetic customer records are used "
            "until you upload your own CSV."
        )

        if st.button(
            "✨ Load Demo Dashboard",
            use_container_width=True
        ):
            st.session_state["demo_loaded"] = True

        if not st.session_state.get("demo_loaded", False):
            st.write("Load the demo dashboard to continue.")
            return

        df = create_demo_data()

    if df.empty:
        st.warning("The dataset contains no customer records.")
        return

    # DETECT COLUMNS

    customer_col = find_column(
        df,
        {
            "customer id",
            "customerid",
            "customer"
        }
    )

    probability_col = find_column(
        df,
        {
            "churn probability",
            "churn score",
            "probability",
            "churn risk score"
        }
    )

    contract_col = find_column(
        df,
        {
            "contract",
            "contract type"
        }
    )

    risk_col = find_column(
        df,
        {
            "risk level",
            "churn risk",
            "risk category"
        }
    )

    # PREPARE PROBABILITY

    if probability_col is not None:

        df[probability_col] = pd.to_numeric(
            df[probability_col],
            errors="coerce"
        )

        valid_values = df[probability_col].dropna()

        if not valid_values.empty and valid_values.max() > 1:
            df[probability_col] = df[probability_col] / 100

        df[probability_col] = df[probability_col].clip(0, 1)

        if risk_col is None:

            risk_col = "Risk Level"

            df[risk_col] = df[probability_col].apply(
                lambda x: (
                    "High" if pd.notna(x) and x >= 0.70
                    else "Medium" if pd.notna(x) and x >= 0.40
                    else "Low" if pd.notna(x)
                    else "Unknown"
                )
            )

    else:

        st.warning(
            "No churn probability column found. "
            "Churn-specific metrics will not be displayed."
        )

    # SIDEBAR FILTERS

    st.sidebar.markdown("## 🎛️ Analytics Filters")

    filtered_df = df.copy()

    if risk_col is not None and risk_col in filtered_df.columns:

        risk_options = sorted(
            filtered_df[risk_col]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_risks = st.sidebar.multiselect(
            "Risk Level",
            risk_options,
            default=risk_options
        )

        filtered_df = filtered_df[
            filtered_df[risk_col].astype(str).isin(selected_risks)
        ]

    if contract_col is not None:

        contract_options = sorted(
            filtered_df[contract_col]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_contracts = st.sidebar.multiselect(
            "Contract Type",
            contract_options,
            default=contract_options
        )

        filtered_df = filtered_df[
            filtered_df[contract_col].astype(str).isin(
                selected_contracts
            )
        ]

    # KPI METRICS

    st.markdown("## ⚡ Customer Performance Overview")

    col1, col2, col3, col4 = st.columns(4)

    total_customers = len(filtered_df)

    high_risk_count = 0
    average_probability = None
    above_70_count = None

    if risk_col is not None and risk_col in filtered_df.columns:

        high_risk_count = (
            filtered_df[risk_col]
            .astype(str)
            .str.lower() == "high"
        ).sum()

    if probability_col is not None:

        valid_probabilities = filtered_df[
            probability_col
        ].dropna()

        if not valid_probabilities.empty:

            average_probability = valid_probabilities.mean()

            above_70_count = (
                valid_probabilities >= 0.70
            ).sum()

    col1.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

    col2.metric(
        "High Risk Customers",
        f"{high_risk_count:,}"
    )

    col3.metric(
        "Average Churn Probability",
        (
            f"{average_probability:.1%}"
            if average_probability is not None
            else "N/A"
        )
    )

    col4.metric(
        "Customers Above 70%",
        (
            f"{above_70_count:,}"
            if above_70_count is not None
            else "N/A"
        )
    )

    st.divider()

    # CHARTS

    st.markdown("## 📊 Customer Risk Intelligence")

    chart1, chart2 = st.columns(2)

    with chart1:

        st.markdown("### Risk Distribution")

        if risk_col is not None:

            risk_counts = (
                filtered_df[risk_col]
                .fillna("Unknown")
                .value_counts()
            )

            st.bar_chart(risk_counts)

        else:
            st.info("Risk information is unavailable.")

    with chart2:

        st.markdown("### Churn Probability")

        if probability_col is not None:

            probability_data = filtered_df[
                [probability_col]
            ].dropna()

            st.bar_chart(probability_data)

        else:
            st.info("Churn probability is unavailable.")

    st.divider()

    # CUSTOMER SEARCH

    st.markdown("## 🔍 Customer Explorer")

    if customer_col is not None:

        search_text = st.text_input(
            "Search customer",
            placeholder="Enter customer ID..."
        )

        if search_text:

            filtered_df = filtered_df[
                filtered_df[customer_col]
                .astype(str)
                .str.contains(
                    search_text,
                    case=False,
                    na=False
                )
            ]

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # CUSTOMER PROFILE

    if customer_col is not None and not filtered_df.empty:

        st.markdown("## 👤 Individual Customer Intelligence")

        customer_options = (
            filtered_df[customer_col]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        if customer_options:

            selected_customer = st.selectbox(
                "Select customer profile",
                customer_options
            )

            record = filtered_df[
                filtered_df[customer_col].astype(str)
                == selected_customer
            ].iloc[0]

            profile1, profile2 = st.columns(2)

            with profile1:

                st.markdown("### Customer Information")

                st.json(record.to_dict())

            with profile2:

                st.markdown("### Churn Assessment")

                if probability_col is not None:

                    probability = record[probability_col]

                    if pd.notna(probability):

                        st.metric(
                            "Churn Probability",
                            f"{probability:.1%}"
                        )

                        if probability >= 0.70:
                            st.error("HIGH CHURN RISK")

                        elif probability >= 0.40:
                            st.warning("MEDIUM CHURN RISK")

                        else:
                            st.success("LOW CHURN RISK")

                    else:
                        st.info("Probability is unavailable.")

                else:
                    st.info(
                        "No churn probability is available "
                        "for this customer."
                    )

    # EXPORT

    st.divider()

    st.markdown("## 📥 Export Analytics")

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Customer Report",
        data=csv_data,
        file_name="customer_intelligence_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.caption(
        "Demo risk bands: High ≥70%, Medium ≥40% and Low <40%. "
        "These are illustrative thresholds, not validated "
        "business decision thresholds."
    )
