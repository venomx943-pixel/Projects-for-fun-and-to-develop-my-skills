import re
from transformers import pipeline

def detect_and_redact_secrets(llm_responses: list) -> list:
    # تحميل نموذج الـ Transformers
    detector = pipeline(
        "token-classification",
        model="dslim/bert-base-NER",
        aggregation_strategy="simple"
    )
    
    secured_responses = []
    
    for idx, text in enumerate(llm_responses):
        redacted_text = text
        leak_found = False
        
        # استخدام نموذج الـ Transformers لتحليل النص واستخراج الكيانات
        entities = detector(text)
        
        if entities:
            leak_found = True
            # ترتيب الكيانات تنازلياً حسب موقع البداية (start) لتفادي تغير الإحداثيات أثناء التعديل
            sorted_entities = sorted(entities, key=lambda x: x['start'], reverse=True)
            
            for ent in sorted_entities:
                start = ent['start']
                end = ent['end']
                # استبدال الجزء المكتشف بواسطة النموذج بالنص المخصص للإخفاء
                redacted_text = redacted_text[:start] + "[REDACTED_SECRET_KEY]" + redacted_text[end:]
        
        secured_responses.append({
            "id": idx + 1,
            "original": text,
            "secured": redacted_text,
            "leak_detected": leak_found
        })
        
    return secured_responses

if __name__ == "__main__":
    comprehensive_test_corpus = [
        # --- LEVEL 1: SAFE NORMAL TEXT & FALSE-POSITIVE TRAPS (1-15) ---
        "You can authenticate using your API key by setting up environment variables securely.",
        "The system deployment was successfully completed on schedule without any errors.",
        "Please ensure that your AWS credentials are never hardcoded in source code repositories.",
        "All database connection strings are properly encrypted using AES-256 standards.",
        "To generate a GitHub token, navigate to your account settings under developer options.",
        "Bearer tokens should be transmitted strictly over encrypted HTTPS connections.",
        "The configuration file expects a variable named OPENAI_API_KEY in the .env file.",
        "Never share your private keys or cryptographic certificates with unauthorized personnel.",
        "Logs indicate that the authentication service started successfully on port 8000.",
        "Developers must rotate their access tokens every ninety days according to policy.",
        "The application interface responds with status code 200 for valid requests.",
        "Python scripts can load configuration parameters using the python-dotenv library.",
        "Continuous integration pipelines automatically scan code for exposed secrets.",
        "The server cluster is hosted in Frankfurt running on an optimized Linux kernel.",
        "Documentation for authentication headers is available in the internal wiki.",

        # --- LEVEL 2: OPENAI API KEY LEAKS (16-25) ---
        "Here is the script you requested, make sure to use your key: sk-proj-1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQ.",
        "The application failed because of an invalid token: sk-ant-api03-abcdefghijklmnopqrstuvwxyz123456789.",
        "Debug output: OpenAI client initialized with key sk-9876543210fedcbaABCDEFGHIJKLM-NOPQRSTUVWXYZ.",
        "Test key found in environment: sk-test-key-abcdefghijklmnopqrstuvwxyz1234567890ABCDEF.",
        "Generated response using token sk-live-999888777666555444333222111abcdefghijkl.",
        "Found credential: sk-proj-ZZZYYYXXXWWWVVVUUUTTTSSSRRRQQQPPPONMLKJIHGFEDCBA.",
        "Config error with token sk-abcedfg1234567890abcdef1234567890abcdef12.",
        "Active session token: sk-proj-abcdef1234567890ABCDEF1234567890ABCDEF123456.",
        "Backup configuration containing sk-sec-99887766554433221100aabbccddeeff.",
        "Legacy key discovered: sk-old-key-1234567890abcdefghijklmnopqrstuvwx.",

        # --- LEVEL 3: AWS ACCESS KEY & SECRET LEAKS (26-35) ---
        "Please use the AWS credential AKIAIOSFODNN7EXAMPLE for secure storage access.",
        "Deployment failed for IAM user with key AKIAI44QH8DHBEXAMPLE.",
        "S3 bucket sync error using access key AKIAIOSFODNN7EXAMP1.",
        "Configured AWS profile with key AKIAIOSFODNN7EXAMP2 for production.",
        "Found hardcoded AWS key: AKIAIOSFODNN7EXAMP3 in deployment logs.",
        "Backup script credentials: AKIAIOSFODNN7EXAMP4 authorized successfully.",
        "Server instance connected via AKIAIOSFODNN7EXAMP5 credentials.",
        "CloudWatch alert triggered by key AKIAIOSFODNN7EXAMP6 activity.",
        "IAM role assumes permissions via AKIAIOSFODNN7EXAMP7 key.",
        "Production environment variable set to AKIAIOSFODNN7EXAMP8.",

        # --- LEVEL 4: GITHUB PERSONAL ACCESS TOKENS (36-45) ---
        "Clone the repository using token ghp_1234567890abcdefghijklmnopqrstuvwxyzABCDEF.",
        "Automation script authenticated with ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890.",
        "GitHub Actions secret updated with ghp_AbCdEfGhIjKlMnOpQrStUvWxYz0123456789.",
        "Workflow failure using token ghp_9876543210FEDCBAzyxwvutsrqponmlkjihgFEDCBA.",
        "Repository access granted via ghp_TokenExample1234567890abcdefghijklmnop.",
        "CI runner token configured as ghp_SecureKeyTestDeployment9876543210ABC.",
        "Developer push rejected due to expired token ghp_OldTokenSample1234567890XYZ.",
        "Automated release generated with ghp_ReleaseManagerTokenABC1234567890.",
        "Webhook authentication header: ghp_WebhookTestKeyForIntegration987654.",
        "Security scan flagged token ghp_ExposedSecretInCodeRepository12345.",

        # --- LEVEL 5: JWT & BEARER TOKEN LEAKS (46-52) ---
        "User session established with token Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjI1MTYyMzkwMjJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c.",
        "Authorization header set to Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI5OTkiLCJyb2xlIjoiYWRtaW4ifQ.signatureExampleTokenString123456789.",
        "API gateway accepted token Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhdXRoMC5jb20ifQ.sampleSignatureTokenStringForTestingPurposesOnly.",
        "Secure session token: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoic2VjcmV0In0.fakeSignatureTokenDataEncryptionHexCode99.",
        "Token validation passed for Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTEyMzA0MDB9.testSignatureTokenVerificationBytes1234."
    ]
    
    print(f"Auditing {len(comprehensive_test_corpus)} LLM responses with expanded database for secret key leaks...")
    audit_results = detect_and_redact_secrets(comprehensive_test_corpus)
    
    leaked_count = sum(1 for r in audit_results if r['leak_detected'])
    clean_count = len(audit_results) - leaked_count
    
    print(f"\nAudit Summary: Clean Responses={clean_count}, Leaks Redacted={leaked_count}")
    for res in audit_results[:50]:
        print(f"[{res['id']:02d}] Leak Detected: {str(res['leak_detected']):<5} | Secured Output: {res['secured'][:82]}...")