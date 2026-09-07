import requests
import plotly.express as px
import streamlit as st


# ============================================================
# Configuration
# ============================================================

API_URL = "http://127.0.0.1:8000/api/v1/analyze"
REQUEST_TIMEOUT = 10


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Pipeline Health Monitor",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# Session State
# ============================================================

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None


# ============================================================
# API Client
# ============================================================

def analyze_pipeline(payload: dict) -> dict:
    """
    Send pipeline data to the FastAPI backend
    and return the analysis result.
    """

    response = requests.post(
        API_URL,
        json=payload,
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.title("Pipeline Monitor")

    st.markdown(
        """
        ### Dashboard

        Monitor ETL pipeline health by entering
        the latest pipeline execution details.
        """
    )

    st.divider()

    st.info(
        "Backend: FastAPI\n\n"
        "Frontend: Streamlit"
    )


# ============================================================
# Header
# ============================================================

st.title("Pipeline Health Monitor")

st.write(
    "Analyze the health and data quality of an ETL pipeline."
)


# ============================================================
# Input Form
# ============================================================

with st.form("pipeline_form"):

    st.subheader("Pipeline Execution Details")

    col1, col2, col3 = st.columns(3)

    with col1:

        pipeline_name = st.text_input(
            "Pipeline Name",
            value="customer_etl",
        )

        records_processed = st.number_input(
            "Records Processed",
            min_value=0,
            value=10000,
            step=100,
        )

    with col2:

        failed_records = st.number_input(
            "Failed Records",
            min_value=0,
            value=100,
            step=10,
        )

        null_percentage = st.number_input(
            "Null Percentage",
            min_value=0.0,
            max_value=100.0,
            value=2.0,
            step=0.5,
        )

    with col3:

        duplicate_percentage = st.number_input(
            "Duplicate Percentage",
            min_value=0.0,
            max_value=100.0,
            value=1.0,
            step=0.5,
        )

        processing_time = st.number_input(
            "Processing Time (seconds)",
            min_value=0.0,
            value=120.0,
            step=10.0,
        )

    submitted = st.form_submit_button(
        "Analyze Pipeline",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# Handle Form Submission
# ============================================================

if submitted:

    payload = {
        "pipeline_name": pipeline_name.strip(),
        "records_processed": records_processed,
        "failed_records": failed_records,
        "null_percentage": null_percentage,
        "duplicate_percentage": duplicate_percentage,
        "processing_time": processing_time,
    }

    # Basic frontend validation
    if not pipeline_name.strip():

        st.error("Pipeline name cannot be empty.")

    elif failed_records > records_processed:

        st.error(
            "Failed records cannot exceed processed records."
        )

    else:

        try:

            with st.spinner("Analyzing pipeline..."):

                result = analyze_pipeline(payload)

            st.session_state.analysis_result = result

            st.success(
                "Pipeline analysis completed successfully."
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "Unable to connect to the FastAPI backend. "
                "Make sure the API is running on port 8000."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The request timed out. "
                "Please try again."
            )

        except requests.exceptions.HTTPError as exc:

            try:
                error_detail = exc.response.json().get(
                    "detail",
                    "Backend returned an error.",
                )
            except (ValueError, AttributeError):
                error_detail = "Backend returned an error."

            st.error(
                f"API Error: {error_detail}"
            )

        except requests.exceptions.RequestException:

            st.error(
                "An error occurred while communicating "
                "with the backend."
            )

        except ValueError:

            st.error(
                "The backend returned an invalid response."
            )


# ============================================================
# Display Analysis Result
# ============================================================

result = st.session_state.analysis_result


if result:

    # ========================================================
    # Pipeline Summary
    # ========================================================

    st.subheader("Pipeline Summary")

    metric1, metric2, metric3 = st.columns(3)

    with metric1:

        st.metric(
            label="Status",
            value=result["status"],
        )

    with metric2:

        st.metric(
            label="Success Rate",
            value=f'{result["success_rate"]}%',
        )

    with metric3:

        st.metric(
            label="Quality Score",
            value=f'{result["quality_score"]}/100',
        )

    # ========================================================
    # Data Quality Chart
    # ========================================================

    st.subheader("Data Quality Metrics")

    chart_data = {
        "Metric": [
            "Success Rate",
            "Quality Score",
        ],
        "Score": [
            result["success_rate"],
            result["quality_score"],
        ],
    }

    # Center and reduce chart width
    _, chart_col, _ = st.columns([1, 2, 1])

    with chart_col:

        fig = px.bar(
            chart_data,
            x="Metric",
            y="Score",
            color_discrete_sequence=["lightgreen"],
            range_y=[0, 100],
        )

        fig.update_layout(
            height=350,
            showlegend=False,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # ========================================================
    # Recommendations
    # ========================================================

    st.subheader("Recommendations")

    for recommendation in result["recommendations"]:

        st.write(
            f"• {recommendation}"
        )

