# # import streamlit as st
# # from db import get_all_records
# # # from main_page import main_app


# # def view_records():
# #     st.title("سجل المرضى")

# #     records = get_all_records()
# #     if records:
# #         for rec in records:
# #             st.markdown(f"### 🧑‍⚕️ المريض: {rec[1]}")
# #             st.markdown(f"**الأعراض:** {rec[2]}")
# #             st.markdown(f"**نتائج الفحص:** {rec[3]}")
# #             st.markdown(f"**التشخيص:** {rec[4]}")
# #             st.markdown("---")
# #     else:
# #         st.info("لا توجد سجلات محفوظة بعد.")
 


# import streamlit as st
# import pandas as pd
# from db import session  # تأكد ان عندك هذا أو نفس ملف قاعدة البيانات
# from models import UserRecord  # تأكد أنك مستورد الـ UserRecord

# def view_records():
#     st.title("📋 عرض سجلات المستخدمين السابقة")

#     records = session.query(UserRecord).order_by(UserRecord.created_at.desc()).all()
#     data = [{
#         "الاسم": r.username,
#         "الأعراض": r.symptoms,
#         "التشخيص": r.diagnosis,
#         "نص الفحص": r.report_text,
#         "تاريخ الإدخال": r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else "غير محدد"
#     } for r in records]

#     df = pd.DataFrame(data)

#     if not df.empty:
#         st.dataframe(df)
#     else:
#         st.info("لا توجد سجلات محفوظة حالياً.")
