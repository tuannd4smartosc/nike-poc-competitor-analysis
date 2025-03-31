import streamlit as st
import sys
from utils import StreamToExpander, show_confetti, markdown_to_pdf, get_pdf_download_link
from datetime import datetime, timedelta
from crew import run_analysis
import os
import traceback

FINAL_PDF_PATH="final_reports"

st.set_page_config(page_title="Competitor Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")

st.sidebar.title("Reports")
if not os.path.exists(FINAL_PDF_PATH):
    os.makedirs(FINAL_PDF_PATH)

report_files = [os.path.join(FINAL_PDF_PATH, f) for f in os.listdir(FINAL_PDF_PATH) if f.endswith(".md")]
selected_file = st.sidebar.selectbox("Select a Marketing Report", report_files)

st.title("Competitor Analysis Dashboard")
st.markdown("Analyze competitor pricing and promotions with a single click!")

date_end = datetime.now().date()

# Set date_start to roughly 1 year before date_end
date_start = date_end - timedelta(days=365)

company_name = st.text_input("Enter your company's name:", value = "Nike")
start_date = st.date_input("Pick a start date:",date_start)
end_date = st.date_input("Pick an end date:", date_end)
date_range = f"From: {start_date.strftime('%B %d, %Y')}. To: {end_date.strftime('%B %d, %Y')}"

if st.button("Run Competitor Analysis"):
    expander = st.expander("Processing Log", expanded=True, icon="🖥️")
    with st.spinner("Running analysis..."):
        original_stdout = sys.stdout
        stream_to_expander = StreamToExpander(expander, st)
        sys.stdout = stream_to_expander
        try:
            output_md_file = run_analysis(company_name, date_range)
            if output_md_file:
                logs = stream_to_expander.get_logs()
                report_files.append(os.path.basename(output_md_file))
                expander.expanded = False  # Collapse the log expander after completion
                st.success("Analysis complete! Check your Mailtrap inbox and see the results below.")
                show_confetti()
                selected_file = output_md_file
                # Save logs to temp file (optional, if you still want to persist logs)
                with open("temp_logs.txt", "w", encoding="utf-8") as f:
                    f.write(logs)
            else:
                st.warning("Analysis completed, but no output files were generated.")
        except Exception as e:
            error_details = traceback.format_exc()
            # Display both the error message and stack trace
            st.error(f"Error during analysis: {str(e)}\n\nDetails:\n{error_details}")
        finally:
            sys.stdout = original_stdout

# Display logs from temp file if it exists (optional)
if os.path.exists("temp_logs.txt"):
    with open("temp_logs.txt", "r", encoding="utf-8") as f:
        logs_content = f.read()
    if logs_content:
        expander = st.expander("Processing Log", expanded=False)
        expander.markdown(logs_content, unsafe_allow_html=True)
    os.remove("temp_logs.txt")

# Display selected report from sidebar (still functional)
if selected_file:
    with open(selected_file, "r") as f:
        report_content = f.read()
    st.markdown(report_content, unsafe_allow_html=True)

    pdf_path = selected_file.replace(".md", ".pdf")
    markdown_to_pdf(report_content, pdf_path)
    st.markdown(get_pdf_download_link(pdf_path, selected_file.replace(".md", ".pdf")), unsafe_allow_html=True)
    st.divider()
    
st.markdown(
    """
    <style>
    /* Existing styles */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #ffffff;
        color: #4CAF50;
        border: 1px solid #4CAF50;
    }
    .stSidebar {
        # background-color: #f8f9fa;
    }
    .stProgress .st-bo {
        # background-color: #4CAF50;
    }
    body {
        font-family: 'Arial', sans-serif;
    }
    h1, h2, h3 {
        # color: #2c3e50;
    }

    /* Log container styling */
    .log-container {
        width: 100%; /* Fill the full width of the expander */
        padding: 10px;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Log entry styling */
    .log-entry {
        margin-bottom: 8px;
        padding: 8px 12px;
        border-left: 4px solid;
        border-radius: 4px;
        animation: fadeIn 0.3s ease-in;
        word-break: break-word;
    }

    /* Fade-in animation */
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    </style>
    """,
    unsafe_allow_html=True
)