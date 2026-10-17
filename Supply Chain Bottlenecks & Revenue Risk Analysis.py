import matplotlib.pyplot as plt

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
projected_revenue = [45000, 48000, 52000, 61000, 75000, 95000, 88000, 82000, 90000, 110000, 135000, 160000]
actual_revenue = [44000, 47000, 50000, 58000, 70000, 82000, 76000, 71000, 85000, 98000, 115000, 130000]
supply_delay_days = [2, 3, 5, 4, 8, 14, 18, 12, 7, 4, 9, 15]
warehouse_cost = [12000, 12500, 13000, 15000, 18000, 24000, 26000, 22000, 19000, 17000, 21000, 28000]
product_categories = ['Electronics', 'Apparel', 'Home & Kitchen', 'Groceries', 'Beauty']
category_loss_share = [40, 25, 15, 12, 8]
delivery_times = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
order_frequencies = [150, 300, 450, 600, 850, 1100, 950, 800, 700, 550, 400, 300, 200, 150, 100, 80, 50, 30, 15, 5]

plt.style.use('seaborn-v0_8-whitegrid')
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('Global Supply Chain & Revenue Risk Analytics Dashboard', fontsize=16, fontweight='bold', color='#222222')

ax1 = axes[0, 0]
ax1.plot(months, projected_revenue, color='#2ca02c', linestyle='--', marker='o', linewidth=2, label='Projected Revenue')
ax1.plot(months, actual_revenue, color='#d62728', linestyle='-', marker='s', linewidth=2.5, label='Actual Revenue')
ax1.set_title('Revenue Shortfall Analysis (2026)', fontsize=12, fontweight='bold')
ax1.set_xlabel('Months')
ax1.set_ylabel('Revenue ($ USD)')
ax1.set_ylim(30000, 180000)
ax1.axvspan('Jun', 'Aug', color='red', alpha=0.15)
ax1.annotate('Peak Supply Chain Crisis', xy=('Jul', 76000), xytext=('Mar', 140000),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))
ax1.legend(loc='upper left')

ax1_twin = ax1.twinx()
ax1_twin.plot(months, supply_delay_days, color='#9467bd', linestyle=':', marker='^', linewidth=1.5, label='Avg Supply Delay (Days)')
ax1_twin.set_ylabel('Delay Duration (Days)', color='#9467bd')
ax1_twin.set_ylim(0, 25)
ax1_twin.legend(loc='upper right')

ax2 = axes[0, 1]
ax2.scatter(supply_delay_days, warehouse_cost, color='#ff7f0e', s=90, edgecolors='black', label='Monthly Metrics')
ax2.set_title('Warehouse Cost vs. Supply Chain Delay', fontsize=12, fontweight='bold')
ax2.set_xlabel('Average Delay (Days)')
ax2.set_ylabel('Warehouse Maintenance Cost ($)')
ax2.set_xlim(0, 20)
ax2.axvline(x=10, color='red', linestyle='--', linewidth=1.5, label='Critical Threshold (10 Days)')
ax2.legend()

ax3 = axes[1, 0]
colors_bar = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c']
bars = ax3.bar(product_categories, category_loss_share, color=colors_bar, edgecolor='black')
ax3.set_title('Financial Loss Share by Product Category (%)', fontsize=12, fontweight='bold')
ax3.set_xlabel('Product Category')
ax3.set_ylabel('Loss Share (%)')
ax3.set_ylim(0, 50)
ax3.tick_params(axis='x', rotation=10)
ax3.axhline(y=20, color='gray', linestyle=':', linewidth=1)

ax4 = axes[1, 1]
ax4.hist(delivery_times, weights=order_frequencies, bins=6, color='#17becf', edgecolor='black', alpha=0.8)
ax4.set_title('Order Fulfillment Time Distribution (Weighted by Volume)', fontsize=12, fontweight='bold')
ax4.set_xlabel('Delivery Time (Days)')
ax4.set_ylabel('Order Volume')
ax4.set_xlim(0, 22)
ax4.axvline(x=7, color='green', linestyle='--', linewidth=2, label='Target SLA (7 Days)')
ax4.legend()

plt.tight_layout()
plt.savefig('supply_chain_risk_dashboard.png', dpi=300)
plt.show()
