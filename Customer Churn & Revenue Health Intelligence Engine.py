import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(42)
dates = pd.date_range(start="2026-01-01", periods=365, freq="D")
n_samples = 365

customer_segments = np.random.choice(["Enterprise", "SMB", "Startup"], size=n_samples, p=[0.2, 0.5, 0.3])
churn_risk = np.random.beta(a=2, b=5, size=n_samples) * 100
monthly_spend = np.random.gamma(shape=3, scale=1500, size=n_samples)
support_tickets = np.random.poisson(lam=4, size=n_samples)
product_adoption = np.random.uniform(low=10.0, high=95.0, size=n_samples)

df = pd.DataFrame({
    "Date": dates,
    "Segment": customer_segments,
    "ChurnRisk": churn_risk,
    "MonthlySpend": monthly_spend,
    "SupportTickets": support_tickets,
    "ProductAdoption": product_adoption
})

df.loc[15:25, "ChurnRisk"] = np.nan
df.loc[100:105, "MonthlySpend"] = np.nan

df["ChurnRisk"] = df["ChurnRisk"].fillna(df["ChurnRisk"].median())
df["MonthlySpend"] = df["MonthlySpend"].fillna(df["MonthlySpend"].mean())

sns.set_theme(style="whitegrid", palette="muted")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Customer Churn Risk & Revenue Health Intelligence Dashboard", fontsize=18, fontweight="bold", y=0.95)

ax1 = axes[0, 0]
sns.histplot(data=df, x="ChurnRisk", hue="Segment", kde=True, bins=25, ax=ax1, palette="Set2")
ax1.set_title("Customer Churn Risk Distribution by Segment", fontsize=12, fontweight="bold")
ax1.set_xlabel("Churn Risk Score (%)")
ax1.set_ylabel("Customer Count")
ax1.axvline(x=50, color="red", linestyle="--", linewidth=1.5, label="Critical Threshold (50%)")
ax1.legend(loc="upper right")

ax2 = axes[0, 1]
sns.boxplot(data=df, x="Segment", y="MonthlySpend", ax=ax2, palette="Pastel1", width=0.5)
sns.stripplot(data=df, x="Segment", y="MonthlySpend", ax=ax2, color="black", alpha=0.3, jitter=0.2, size=4)
ax2.set_title("Monthly Spend Variance and Outliers Across Segments", fontsize=12, fontweight="bold")
ax2.set_xlabel("Customer Segment")
ax2.set_ylabel("Monthly Spend ($ USD)")

ax3 = axes[1, 0]
sns.scatterplot(data=df, x="ProductAdoption", y="MonthlySpend", hue="ChurnRisk", size="SupportTickets", sizes=(20, 200), palette="coolwarm", ax=ax3)
ax3.set_title("Product Adoption vs. Monthly Spend (Colored by Churn Risk)", fontsize=12, fontweight="bold")
ax3.set_xlabel("Product Adoption Rate (%)")
ax3.set_ylabel("Monthly Spend ($ USD)")
ax3.legend(bbox_to_anchor=(1.05, 1), loc="upper left", title="Metrics")

ax4 = axes[1, 1]
numeric_df = df.select_dtypes(include=[np.number])
corr_matrix = numeric_df.corr()
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="vlag", center=0, cbar=True, ax=ax4, linewidths=0.5)
ax4.set_title("Feature Correlation Matrix", fontsize=12, fontweight="bold")
ax4.tick_params(axis="x", rotation=30)
ax4.tick_params(axis="y", rotation=0)

plt.tight_layout()
plt.savefig("customer_churn_analytics_dashboard.png", dpi=300)
plt.show()