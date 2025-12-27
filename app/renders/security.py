import streamlit as st

def render_security(report):
    data = report.get("SecurityAnalyzer", {})

    st.subheader("🔐 Security & Access")

    st.write("**Authentication:**")
    for method in data.get("authentication", []):
        st.success(method)

    st.write("**Access Control:**", data.get("access_control"))
    st.write("**Security Rating:**", data.get("security_rating"))
