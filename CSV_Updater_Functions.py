import pandas as pd
import io
import os

def process_csv_data(input_file):
    """
    Reads a CSV file, processes the data, and saves the updated data to a new CSV file.

    Specifically, it takes comma and alt+enter separated values from 'Child ID' and
    expands them into new rows, duplicating the corresponding 'Parent ID'.

    The output file is named based on the input file, with '_updated' appended
    before the '.csv' extension.

    Args:
        input_file (str): The path to the input CSV file.
    """
    # Define a custom parser for the alt+enter character.
    # The alt+enter character in Excel is a newline character '\n'.
    # We will also split by commas.
    def custom_split(cell_value):
        # Use a try-except block to handle potential NaN values gracefully.
        try:
            # Check if the value is a string before trying to split.
            if isinstance(cell_value, str):
                # Replace newline characters with commas, then split by commas.
                # This handles both comma and alt+enter separated values.
                return cell_value.replace('\n', ',').split(',')
            else:
                return [cell_value] # Return a list with the original value if it's not a string
        except AttributeError:
            return [cell_value] # Return a list with the original value on error

    # Read the CSV file into a pandas DataFrame.
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return

    # Create a new DataFrame to store the expanded data.
    expanded_rows = []

    # Iterate through each row of the original DataFrame.
    for index, row in df.iterrows():
        # Get the 'Parent ID' and 'Child ID' from the current row.
        parent_id = row['Parent ID']
        child_id_values = row['Child ID']

        # Split the 'Child ID' cell content by commas and newlines.
        # Strip any leading/trailing whitespace from each value.
        child_ids = [val.strip() for val in custom_split(child_id_values)]

        # Create a new row for each 'Child ID' value.
        for child_id in child_ids:
            # Only add a row if the child_id is not empty
            if child_id:
                expanded_rows.append({'Parent ID': parent_id, 'Child ID': child_id})

    # Create a new DataFrame from the list of expanded rows.
    updated_df = pd.DataFrame(expanded_rows)
    
    # Construct the output filename
    # os.path.splitext separates the file path into a root and an extension
    file_root, file_ext = os.path.splitext(input_file)
    output_file = f"{file_root}_updated{file_ext}"

    # Save the new DataFrame to the generated CSV file.
    updated_df.to_csv(output_file, index=False)

    print(f"Successfully processed data and saved it to '{output_file}'.")