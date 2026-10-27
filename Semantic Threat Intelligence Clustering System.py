import numpy as np
from sentence_transformers import SentenceTransformer


class ThreatIntelligenceSemanticClusterer:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def cluster_reports(self, reports: list, similarity_threshold: float = 0.60) -> list:
        embeddings = self.model.encode(reports, convert_to_tensor=False)
        
        norm = np.linalg.norm(embeddings, axis=1, keepdims=True)
        normalized_embeddings = embeddings / (norm + 1e-8)
        similarity_matrix = np.dot(normalized_embeddings, normalized_embeddings.T)
        
        clustered_groups = []
        visited = set()
        
        for i in range(len(reports)):
            if i in visited:
                continue
            current_cluster = [i]
            visited.add(i)
            
            for j in range(i + 1, len(reports)):
                if j not in visited and similarity_matrix[i, j] >= similarity_threshold:
                    current_cluster.append(j)
                    visited.add(j)
                    
            clustered_groups.append(current_cluster)
            
        formatted_clusters = []
        for idx, group in enumerate(clustered_groups):
            cluster_items = [reports[i] for i in group]
            formatted_clusters.append({
                "cluster_id": idx + 1,
                "reports_count": len(cluster_items),
                "reports": cluster_items
            })
            
        return formatted_clusters


if __name__ == "__main__":
    raw_threat_reports = [
        "APT29 launched a spear-phishing campaign targeting government diplomats using malicious PDF attachments.",
        "Russian threat actors deployed custom malware via compromised credentials in state agencies.",
        "A new ransomware variant called LockBit 3.0 was detected encrypting healthcare databases.",
        "Healthcare providers are facing widespread operational disruption due to file-encrypting extortion software.",
        "DDoS attacks overwhelmed financial sector servers using a massive botnet of infected IoT devices.",
        "Financial institutions experienced major service outages caused by distributed denial of service botnets.",
        "Phishing emails impersonating tax authorities are tricking corporate employees into revealing credentials."
    ]

    clusterer = ThreatIntelligenceSemanticClusterer()
    clusters = clusterer.cluster_reports(raw_threat_reports, similarity_threshold=0.60)

    print("--- Threat Intelligence Semantic Clusters ---")
    for cluster in clusters:
        print(f"\n[Cluster #{cluster['cluster_id']}] Containing {cluster['reports_count']} related reports:")
        for rep in cluster['reports']:
            print(f"  - {rep}")