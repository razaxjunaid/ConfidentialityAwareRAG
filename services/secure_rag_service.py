from auth.login import login
from retrieval.retriever import retrieve
from llm.generator import generate_answer


def authenticate_and_answer(username, password, query, top_k=4):
    """
    Authenticate the user, retrieve only authorized documents,
    and generate an answer using the authorized context.
    """

    # Step 1: Authenticate user
    user = login(username, password)

    if user is None:
        return {
            "success": False,
            "message": "Authentication failed.",
            "user": None,
            "results": [],
            "answer": None
        }

    # Step 2: Get user's role
    user_role = user["role"]

    # Step 3: Retrieve only documents authorized for this role
    results = retrieve(
        query=query,
        user_role=user_role,
        top_k=top_k
    )

    # Step 4: Generate answer using only authorized documents
    answer = generate_answer(
        query=query,
        retrieved_results=results
    )

    return {
        "success": True,
        "message": "Secure RAG completed successfully.",
        "user": user,
        "results": results,
        "answer": answer
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
        print("No authorized information found.")

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