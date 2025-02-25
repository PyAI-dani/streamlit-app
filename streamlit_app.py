import streamlit as st
from persiantools.jdatetime import JalaliDate

import mysql.connector

config = {
    'user': 'root',
    'password': 'mysql1234',
    'host': 'localhost',
    'database': 'barobon_db',
}


def insert_departmental(job_title, people, day, created_at):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO departmental (job_title, people, day, created_at)
            VALUES (%s, %s, %s, %s)
            """
            values = (job_title, people, day, created_at)
            cursor.execute(insert_query, values)
            connection.commit()
            print(f'report inserted successfully: {job_title}, {people}, {day}, {created_at}')
    except mysql.connector.Error as err:
        print(f"خطا در اتصال یا درج داده: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# ======================================================================================================================

def insert_user_info(cid, name, username):
    try:
        connection = mysql.connector.connect(**config)

        if connection.is_connected():
            cursor = connection.cursor()

            sql_insert_query = """
            INSERT INTO user_info (cid, name, usename)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE name=%s, usename=%s
            """
            values = (cid, name, username, name, username)

            cursor.execute(sql_insert_query, values)
            connection.commit()

            print(f'User added or updated successfully: cid={cid}, name={name}, username={username}')

    except mysql.connector.Error as err:
        print(f"خطا در اتصال یا درج داده: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



# ======================================================================================================================

def display_departmental_data():
    try:
        connection = mysql.connector.connect(**config)

        if connection.is_connected():
            cursor = connection.cursor()

            # اجرای کوئری برای انتخاب همه‌ی داده‌ها از جدول
            select_query = "SELECT * FROM departmental"
            cursor.execute(select_query)

            # دریافت تمام رکوردها
            result = cursor.fetchall()

            # بررسی اینکه آیا رکوردی وجود دارد
            if result:
                print("داده‌های موجود در جدول departmental:")
                for row in result:
                    print(f"Job Title: {row[0]}, People: {row[1]}, Day: {row[2]}, Created At: {row[3]}")
            else:
                print("هیچ رکوردی در جدول departmental یافت نشد.")
    except mysql.connector.Error as err:
        print(f"خطا در اتصال یا خواندن داده‌ها: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

display_departmental_data()

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
