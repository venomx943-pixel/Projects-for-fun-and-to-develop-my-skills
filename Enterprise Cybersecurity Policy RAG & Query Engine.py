import os
from llama_index.core import Document, Settings, SummaryIndex, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI


class EnterpriseSecurityRAGEngine:
    def __init__(self, documents_text: list):
        # Configure local embedding model to avoid external API dependencies for embeddings
        Settings.embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")
        Settings.chunk_size = 512
        Settings.chunk_overlap = 50

        # Transform raw text strings into LlamaIndex Document objects
        self.documents = [Document(text=t) for t in documents_text]
        self.index = None
        self.query_engine = None

    def build_index(self):
        # Build vector store index for semantic similarity search & retrieval
        self.index = VectorStoreIndex.from_documents(self.documents)
        self.query_engine = self.index.as_query_engine(similarity_top_k=2)

    def query_knowledge_base(self, user_query: str) -> dict:
        if not self.query_engine:
            raise ValueError("Index has not been built yet. Call build_index() first.")
        
        response = self.query_engine.query(user_query)
        
        # Extract source nodes / citations used to generate the answer
        sources = []
        for node in response.source_nodes:
            sources.append({
                "score": round(float(node.score), 4) if node.score else None,
                "text_snippet": node.text[:120] + "..."
            })

        return {
            "query": user_query,
            "answer": str(response),
            "sources": sources
        }


if __name__ == "__main__":
    # Enterprise Security Policy Knowledge Base (Simulated Documents)
    security_policies = [
        "Policy Section 1.1: Multi-Factor Authentication (MFA) is strictly mandatory for all employees accessing corporate cloud infrastructure, database servers, and VPN networks. Hardware security keys or authenticator apps must be used; SMS-based verification is deprecated due to SIM-swapping vulnerabilities.",
        "Policy Section 2.4: Incident Response Protocol. In the event of a suspected ransomware infection or data breach, the affected host must be isolated from the network immediately by disconnecting the physical ethernet cable or disabling the virtual interface. The security operations center (SOC) must be notified within 15 minutes.",
        "Policy Section 3.8: Secure Code Review & Vulnerability Management. All production code changes must undergo Static Application Security Testing (SAST) and manual peer review before merging. Any critical vulnerability discovered must be patched within 48 hours of disclosure.",
        "Policy Section 4.2: Access Control & Privileged Accounts. Root and administrator privileges follow the Principle of Least Privilege (PoLP). Access must be reviewed on a quarterly basis, and dormant accounts exceeding 90 days of inactivity must be permanently disabled."
    ]

    print("Initializing Enterprise Security RAGEngine...")
    rag_engine = EnterpriseSecurityRAGEngine(security_policies)
    rag_engine.build_index()

    test_query = "What is the mandatory protocol if a ransomware infection is suspected?"
    print(f"\nExecuting Query: {test_query}\n")

    result = rag_engine.query_knowledge_base(test_query)

    print("--- RAG Engine Response Report ---")
    print(f"Answer: {result['answer']}\n")
    print("Citations & Sources Used:")
    for src in result['sources']:
        print(f" - [Score: {src['score']}] {src['text_snippet']}")