import matplotlib.pyplot as plt


# أوقات التشغيل (ساعات)
hours = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

loss_values = [0.85, 0.62, 0.45, 0.30, 0.22, 0.18, 0.15, 0.12, 0.10, 0.08]
cpu_usage = [25, 30, 45, 50, 85, 90, 60, 40, 35, 30] # نقطة ارتفاع عند الساعة 5-6

latencies = [120, 130, 125, 140, 135, 150, 160, 120, 125, 130, 300, 110, 125, 130, 145]

request_types = ['Normal Query', 'Prompt Injection', 'Rate Limit Exceeded', 'Malformed Payload']
request_counts = [1200, 150, 80, 30]

input_sizes = [10, 25, 50, 100, 200, 350, 500, 750, 1000]
processing_times = [5, 12, 22, 45, 90, 160, 240, 480, 950]


plt.style.use('seaborn-v0_8-darkgrid')

fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('AI Server Health & Security Threat Dashboard', fontsize=18, fontweight='bold', color='#1a1a1a')

ax1 = axes[0, 0]

line1 = ax1.plot(hours, loss_values, color='blue', marker='o', linewidth=2, label='Model Loss')
ax1.set_title('Model Loss & CPU Load Over Time', fontsize=12, fontweight='bold')
ax1.set_xlabel('Operation Time (Hours)')
ax1.set_ylabel('Loss Value', color='blue')
ax1.set_ylim(0, 1.0)

# استخدام المحور المزدوج (Twinx) لرسم نسبة استخدام المعالج
ax1_twin = ax1.twinx()
line2 = ax1_twin.plot(hours, cpu_usage, color='red', linestyle='--', marker='s', label='CPU Usage (%)')
ax1_twin.set_ylabel('CPU Usage (%)', color='red')
ax1_twin.set_ylim(0, 100)

# إضافة التظليل التوضيحي لفترة الضغط العالي (axvspan)
ax1.axvspan(5, 6.5, color='orange', alpha=0.3)

ax1.annotate('High Traffic / Attack Spike', xy=(5.5, 0.2), xytext=(2.5, 0.5),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper right')


ax2 = axes[0, 1]
colors = ['#2ca02c', '#d62728', '#ff7f0e', '#9467bd']
bars = ax2.bar(request_types, request_counts, color=colors)
ax2.set_title('Security Categorization of Incoming Requests', fontsize=12, fontweight='bold')
ax2.set_xlabel('Request Classification')
ax2.set_ylabel('Count')
ax2.set_yscale('log') # تحويل المحور لمقياس لوغاريتمي لرؤية الأعداد الصغيرة بوضوح
ax2.set_yticks([10, 100, 1000, 2000])
ax2.set_yticklabels(['10', '100', '1K', '2K'])
ax2.tick_params(axis='x', rotation=15) # تدوير النصوص لمنع التداخل

# إضافة خط أفقي مرجعي كحد تحذيري (axhline)
ax2.axhline(y=100, color='red', linestyle=':', linewidth=1.5, label='Alert Threshold (100)')
ax2.legend()


ax3 = axes[1, 0]
ax3.hist(latencies, bins=8, color='#1f77b4', edgecolor='black', alpha=0.7)
ax3.set_title('Latency Distribution (Response Time)', fontsize=12, fontweight='bold')
ax3.set_xlabel('Latency (ms)')
ax3.set_ylabel('Frequency')
ax3.set_xlim(80, 350)

# وضع خط رأسي مرجعي لمعدل الأمان (axvline)
ax3.axvline(x=200, color='darkorange', linestyle='--', linewidth=2, label='SLA Target (200ms)')
ax3.legend()
ax3.grid(True)


ax4 = axes[1, 1]
ax4.scatter(input_sizes, processing_times, color='purple', s=80, edgecolors='black', label='Requests')
ax4.set_title('Processing Time vs. Input Payload Size', fontsize=12, fontweight='bold')
ax4.set_xlabel('Payload Size (Tokens / KB)')
ax4.set_ylabel('Processing Time (ms)')
ax4.set_xticks([0, 250, 500, 750, 1000])

# إضافة نص توضيحي داخلي
ax4.annotate('Outlier Payload', xy=(1000, 950), xytext=(600, 800),
             arrowprops=dict(arrowstyle='->', color='purple', lw=1.5))
ax4.grid(True)
ax4.legend()

plt.tight_layout() 
plt.savefig('ai_server_monitoring_dashboard.png', dpi=300) # حفظ اللوحة كصورة عالي الجودة
plt.show() 