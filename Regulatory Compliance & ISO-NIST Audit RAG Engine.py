from abc import ABC, abstractmethod
import os
from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


class BaseComplianceAuditor(ABC):
    @abstractmethod
    def build_index(self):
        pass

    @abstractmethod
    def audit_query(self, query: str) -> dict:
        pass


class EnterpriseComplianceRAGEngine(BaseComplianceAuditor):
    def __init__(self, compliance_texts: list, model_name: str = "all-MiniLM-L6-v2"):
        Settings.embed_model = HuggingFaceEmbedding(model_name=model_name)
        Settings.chunk_size = 512
        Settings.chunk_overlap = 50
        self._documents = [Document(text=t) for t in compliance_texts]
        self._index = None
        self._query_engine = None

    def build_index(self):
        self._index = VectorStoreIndex.from_documents(self._documents)
        self._query_engine = self._index.as_query_engine(similarity_top_k=2)

    def audit_query(self, query: str) -> dict:
        if not self._query_engine:
            raise RuntimeError("Index not initialized. Run build_index() first.")
        
        response = self._query_engine.query(query)
        sources = [
            {"score": round(float(n.score), 4) if n.score else None, "clause": n.text[:120] + "..."}
            for n in response.source_nodes
        ]
        return {
            "query": query,
            "audit_finding": str(response),
            "evidence_sources": sources
        }


if __name__ == "__main__":
    # Expanded Enterprise Compliance Knowledge Base (30 Regulatory Clauses & Controls)
    compliance_controls = [
        # ISO 27001 Controls (1-10)
        "ISO-27001 Clause A.5.1: Information security policies must be defined, approved by management, published, and communicated to all employees and relevant external parties.",
        "ISO-27001 Clause A.6.1: Internal organization. Roles and responsibilities for information security must be organized, assigned, and documented clearly.",
        "ISO-27001 Clause A.7.1: Human resource security. Screening background checks must be conducted on all candidates for employment prior to onboarding.",
        "ISO-27001 Clause A.8.1: Asset management. All information assets associated with information processing facilities must be inventoried and owned.",
        "ISO-27001 Clause A.9.1: Access control. Access to information and application functions must be restricted in accordance with business and security requirements.",
        "ISO-27001 Clause A.10.1: Cryptographic controls. Policies on the use of encryption and cryptographic controls for protection of data must be implemented.",
        "ISO-27001 Clause A.11.1: Physical and environmental security. Perimeters of secure areas must be defined and protected by physical barrier controls.",
        "ISO-27001 Clause A.12.1: Operations security. Operating procedures for IT facilities must be documented, maintained, and made available to all users.",
        "ISO-27001 Clause A.13.1: Communications security. Network services must be secured and managed to protect information in transit across public and private networks.",
        "ISO-27001 Clause A.14.1: System acquisition, development, and maintenance. Security requirements must be integrated into the entire software development lifecycle (SDLC).",

        # NIST SP 800-53 Security Controls (11-20)
        "NIST AC-1: Access Control Policy and Procedures. The organization develops, documents, and disseminates to designated personnel an access control policy.",
        "NIST AT-1: Awareness and Training Policy. The organization implements a security awareness and training program for all system users annually.",
        "NIST AU-1: Audit and Accountability Policy. The organization ensures that audit logs capture sufficient information to establish what events occurred.",
        "NIST CA-1: Assessment, Authorization, and Monitoring. The organization assesses security controls in organizational systems and environment of operation.",
        "NIST CM-1: Configuration Management Policy. The organization establishes baseline configurations and inventory of information system components.",
        "NIST CP-1: Contingency Planning Policy. The organization develops and maintains a contingency planning policy addressing system recovery operations.",
        "NIST IA-1: Identification and Authentication Policy. The organization manages information system identifiers and authenticators securely.",
        "NIST IR-1: Incident Response Policy. The organization implements an incident response capability for security incidents including preparation and containment.",
        "NIST MP-1: Media Protection Policy. The organization protects digital and physical media containing sensitive information throughout its lifecycle.",
        "NIST PE-1: Physical and Environmental Protection. The organization limits physical access to information systems, equipment, and respective operating environments.",

        # SOC 2 Trust Services Criteria & GDPR (21-30)
        "SOC2 CC6.1: Logical Access Controls. The entity implements logical access security software, infrastructure, and architectures over protected information assets.",
        "SOC2 CC6.2: User Registration and De-registration. Prior to issuing system credentials, the entity registers and authorizes new users based on role requirements.",
        "SOC2 CC6.3: Access Modification and Removal. The entity revokes access privileges promptly upon termination, role change, or agreement expiration.",
        "SOC2 CC7.1: Vulnerability Detection and Monitoring. The entity detects and monitors vulnerabilities through automated scanning and threat intelligence feeds.",
        "SOC2 CC7.2: Incident Response Execution. The entity responds to identified security incidents by executing defined containment and remediation procedures.",
        "GDPR Article 32: Security of Processing. The controller and processor shall implement appropriate technical and organizational measures ensuring a level of security.",
        "GDPR Article 33: Notification of Personal Data Breach. In case of a personal data breach, the controller shall notify supervisory authority without undue delay.",
        "GDPR Article 35: Data Protection Impact Assessment (DPIA). Where a type of processing is likely to result in high risk, the controller shall carry out an assessment.",
        "ISO-27001 Clause A.15.1: Supplier relationships. Information security requirements for mitigating risks associated with supplier products must be established.",
        "ISO-27001 Clause A.18.1: Compliance. All statutory, regulatory, and contractual requirements must be explicitly identified, documented, and met."
    ]

    # 20 Distinct Test Audit Queries
    test_queries = [
        "What are the requirements for defining and publishing information security policies?",
        "How should internal organization roles and responsibilities be structured?",
        "What candidate screening procedures are mandated for human resource security?",
        "How must information assets and processing facilities be managed and owned?",
        "What are the core principles for restricting logical access to information?",
        "What policies govern the implementation of cryptographic controls and encryption?",
        "How must physical perimeters and secure operating areas be protected?",
        "What operational procedures must be documented for IT facilities?",
        "How should network communications and data in transit be secured?",
        "At what stage must security requirements be integrated into software development?",
        "What are the mandatory documentation rules for organization access control policy under NIST?",
        "How often must security awareness and training programs be executed?",
        "What information must audit logs capture to ensure accountability?",
        "How are security controls assessed across organizational systems?",
        "What baseline configuration and inventory rules apply to system components?",
        "What provisions must contingency planning policies address for system recovery?",
        "How should system identifiers and authenticators be managed securely?",
        "What capabilities must incident response policies include for threat handling?",
        "How must digital and physical media be protected throughout its lifecycle?",
        "What technical measures are required under GDPR Article 32 for data security?"
    ]

    print("Initializing Enterprise Compliance RAGEngine using ABC & Strategy Pattern...")
    auditor = EnterpriseComplianceRAGEngine(compliance_controls)
    auditor.build_index()

    print(f"\n--- Enterprise Regulatory Compliance Audit Report ({len(test_queries)} Queries) ---\n" + "="*70)
    for i, query in enumerate(test_queries, 1):
        res = auditor.audit_query(query)
        print(f"\n[Audit Query {i}] {res['query']}")
        print(f"-> Finding: {res['audit_finding']}")
        print("-> Evidence Clauses:")
        for ev in res['evidence_sources']:
            print(f"    • [Score: {ev['score']}] {ev['clause']}")
        print("-" * 70)