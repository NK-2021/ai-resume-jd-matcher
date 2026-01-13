import streamlit as st
import traceback

from pipeline import generate_report


def render_form_view():
    st.title("AI Resume ↔ Job Description Matcher")
    st.write("Generate a professional Resume–JD matching report (PDF).")

    with st.form("report_form", clear_on_submit=False):
        resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
        resume_text = st.text_area("Or paste resume text (optional)", height=180)
        jd_text = st.text_area("Paste Job Description", height=180)

        target_role = st.text_input("Target Role (optional)", placeholder="e.g. Frontend Engineer")
        seniority = st.selectbox(
            "Seniority Level (optional)",
            ["Not specified", "Intern", "Junior", "Mid", "Senior", "Lead"]
        )

        submitted = st.form_submit_button("Generate Report")

    log_box = st.empty()

    if submitted:
        st.session_state.last_error = None
        st.session_state.output_path = None
        st.session_state.preview = None

        if not jd_text or (not resume_file and not (resume_text and resume_text.strip())):
            st.error("Please provide a resume (upload or paste) and a job description.")
            return

        try:
            with st.spinner("Analyzing resume and job description..."):
                out_path, preview = generate_report(
                    resume_file=resume_file,
                    resume_text=resume_text,
                    jd_text=jd_text,
                    target_role=target_role,
                    seniority=seniority,
                    ui_log=log_box,
                )

            st.session_state.output_path = out_path
            st.session_state.preview = preview
            st.success("Report generated successfully!")

            st.session_state.view = "result"
            st.rerun()

        except Exception:
            st.session_state.last_error = traceback.format_exc()
            st.error("Failed to generate report.")
            st.code(st.session_state.last_error)
