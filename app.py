import streamlit as st
import pandas as pd
import re


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AgentCart AI",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #f6f7fb;
}


/* ================= HERO ================= */

.hero {
    background: linear-gradient(135deg, #111827, #312e81);
    padding: 40px;
    border-radius: 25px;
    margin-bottom: 30px;
    color: white;
}

.hero-title {
    font-size: 44px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 18px;
    color: #dbeafe;
    line-height: 1.6;
}


/* ================= CARDS ================= */

.card {
    background: white;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    margin-bottom: 20px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.04);
}

.product-card {
    background: white;
    padding: 22px;
    border-radius: 20px;
    border: 1px solid #e5e7eb;
    min-height: 360px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.05);
}

.product-name {
    font-size: 21px;
    font-weight: 700;
    margin-bottom: 8px;
}

.product-price {
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 15px;
}

.product-info {
    line-height: 2;
    color: #374151;
}

.ai-score {
    display: inline-block;
    background: #eef2ff;
    color: #3730a3;
    padding: 7px 13px;
    border-radius: 20px;
    font-weight: 700;
    margin-top: 10px;
}

.reason {
    background: #f0fdf4;
    border-left: 4px solid #22c55e;
    padding: 14px;
    border-radius: 10px;
    margin-top: 15px;
    color: #166534;
}


/* ================= SECTION ================= */

.section-title {
    font-size: 28px;
    font-weight: 800;
    margin-top: 20px;
    margin-bottom: 20px;
}


/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white;
}


/* ================= BUTTON ================= */

.stButton > button {
    border-radius: 12px;
    font-weight: 700;
    min-height: 45px;
}


/* ================= INPUT ================= */

textarea {
    border-radius: 12px !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# PRODUCT DATABASE
# ============================================================

products = pd.DataFrame([
    {
        "name": "ASUS Vivobook 15",
        "category": "Laptop",
        "price": 54990,
        "ram": 16,
        "storage": 512,
        "processor": "Intel Core i5",
        "gpu": "Integrated",
        "rating": 4.4,
        "battery": 7,
        "use": "Coding AI ML Student"
    },

    {
        "name": "HP Pavilion 14",
        "category": "Laptop",
        "price": 58990,
        "ram": 16,
        "storage": 512,
        "processor": "Intel Core i5",
        "gpu": "Integrated",
        "rating": 4.3,
        "battery": 8,
        "use": "Coding Student"
    },

    {
        "name": "Acer Aspire 7",
        "category": "Laptop",
        "price": 59990,
        "ram": 16,
        "storage": 512,
        "processor": "AMD Ryzen 5",
        "gpu": "RTX 2050",
        "rating": 4.5,
        "battery": 6,
        "use": "Gaming AI ML"
    },

    {
        "name": "Lenovo IdeaPad Slim 5",
        "category": "Laptop",
        "price": 62990,
        "ram": 16,
        "storage": 512,
        "processor": "AMD Ryzen 7",
        "gpu": "Integrated",
        "rating": 4.6,
        "battery": 9,
        "use": "Coding AI ML Student"
    },

    {
        "name": "Dell Inspiron 15",
        "category": "Laptop",
        "price": 57990,
        "ram": 16,
        "storage": 512,
        "processor": "Intel Core i5",
        "gpu": "Integrated",
        "rating": 4.2,
        "battery": 7,
        "use": "Coding Student"
    },

    {
        "name": "Lenovo LOQ Gaming",
        "category": "Laptop",
        "price": 69990,
        "ram": 16,
        "storage": 512,
        "processor": "Intel Core i5",
        "gpu": "RTX 3050",
        "rating": 4.7,
        "battery": 6,
        "use": "Gaming AI ML"
    },

    {
        "name": "HP Victus",
        "category": "Laptop",
        "price": 67990,
        "ram": 16,
        "storage": 512,
        "processor": "AMD Ryzen 5",
        "gpu": "RTX 3050",
        "rating": 4.6,
        "battery": 6,
        "use": "Gaming AI ML"
    },

    {
        "name": "MacBook Air M2",
        "category": "Laptop",
        "price": 74990,
        "ram": 8,
        "storage": 256,
        "processor": "Apple M2",
        "gpu": "Integrated",
        "rating": 4.8,
        "battery": 15,
        "use": "Coding Student"
    }
])


# ============================================================
# BUDGET EXTRACTION
# ============================================================

def extract_budget(text):

    text = text.lower()

    # Find values such as 60000
    numbers = re.findall(r'\d[\d,]*', text)

    values = []

    for number in numbers:

        number = number.replace(",", "")

        try:
            values.append(int(number))
        except ValueError:
            pass

    # Find values such as 60k
    k_values = re.findall(r'(\d+(?:\.\d+)?)\s*k', text)

    for value in k_values:

        try:
            values.append(int(float(value) * 1000))
        except ValueError:
            pass

    if values:
        return max(values)

    return None


# ============================================================
# USE-CASE DETECTION
# ============================================================

def detect_use_cases(text):

    text = text.lower()

    detected = []

    if (
        "ai" in text
        or "machine learning" in text
        or "ml" in text
    ):
        detected.append("AI ML")

    if (
        "coding" in text
        or "programming" in text
        or "developer" in text
    ):
        detected.append("Coding")

    if (
        "gaming" in text
        or "gaming laptop" in text
        or "games" in text
    ):
        detected.append("Gaming")

    if (
        "student" in text
        or "college" in text
        or "study" in text
    ):
        detected.append("Student")

    return detected


# ============================================================
# PRODUCT RECOMMENDATION ENGINE
# ============================================================

def recommend_products(user_request):

    budget = extract_budget(user_request)

    use_cases = detect_use_cases(user_request)

    data = products.copy()

    # ---------------- Budget filter ----------------

    if budget:

        data = data[
            data["price"] <= budget
        ]

    # ---------------- If no products ----------------

    if data.empty:

        return data, budget, use_cases

    # ---------------- Calculate AI score ----------------

    scores = []

    for _, product in data.iterrows():

        score = 0

        # Product rating
        score += product["rating"] * 15

        # RAM
        score += product["ram"] * 1.2

        # Storage
        score += product["storage"] / 100

        # Battery
        score += product["battery"] * 1.5

        # Use case matching
        for use_case in use_cases:

            if use_case in product["use"]:

                score += 20

        # GPU bonus
        if (
            "AI ML" in use_cases
            and "RTX" in product["gpu"]
        ):

            score += 25

        if (
            "Gaming" in use_cases
            and "RTX" in product["gpu"]
        ):

            score += 25

        scores.append(score)

    data["ai_score"] = scores

    data = data.sort_values(
        by="ai_score",
        ascending=False
    )

    return data.head(3), budget, use_cases


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🛒 AgentCart AI")

    st.markdown("---")

    st.markdown("### Navigation")

    page = st.radio(
        "Choose a page",
        [
            "🤖 AI Shopping Agent",
            "🔎 Product Explorer",
            "🧠 How It Works"
        ]
    )

    st.markdown("---")

    st.markdown("### 🤖 Agent Status")

    st.success("AI Agent Online")

    st.write("🟢 Recommendation Engine")
    st.write("🟢 Personalization Engine")
    st.write("🟢 Product Database")


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
🛒 AgentCart AI
</div>

<div class="hero-subtitle">
Your intelligent AI shopping companion.<br>
Describe what you need and let AgentCart AI
research, compare and recommend suitable products.
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# AI SHOPPING AGENT
# ============================================================

if page == "🤖 AI Shopping Agent":

    st.markdown(
        '<div class="section-title">🤖 AI Shopping Agent</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Describe your shopping requirement in normal language."
    )

    user_request = st.text_area(
        "What are you looking for?",
        placeholder=(
            "Example: I need a laptop under ₹60,000 "
            "for coding and AI/ML"
        ),
        height=120
    )

    if st.button(
        "✨ Ask Agent",
        type="primary",
        use_container_width=True
    ):

        if not user_request.strip():

            st.warning(
                "Please enter your shopping requirement."
            )

        else:

            with st.spinner(
                "🤖 Agent is analyzing your requirements..."
            ):

                recommendations, budget, use_cases = (
                    recommend_products(user_request)
                )

            # ---------------- Analysis ----------------

            st.markdown("## 🧠 Agent Analysis")

            col1, col2, col3 = st.columns(3)

            with col1:

                if budget:

                    st.metric(
                        "💰 Detected Budget",
                        f"₹{budget:,}"
                    )

                else:

                    st.metric(
                        "💰 Detected Budget",
                        "Not detected"
                    )

            with col2:

                st.metric(
                    "🎯 Requirements",
                    len(use_cases)
                )

            with col3:

                st.metric(
                    "🔎 Products Found",
                    len(recommendations)
                )

            if use_cases:

                st.info(
                    "🎯 Detected use cases: "
                    + ", ".join(use_cases)
                )

            # ---------------- Recommendations ----------------

            if recommendations.empty:

                st.error(
                    "❌ No products were found within "
                    "your budget."
                )

                st.write(
                    "Try increasing your budget or "
                    "changing your requirements."
                )

            else:

                st.markdown(
                    "## 🏆 AI Recommendations"
                )

                columns = st.columns(
                    len(recommendations)
                )

                for column, (_, product) in zip(
                    columns,
                    recommendations.iterrows()
                ):

                    with column:

                        st.markdown(
                            f"""
                            <div class="product-card">

                            <div class="product-name">
                            {product['name']}
                            </div>

                            <div class="product-price">
                            ₹{product['price']:,}
                            </div>

                            <div class="product-info">

                            ⚡ <b>Processor:</b>
                            {product['processor']}<br>

                            🧠 <b>RAM:</b>
                            {product['ram']} GB<br>

                            💾 <b>Storage:</b>
                            {product['storage']} GB<br>

                            🎮 <b>GPU:</b>
                            {product['gpu']}<br>

                            🔋 <b>Battery:</b>
                            {product['battery']} hours<br>

                            ⭐ <b>Rating:</b>
                            {product['rating']}/5

                            </div>

                            <div class="ai-score">

                            🤖 AI Score:
                            {product['ai_score']:.1f}

                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"""
                            <div class="reason">

                            <b>💡 Why AgentCart recommends it</b>

                            <br><br>

                            This product has a
                            <b>{product['rating']}/5</b> rating,
                            <b>{product['ram']}GB RAM</b>,
                            <b>{product['storage']}GB</b> storage
                            and is suitable for
                            <b>{product['use']}</b>.

                            </div>
                            """,
                            unsafe_allow_html=True
                        )


# ============================================================
# PRODUCT EXPLORER
# ============================================================

elif page == "🔎 Product Explorer":

    st.markdown(
        '<div class="section-title">🔎 Product Explorer</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Products currently available to the "
        "AgentCart recommendation engine."
    )

    st.dataframe(
        products,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# HOW IT WORKS
# ============================================================

elif page == "🧠 How It Works":

    st.markdown(
        '<div class="section-title">🧠 How AgentCart AI Works</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="card">

    <h3>1️⃣ Understand</h3>

    AgentCart analyzes the user's natural-language
    shopping request and identifies important
    requirements such as budget and intended use.

    </div>

    <div class="card">

    <h3>2️⃣ Filter</h3>

    The system filters products according to
    the user's budget and requirements.

    </div>

    <div class="card">

    <h3>3️⃣ Compare</h3>

    Products are evaluated using price, rating,
    RAM, storage, battery and GPU information.

    </div>

    <div class="card">

    <h3>4️⃣ Score</h3>

    Each product receives an AI recommendation
    score based on how well it matches the user's
    requirements.

    </div>

    <div class="card">

    <h3>5️⃣ Recommend</h3>

    The highest-scoring products are presented
    to the user along with an explanation.

    </div>

    """, unsafe_allow_html=True)
