import re
import sqlite3

# --- 0. Boshlang'ich ma'lumotlar ---
students = [
    {'name': 'Aida', 'group': 'IS-24-01', 'score': 82, 'attendance': 91, 'email': 'aida@atu.edu.kz'},
    {'name': 'Miras', 'group': 'IS-24-01', 'score': 69, 'attendance': 88, 'email': 'miras@atu.edu.kz'},
    {'name': 'Dana', 'group': 'IS-24-02', 'score': 91, 'attendance': 96, 'email': 'dana@atu.edu.kz'},
    {'name': 'Timur', 'group': 'IS-24-02', 'score': 74, 'attendance': 62, 'email': 'timur_at_atu.kz'},
    {'name': 'Aliya', 'group': 'IS-24-03', 'score': 87, 'attendance': 79, 'email': 'aliya@atu.edu.kz'},
    {'name': 'Arman', 'group': 'IS-24-03', 'score': 55, 'attendance': 72, 'email': 'arman@atu.edu.kz'}
]

print("=== ZADANIYA 1: Sravnenie dvux stiley ===")
# Imperativ uslub (sikl yordamida)
passed_imperative = []
for student in students:
    if student['score'] >= 75:
        passed_imperative.append(student['name'])

# Deklarativ uslub (list comprehension)
passed_declarative = [
    student['name'] for student in students if student['score'] >= 75
]

print("Imperativ:", passed_imperative)
print("Deklarativ:", passed_declarative)
print(" Tengmi?", passed_imperative == passed_declarative)


print("\n=== ZADANIYA 2: Usloviya dlya kolleksiy ===")
has_excellent = any(s['score'] >= 90 for s in students)
all_attended = all(s['attendance'] >= 60 for s in students)

# O'rtacha ballni hisoblash (bo'sh ro'yxatni nazorat qilish bilan)
average = (
    sum(s['score'] for s in students) / len(students)
    if students else 0
)

print("Est otlichnik:", has_excellent)
print(" Posemushnost vsex ne nije 60%:", all_attended)
print(" Sredniy ball:", round(average, 1))


print("\n=== ZADANIYA 3: Proverka dannix regulyarnimi vyrajeniyami ===")
group_pattern = r"^[A-Z]{2}-\d{2}-\d{2}$"
email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2}$"

invalid_groups = [
    s['group'] for s in students 
    if not re.fullmatch(group_pattern, s['group'])
]
invalid_emails = [
    s['email'] for s in students 
    if not re.fullmatch(email_pattern, s['email'])
]

print("Oshibochnie gruppi:", invalid_groups)
print("Oshibochnie email:", invalid_emails)


print("\n=== ZADANIYA 4 & 5: SQLite baza va Deklarativ SQL so'rovlari ===")
connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE students (
    name TEXT NOT NULL,
    group_name TEXT NOT NULL,
    score INTEGER NOT NULL,
    attendance INTEGER NOT NULL,
    email TEXT NOT NULL
)
""")

rows = [
    (s['name'], s['group'], s['score'], s['attendance'], s['email'])
    for s in students
]

cursor.executemany("""
INSERT INTO students VALUES (?, ?, ?, ?, ?)
""", rows)
connection.commit()

print("\n--- Tanlangan va saralangan talabalar (score >= 75, attendance >= 70) ---")
query_select = """
SELECT name, score, attendance
FROM students
WHERE score >= 75 AND attendance >= 70
ORDER BY score DESC
"""
for row in cursor.execute(query_select):
    print(row)

print("\n--- Guruhlar bo'yicha yigirma va o'rtacha ball ---")
query_group = """
SELECT group_name, 
       COUNT(*) AS student_count,
       ROUND(AVG(score), 1) AS average_score
FROM students
GROUP BY group_name
HAVING AVG(score) >= 70
ORDER BY average_score DESC
"""
for row in cursor.execute(query_group):
    print(row)


print("\n=== ZADANIYA 6: Integrirovanniy rezultat ===")
query_integrated = """
SELECT name, group_name, score, email
FROM students
WHERE score >= 70 AND attendance >= 70
ORDER BY score DESC
"""

result = cursor.execute(query_integrated).fetchall()
valid_result = [
    row for row in result 
    if re.fullmatch(email_pattern, row[3])
]

for place, row in enumerate(valid_result, start=1):
    name, group_name, score, email = row
    print(f"{place}. {name} | {group_name} | {score} | {email}")

connection.close()
