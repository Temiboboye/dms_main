import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Load the Excel file
file_path = 'updated_test5.xlsx'
df = pd.read_excel(file_path)

# Function to check and convert START_DATE column to datetime
def check_and_convert_dates(df, date_column='START DATE', expected_format='%d-%b', year=2024):
    try:
        # Append year for conversion since the original dates might not include it
        full_dates = df[date_column].apply(lambda x: f"{x}-{year}")
        # Convert to datetime
        df[date_column] = pd.to_datetime(full_dates, format=f"{expected_format}-%Y")
        print(f"'{date_column}' converted successfully to datetime format.")
    except ValueError as e:
        print(f"Error converting '{date_column}' to datetime: {e}")

# Convert 'START DATE' to datetime
check_and_convert_dates(df, date_column='START DATE', expected_format='%d-%b', year=2024)

# Sort the DataFrame by 'START DATE'
df_sorted = df.sort_values(by='START DATE', ascending=False)

# Assuming 'DURATION' or similar is required but not present, let's create a dummy 'DURATION' for demonstration
# Replace or adjust as necessary based on your data
#df_sorted['DURATION'] =   # Example: random durations between 1 to 4

# Initialize the figure and axis for plotting
fig, ax = plt.subplots(figsize=(10, 6))

# Set y-axis with the 'INSTANCES' as labels
ax.set_yticks(range(len(df_sorted['INSTANCES'])))
ax.set_yticklabels(df_sorted['INSTANCES'])

# Plot each 'INSTANCE' as a horizontal bar
for i, (start_date, duration) in enumerate(zip(df_sorted['START DATE'], df_sorted['DURATION'])):
    ax.barh(i, duration, left=start_date, color='skyblue', edgecolor='black')

# Set x-axis format for dates
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))

# Adding labels and title
plt.xlabel('Date')
plt.ylabel('Instances')
plt.title('Gantt Chart of Instances by Start Date')

plt.tight_layout()
plt.show()
