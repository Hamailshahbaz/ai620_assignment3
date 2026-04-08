import pandas as pd
import os

# PART A: CLEANING PAKWHEELS
print("Cleaning PakWheels dataset...")
pw_df = pd.read_csv('data/PakWheels.csv')
pw_df.columns = pw_df.columns.str.strip().str.lower()


pw_df['transmission'] = pw_df['transmission'].str.capitalize()

pw_df = pw_df[(pw_df['engine'] >= 600) & (pw_df['engine'] <= 6000)]
pw_df = pw_df[pw_df['price'] >= 100000]

pw_df.drop_duplicates(subset=['addref'], inplace=True)
pw_df.to_csv('data/PakWheels_Cleaned.csv', index=False)


# PART B: CLEANING CORRUPTED SYNTHETIC
print("Cleaning Corrupted Synthetic dataset...")
syn_df = pd.read_csv('data/corrupted_synthetic_dataset.csv')
syn_df.columns = syn_df.columns.str.strip().str.lower()

syn_df = syn_df.dropna(subset=['customer_id'])

syn_df = syn_df[(syn_df['amount'] >= 5) & (syn_df['amount'] <= 1000)]

syn_df.drop_duplicates(subset=['sale_id'], inplace=True)

syn_df.to_csv('data/Synthetic_Cleaned_Task4.csv', index=False)
print("✅ Done! Both cleaned files are in the data/ folder.")