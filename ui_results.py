import streamlit as st
from pathlib import Path

def render_score_circle(score: int):
    if score >= 75:
        color = "#2ecc71"   # green
        label = "Strong Fit"
    elif score >= 55:
        color = "#f1c40f"   # yellow
        label = "Moderate Fit"
    else:
        color = "#e74c3c"   # red
        label = "Low Fit"

    st.markdown(
        f"""
        <div style="
            width:140px;
            height:140px;
            border-radius:50%;
            background: conic-gradient(
                {color} {score*3.6}deg,
                #eeeeee 0deg
            );
            display:flex;
            align-items:center;
            justify-content:center;
            margin:auto;
        ">
            <div style="
                width:110px;
                height:110px;
                background:white;
                border-radius:50%;
                display:flex;
                flex-direction:column;
                align-items:center;
                justify-content:center;
                font-family:sans-serif;
            ">
                <div style="font-size:28px;font-weight:bold;">{score}%</div>
                <div style="font-size:12px;color:#555;">{label}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_results_view():
    st.title("Results")

    if st.button("← Back", key="back_btn"):
        st.session_state.view = "form"
        st.rerun()

    preview = st.session_state.get("preview")
    output_path = st.session_state.get("output_path")

    if not preview and not output_path:
        st.warning("No report found. Please generate a report first.")
        return

    # ---- Quick Preview ----
    if preview:
        st.subheader("Quick Preview")

        col1, col2 = st.columns(2)
        with col1:
            render_score_circle(preview.get("score_pct", 0))
        with col2:
            st.write("**Verdict**")
            st.write(preview.get("verdict", ""))

        st.write("---")

        c1, c2 = st.columns(2)
        with c1:
            st.write("### ✅ Top Strengths")
            strengths = preview.get("strengths", []) or []
            if strengths:
                for s in strengths:
                    st.write(f"- {s}")
            else:
                st.write("- (No strengths returned)")

        with c2:
            st.write("### ⚠️ Top Risks")
            gaps = preview.get("gaps", []) or []
            if gaps:
                for g in gaps:
                    st.write(f"- {g}")
            else:
                st.write("- (No gaps returned)")

        st.write("### 🎯 Next Actions (7 Days)")
        actions = preview.get("actions", []) or []
        if actions:
            for a in actions:
                st.write(f"- {a}")
        else:
            st.write("- (No actions returned)")

    # ---- Download PDF ----
    if output_path:
        st.info(f"Latest report: {Path(output_path).name}")

        with open(output_path, "rb") as f:
            st.download_button(
                label="Download PDF Report",
                data=f,
                file_name=Path(output_path).name,
                mime="application/pdf",
                key="download_btn"
            )
