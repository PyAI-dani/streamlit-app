import streamlit as st
from db import *
from persiantools.jdatetime import JalaliDate

st.title('فرم ثبت گزارش روزانه(اداری-منابع انسانی)')

jobs = [
    'سرپرست کارگاه', 'تکنسین', 'مهندس', 'کارمند دفتری', 'تدارکات', 'نگهبان',
    'راننده', 'کارگر ساده', 'سیمانکار', 'بنا', 'برقکار', 'ارماتور بند',
    'آهنگر', 'جوشکار', 'سنگ کار'
]

today_date = JalaliDate.today().strftime("%Y-%m-%d")


with st.form("job_form"):
    people_counts = []
    day_counts = []

    for job in jobs:
        col1, col2, col3 = st.columns(3)

        col1.write(job)

        people_count = col2.number_input(f'تعداد نفرات ({job})', min_value=0, value=0)
        people_counts.append(people_count)

        day_count = col3.number_input(f'تعداد روزها ({job})', min_value=0, value=0)
        day_counts.append(day_count)

    submitted = st.form_submit_button("ثبت گزارش روزانه")

    if submitted:
        for i, job in enumerate(jobs):
            people = people_counts[i]
            days = day_counts[i]
            insert_departmental(job, people, days, today_date)

    if submitted:
        for i, job in enumerate(jobs):
            people = people_counts[i]
            days = day_counts[i]

            if people > 0 or days > 0:
                insert_departmental(job, people, days, today_date)

        st.write("گزارش روزانه(امور اداری-منابع انسانی) ثبت شد\nخسته نباشید🌹")
