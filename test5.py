from func import load_excel()
import pandas as pd
from collections import defaultdict, OrderedDict
import math
from datetime import datetime, timedelta

# Load the Excel file
load_excel()
print(df)
# Constants
total_hours_per_day = 200
daily_hours_per_worker = 8
total_number_of_workers = 25
start_date = datetime.now()  # Starting from today

# Calculate the total required hours for each task
df['Required Hours'] = df['RESIL TIM(Hrs)'] * df['PEP RQ']
df_sorted = df.sort_values(by='PRIORITY', ascending=False)

# Initialize variables for the allocation process
tasks_daily_hours = defaultdict(lambda: OrderedDict((f"Day {i+1}", 0) for i in range(len(df_sorted) * 2)))
tasks_start_end_dates = defaultdict(lambda: {'Start_Date': None, 'End_Date': None})
daily_totals = defaultdict(int)


def allocate_task_hours(task_id, required_hours, pep_rq):
    current_day = 1
    while required_hours > 0:
        available_workers_today = min(pep_rq, total_number_of_workers - daily_totals[f"Day {current_day}"] // daily_hours_per_worker)
        max_hours_today = available_workers_today * daily_hours_per_worker
        available_hours_today = min(max_hours_today, total_hours_per_day - daily_totals[f"Day {current_day}"])
        
        if available_hours_today <= 0:
            current_day += 1
            continue

        hours_allocated_today = min(required_hours, available_hours_today)
        tasks_daily_hours[task_id][f"Day {current_day}"] += hours_allocated_today
        daily_totals[f"Day {current_day}"] += hours_allocated_today
        required_hours -= hours_allocated_today

        if tasks_start_end_dates[task_id]['Start_Date'] is None:
            tasks_start_end_dates[task_id]['Start_Date'] = start_date + timedelta(days=current_day-1)
        tasks_start_end_dates[task_id]['End_Date'] = start_date + timedelta(days=current_day-1)

        if required_hours > 0:
            current_day += 1

# Allocate hours for all tasks
for index, row in df_sorted.iterrows():
    allocate_task_hours(row['TASKS'], row['Required Hours'], row['PEP RQ'])

# Convert the tasks_daily_hours to a DataFrame and add 'Start_Date' and 'End_Date'
tasks_per_day_df = pd.DataFrame.from_dict(tasks_daily_hours, orient='index')

# Limit Days to only days with work
tasks_per_day_df = tasks_per_day_df.loc[:, (tasks_per_day_df != 0).any(axis=0) | tasks_per_day_df.columns.isin(['Start_Date', 'End_Date'])]

tasks_per_day_df['Start_Date'] = tasks_per_day_df.index.map(lambda task: tasks_start_end_dates[task]['Start_Date'])
tasks_per_day_df['End_Date'] = tasks_per_day_df.index.map(lambda task: tasks_start_end_dates[task]['End_Date'])

# Calculate 'DURATION' before converting dates to strings for better accuracy
tasks_per_day_df['DURATION'] = (tasks_per_day_df['End_Date'] - tasks_per_day_df['Start_Date']).dt.days + 1

# Now convert 'Start_Date' and 'End_Date' to string format if needed
tasks_per_day_df['Start_Date'] = tasks_per_day_df['Start_Date'].dt.strftime('%d-%b')
tasks_per_day_df['End_Date'] = tasks_per_day_df['End_Date'].dt.strftime('%d-%b')

tasks_per_day_df_reset = tasks_per_day_df.reset_index().rename(columns={'index': 'INSTANCES', 'Start_Date': 'START DATE', 'End_Date': 'END DATE'})
df_sorted = df_sorted.rename(columns={'TASKS': 'INSTANCES', 'PEP RQ':'NO. OF PEOPLE REQUIRED', 'Required Hours': 'REQUIRED HOURS'})

# Merge tasks_per_day_df_reset with df_sorted on 'INSTANCES'
merged_df = pd.merge(df_sorted, tasks_per_day_df_reset, on='INSTANCES', how='left')

# Display the merged DataFrame
print(merged_df.head())

# Save the merged DataFrame to an Excel file
output_file_path = 'updated_test5.xlsx'  # Adjust the path as needed
merged_df.to_excel(output_file_path, index=False)

print(f"Data saved to {output_file_path}. Please check your file.")
