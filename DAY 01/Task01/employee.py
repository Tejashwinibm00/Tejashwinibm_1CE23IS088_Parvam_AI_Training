import pandas as pd
import matplotlib.pyplot as plt
# Step 1: Create Employee Data
data = {
    "EmployeeID": [101, 102, 103, 104, 105],
    "Name": ["John", "Alice", "Bob", "David", "Emma"],
    "Department": ["HR", "Finance", "IT", "Marketing", "Sales"],
    "Age": [25, 30, 22, 35, 28],
    "Salary": [50000, 60000, 45000, 70000, 65000]
}

# Step 2: Create DataFrame
df = pd.DataFrame(data)

# Step 3: Save CSV file automatically in current folder
df.to_csv("employees.csv", index=False)
print("CSV file created successfully!")

# Step 4: Read CSV file
df = pd.read_csv("employees.csv")

print("\n--- Full Employee Data ---")
print(df)

# Step 5: Selecting Data
print("\n--- Select Name Column ---")
print(df["Name"])

print("\n--- Select Name & Salary ---")
print(df[["Name", "Salary"]])

print("\n--- Select First Row ---")
print(df.iloc[0])

# Step 6: Filtering Data
print("\n--- Employees with Salary > 55000 ---")
filtered = df[df["Salary"] > 55000]
print(filtered)

# Step 7: Add New Column (Performance Rating)
df["Performance"] = ["Good", "Excellent", "Average", "Good", "Excellent"]
print("\n--- After Adding Performance Column ---")
print(df)

# Step 8: Basic Operations
print("\n--- Statistics ---")
print("Average Salary:", df["Salary"].mean())
print("Maximum Salary:", df["Salary"].max())
print("Minimum Salary:", df["Salary"].min())

import matplotlib.pyplot as plt
import numpy as np

# Sample employee data
employees = np.arange(1, 11)  # Employee IDs
salaries = np.array([40, 50, 60, 55, 70, 65, 80, 75, 90, 85])  # in thousands
performance = np.array([3, 4, 5, 4, 3, 5, 4, 2, 5, 4])  # rating out of 5
experience = np.array([1, 2, 3, 5, 4, 6, 7, 8, 10, 9])  # years
ages = np.array([22, 25, 28, 30, 35, 40, 45, 50, 55, 60])  # age
departments = ['HR', 'IT', 'Finance', 'Sales']

# Create a 3x2 grid (6 graphs)
plt.figure(figsize=(12, 10))

# 1. Line Graph - Salary trend
plt.subplot(3, 2, 1)
plt.plot(employees, salaries, color='red')
plt.title("Salary Trend")

# 2. Bar Graph - Performance ratings
plt.subplot(3, 2, 2)
plt.bar(employees, performance, color='blue')
plt.title("Performance Ratings")

# 3. Scatter Plot - Experience vs Salary
plt.subplot(3, 2, 3)
plt.scatter(experience, salaries, color='green')
plt.title("Experience vs Salary")

# 4. Histogram - Age distribution
plt.subplot(3, 2, 4)
plt.hist(ages, bins=5, color='purple')
plt.title("Age Distribution")

# 5. Pie Chart - Department distribution
plt.subplot(3, 2, 5)
sizes = [20, 30, 25, 25]  # Example department sizes
plt.pie(sizes, labels=departments, autopct='%1.1f%%',
        colors=['gold', 'cyan', 'lightcoral', 'pink'])
plt.title("Department Distribution")

# 6. Area Plot - Cumulative performance
plt.subplot(3, 2, 6)
plt.fill_between(employees, np.cumsum(performance), color='orange')
plt.title("Cumulative Performance")

# Adjust layout
plt.tight_layout()
plt.show()
