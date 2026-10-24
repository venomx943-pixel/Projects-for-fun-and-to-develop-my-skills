from transformers import pipeline


def detect_and_mask_pii(llm_outputs: list) -> list:
    ner_detector = pipeline(
        "ner",
        model="dbmdz/bert-large-cased-finetuned-conll03-english",
        aggregation_strategy="simple",
    )
    masked_results = []
    for text in llm_outputs:
        entities = ner_detector(text)
        masked_text = text
        for ent in sorted(entities, key=lambda x: x["start"], reverse=True):
            if ent["entity_group"] in ["PER", "ORG", "LOC"]:
                start, end = ent["start"], ent["end"]
                masked_text = (
                    masked_text[:start] + "[REDACTED]" + masked_text[end:]
                )
        masked_results.append(masked_text)
    return masked_results


if __name__ == "__main__":
    sample_outputs = [
        "John Smith works at OpenAI in San Francisco and can be reached via email.",
        "The project deployment was successfully completed on schedule.",
    ]
    secured_outputs = detect_and_mask_pii(sample_outputs)
    for out in secured_outputs:
        print("Secured Output:", out)