import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from func import load_excel


df = load_excel()  # Adjust the path to your file
tasks_now = df.sort_values(by='START DATE', ascending=False)
print (tasks_now['INSTANCES'])
data_dict = {column: tasks_now[column].tolist() for column in tasks_now.columns}
print(data_dict)

tasks = data_dict['INSTANCES']
start_dates = data_dict['START DATE']
end_dates = data_dict['END DATE']
durations = data_dict['NO. OF PEOPLE REQUIRED']

# Step 3: Initialize the figure and axis
fig, ax = plt.subplots()

# Step 4: Set y-axis tick labels
ax.set_yticks(np.arange(len(tasks)))
ax.set_yticklabels(tasks)

# Step 5: Plot each task as a horizontal bar
for i in range(len(tasks)):
    start_date = pd.to_datetime(start_dates[i])
    end_date = start_date + pd.DateOffset(days=durations[i])
    ax.barh(i, end_date - start_date, left=start_date, height=0.5, align='center')

# Step 6: Set x-axis limits
min_date = pd.to_datetime(min(start_dates))
max_date = pd.to_datetime(max(start_dates)) + pd.DateOffset(days=max(durations))
ax.set_xlim(min_date, max_date)

# Step 7: Customize the chart
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.WeekdayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
ax.set_xlabel('Date')
ax.set_ylabel('Tasks')
ax.set_title('Task 1 Gantt Chart')

# Step 8: Display the chart
plt.grid(True)
plt.grid(ls='-.')
plt.show()