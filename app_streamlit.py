import streamlit as st
from rag import recommend
import requests

# 🔗 your n8n webhook
WEBHOOK_URL = "https://rounakdas.app.n8n.cloud/webhook-test/course-bot"

st.set_page_config(page_title="AI Course Bot", page_icon="🎓")

st.title("🎓 AI Course Recommendation Bot")
st.markdown("Get personalized FREE course suggestions 🚀")

# Inputs
name = st.text_input("Your Name")
email = st.text_input("Your Email")
goal = st.text_input("What do you want to learn?")

# Button
if st.button("Get Recommendation"):

    if name and email and goal:

        with st.spinner("Finding best courses for you..."):
            response = recommend(goal)

        st.success("Here are your recommendations:")
        st.write(response)

        # Send to n8n
        try:
            data = {
                "name": name,
                "email": email,
                "goal": goal,
                "recommendation": response
            }
            requests.post(WEBHOOK_URL, json=data)
        except:
            st.warning("Automation not connected")

    else:
        st.error("Please fill all fields")
