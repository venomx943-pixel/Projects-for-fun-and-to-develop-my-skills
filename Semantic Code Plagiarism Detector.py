import numpy as np
from sentence_transformers import SentenceTransformer


class CodePlagiarismDetector:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def analyze_submission(self, reference_code: str, student_submissions: list, threshold: float = 0.75) -> list:
        ref_embedding = self.model.encode(reference_code, convert_to_tensor=False)
        results = []
        
        for idx, sub in enumerate(student_submissions):
            sub_embedding = self.model.encode(sub["code"], convert_to_tensor=False)
            similarity = np.dot(ref_embedding, sub_embedding) / (
                np.linalg.norm(ref_embedding) * np.linalg.norm(sub_embedding)
            )
            
            is_plagiarized = similarity >= threshold
            results.append({
                "id": idx + 1,
                "student": sub["student"],
                "similarity_score": round(float(similarity), 4),
                "status": "FLAGGED_PLAGIARISM" if is_plagiarized else "CLEAN_SUBMISSION"
            })
        return results


if __name__ == "__main__":
    reference_solution = """
    def calculate_fibonacci(n):
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    """

    submissions = [
        {
            "student": "Alice",
            "code": "def fib(num):\n    if num <= 1:\n        return num\n    x, y = 0, 1\n    for _ in range(2, num + 1):\n        x, y = y, x + y\n    return y"
        },
        {
            "student": "Bob",
            "code": "def compute_fib(n):\n    if n == 0: return 0\n    elif n == 1: return 1\n    else: return compute_fib(n-1) + compute_fib(n-2)"
        },
        {
            "student": "Charlie",
            "code": "def sort_array(arr):\n    return sorted(arr)"
        }
    ]

    detector = CodePlagiarismDetector()
    audit_report = detector.analyze_submission(reference_solution, submissions, threshold=0.75)

    print("--- Code Plagiarism & Semantic Similarity Report ---")
    for report in audit_report:
        print(f"Student: {report['student']} | Score: {report['similarity_score']} | Status: {report['status']}") 