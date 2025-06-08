import base64
import streamlit as st
from PIL import Image
import openai
import io
import os

# 🔐 Your OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")  # <-- Replace with your actual key

st.set_page_config(page_title="Chart101", layout="centered")
st.title("📈 Chart101 – Your AI Trading Copilot")
st.subheader("Upload a stock chart. Get instant trading insights.")

uploaded_file = st.file_uploader("📤 Upload your chart", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Chart", use_column_width=True)

    if st.button("🔍 Analyze Chart"):
        st.info("🧠 Chart sent to Chart101 AI. Please wait...")

        # Convert image to bytes
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()

        # Vision + Text prompt to GPT-4o
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                          "You are a professional technical analyst. Analyze the uploaded stock chart "
                            "for a publicly listed Indian stock.\n\n"
                            "Return the analysis in the following format:\n\n"
                            "📈 Chart Context:\n"
                            "- Chart Type (e.g., Daily, Weekly, Monthly)\n"
                            "- Current Price (if visible)\n"
                            "- Candle Type (bullish/bearish/doji etc.)\n"
                            "- Time Period Covered (e.g., Jan 2023 – Jun 2025)\n"
                            "- Exchange (e.g., NSE/BSE)\n\n"
                            "🧠 Key Observations:\n"
                            "1. Trend Analysis\n"
                            "2. Support & Resistance\n"
                            "3. Pattern Detected (e.g., Cup & Handle, Triangle)\n"
                            "4. Candlestick Behavior (body, wicks, gaps)\n"
                            "5. Volume Insight (if visible — else mention volume not shown)\n\n"
                            "✅ Bullish/Bearish Signals (bullet points)\n\n"
                            "⚠️ Risks / What to Watch Out For:\n"
                            "- Potential pullbacks or invalidations\n"
                            "- Exhaustion signals\n\n"
                            "🔧 Strategy Suggestions:\n"
                            "- For existing holders\n"
                            "- For fresh entry seekers\n"
                            "- Where to place stop-loss or trail it\n\n"
                            "📊 Confidence Rating (out of 100%)\n\n"
                            "Be specific but concise. Write like a real trader journaling his notes. "
                            "Avoid giving investment advice or speculative calls."
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "data:image/png;base64," + base64.b64encode(image_bytes).decode()
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )

        # Extract response
        result = response.choices[0].message.content
        st.markdown("### 🧠 Chart101 AI Analysis:")
        st.success(result)
