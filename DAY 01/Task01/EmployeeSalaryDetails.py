import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# Step 1: Create Employee Data (15 employees)
data = {
    "EmployeeID": list(range(101, 116)),
    "Name": ["John", "Alice", "Bob", "David", "Emma",
             "Frank", "Grace", "Hannah", "Ian", "Jack",
             "Karen", "Leo", "Mona", "Nina", "Oscar"],
    "Department": ["HR", "Finance", "IT", "Marketing", "Sales",
                   "HR", "Finance", "IT", "Marketing", "Sales",
                   "HR", "Finance", "IT", "Marketing", "Sales"],
    "Age": [25, 30, 22, 35, 28,
            29, 31, 33, 27, 34,
            35, 36, 28, 29, 37],
    "Salary": [0]*15
}

# Step 2: Create DataFrame and save to CSV
df = pd.DataFrame(data)
csv_file = "employees.csv"
df.to_csv(csv_file, index=False)

print("CSV file created successfully!")

# Step 3: Ask for employee name and salary
name_input = input("Enter the employee's name: ").strip()
if name_input not in df["Name"].values:
    print("Employee not found.")
    exit()

try:
    salary_input = int(input(f"Enter {name_input}'s salary: "))
except ValueError:
    print("Invalid salary input. Please enter a number.")
    exit()

# Step 4: Update salary
df.loc[df["Name"] == name_input, "Salary"] = salary_input
df.to_csv(csv_file, index=False)
print(f"Salary updated for {name_input}!")

# Step 5: Generate PDF with attractive table
emp = df[df["Name"] == name_input].iloc[0]

pdf_file = f"{name_input}_details.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=letter)
elements = []

styles = getSampleStyleSheet()
title = Paragraph("Employee Report", styles['Title'])
elements.append(title)
elements.append(Spacer(1, 20))

# Table data
table_data = [
    ["Field", "Details"],
    ["Employee ID", emp["EmployeeID"]],
    ["Name", emp["Name"]],
    ["Department", emp["Department"]],
    ["Age", emp["Age"]],
    ["Salary", emp["Salary"]],
]

# Create table
table = Table(table_data, colWidths=[120, 250])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#DCE6F1")),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

elements.append(table)
elements.append(Spacer(1, 30))


doc.build(elements)
print(f"PDF generated: {pdf_file}")
