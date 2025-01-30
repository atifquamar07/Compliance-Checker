import streamlit as st
import requests

st.set_page_config(page_title="Compliance Checker", layout="wide")
st.title("Compliance Checker")

# Input fields
webpage_url = st.text_input("Webpage URL", placeholder="Enter webpage URL")
policy_url = st.text_input("Policy URL", placeholder="Enter policy URL")

if st.button("Check Compliance"):
    if not webpage_url or not policy_url:
        st.warning("Please fill both URL fields")
    else:
        payload = {
            "webpage_url": webpage_url,
            "policy_url": policy_url
        }
        
        try:
            response = requests.post(
                "http://api.insituate.ai:8050/check-compliance",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Display results
                st.subheader("Compliance Check Results")
                st.write(f"**Webpage URL:** {result['webpage_url']}")
                st.write(f"**Policy URL:** {result['policy_url']}")
                st.write(f"**Scan Timestamp:** {result['scan_timestamp']}")
                
                # Display violations
                st.subheader("Violations Found", divider="red")
                for i, violation in enumerate(result.get('violations', []), 1):
                    # Modified suggestion display in the expander section
                    with st.expander(f"Violation {i}: {violation['type'].replace('$', '\\$')} ({violation['severity'].title()} Severity)", expanded=True):
                        st.markdown(f"**Description:** {violation['description'].replace('$', '\\$')}")
                        st.markdown(f"**Context:** `{violation['context'].replace('$', '\\$')}`")
                        
                        # Fix: Add .replace() to handle dollar signs
                        fixed_suggestion = violation['suggestion'].replace('$', '\\$')
                        st.markdown(f"**Suggestion:** {fixed_suggestion}")
                        
            else:
                st.error(f"API request failed with status code {response.status_code}")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")