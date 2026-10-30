import os
from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


class IncidentResponseRAGEngine:
    def __init__(self, runbook_texts: list):
        Settings.embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")
        Settings.chunk_size = 512
        Settings.chunk_overlap = 50
        self.documents = [Document(text=text) for text in runbook_texts]
        self.index = None
        self.query_engine = None

    def build_index(self):
        self.index = VectorStoreIndex.from_documents(self.documents)
        self.query_engine = self.index.as_query_engine(similarity_top_k=2)

    def query_runbook(self, incident_query: str) -> dict:
        if not self.query_engine:
            raise ValueError("Index has not been built yet. Call build_index() first.")
        
        response = self.query_engine.query(incident_query)
        
        sources = []
        for node in response.source_nodes:
            sources.append({
                "score": round(float(node.score), 4) if node.score else None,
                "snippet": node.text[:120] + "..."
            })

        return {
            "incident_query": incident_query,
            "recommended_action": str(response),
            "sources": sources
        }


if __name__ == "__main__":
    # Expanded Enterprise Incident Response Knowledge Base (30 Comprehensive Runbooks)
    runbooks = [
        # 1-5: Ransomware & Malware Incidents
        "Runbook ID IR-01: Ransomware Containment. Step 1: Immediately isolate the compromised host from the network by disabling physical and virtual interfaces. Step 2: Preserve volatile RAM memory for forensic analysis using dumping tools. Step 3: Notify the Chief Information Security Officer (CISO) and legal counsel within 30 minutes. Step 4: Initiate offline backups verification for data restoration.",
        "Runbook ID IR-02: Advanced Malware Eradication. Step 1: Terminate malicious process trees using administrative endpoint management tools. Step 2: Quarantine suspicious binaries and extract hashes for IOC sharing. Step 3: Perform a full signature-based antivirus and EDR scan across adjacent subnet assets. Step 4: Rebuild infected workstations from golden enterprise system images if integrity cannot be verified.",
        "Runbook ID IR-03: Zero-Day Exploit Isolation. Step 1: Implement emergency network boundary blocks at the firewall level for affected software protocols. Step 2: Deploy temporary vendor workarounds or virtual patching rules. Step 3: Monitor telemetry for abnormal memory allocation patterns and unexpected child process spawns. Step 4: Escalate to threat intelligence engineering for custom YARA rule generation.",
        "Runbook ID IR-04: Worm Propagation Mitigation. Step 1: Segment internal network zones immediately to halt lateral movement across VLANs. Step 2: Disable Server Message Block version 1 (SMBv1) and unnecessary RPC services enterprise-wide. Step 3: Force global credential resets for service accounts potentially exposed via pass-the-hash. Step 4: Review active directory replication logs for unauthorized domain controller modifications.",
        "Runbook ID IR-05: Spyware & Keylogger Remediation. Step 1: Isolate the affected executive or developer workstation from production networks. Step 2: Capture disk image and analyze process injection hooks and API hooking mechanisms. Step 3: Revoke all active API keys, session cookies, and SSH keys associated with the user profile. Step 4: Conduct comprehensive hardware integrity inspection for physical keystroke loggers.",

        # 6-10: Credential, Authentication & Access Breaches
        "Runbook ID IR-06: Credential Stuffing & Unauthorized Login. Step 1: Force immediate password reset for the affected user account across all active sessions. Step 2: Revoke all active OAuth tokens and API access keys. Step 3: Review authentication audit logs for IP address anomalies and geographic shifts. Step 4: Enable mandatory hardware-based MFA for the user.",
        "Runbook ID IR-07: Privilege Escalation Incident. Step 1: Immediately suspend the compromised administrative user account. Step 2: Audit local administrators groups across domain controllers and member servers. Step 3: Review Windows Event Logs (ID 4672 and 4720) for unauthorized privilege assignments. Step 4: Rotate all domain admin krbtgt account passwords twice to invalidate existing Kerberos tickets.",
        "Runbook ID IR-08: Brute-Force SSH Attack Mitigation. Step 1: Block attacking IP addresses dynamically using fail2ban and perimeter firewall rules. Step 2: Enforce strict public-key authentication only and disable password-based SSH logins globally. Step 3: Change default SSH listening ports on non-critical bastion hosts. Step 4: Review auth.log files for successful brute-force compromise attempts.",
        "Runbook ID IR-09: Session Hijacking Response. Step 1: Invalidate all active user session tokens in the Redis cache and application database. Step 2: Force re-authentication with multi-factor verification across all web applications. Step 3: Investigate client-side browser extensions and XSS vulnerabilities that enabled cookie theft. Step 4: Monitor subsequent requests for abnormal user-agent and IP signature changes.",
        "Runbook ID IR-10: Compromised API Key Remediation. Step 1: Revoke the leaked API key instantly in the developer portal or secret manager. Step 2: Audit API gateway access logs to identify data exfiltration scope and accessed endpoints. Step 3: Generate new cryptographic keys and enforce secure secret injection pipelines. Step 4: Notify downstream consumers and partners regarding potential data exposure.",

        # 11-15: Web Application & Database Attacks
        "Runbook ID IR-11: SQL Injection Attack Detection. Step 1: Inspect web application firewall (WAF) logs for malicious payload patterns (e.g., UNION SELECT, OR 1=1). Step 2: Rate-limit or block the originating IP address at the edge gateway. Step 3: Audit database query execution logs for unauthorized data exfiltration attempts. Step 4: Apply input sanitization patches to vulnerable endpoints.",
        "Runbook ID IR-12: Cross-Site Scripting (XSS) Incident. Step 1: Identify and quarantine the injected web script payload within application source code. Step 2: Purge contaminated content delivery network (CDN) caches and browser local storage states. Step 3: Strengthen Content Security Policy (CSP) headers to restrict unauthorized script execution. Step 4: Perform automated dynamic application security testing (DAST) on the web module.",
        "Runbook ID IR-13: Remote Code Execution (RCE) Response. Step 1: Take an offline snapshot of the vulnerable web server virtual machine for forensic investigation. Step 2: Terminate the web application service container to prevent shell execution persistence. Step 3: Patch underlying deserialization or template injection vulnerabilities immediately. Step 4: Conduct integrity checks on system binaries and configuration files.",
        "Runbook ID IR-14: Server-Side Request Forgery (SSRF). Step 1: Block internal metadata service access (e.g., 169.254.169.254) via strict egress firewall rules. Step 2: Validate and sanitize all user-supplied URL inputs using strict allow-lists. Step 3: Review cloud provider VPC flow logs for unusual outbound connection attempts. Step 4: Rotate cloud IAM role credentials attached to the affected compute instance.",
        "Runbook ID IR-15: Broken Object Level Authorization (BOLA). Step 1: Suspend affected API endpoints temporarily if active data harvesting is detected. Step 2: Audit authorization checks and token validations in backend controller logic. Step 3: Implement rigorous ownership validation tests in CI/CD pipeline security gates. Step 4: Notify affected customers if personal identifiable information (PII) was accessed.",

        # 16-20: Network Infrastructure & DDoS Incidents
        "Runbook ID IR-16: DDoS Mitigation Protocol. Step 1: Activate anti-DDoS scrubbing center and traffic rate-limiting rules. Step 2: Analyze volumetric traffic spikes using NetFlow and BGP telemetry. Step 3: Scale backend compute instances horizontally via auto-scaling groups. Step 4: Contact cloud infrastructure provider DDoS support hotline for upstream traffic filtering.",
        "Runbook ID IR-17: Border Gateway Protocol (BGP) Hijacking. Step 1: Coordinate immediately with upstream Internet Service Providers (ISPs) and peering partners. Step 2: Verify route origin authorizations (ROAs) and Resource Public Key Infrastructure (RPKI) validity. Step 3: Monitor global looking glass networks for abnormal ASN path announcements. Step 4: Apply strict prefix filtering policies on corporate edge routers.",
        "Runbook ID IR-18: DNS Spoofing & Cache Poisoning. Step 1: Purge recursive resolver local caches immediately. Step 2: Verify DNS records integrity against authoritative name server masters. Step 3: Enforce DNSSEC validation across all corporate domains. Step 4: Monitor DNS query traffic for abnormal amplification patterns.",
        "Runbook ID IR-19: ARP Spoofing Mitigation. Step 1: Enable Dynamic ARP Inspection (DAI) on all enterprise network switches. Step 2: Lock switch port MAC addresses using static port security configurations. Step 3: Isolate affected local subnet segments to prevent man-in-the-middle sniffing. Step 4: Scan local network for rogue hypervisors or unauthorized bridging tools.",
        "Runbook ID IR-20: Unencrypted Traffic Interception. Step 1: Enforce HTTP Strict Transport Security (HSTS) and mandatory TLS 1.3 across all services. Step 2: Revoke legacy SSL/TLS cipher suites vulnerable to downgrade attacks. Step 3: Audit load balancers and proxy configurations for cleartext forwarding. Step 4: Deploy internal network monitoring sensors to detect plain-text credential leaks.",

        # 21-25: Cloud Infrastructure & Container Security
        "Runbook ID IR-21: Misconfigured S3 Bucket Exposure. Step 1: Apply immediate public access block policies to the affected cloud storage bucket. Step 2: Audit cloud trail logs to determine exact download volumes and enumeration scope. Step 3: Review IAM bucket policies and ACL permissions across all enterprise storage. Step 4: Enable automated cloud security posture management (CSPM) compliance guardrails.",
        "Runbook ID IR-22: Container Escape Incident. Step 1: Terminate the compromised Kubernetes pod and isolate the underlying worker node. Step 2: Audit container image layers for malicious binaries and privilege escalation exploits. Step 3: Review Kubernetes API server audit logs for unauthorized cluster role bindings. Step 4: Enforce strict Pod Security Standards (PSS) and AppArmor/SELinux profiles.",
        "Runbook ID IR-23: Compromised CI/CD Pipeline Secret. Step 1: Revoke exposed GitHub/GitLab secrets, deployment tokens, and container registry keys. Step 2: Audit recent code commits and pull requests for unauthorized backdoor injections. Step 3: Rotate all production database and infrastructure credentials touched by the pipeline. Step 4: Implement secret scanning tools and pre-commit hooks in development workflows.",
        "Runbook ID IR-24: Kubernetes Cluster Node Compromise. Step 1: Drain the compromised Kubernetes worker node using kubectl drain command. Step 2: Preserve etcd database snapshot and node system logs for forensic analysis. Step 3: Re-image the underlying virtual machine instance from a clean base template. Step 4: Audit cluster RBAC roles and service account permissions for excessive privileges.",
        "Runbook ID IR-25: Serverless Function Abuse (Lambda/Cloud Functions). Step 1: Restrict execution timeout limits and memory allocations on the affected function. Step 2: Audit event source triggers and API gateway permissions for unauthorized invocations. Step 3: Inspect function source code for dependency vulnerabilities and injection flaws. Step 4: Enable AWS GuardDuty or equivalent cloud threat detection monitoring.",

        # 26-30: Insider Threats, Physical & Compliance Incidents
        "Runbook ID IR-26: Insider Data Exfiltration. Step 1: Immediately disable physical access badge credentials and revoke IT system accounts. Step 2: Preserve workstation storage drives and cloud drive access logs for legal hold. Step 3: Audit data loss prevention (DLP) alerts for mass file downloads or USB transfers. Step 4: Coordinate containment strategy with corporate legal and human resources teams.",
        "Runbook ID IR-27: Unauthorized Physical Hardware Tap. Step 1: Inspect server racks and telecommunication closets for rogue network taps or keyloggers. Step 2: Review physical access security logs and CCTV footage for unauthorized entry. Step 3: Disable switch ports connected to unidentified physical hardware drops. Step 4: Conduct physical security audit across all enterprise data center facilities.",
        "Runbook ID IR-28: Supply Chain Software Dependency Compromise. Step 1: Identify impacted software versions using software bill of materials (SBOM) inventories. Step 2: Isolate or update vulnerable open-source library packages to patched releases. Step 3: Run static code analysis to verify whether malicious payload functions are invoked. Step 4: Notify software vendors and legal counsel regarding upstream contamination.",
        "Runbook ID IR-29: Phishing Campaign Credential Harvesting. Step 1: Block malicious domains and phishing landing page URLs at the corporate DNS filter. Step 2: Reset passwords and revoke sessions for all employees identified as submitters. Step 3: Analyze email headers and launch enterprise-wide security awareness warnings. Step 4: Submit threat intelligence feeds to email security gateway vendors.",
        "Runbook ID IR-30: Regulatory Compliance Data Breach Reporting. Step 1: Convene incident response legal committee to evaluate mandatory notification timelines (e.g., GDPR 72 hours). Step 2: Compile forensic impact assessment detailing exposed personal data records. Step 3: Draft formal notification disclosures for supervisory authorities and affected data subjects. Step 4: Document all remediation actions taken in the official compliance incident ledger."
    ]

    engine = IncidentResponseRAGEngine(runbooks)
    engine.build_index()

    # 20 Distinct and Diverse Test Queries for RAG Evaluation
    test_queries = [
        "What is the exact containment protocol for a suspected ransomware infection?",
        "How do we handle an advanced malware eradication and process termination?",
        "What are the emergency steps for zero-day exploit isolation?",
        "How should we mitigate worm propagation and disable SMBv1 across the network?",
        "What is the protocol for spyware and keylogger remediation on workstations?",
        "What immediate actions are required during a credential stuffing and unauthorized login attack?",
        "How do we handle a privilege escalation incident and rotate krbtgt passwords?",
        "What is the mitigation procedure for brute-force SSH attacks?",
        "How do we respond to a session hijacking and cookie theft incident?",
        "What steps are needed when an API key leak or compromise is detected?",
        "How do we detect and contain SQL injection attack patterns?",
        "What is the response protocol for Cross-Site Scripting (XSS) web incidents?",
        "How do we handle Remote Code Execution (RCE) container termination and snapshotting?",
        "What are the firewall rules required to prevent Server-Side Request Forgery (SSRF)?",
        "How do we address Broken Object Level Authorization (BOLA) vulnerabilities?",
        "What is the mitigation protocol for large-scale volumetric DDoS attacks?",
        "How do we coordinate with ISPs during a Border Gateway Protocol (BGP) hijacking?",
        "What steps ensure DNS spoofing and cache poisoning recovery?",
        "How do we enable Dynamic ARP Inspection to mitigate ARP spoofing?",
        "What is the compliance timeline and reporting procedure for regulatory data breaches?"
    ]

    print(f"--- Enterprise Incident Response RAG Audit Report ({len(test_queries)} Test Queries) ---")
    print(f"Knowledge Base Size: {len(runbooks)} Runbooks Loaded & Indexed.\n" + "="*70)

    for i, query in enumerate(test_queries, 1):
        result = query_result = engine.query_runbook(query)
        print(f"\n[Test Query {i}] {result['incident_query']}")
        print(f"-> Recommended Action: {result['recommended_action']}")
        print("-> Top Citations / Sources:")
        for src in result['sources']:
            print(f"    • [Score: {src['score']}] {src['snippet']}")
        print("-" * 70)