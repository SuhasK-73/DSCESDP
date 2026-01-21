import streamlit as st
from groq import Groq
from PIL import Image
import base64
from io import BytesIO

st.set_page_config("PragyanAI Content Generator", layout="wide")
st.title("SUHAS K – Content Generator")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


# ---------- FUNCTION TO SET BACKGROUND ----------
def set_background(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        /* Optional overlay for readability */
        .block-container {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 12px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


col1, col2 = st.columns(2)

with col1:
    product = st.text_input("Product")
    audience = st.text_input("Audience")

    uploaded_image = st.file_uploader(
        "Upload Product Image (used as background)",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_image:
        image = Image.open(uploaded_image)
        set_background(image)

    if st.button("Generate Content"):
        prompt = f"Write marketing content for {product} targeting {audience}."
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        st.session_state.text = response.choices[0].message.content


with col2:
    if "text" in st.session_state:
        content = st.text_area(
            "Generated Content",
            st.session_state.text,
            height=300
        )

        st.download_button(
            label="⬇️ Download as TXT",
            data=content,
            file_name="marketing_copy.txt",
            mime="text/plain"
        )
    else:
        st.info("Generate content first")

