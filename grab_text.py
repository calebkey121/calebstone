import os
import shutil

# Delete the text_files directory if it exists
if os.path.exists('text_files'):
    shutil.rmtree('text_files')

# Create new text_files directory
os.makedirs('text_files')

# Walk through current directory
for root, dirs, files in os.walk('./claude'):
    # Filter for .py files
    python_files = [f for f in files if f.endswith('.py')]
    
    # Process each .py file
    for file_name in python_files:
        full_path = os.path.join(root, file_name)
        
        try:
            # Read the content of the file
            with open(full_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Create output filename (replace .py with _py.txt)
            output_name = file_name.replace('.py', '_py.txt')
            output_path = os.path.join('text_files', output_name)
            
            # Write to new text file
            with open(output_path, 'w', encoding='utf-8') as output:
                output.write(f"{file_name}\n")
                output.write(f"{content}\n")
                
        except Exception as e:
            print(f"Error processing {file_name}: {str(e)}")