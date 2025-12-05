import yaml
import os

def merge_swagger_files():
    # Merge multiple swagger files into one comprehensive API documentation
    
    swagger_dir = 'swagger'  # Directory containing swagger files
    
    # Base file - this will be the foundation
    base_file = os.path.join(swagger_dir, 'mechanic_shop_swagger.yaml')
    
    if not os.path.exists(base_file):
        print(f"Error: Base file {base_file} not found!")
        return None
    
    with open(base_file, 'r') as f:
        base = yaml.safe_load(f)
    
    # Initialize base structure if needed
    if 'paths' not in base:
        base['paths'] = {}
    if 'definitions' not in base:
        base['definitions'] = {}
    
    # Files to merge (in order of priority)
    files_to_merge = [
        'customer_swagger.yaml',
        'mechanic_swagger.yaml',
        'parts_and_inventory_swagger.yaml',
        'service_tickets_swagger.yaml'
    ]
    
    print("Starting swagger merge process...")
    
    for file in files_to_merge:
        file_path = os.path.join(swagger_dir, file)
        
        if os.path.exists(file_path):
            print(f"  - Merging {file}...")
            try:
                with open(file_path, 'r') as f:
                    additional = yaml.safe_load(f)
                
                # Merge paths
                if 'paths' in additional:
                    for path, methods in additional['paths'].items():
                        if path in base['paths']:
                            # Merge methods for existing path
                            base['paths'][path].update(methods)
                        else:
                            # Add new path
                            base['paths'][path] = methods
                
                # Merge definitions (schemas)
                if 'definitions' in additional:
                    base['definitions'].update(additional['definitions'])
                
                # Merge tags if they exist
                if 'tags' in additional:
                    if 'tags' not in base:
                        base['tags'] = []
                    for tag in additional['tags']:
                        if tag not in base['tags']:
                            base['tags'].append(tag)
                
            except Exception as e:
                print(f"    ERROR merging {file}: {e}")
        else:
            print(f"  - Warning: {file} not found, skipping...")
    
    # Write the merged file to static directory for Flask
    output_file = 'static/mechanic_shop_swagger.yaml'
    os.makedirs('static', exist_ok=True)
    
    with open(output_file, 'w') as f:
        yaml.dump(base, f, default_flow_style=False, sort_keys=False)
    
    print(f"\n✓ Swagger files merged successfully!")
    print(f"  Output: {output_file}")
    print(f"  Total paths: {len(base['paths'])}")
    print(f"  Total definitions: {len(base['definitions'])}")
    
    return base

if __name__ == '__main__':
    merged_swagger = merge_swagger_files()
    
    if merged_swagger:
        print("\nMerge complete! You can now access the API docs at /api/docs")
    else:
        print("\nMerge failed! Please check the error messages above.")