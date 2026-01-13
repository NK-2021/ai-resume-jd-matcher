import streamlit as st

from ui_form import render_form_view
from ui_results import render_results_view

st.set_page_config(page_title="AI Resume ↔ JD Matcher", layout="centered")

# -------- Session State Defaults --------
if "view" not in st.session_state:
    st.session_state.view = "form"  # "form" | "result"

if "output_path" not in st.session_state:
    st.session_state.output_path = None

if "preview" not in st.session_state:
    st.session_state.preview = None

if "last_error" not in st.session_state:
    st.session_state.last_error = None

# If somehow an invalid view value gets set, recover gracefully
if st.session_state.view not in ("form", "result"):
    st.session_state.view = "form"

# -------- Router --------
if st.session_state.view == "form":
    render_form_view()
else:
    render_results_view()
