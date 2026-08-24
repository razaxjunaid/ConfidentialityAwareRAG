import streamlit as st

# -----------------------------------------------------
# Page Configuration
# Must come before other Streamlit commands
# -----------------------------------------------------

st.set_page_config(
    page_title="Confidentiality-Aware RAG",
    page_icon="🔐",
    layout="wide"
)

from database.init_db import initialize_database
from services.secure_rag_service import authenticate_and_answer

# Optional: ChromaDB debugging
from vectorstore.chroma_store import collection_info, debug_collection


# -----------------------------------------------------
# Initialize Database and Check ChromaDB
# -----------------------------------------------------

@st.cache_resource
def setup_database():

    initialize_database()

    print("\n========== CHROMADB CHECK ==========\n")

    collection_info()
    debug_collection()

    print("\n====================================\n")


setup_database()


# -----------------------------------------------------
# Title
# -----------------------------------------------------

st.title("🔐 Confidentiality-Aware RAG System")

st.markdown(
    """
    A secure Retrieval-Augmented Generation system with
    **Authentication, Role-Based Access Control (RBAC),
    Confidentiality-Aware Retrieval, and Local LLM Generation**.
    """
)

st.divider()


# -----------------------------------------------------
# Sidebar - Login
# -----------------------------------------------------

with st.sidebar:

    st.header("🔑 User Authentication")

    username = st.text_input(
        "Username",
        placeholder="Enter username"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password"
    )

    st.markdown("---")

    st.markdown("### Demo Users")

    st.code(
        """viewer / viewer123
staff / staff123
senior / senior123
executive / executive123"""
    )


# -----------------------------------------------------
# Main Question Area
# -----------------------------------------------------

st.subheader("💬 Ask a Question")

query = st.text_area(
    "Enter your question",
    placeholder="Example: What are the company's strategic plans?",
    height=120
)


# -----------------------------------------------------
# Ask Button
# -----------------------------------------------------

if st.button(
    "🔍 Ask Secure RAG",
    use_container_width=True
):

    # -------------------------------------------------
    # Validate Inputs
    # -------------------------------------------------

    if not username or not password:

        st.warning(
            "Please enter both username and password."
        )

    elif not query:

        st.warning(
            "Please enter a question."
        )

    else:

        # -------------------------------------------------
        # Secure RAG Processing
        # -------------------------------------------------

        with st.spinner(
            "Authenticating user and retrieving authorized information..."
        ):

            response = authenticate_and_answer(
                username=username,
                password=password,
                query=query,
                top_k=4
            )

        # -------------------------------------------------
        # Authentication Failure
        # -------------------------------------------------

        if not response["success"]:

            st.error("❌ Authentication failed.")

        else:

            user = response["user"]

            # -------------------------------------------------
            # User Information
            # -------------------------------------------------

            st.success("✅ Login Successful!")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Username",
                    user["username"]
                )

            with col2:

                st.metric(
                    "Role",
                    user["role"].upper()
                )

            st.divider()

            # -------------------------------------------------
            # Secure Answer
            # -------------------------------------------------

            st.subheader("🤖 Secure Answer")

            if response.get("access_denied", False):

                st.error(
                    response["answer"]
                )

            else:

                st.write(
                    response["answer"]
                )

            st.divider()

            # -------------------------------------------------
            # Authorized Sources
            # -------------------------------------------------

            st.subheader("📚 Authorized Sources")

            results = response["results"]

            # Case 1: Relevant information exists,
            # but the user is not authorized
            if response.get("access_denied", False):

                st.error(
                    "🔒 Access to relevant confidential information "
                    "is not authorized for your current role."
                )

            # Case 2: No relevant authorized information exists
            elif not results:

                st.warning(
                    "No relevant information was found in the documents "
                    "you are authorized to access."
                )

            # Case 3: Authorized documents found
            else:

                for i, result in enumerate(
                    results,
                    start=1
                ):

                    with st.expander(
                        f"Source {i} — "
                        f"{result['filename']} "
                        f"({result['classification']})"
                    ):

                        st.write(
                            f"**Classification:** "
                            f"{result['classification']}"
                        )

                        st.write(
                            f"**Similarity Distance:** "
                            f"{result['distance']:.4f}"
                        )

                        st.markdown("**Content:**")

                        st.write(
                            result["text"]
                        )


# -----------------------------------------------------
# Footer
# -----------------------------------------------------

st.divider()

st.caption(
    "🔒 Security Principle: Unauthorized documents are filtered "
    "before being passed to the LLM."
)