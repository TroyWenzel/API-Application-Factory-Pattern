import yaml
import os

def merge_swagger_files():
    """Merge multiple swagger files into one"""
    
    swagger_dir = 'swagger'  # Adjust this path to where your swagger files are located
    
    # Base file
    base_file = os.path.join(swagger_dir, 'mechanic_shop_swagger.yaml')
    with open(base_file, 'r') as f:
        base = yaml.safe_load(f)
    
    # Files to merge
    files_to_merge = [
        'parts_and_inventory_swagger.yaml',
        'service_tickets_swagger.yaml'
    ]
    
    for file in files_to_merge:
        file_path = os.path.join(swagger_dir, file)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                additional = yaml.safe_load(f)
                
                # Merge paths
                if 'paths' in additional:
                    base['paths'].update(additional['paths'])
                
                # Merge definitions
                if 'definitions' in additional:
                    base['definitions'].update(additional['definitions'])
        else:
            print(f"Warning: {file_path} not found, skipping...")
    
    return base

# Generate merged swagger when this module is imported
try:
    merged_swagger = merge_swagger_files()
except Exception as e:
    print(f"Error merging swagger files: {e}")
    merged_swagger = None