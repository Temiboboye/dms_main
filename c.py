import pandas as pd
from collections import defaultdict, OrderedDict
import math
from datetime import datetime, timedelta

# Load the Excel file
file_path = 'out.xls'  # Update this path to your file
df = pd.read_excel(file_path)

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
tasks_start_end_dates = defaultdict(lambda: {'START DATE': None, 'END DATE': None})
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
        
        if hours_allocated_today < required_hours:
            hours_per_worker_today = min(daily_hours_per_worker, math.floor(hours_allocated_today / pep_rq))
            adjusted_hours_today = hours_per_worker_today * pep_rq
        else:
            adjusted_hours_today = hours_allocated_today
        
        # Mark the start and end dates for the task
        if tasks_start_end_dates[task_id]['START DATE'] is None:
            tasks_start_end_dates[task_id]['START DATE'] = start_date + timedelta(days=current_day-1)
        tasks_start_end_dates[task_id]['END DATE'] = start_date + timedelta(days=current_day-1)
        
        tasks_daily_hours[task_id][f"Day {current_day}"] += adjusted_hours_today
        daily_totals[f"Day {current_day}"] += adjusted_hours_today
        required_hours -= adjusted_hours_today

        if required_hours > 0:
            current_day += 1

# Allocate hours for all tasks
for index, row in df_sorted.iterrows():
    allocate_task_hours(row['TASKS'], row['Required Hours'], row['PEP RQ'])


# Convert the tasks_daily_hours to a DataFrame and add 'START DATE' and 'END DATE'
tasks_per_day_df = pd.DataFrame.from_dict(tasks_daily_hours, orient='index')
tasks_per_day_df['START DATE'] = tasks_per_day_df.index.map(lambda task: tasks_start_end_dates[task]['START DATE'])
tasks_per_day_df['END DATE'] = tasks_per_day_df.index.map(lambda task: tasks_start_end_dates[task]['END DATE'])

# Calculate 'DURATION' as the difference between 'END DATE' and 'START DATE' plus one day
tasks_per_day_df['DURATION'] = (tasks_per_day_df['END DATE'] - tasks_per_day_df['START DATE']).dt.days + 1

# Prepare for merging by resetting index and renaming as needed
tasks_per_day_df_reset = tasks_per_day_df.reset_index().rename(columns={'index': 'INSTANCES'})
df_sorted = df_sorted.rename(columns={'TASKS': 'INSTANCES', 'PEP RQ': 'NO. OF PEOPLE REQUIRED'})
print(df_sorted)
# Merge tasks_per_day_df_reset with df_sorted on 'INSTANCES'
merged_df = pd.merge(df_sorted, tasks_per_day_df_reset[['INSTANCES', 'START DATE', 'END DATE', 'DURATION']], on='INSTANCES', how='left')

# Optionally, format dates for readability
merged_df['START DATE'] = merged_df['START DATE'].dt.strftime('%d-%b')
merged_df['END DATE'] = merged_df['END DATE'].dt.strftime('%d-%b')

# Display the head of the merged DataFrame to verify
print(merged_df)

# Optionally, save the merged DataFrame to an Excel file
output_path = 'merged_output.xlsx'  # Adjust path as needed
merged_df.to_excel(output_path, index=False)

print(f"Data saved to {output_path}. Please check your file.")