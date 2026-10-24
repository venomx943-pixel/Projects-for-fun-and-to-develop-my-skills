from transformers import pipeline


def verify_llm_faithfulness(contexts: list, hypotheses: list) -> list:
    nli_verifier = pipeline("text-classification", model="roberta-large-mnli")
    results = []
    for ctx, hyp in zip(contexts, hypotheses):
        prediction = nli_verifier(text=ctx, text_pair=hyp)
        results.append(prediction)
    return results


if __name__ == "__main__":
    source_documents = [
        "The core server cluster is hosted in Frankfurt, Germany, running on Linux.",
        "The system API key must be rotated strictly every 90 days.",
    ]
    generated_responses = [
        "Our main server cluster is hosted in Frankfurt, Germany and runs on Linux.",
        "The system API key needs to be changed every 30 days.",
    ]
    validation_results = verify_llm_faithfulness(
        source_documents, generated_responses
    )
    for idx, res in enumerate(validation_results):
        print(f"Response {idx + 1} Verification -> Result: {res}")