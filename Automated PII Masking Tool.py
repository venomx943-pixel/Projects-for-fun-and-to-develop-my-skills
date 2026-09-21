import pandas as pd
import re

# إنشاء بيانات وهمية لشركة ناشئة تحتوي على معلومات حساسة (PII)
data = {
    'User_ID': [101, 102, 103, 104],
    'Name': ['Ahmed Ali', 'Sara Omar', 'Khaled Zaid', 'Fatima Noor'],
    'Email': ['ahmed.ceo@company.com', 'sara.finance@company.com', 'khaled.dev@company.com', 'fatima.hr@company.com'],
    'Phone': ['+966501234567', '+966559876543', '+966541112233', '+966567778899'],
    'Salary': [12000, 15000, 11000, 14000]
}

df = pd.DataFrame(data)
print("--- البيانات الأصلية (تحتوي على مخاطر تسريب PII) ---")
print(df)
print("\n" + "="*50 + "\n")

# دالة لإخفاء الإيميلات (Masking Emails) - نترك الحرف الأول واسم النطاق للتمويه الجزئي
def mask_email(email):
    if pd.isna(email) or '@' not in email:
        return email
    username, domain = email.split('@')
    masked_username = username[0] + '***' + username[-1] if len(username) > 2 else '***'
    return f"{masked_username}@{domain}"

# دالة لإخفاء أقام الهواتف (Masking Phones) - إظهار آخر 4 أرقام فقط
def mask_phone(phone):
    if pd.isna(phone):
        return phone
    # استبدال كل الأرقام عدا آخر 4 نجوم بـ *
    return re.sub(r'\d(?=\d{4})', '*', str(phone))

# تطبيق الدوال على الجدول باستخدام Pandas
df['Email'] = df['Email'].apply(mask_email)
df['Phone'] = df['Phone'].apply(mask_phone)

# إخفاء جزء من الأسماء (اختياري لزيادة الأمان)
df['Name'] = df['Name'].apply(lambda x: x.split()[0] + " [REDACTED]")

print("--- البيانات بعد التطهير والإخفاء (الآمنة للتدريب) ---")
print(df)

#  حفظ البيانات النظيفة في ملف CSV جديد جاهز للذكاء الاصطناعي
# df.to_csv('sanitized_training_data.csv', index=False)