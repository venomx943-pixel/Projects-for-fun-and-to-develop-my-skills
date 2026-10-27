import numpy as np
from sentence_transformers import SentenceTransformer


class HybridSemanticSearchEngine:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.corpus = []
        self.corpus_embeddings = None

    def add_documents(self, documents: list):
        self.corpus = documents
        self.corpus_embeddings = self.model.encode(
            self.corpus, convert_to_tensor=False
        )

    def search(self, query: str, top_k: int = 3) -> list:
        query_embedding = self.model.encode(query, convert_to_tensor=False)
        
        similarities = np.dot(self.corpus_embeddings, query_embedding) / (
            np.linalg.norm(self.corpus_embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                "document": self.corpus[idx],
                "score": round(float(similarities[idx]), 4)
            })
        return results


if __name__ == "__main__":
    security_knowledge_base = [
        "MFA (Multi-Factor Authentication) significantly reduces the risk of unauthorized credential access.",
        "SQL injection vulnerabilities occur when untrusted user input is directly concatenated into database queries.",
        "Zero-trust network architecture assumes zero implicit trust and verifies every user and device continuously.",
        "Cross-Site Scripting (XSS) allows attackers to inject malicious JavaScript into web pages viewed by other users.",
        "End-to-end encryption ensures that data is encrypted on the sender's device and can only be decrypted by the recipient.",
        "Buffer overflow vulnerabilities happen when a program writes more data to a buffer than it can hold, overwriting adjacent memory.",
        "Regular security audits and automated penetration testing help identify system misconfigurations before attackers exploit them."
    ]

    engine = HybridSemanticSearchEngine()
    engine.add_documents(security_knowledge_base)

    test_query = "How can we prevent unauthorized logins using multiple verification steps?"
    print(f"Query: {test_query}\n")

    search_results = engine.search(test_query, top_k=3)
    for res in search_results:
        print(f"Score: {res['score']} | Document: {res['document']}")