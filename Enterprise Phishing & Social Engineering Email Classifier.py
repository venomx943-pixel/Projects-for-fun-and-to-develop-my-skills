from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline


class EnterprisePhishingClassifier:
    def __init__(self):
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1, 2))),
            ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
        ])

    def train(self, training_data: list, labels: list):
        self.pipeline.fit(training_data, labels)

    def predict_threats(self, emails: list) -> list:
        predictions = self.pipeline.predict(emails)
        probabilities = self.pipeline.predict_proba(emails)
        
        results = []
        for idx, email in enumerate(emails):
            pred_label = predictions[idx]
            confidence = float(max(probabilities[idx]))
            results.append({
                "id": idx + 1,
                "email_snippet": email[:60] + "...",
                "classification": "MALICIOUS_PHISHING" if pred_label == 1 else "SAFE_LEGITIMATE",
                "confidence": round(confidence, 4)
            })
        return results


if __name__ == "__main__":
    corpus = [
        "Please update your corporate password immediately via the external link provided to avoid account suspension.",
        "Your quarterly financial performance report has been successfully uploaded to the internal SharePoint portal.",
        "URGENT: Verify your Microsoft 365 credentials now or your mailbox will be permanently deactivated today.",
        "Scheduled server maintenance will take place this Saturday from 02:00 AM to 04:00 AM UTC.",
        "Dear employee, your payroll direct deposit details require immediate confirmation through this login page.",
        "The software architecture review meeting is rescheduled to Thursday afternoon in conference room B.",
        "Security Alert: Unusual sign-in attempt detected from an unrecognized IP address. Confirm your identity here.",
        "Please review the attached project roadmap and provide your feedback before the Friday deadline.",
        "Congratulations! You have won a corporate bonus reward. Claim your funds by entering your banking info.",
        "Access guidelines for the new cloud infrastructure staging servers have been published on the wiki.",
        "Action Required: Your VPN security certificate has expired. Download the update patch immediately.",
        "The cafeteria menu for next week has been updated with new healthy dietary options.",
        "Final notice: Update your employee portal account details to continue receiving health insurance benefits.",
        "Team building event registration closes tomorrow evening. Make sure to submit your RSVP.",
        "IT Support: Your account has triggered a security policy violation. Verify your credentials to unlock.",
        "Please submit your travel expense reports for the recent conference before the end of the month.",
        "Urgent bank notice: Unauthorized wire transfer attempted on your corporate card. Verify identity now.",
        "Weekly engineering sync notes and architecture decisions are now available on Confluence.",
        "Security update: Install the latest patch for your workstation operating system by tonight.",
        "Reminder: Annual compliance training modules must be completed prior to the end of Q3.",
        "Alert: Your cloud storage quota is 95% full. Upgrade your storage tier using this verification link.",
        "The office network will experience intermittent connectivity during tomorrow's fiber upgrade.",
        "Critical security advisory: Immediate password reset required for all database administrators.",
        "Please welcome our new senior software engineer joining the artificial intelligence team today.",
        "Account suspension warning: Confirm your billing details to maintain active cloud server subscriptions.",
        "Standard operating procedures for containerized microservices deployment have been updated.",
        "Immediate action needed: Verify your identity to prevent permanent deletion of your corporate email.",
        "Code review guidelines for Python and C++ repositories are posted in the developer channel.",
        "Security warning: Suspicious login blocked from an overseas location. Review recent activity.",
        "The quarterly cybersecurity awareness seminar will be held via video conference on Wednesday.",
        "Urgent notification: Your employee benefits portal requires immediate re-authentication.",
        "Database backup scripts executed successfully across all production and staging environments.",
        "Action required: Confirm your corporate travel booking details through the HR portal link.",
        "Network latency metrics have stabilized following the recent firewall rule optimization.",
        "Security notice: Click here to authenticate your credentials and secure your digital workspace.",
        "The internal bug bounty program leaderboard has been updated with new vulnerability points.",
        "Urgent alert: Your email storage limit exceeded. Validate your account credentials to expand.",
        "API rate limiting policies and documentation for external developers are now online.",
        "Final warning: Update your payroll direct deposit information to avoid processing delays.",
        "Automated vulnerability scan completed with zero critical findings on primary web servers.",
        "Security alert: Verify your multi-factor authentication device to restore portal access.",
        "Project sprint planning and backlog grooming sessions are scheduled for Monday morning.",
        "Urgent request: Update your corporate SSO credentials to comply with new security mandates.",
        "System architecture diagrams for the microservices infrastructure have been revised.",
        "Account verification required: Confirm your identity to prevent termination of network access.",
        "The annual developer conference registration is now open for all engineering team members.",
        "Security warning: Unauthorized access attempt detected on your server instance. Verify now.",
        "Internal code repository migration to GitHub Enterprise is scheduled for this weekend.",
        "Urgent notice: Update your password to prevent immediate suspension of cloud privileges.",
        "Standard agile development methodologies and sprint retrospectives summary report."
    ]

    labels = [
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
        1, 0, 1, 0, 1, 0, 1, 0, 0, 0,
        1, 0, 0, 0, 1, 0, 1, 0, 0, 0,
        1, 0, 0, 0, 1, 0, 1, 0, 1, 0,
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0
    ]

    test_emails = [
        "URGENT: Verify your Microsoft 365 credentials now or your mailbox will be deactivated.",
        "The software architecture review meeting is rescheduled to Thursday afternoon.",
        "Security Alert: Unusual sign-in attempt detected. Confirm your identity immediately via this link.",
        "Weekly engineering sync notes and architecture decisions are now available on Confluence.",
          "Account suspension warning: Confirm your billing details to maintain active cloud server subscriptions.",
                "Standard operating procedures for containerized microservices deployment have been updated.",
                "Immediate action needed: Verify your identity to prevent permanent deletion of your corporate email.",
                "Code review guidelines for Python and C++ repositories are posted in the developer channel.",
                "Security warning: Suspicious login blocked from an overseas location. Review recent activity.",
                "The quarterly cybersecurity awareness seminar will be held via video conference on Wednesday.",
                "Urgent notification: Your employee benefits portal requires immediate re-authentication.",
                "Database backup scripts executed successfully across all production and staging environments.",
                "Action required: Confirm your corporate travel booking details through the HR portal link.",
                "Network latency metrics have stabilized following the recent firewall rule optimization.",
                "Security notice: Click here to authenticate your credentials and secure your digital workspace.",
                "The internal bug bounty program leaderboard has been updated with new vulnerability points.",
                "Urgent alert: Your email storage limit exceeded. Validate your account credentials to expand.",
                "API rate limiting policies and documentation for external developers are now online.",
                "Final warning: Update your payroll direct deposit information to avoid processing delays.",
                "Automated vulnerability scan completed with zero critical findings on primary web servers.",
                "Security alert: Verify your multi-factor authentication device to restore portal access.",
                "Project sprint planning and backlog grooming sessions are scheduled for Monday morning.",
                "Urgent request: Update your corporate SSO credentials to comply with new security mandates.",
                "System architecture diagrams for the microservices infrastructure have been revised.",
                "Account verification required: Confirm your identity to prevent termination of network access.",
                "The annual developer conference registration is now open for all engineering team members.",
                "Security warning: Unauthorized access attempt detected on your server instance. Verify now."
    ]

    classifier = EnterprisePhishingClassifier()
    classifier.train(corpus, labels)
    
    audit_results = classifier.predict_threats(test_emails)
    
    print("--- Enterprise Phishing Detection Audit Report ---")
    for res in audit_results:
        print(f"[{res['id']}] Status: {res['classification']} | Confidence: {res['confidence']} | Text: {res['email_snippet']}")