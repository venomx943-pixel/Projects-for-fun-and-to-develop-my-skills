import numpy as np
from sentence_transformers import SentenceTransformer


class CrossModalSecurityForensicsEngine:
    def __init__(self, model_name: str = "clip-ViT-B-32"):
        self.model = SentenceTransformer(model_name)
        self.evidence_descriptions = []
        self.evidence_embeddings = None

    def index_evidence(self, descriptions: list):
        self.evidence_descriptions = descriptions
        self.evidence_embeddings = self.model.encode(
            self.evidence_descriptions, convert_to_tensor=False
        )

    def search_by_text(self, text_query: str, top_k: int = 2) -> list:
        query_embedding = self.model.encode(text_query, convert_to_tensor=False)
        
        similarities = np.dot(self.evidence_embeddings, query_embedding) / (
            np.linalg.norm(self.evidence_embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                "evidence_item": self.evidence_descriptions[idx],
                "match_score": round(float(similarities[idx]), 4)
            })
        return results


if __name__ == "__main__":
    security_evidence_database = [
        "Network architecture diagram showing firewall misconfiguration between DMZ and internal database server.",
        "Console screenshot displaying unauthorized root access attempt via SSH brute-force attack.",
        "Database schema layout highlighting unencrypted user credentials table vulnerability.",
        "System error log excerpt showing buffer overflow segmentation fault in memory address 0x7fff.",
        "Flowchart illustrating zero-trust authentication handshake failure and token rejection."
    ]

    engine = CrossModalSecurityForensicsEngine()
    engine.index_evidence(security_evidence_database)

    investigation_query = "Show me screenshots or logs related to unauthorized root login attempts."
    print(f"Investigation Query: {investigation_query}\n")

    search_results = engine.search_by_text(investigation_query, top_k=2)
    for res in search_results:
        print(f"Score: {res['match_score']} | Evidence: {res['evidence_item']}")