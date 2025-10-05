import os
import pandas as pd

folder_path = 'C:/Users/Minh Ngoc/OneDrive/Documents/FPT_AI Materials/Fall 2025/ADY201m_AI & DS vs Python & SQL/Hotel Analysis'

dfs = []

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        city_province = filename.replace('booking_', '').replace('.csv', '').upper()
        df = pd.read_csv(file_path)
        df['City/Province'] = city_province
        # Move 'City/Province' column to after 'Stay'
        cols = df.columns.tolist()
        if 'Stay' in cols and 'City/Province' in cols:
            stay_idx = cols.index('Stay')
            # Remove 'City/Province' and insert after 'Stay'
            cols.remove('City/Province')
            cols.insert(stay_idx + 1, 'City/Province')
            df = df[cols]
        dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)
combined_df.to_csv('combined_bookings.csv', index=False)

print('All files combined successfully into combined_bookings.csv')