from abc import ABC, abstractmethod
import os
from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


class IQueryProcessor(ABC):
    @abstractmethod
    def process_remediation_query(self, query: str) -> dict:
        pass


class EnterpriseSupplyChainRAGEngine(IQueryProcessor):
    def __init__(self, remediation_data: list, model_name: str = "all-MiniLM-L6-v2"):
        Settings.embed_model = HuggingFaceEmbedding(model_name=model_name)
        Settings.chunk_size = 512
        Settings.chunk_overlap = 50
        self._documents = [Document(text=text) for text in remediation_data]
        self._index = None
        self._query_engine = None

    def build_index(self):
        self._index = VectorStoreIndex.from_documents(self._documents)
        self._query_engine = self._index.as_query_engine(similarity_top_k=2)

    def process_remediation_query(self, query: str) -> dict:
        if not self._query_engine:
            raise RuntimeError("Engine index is uninitialized. Call build_index() prior to querying.")
        
        response = self._query_engine.query(query)
        sources = [
            {"score": round(float(n.score), 4) if n.score else None, "remediation_record": n.text[:120] + "..."}
            for n in response.source_nodes
        ]
        return {
            "query": query,
            "remediation_plan": str(response),
            "citations": sources
        }


if __name__ == "__main__":
    # Expanded Supply Chain & AI Guardrail Remediation Records (30 Enterprise Documents)
    remediation_records = [
        # AI Guardrail & LLM Remediation (1-10)
        "LLM-REM-01: Direct Prompt Injection Mitigation. Step 1: Wrap input in XML boundary tags and apply system prompt isolators. Step 2: Integrate input sanitization guardrails via regex patterns. Step 3: Reject queries containing override syntax.",
        "LLM-REM-02: Indirect Prompt Injection Defense. Step 1: Sanitize all third-party fetched web content before embedding insertion. Step 2: Enforce strict privilege separation between agent reasoning and external tools. Step 3: Audit RAG context blocks for embedded payload markers.",
        "LLM-REM-03: Vector Database Context Poisoning. Step 1: Implement cryptographic signature checks on all incoming document chunks prior to indexing. Step 2: Purge infected vector namespaces. Step 3: Re-index data from verified immutable storage backups.",
        "LLM-REM-04: Training Data Contamination Triage. Step 1: Quarantine suspicious dataset partitions uploaded from untrusted sources. Step 2: Run automated anomaly detection on vector embedding distributions. Step 3: Fine-tune model on verified clean golden data.",
        "LLM-REM-05: Model Inversion & Data Extraction Prevention. Step 1: Implement output filter guardrails to block personally identifiable information (PII). Step 2: Apply differential privacy noise to confidence scores. Step 3: Rate-limit high-frequency repetitive queries.",
        "LLM-REM-06: Adversarial Jailbreak Pattern Handling. Step 1: Update refusal classifiers with newly discovered adversarial prompts. Step 2: Terminate active user sessions attempting systemic jailbreaks. Step 3: Log full payload sequences to threat intelligence storage.",
        "LLM-REM-07: Insecure Output Handling Patching. Step 1: Enforce strict HTML entity encoding on all raw LLM text responses rendered in web UI. Step 2: Parameterize all downstream database queries executed by AI agents. Step 3: Disable arbitrary system execution capabilities.",
        "LLM-REM-08: Excessive Agency Vulnerability Fix. Step 1: Restrict automated LLM agent permissions to read-only API actions. Step 2: Require mandatory human-in-the-loop authorization for state-changing endpoints. Step 3: Log all tool invocation payloads.",
        "LLM-REM-09: Model Denial of Service (DoS) Defense. Step 1: Cap maximum input token lengths at API gateway layer. Step 2: Enforce strict execution timeouts on generation pipelines. Step 3: Implement token bucket rate-limiting algorithms per API client key.",
        "LLM-REM-10: Sensitive Information Disclosure Guardrail. Step 1: Intercept responses containing private SSH keys, AWS tokens, or internal IP addresses. Step 2: Mask sensitive string patterns with redacted placeholders. Step 3: Trigger alert to SecOps team.",

        # Software Supply Chain & Dependency Remediation (11-20)
        "SUP-REM-11: Malicious PyPI Package Removal. Step 1: Remove compromised library dependency from requirements.txt and lockfile. Step 2: Purge local pip artifact cache. Step 3: Audit CI/CD build logs for unauthorized code execution during setup scripts.",
        "SUP-REM-12: Compromised NPM Dependency Fix. Step 1: Audit package-lock.json using npm audit and pin verified secure sub-dependencies. Step 2: Revoke exposed developer publish tokens. Step 3: Rebuild container images from base minimal distroless sources.",
        "SUP-REM-13: Typosquatting Library Incident. Step 1: Identify and block rogue package names closely resembling enterprise internal modules. Step 2: Enforce private enterprise artifact proxy repository (e.g., Nexus or Artifactory). Step 3: Block public index fallback.",
        "SUP-REM-14: Container Base Image Vulnerability. Step 1: Upgrade base Linux distribution image to latest stable release containing patched glibc libraries. Step 2: Scan images using Trivy scanner. Step 3: Sign container images using Cosign keys.",
        "SUP-REM-15: Unsigned Artifact Execution Protocol. Step 1: Enforce binary authorization policies across production Kubernetes clusters. Step 2: Reject deployment of images without valid cryptographic signature. Step 3: Isolate non-compliant pods.",
        "SUP-REM-16: Upstream Repository Hijacking. Step 1: Pin internal dependencies to verified immutable commit SHAs rather than loose tags. Step 2: Mirrored repository code locally to prevent sudden remote deletion. Step 3: Re-verify checksum hashes.",
        "SUP-REM-17: Leaked CI/CD Runner Secrets Remediation. Step 1: Rotate all cloud deployment keys and database credentials stored in pipeline variables. Step 2: Restrict runner access scope. Step 3: Require explicit approval for external PR executions.",
        "SUP-REM-18: Dependency Confusion Vulnerability Patch. Step 1: Configure internal package management tools to prioritize private registry namespaces. Step 2: Register placeholder packages on public indices for internal module names. Step 3: Enforce strict scoped packages.",
        "SUP-REM-19: Open Source License Non-Compliance. Step 1: Run automated license scanner across all third-party code repositories. Step 2: Replace viral GPL dependencies in commercial modules with permissive MIT/Apache equivalents. Step 3: Document legal SBOM.",
        "SUP-REM-20: Obsolete Unsupported Library Replacement. Step 1: Identify abandoned software dependencies lacking security updates. Step 2: Refactor codebase to use actively maintained core packages. Step 3: Execute integration test suite to verify stability.",

        # Infrastructure & Enterprise Contingency (21-30)
        "SUP-REM-21: Firmware Tampering Containment. Step 1: Flash authenticated signed firmware updates to network routers and switches. Step 2: Isolate devices failing cryptographic boot checks. Step 3: Review physical access logs to hardware rooms.",
        "SUP-REM-22: Zero-Day Library Vulnerability Workaround. Step 1: Implement web application firewall (WAF) virtual patch rule targeting exploit vector. Step 2: Disable vulnerable feature flag in application settings. Step 3: Monitor telemetry for bypass attempts.",
        "SUP-REM-23: Compromised Vendor Remote Access. Step 1: Terminate active VPN tunnels and third-party remote desktop sessions. Step 2: Enforce mandatory session recording and granular access control for vendor connections. Step 3: Audit vendor activity logs.",
        "SUP-REM-24: Rogue Hardware Infrastructure Device. Step 1: Conduct automated MAC address inventory audit across core switches. Step 2: Disable unauthorized switch ports dynamically. Step 3: Dispatch physical security team for asset inspection.",
        "SUP-REM-25: Outdated TLS Dependency Deprecation. Step 1: Enforce minimum TLS 1.3 requirement across all external endpoints. Step 2: Update application server configuration files to disable legacy SSL/TLS libraries. Step 3: Test client compatibility.",
        "SUP-REM-26: Database Driver Exploit Patching. Step 1: Apply security hotfix to internal database connector libraries. Step 2: Restrict database user network privileges to localhost. Step 3: Perform memory corruption scan on server processes.",
        "SUP-REM-27: Supply Chain Software Integrity Audit. Step 1: Generate full Software Bill of Materials (SBOM) using Syft tool. Step 2: Cross-reference dependencies against vulnerability databases. Step 3: Publish signed SBOM report to audit repository.",
        "SUP-REM-28: Malicious Code Injection in Build Pipeline. Step 1: Halt automated CI/CD deployment pipelines immediately. Step 2: Inspect build agent host virtual machines for unauthorized persistence mechanisms. Step 3: Re-provision clean build infrastructure.",
        "SUP-REM-29: Cloud Vendor Service Outage Contingency. Step 1: Failover application traffic to secondary cloud provider region via DNS routing. Step 2: Verify database read-replica promotion to primary status. Step 3: Monitor cross-region data latency.",
        "SUP-REM-30: Critical Vulnerability Zero-Day Patch Deployment. Step 1: Deploy emergency patch to production environment following fast-track approval. Step 2: Execute automated smoke tests. Step 3: Monitor error reporting systems for regression spikes."
    ]

    # 20 Distinct Test Remediation Queries
    test_queries = [
        "What are the immediate steps to mitigate direct prompt injection in LLM inputs?",
        "How do we defend against indirect prompt injections from third-party web content?",
        "What protocol addresses vector database context poisoning?",
        "How do we handle training data contamination uploaded from untrusted sources?",
        "What guardrails prevent model inversion and PII extraction?",
        "How do we process adversarial jailbreak prompts and session terminations?",
        "What patching steps protect against insecure output handling in web UIs?",
        "How do we restrict excessive agency in automated AI tool invocations?",
        "What measures block model denial of service (DoS) input token attacks?",
        "How do output guardrails handle sensitive information disclosure like private keys?",
        "What is the procedure for removing a malicious PyPI package from requirements?",
        "How do we fix compromised NPM sub-dependencies and tokens?",
        "How do we prevent typosquatting attacks targeting internal enterprise modules?",
        "What steps upgrade container base images and scan for glibc vulnerabilities?",
        "How do we enforce binary authorization for unsigned container execution?",
        "What protocol handles upstream software repository hijacking?",
        "How do we remediate leaked secrets within CI/CD build runner variables?",
        "How do we patch dependency confusion vulnerabilities across private registries?",
        "What steps ensure open-source license compliance and GPL replacement?",
        "How do we handle obsolete unsupported library replacement in legacy code?"
    ]

    print("Initializing Enterprise Supply Chain RAGEngine with Dependency Injection Pattern...")
    engine = EnterpriseSupplyChainRAGEngine(remediation_records)
    engine.build_index()

    print(f"\n--- Enterprise Supply Chain & Guardrail Remediation Audit ({len(test_queries)} Queries) ---\n" + "="*70)
    for i, query in enumerate(test_queries, 1):
        res = engine.process_remediation_query(query)
        print(f"\n[Test Query {i}] {res['query']}")
        print(f"-> Action Plan: {res['remediation_plan']}")
        print("-> Citations:")
        for cit in res['citations']:
            print(f"    • [Score: {cit['score']}] {cit['remediation_record']}")
        print("-" * 70)