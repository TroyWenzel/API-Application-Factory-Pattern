import yaml
import os
import sys

def merge_swagger_files():
    """Merge multiple swagger files into one comprehensive API documentation"""
    
    # Try to find the static directory in multiple locations
    possible_static_dirs = [
        'static',           # Root level
        'app/static',       # Inside app folder
        './static',         # Explicit current directory
        './app/static'      # Explicit app folder
    ]
    
    swagger_dir = None
    for dir_path in possible_static_dirs:
        if os.path.exists(dir_path):
            swagger_dir = dir_path
            break
    
    if not swagger_dir:
        print(f"Error: Static directory not found in any of these locations:")
        for dir_path in possible_static_dirs:
            print(f"  - {dir_path}")
        print(f"\nCurrent directory: {os.getcwd()}")
        print(f"Files in current directory: {os.listdir('.')}")
        return None
    
    print(f"✓ Found swagger directory: {swagger_dir}")
    
    # Base file - this will be the foundation
    base_file = os.path.join(swagger_dir, 'mechanic_shop_swagger.yaml')
    
    if not os.path.exists(base_file):
        print(f"Error: Base file not found: {base_file}")
        print(f"Files in {swagger_dir}:")
        try:
            for f in os.listdir(swagger_dir):
                print(f"  - {f}")
        except Exception as e:
            print(f"  Could not list files: {e}")
        return None
    
    print(f"✓ Loading base file: {base_file}")
    
    try:
        with open(base_file, 'r', encoding='utf-8') as f:
            base = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading base file: {e}")
        return None
    
    # Initialize base structure if needed
    if 'paths' not in base:
        base['paths'] = {}
    if 'definitions' not in base:
        base['definitions'] = {}
    
    # Files to merge
    files_to_merge = [
        'parts_and_inventory_swagger.yaml',
        'service_tickets_swagger.yaml'
    ]
    
    print(f"\n📊 Starting with {len(base.get('paths', {}))} paths and {len(base.get('definitions', {}))} definitions")
    
    merged_count = 0
    for file in files_to_merge:
        file_path = os.path.join(swagger_dir, file)
        
        if os.path.exists(file_path):
            print(f"\n📄 Merging {file}...")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    additional = yaml.safe_load(f)
                
                paths_before = len(base['paths'])
                defs_before = len(base['definitions'])
                
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
                    for def_name, def_schema in additional['definitions'].items():
                        if def_name not in base['definitions']:
                            base['definitions'][def_name] = def_schema
                
                paths_after = len(base['paths'])
                defs_after = len(base['definitions'])
                
                print(f"   ✓ Added {paths_after - paths_before} paths, {defs_after - defs_before} definitions")
                merged_count += 1
                
            except Exception as e:
                print(f"   ✗ ERROR merging {file}: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"⚠️  Warning: {file} not found at {file_path}")
    
    # Write the merged file back to static directory
    output_file = os.path.join(swagger_dir, 'mechanic_shop_swagger.yaml')
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(base, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        print(f"\n✅ SUCCESS!")
        print(f"   Output: {output_file}")
        print(f"   Total paths: {len(base['paths'])}")
        print(f"   Total definitions: {len(base['definitions'])}")
        print(f"   Files merged: {merged_count}/{len(files_to_merge)}")
        
    except Exception as e:
        print(f"\n❌ ERROR writing merged file: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    return base

# Auto-run when imported
try:
    merged_swagger = merge_swagger_files()
    if not merged_swagger:
        print("\n⚠️  WARNING: Swagger merge failed! API documentation may be incomplete.")
except Exception as e:
    print(f"\n❌ CRITICAL ERROR during swagger merge: {e}")
    import traceback
    traceback.print_exc()
    merged_swagger = None

if __name__ == '__main__':
    # Run the merge when executed directly
    if merged_swagger:
        print("\n🎉 Merge complete! You can now access the API docs at /api/docs")
    else:
        print("\n❌ Merge failed! Please check the error messages above.")
        sys.exit(1)