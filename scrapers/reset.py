import os
import glob


def delete_csv_files(folder_path):
    # Get a list of all CSV files in the specified folder
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

    # Delete each file
    for file in csv_files:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")


# Specify the folder path
folder_path = "./"

# Call the function to delete CSV files
delete_csv_files(folder_path)
