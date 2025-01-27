import pandas as pd
import ast
import os

# Directory where the batch result files are stored
directory = './'  # Change this to the directory where your files are located
output_file = 'merged_results.csv'  # Output file name

# List of result filenames (you can add more if necessary)
metric_files = [
    'test_tf_batch_1_overlap_results.csv',
    'test_tf_batch_1_jaccard_results.csv',
    'test_tf_batch_1_dice_results.csv',
    'test_tf_batch_1_simpson_results.csv',
    'test_tf_batch_1_pmi_results.csv',
    'test_tf_batch_1_npmi_results.csv'
]

# Function to extract the average of the Coef(95% CI) range
def extract_coef_range(coef_range):
    try:
        # Convert the string '[x, y]' into a list
        coef_list = ast.literal_eval(coef_range)
        return (coef_list[0] + coef_list[1]) / 2  # Return the mean of the range
    except:
        return None  # Return None if parsing fails

# Initialize an empty DataFrame to hold merged results
merged_df = None

# Iterate through each metric file and clean/merge the data
for file in metric_files:
    # Construct the full path to the file
    file_path = os.path.join(directory, file)

    # Check if the file exists before attempting to read it
    if os.path.exists(file_path):
        print(f"Reading {file_path}...")

        # Try reading the file with space or tab delimiter
        try:
            # Try reading with whitespace delimiter first
            df = pd.read_csv(file_path, sep='\s+', header=None)
        except pd.errors.ParserError:
            # If space delimiter doesn't work, try tab delimiter
            df = pd.read_csv(file_path, delimiter='\t', header=None)

        # Inspect column names and fix them
        print(f"Columns in {file}: {df.columns.tolist()}")
        
        # Add headers manually if the data doesn't contain them
        # These headers need to match the actual structure of your data
        df.columns = ['A.name', 'B.name', 'A.interval_count', 'B.interval_count', 'A.size', 'B.size', 'A_or_B.size', 'A_and_B.size', 'Coef', 'Coef(expected)', 'Coef(95% CI)']
        
        # Ensure the 'TF' column (or equivalent identifier) exists
        if 'TF' not in df.columns:
            print(f"Skipping {file_path} as it does not contain 'TF' column.")
            continue

        # Extract the mean from the Coef(95% CI) column if it exists
        if 'Coef(95% CI)' in df.columns:
            df['Coef(95% CI)_mean'] = df['Coef(95% CI)'].apply(extract_coef_range)

        # Add a column for the metric type based on the filename
        metric_name = file.split('_')[4]  # Extracts the metric name (e.g., 'overlap', 'jaccard')
        df['Metric'] = metric_name

        # Merge the current DataFrame with the previous one (or initialize the first merge)
        if merged_df is None:
            merged_df = df
        else:
            # Merge on the 'TF' column (or another identifier)
            merged_df = pd.merge(merged_df, df[['TF', 'Metric', 'Coef', 'Coef(95% CI)_mean']], on='TF', how='outer')

# Check if merging was successful
if merged_df is not None:
    # Save the merged DataFrame to a CSV file
    merged_df.to_csv(output_file, index=False)
    print(f"Files merged successfully into {output_file}")
else:
    print("No valid data to merge.")

