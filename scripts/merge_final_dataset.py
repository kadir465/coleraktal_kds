import pandas as pd
import os

def merge_stories():
    base_dir = r"c:\Users\kadir\OneDrive\Masaüstü\korelaktal"
    all_dfs = []
    
    # Walk through all directories
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith("_Stories.csv"):
                file_path = os.path.join(root, file)
                print(f"Merging: {file_path}")
                try:
                    df = pd.read_csv(file_path)
                    # Add source info if needed
                    df['Source_File'] = file
                    all_dfs.append(df)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        output_path = os.path.join(base_dir, "Final_NHANES_Patient_Narratives.csv")
        final_df.to_csv(output_path, index=False)
        print(f"\nSuccessfully merged {len(all_dfs)} files.")
        print(f"Total records: {len(final_df)}")
        print(f"Final dataset saved to: {output_path}")
        
        # Display class distribution
        if 'Label' in final_df.columns:
            print("\nClass Distribution:")
            print(final_df['Label'].value_counts())
    else:
        print("No _Stories.csv files found to merge.")

if __name__ == "__main__":
    merge_stories()
