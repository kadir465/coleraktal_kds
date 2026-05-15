import pandas as pd
import glob
import os

def merge_all_stories():
    # Find all _Stories.csv files in data/raw subdirectories
    story_files = glob.glob('data/raw/**/*_Stories.csv', recursive=True)
    
    if not story_files:
        print("No _Stories.csv files found in data/raw/")
        return

    print(f"Found {len(story_files)} story files to merge.")
    
    dfs = []
    for f in story_files:
        try:
            df = pd.read_csv(f)
            # Ensure columns are Hasta_Yorumu and Label
            if 'Hasta_Yorumu' not in df.columns and 'Text' in df.columns:
                df = df.rename(columns={'Text': 'Hasta_Yorumu'})
            
            # Keep only relevant columns
            if 'Hasta_Yorumu' in df.columns and 'Label' in df.columns:
                df = df[['Hasta_Yorumu', 'Label']]
                dfs.append(df)
                print(f"Loaded {f}: {len(df)} rows.")
            else:
                print(f"Skipping {f}: Required columns not found. Columns: {df.columns.tolist()}")
        except Exception as e:
            print(f"Error loading {f}: {e}")

    if not dfs:
        print("No valid dataframes to merge.")
        return

    merged_df = pd.concat(dfs, ignore_index=True)
    
    # Remove duplicates
    initial_len = len(merged_df)
    merged_df = merged_df.drop_duplicates(subset=['Hasta_Yorumu'])
    final_len = len(merged_df)
    
    print(f"\nMerged Total: {initial_len} rows.")
    print(f"After removing duplicates: {final_len} rows.")
    print(f"Class distribution:\n{merged_df['Label'].value_counts()}")
    
    # Save to data/processed/
    output_path = 'data/processed/Final_NHANES_Patient_Narratives.csv'
    merged_df.to_csv(output_path, index=False)
    print(f"\nSaved merged stories to: {output_path}")

if __name__ == "__main__":
    merge_all_stories()
