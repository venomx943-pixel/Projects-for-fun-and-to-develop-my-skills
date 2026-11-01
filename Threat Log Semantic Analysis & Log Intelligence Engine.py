import os
from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


class ThreatLogAnalysisRAGEngine:
    def __init__(self, log_telemetry_texts: list):
        Settings.embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")
        Settings.chunk_size = 512
        Settings.chunk_overlap = 50
        self.documents = [Document(text=text) for text in log_telemetry_texts]
        self.index = None
        self.query_engine = None

    def build_index(self):
        self.index = VectorStoreIndex.from_documents(self.documents)
        self.query_engine = self.index.as_query_engine(similarity_top_k=2)

    def analyze_logs(self, analytical_query: str) -> dict:
        if not self.query_engine:
            raise ValueError("Index has not been built yet. Call build_index() first.")
        
        response = self.query_engine.query(analytical_query)
        
        sources = []
        for node in response.source_nodes:
            sources.append({
                "score": round(float(node.score), 4) if node.score else None,
                "log_snippet": node.text[:120] + "..."
            })

        return {
            "analytical_query": analytical_query,
            "intelligence_report": str(response),
            "sources": sources
        }


if __name__ == "__main__":
    # Enterprise Threat Log Telemetry & Security Audit Records
    threat_logs = [
        "Log Record ID LOG-101: Timestamp 2026-10-31T02:14:22Z | Source IP: 192.168.1.150 | Event: Multiple failed SSH login attempts (5 failures in 30 seconds) on Bastion Host 'srv-bastion-01' using root account. Status: Flagged for brute-force suspicion.",
        "Log Record ID LOG-102: Timestamp 2026-10-31T03:45:10Z | Source IP: 45.33.22.11 | Event: Unauthorized SQL injection payload detected in HTTP POST request parameters targeting '/api/v1/login' endpoint. Payload: 'UNION SELECT 1, version()--'. Status: Blocked by WAF rule ID 942100.",
        "Log Record ID LOG-103: Timestamp 2026-10-31T05:20:00Z | Source IP: 10.0.4.52 | Event: Kubernetes cluster role binding modification detected. Service account 'default-deployer' granted cluster-admin privileges. Status: High-severity privilege escalation alert triggered.",
        "Log Record ID LOG-104: Timestamp 2026-10-31T08:12:33Z | Source IP: 198.51.100.44 | Event: Outbound data exfiltration spike detected. Internal host 'db-prod-02' transferred 4.2 GB of compressed archive data to external unverified destination port 443. Status: Isolated automatically by DLP agent."
    ]

    print("Initializing Threat Log Analysis RAGEngine...")
    log_engine = ThreatLogAnalysisRAGEngine(threat_logs)
    log_engine.build_index()

    query = "Were there any SQL injection payloads detected, and how were they handled?"
    print(f"\nExecuting Analytical Query: {query}\n")

    result = log_engine.analyze_logs(query)

    print("--- Threat Log Intelligence Audit Report ---")
    print(f"Report: {result['intelligence_report']}\n")
    print("Referenced Log Sources:")
    for src in result['sources']:
        print(f" - [Score: {src['score']}] {src['log_snippet']}")