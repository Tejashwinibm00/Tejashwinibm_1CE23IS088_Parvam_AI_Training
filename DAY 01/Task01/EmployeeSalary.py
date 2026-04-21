import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    "Salary": [50000, 60000, 45000, 70000, 65000,
               52000, 58000, 47000, 68000, 64000,
               55000, 72000, 46000, 63000, 75000]
}

# Step 2: Create DataFrame
df = pd.DataFrame(data)

# Step 3: Save CSV file automatically
csv_file = "employees.csv"
df.to_csv(csv_file, index=False)
print("CSV file created successfully!")

# Step 4: Read CSV file
df = pd.read_csv(csv_file)

print("\n--- Full Employee Data ---")
print(df)

# Step 5: Ask user for salary input and show details
try:
    salary_input = int(input("\nEnter the salary: "))
    result = df[df["Salary"] == salary_input]
    if not result.empty:
        print("\n--- Employee(s) with Salary", salary_input, "---")
        print(result)
    else:
        print("No employee found with that salary.")
except ValueError:
    print("Invalid input. Please enter a number.")

# Step 6: Filtering Example
print("\n--- Employees with Salary > 60000 ---")
print(df[df["Salary"] > 60000])

# Step 7: Add New Column (Performance Rating)
df["Performance"] = ["Good", "Excellent", "Average", "Good", "Excellent",
                     "Good", "Excellent", "Average", "Good", "Excellent",
                     "Good", "Excellent", "Average", "Good", "Excellent"]
print("\n--- After Adding Performance Column ---")
print(df)

# Step 8: Basic Statistics
print("\n--- Statistics ---")
print("Average Salary:", df["Salary"].mean())
print("Maximum Salary:", df["Salary"].max())
print("Minimum Salary:", df["Salary"].min())

# Step 9: Visualizations
employees = df["EmployeeID"]
salaries = df["Salary"]
performance = [3, 4, 5, 4, 3, 5, 4, 2, 5, 4, 3, 4, 5, 4, 3]
experience = [1, 2, 3, 5, 4, 6, 7, 8, 10, 9, 4, 6, 3, 7, 8]
ages = df["Age"]
departments = df["Department"].unique()

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
sizes = df["Department"].value_counts().values
plt.pie(sizes, labels=departments, autopct='%1.1f%%',
        colors=['gold', 'cyan', 'lightcoral', 'pink', 'lightblue'])
plt.title("Department Distribution")

# 6. Area Plot - Cumulative performance
plt.subplot(3, 2, 6)
plt.fill_between(employees, np.cumsum(performance), color='orange')
plt.title("Cumulative Performance")

plt.tight_layout()
plt.show()
