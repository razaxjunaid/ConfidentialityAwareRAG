from auth.login import login
from retrieval.retriever import retrieve_with_access_status
from llm.generator import generate_answer


def authenticate_and_answer(username, password, query, top_k=4):
    """
    Authenticate the user, perform confidentiality-aware retrieval,
    enforce RBAC, and generate an answer only from authorized documents.

    If the LLM is unavailable, return authorized retrieved information
    as a fallback.
    """

    # Step 1: Authenticate user
    user = login(username, password)

    if user is None:
        return {
            "success": False,
            "message": "Authentication failed.",
            "user": None,
            "results": [],
            "answer": None,
            "access_denied": False
        }

    # Step 2: Get user's role
    user_role = user["role"]

    # Step 3: Retrieve documents and check access status
    retrieval_response = retrieve_with_access_status(
        query=query,
        user_role=user_role,
        top_k=top_k
    )

    results = retrieval_response["authorized_results"]
    access_denied = retrieval_response["access_denied"]

    # Step 4: Handle access denial
    if access_denied:
        return {
            "success": True,
            "message": "Access denied.",
            "user": user,
            "results": [],
            "answer": (
                "🔒 Access Denied: You are not authorized to access "
                "information relevant to this request."
            ),
            "access_denied": True
        }

    # Step 5: No relevant authorized information
    if not results:
        return {
            "success": True,
            "message": "No authorized information found.",
            "user": user,
            "results": [],
            "answer": (
                "No relevant information was found in the documents "
                "you are authorized to access."
            ),
            "access_denied": False
        }

    # Step 6: Generate answer using ONLY authorized documents
    try:
        answer = generate_answer(
            query=query,
            retrieved_results=results
        )

    except Exception as e:
        print(f"LLM generation failed: {e}")

        # Fallback: show authorized retrieved information
        answer_parts = [
            "The following information was found in documents you are authorized to access:\n"
        ]

        for i, result in enumerate(results, start=1):
            answer_parts.append(
                f"\n{i}. {result['text']}"
            )

        answer = "\n".join(answer_parts)

    return {
        "success": True,
        "message": "Secure RAG completed successfully.",
        "user": user,
        "results": results,
        "answer": answer,
        "access_denied": False
    }


if __name__ == "__main__":

    print("\n========== CONFIDENTIALITY-AWARE RAG ==========\n")

    username = input("Username: ").strip()
    password = input("Password: ").strip()
    query = input("Question: ").strip()

    if not query:
        print("\n❌ Question cannot be empty.")
        raise SystemExit

    response = authenticate_and_answer(
        username=username,
        password=password,
        query=query,
        top_k=4
    )

    if not response["success"]:
        print(f"\n❌ {response['message']}")
        raise SystemExit

    # Display authenticated user
    user = response["user"]

    print("\n✅ Login Successful!")
    print(f"Username : {user['username']}")
    print(f"Role     : {user['role']}")

    # Display final answer
    print("\n========== FINAL ANSWER ==========\n")
    print(response["answer"])

    # Display authorized sources
    print("\n========== AUTHORIZED SOURCES ==========\n")

    results = response["results"]

    if not results:
        print("No authorized sources are displayed.")

    else:
        for i, result in enumerate(results, start=1):
            print("=" * 60)
            print(f"Rank           : {i}")
            print(f"File           : {result['filename']}")
            print(f"Classification : {result['classification']}")
            print(f"Distance       : {result['distance']:.4f}")
            print("\nContent:")
            print(result["text"])
            print()