import numpy as np
from sentence_transformers import SentenceTransformer


class SecuritySolutionRecommender:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.catalog = []
        self.catalog_embeddings = None

    def load_catalog(self, solutions: list):
        self.catalog = solutions
        descriptions = [sol["description"] for sol in self.catalog]
        self.catalog_embeddings = self.model.encode(descriptions, convert_to_tensor=False)

    def recommend(self, client_requirement: str, top_k: int = 2) -> list:
        req_embedding = self.model.encode(client_requirement, convert_to_tensor=False)
        
        similarities = np.dot(self.catalog_embeddings, req_embedding) / (
            np.linalg.norm(self.catalog_embeddings, axis=1) * np.linalg.norm(req_embedding)
        )
        
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        recommendations = []
        for idx in top_indices:
            recommendations.append({
                "solution_name": self.catalog[idx]["name"],
                "description": self.catalog[idx]["description"],
                "match_score": round(float(similarities[idx]), 4)
            })
        return recommendations


if __name__ == "__main__":
    security_catalog = [
        {
            "name": "ShieldDB Firewall",
            "description": "Advanced database firewall protecting against SQL injection, unauthorized queries, and data exfiltration."
        },
        {
            "name": "CloudZero Zero-Trust Gateway",
            "description": "Continuous user and device verification platform enforcing zero-trust access across multi-cloud infrastructure."
        },
        {
            "name": "NexusGuard IAM",
            "description": "Multi-factor authentication and role-based access control system ensuring secure credential management."
        },
        {
            "name": "CodeArmor SAST",
            "description": "Static application security testing tool scanning source code for buffer overflows and memory vulnerabilities."
        }
    ]

    recommender = SecuritySolutionRecommender()
    recommender.load_catalog(security_catalog)

    client_query = "We need a system to prevent unauthorized logins using multi-factor verification."
    print(f"Client Requirement: {client_query}\n")

    results = recommender.recommend(client_query, top_k=2)
    for res in results:
        print(f"Score: {res['match_score']} | Solution: {res['solution_name']} - {res['description']}")