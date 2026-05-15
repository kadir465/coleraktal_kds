import pandas as pd
import os

def final_merge():
    file1 = 'data/processed/Final_NHANES_Patient_Narratives_Balanced.csv'
    file2 = 'data/processed/korelaktal_hasta_hikayeleri.csv'
    
    print("Loading datasets for final merge...")
    
    if not os.path.exists(file1):
        print(f"Error: {file1} not found.")
        return
    if not os.path.exists(file2):
        print(f"Error: {file2} not found.")
        return
        
    df_nhanes = pd.read_csv(file1)
    df_global = pd.read_csv(file2)
    
    # Ensure column names match
    # NHANES has 'Hasta_Yorumu' and 'Label'
    # Global has 'Label' and 'Hasta_Yorumu'
    
    # Standardize to 'Hasta_Yorumu' and 'Label'
    df_nhanes = df_nhanes[['Hasta_Yorumu', 'Label']]
    df_global = df_global[['Hasta_Yorumu', 'Label']]
    
    print(f"NHANES Balanced: {len(df_nhanes)} rows.")
    print(f"Global Data: {len(df_global)} rows.")
    
    # Combine
    df_final = pd.concat([df_nhanes, df_global], ignore_index=True)
    
    # Shuffle
    df_final = df_final.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Remove duplicates
    initial_len = len(df_final)
    df_final = df_final.drop_duplicates(subset=['Hasta_Yorumu'])
    final_len = len(df_final)
    
    print(f"\nFinal Combined Total: {initial_len} rows.")
    print(f"After removing duplicates: {final_len} rows.")
    print(f"Final Class Distribution:\n{df_final['Label'].value_counts()}")
    
    # Save to data/final/
    output_path = 'data/final/Korelaktal_Final_Dataset.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_final.to_csv(output_path, index=False)
    
    print(f"\nFinal Dataset saved to: {output_path}")

if __name__ == "__main__":
    final_merge()
