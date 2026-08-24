import ollama


def generate_answer(query, retrieved_results):
    """
    Generate an answer using only results that have already
    passed authentication and RBAC authorization.
    """

    # If no authorized documents were retrieved
    if not retrieved_results:
        return (
            "The requested information is not available in the "
            "documents you are authorized to access."
        )

    # Build context from authorized retrieved results
    context_parts = []

    for i, result in enumerate(retrieved_results, start=1):
        context_parts.append(
            f"Source {i}:\n{result['text']}"
        )

    context = "\n\n".join(context_parts)

    # Create prompt INSIDE the function because context and query
    # are defined here
    prompt = f"""You are a document question-answering system.

Answer the QUESTION directly using only the SOURCE TEXT below.

SOURCE TEXT:
{context}

QUESTION:
{query}

Rules:
1. Extract and summarize relevant information from the source text.
2. If the source explicitly provides relevant facts, state those facts directly.
3. Do not say "the answer is not explicitly stated" when relevant facts are present.
4. Do not discuss what the source does not say.
5. Do not make inferences beyond the source.
6. Do not mention permissions, authorization, or access control.
7. Give a concise answer.

ANSWER:
"""

    try:
        response = ollama.generate(
            model="llama3.2:3b",
            prompt=prompt,
            options={
                "temperature": 0.1,
                "num_predict": 200
            }
        )

        return response["response"].strip()

    except Exception as e:
        return f"Error generating answer: {str(e)}"


# Test the generator directly
if __name__ == "__main__":

    sample_query = (
        "What is the company's acquisition strategy and "
        "what merger plans are being reviewed?"
    )

    sample_results = [
        {
            "text": (
                "The company is evaluating a potential acquisition "
                "to expand its enterprise technology business. "
                "The acquisition strategy includes evaluating potential "
                "target companies, analyzing financial risks, and planning "
                "integration with the company's existing products. "
                "The executive board is also reviewing potential merger "
                "plans and their financial and operational impact."
            )
        }
    ]

    answer = generate_answer(sample_query, sample_results)

    print("\n========== GENERATOR TEST ==========\n")

    print("Question:")
    print(sample_query)

    print("\nAnswer:")
    print(answer)