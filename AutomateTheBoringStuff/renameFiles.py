import os
import sys

# Specify the directory where your files are located
# Get user input
directory = input("Please enter something: ")
# Print the user's input
print(f"You entered: {directory}")

# Loop through all files in the directory
for filename in os.listdir(directory):
    # Check if the filename contains "-jpg."
    if "-jpg." in filename:
        # Split the filename at "-jpg." to keep only the part before it
        parts = filename.split("-jpg.")
        if len(parts) > 1:
            # Construct the new filename by joining the parts and adding ".jpg"
            new_filename = f"{parts[0]}.jpg"

            # Create the full file paths for the old and new filenames
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)

            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} to {new_filename}")
# Exit the program (optional)
sys.exit()
