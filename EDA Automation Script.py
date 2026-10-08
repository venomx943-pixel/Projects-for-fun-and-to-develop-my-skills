import numpy as np

class AutomatedEDAPipeline:
    def __init__(self, data, feature_names=None):
        self.data = np.array(data, dtype=float)
        self.n_samples, self.n_features = self.data.shape
        self.feature_names = feature_names if feature_names else [f"Feature_{i+1}" for i in range(self.n_features)]

    def compute_summary_statistics(self):
        stats = {}
        for i, name in enumerate(self.feature_names):
            col = self.data[:, i]
            stats[name] = {
                "Mean": float(np.mean(col)),
                "Median": float(np.median(col)),
                "Std_Dev": float(np.std(col)),
                "Min": float(np.min(col)),
                "Max": float(np.max(col))
            }
        return stats

    def compute_correlation_matrix(self):
        # Compute Pearson correlation matrix across features
        corr_matrix = np.corrcoef(self.data, rowvar=False)
        return corr_matrix

    def detect_outliers_iqr(self, threshold=1.5):
        outliers_report = {}
        for i, name in enumerate(self.feature_names):
            col = self.data[:, i]
            q25, q75 = np.percentile(col, [25, 75])
            iqr = q75 - q25
            lower_bound = q25 - (threshold * iqr)
            upper_bound = q75 + (threshold * iqr)
            
            outlier_indices = np.where((col < lower_bound) | (col > upper_bound))[0].tolist()
            outliers_report[name] = {
                "lower_bound": float(lower_bound),
                "upper_bound": float(upper_bound),
                "outlier_count": len(outlier_indices),
                "outlier_rows": outlier_indices
            }
        return outliers_report

    def generate_full_report(self):
        print("==================================================")
        print("          AUTOMATED EDA ENGINE REPORT             ")
        print("==================================================")
        print(f"Dataset Shape: {self.n_samples} Samples, {self.n_features} Features\n")
        
        # Summary Statistics
        print("--- 1. Summary Statistics ---")
        stats = self.compute_summary_statistics()
        for feat, val in stats.items():
            print(f"Feature: {feat}")
            for metric, m_val in val.items():
                print(f"   {metric}: {m_val:.4f}")
            print("-" * 30)
            
        # Outliers Report
        print("\n--- 2. Outliers Detection (IQR Method) ---")
        outliers = self.detect_outliers_iqr()
        for feat, val in outliers.items():
            print(f"Feature: {feat} | Outliers Found: {val['outlier_count']} (Rows: {val['outlier_rows']})")
            
        # Correlation Matrix
        print("\n--- 3. Correlation Matrix ---")
        corr = self.compute_correlation_matrix()
        print(np.round(corr, 4))
        print("==================================================")

# --- Testing the Pipeline ---
if __name__ == "__main__":
    # Mock dataset: [Study_Hours, Exam_Score, Sleep_Hours, Stress_Level]
    mock_dataset = [
        [2.0, 50.0, 7.0, 3.0],
        [4.0, 65.0, 6.5, 4.0],
        [6.0, 80.0, 8.0, 2.0],
        [8.0, 95.0, 7.5, 1.0],
        [1.0, 40.0, 5.0, 5.0],
        [10.0, 98.0, 9.0, 1.0],
        [15.0, 30.0, 4.0, 9.0] # Contains an anomaly / outlier row
    ]
    
    features = ["Study_Hours", "Exam_Score", "Sleep_Hours", "Stress_Level"]
    
    eda_pipeline = AutomatedEDAPipeline(mock_dataset, feature_names=features)
    eda_pipeline.generate_full_report()