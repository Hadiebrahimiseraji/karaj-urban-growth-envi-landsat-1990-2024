import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import yaml

def read_export_plan():
    with open('configs/export_plan.yaml', 'r') as f:
        return yaml.safe_load(f)

def publish_assets():
    export_plan = read_export_plan()
    
    source_base = 'outputs'
    dest_base = export_plan['output_organization']['base_directory']
    
    print(f"Publishing PNG assets from {source_base} to {dest_base}...")
    
    copied_files = []
    
    years = export_plan['outputs_per_year']['required_files']
    years_list = export_plan['years_to_export']
    
    for year in years_list:
        source_dir = os.path.join(source_base, str(year))
        dest_dir = os.path.join(dest_base, str(year))
        
        if not os.path.exists(source_dir):
            print(f"Warning: Source directory not found: {source_dir}")
            continue
        
        os.makedirs(dest_dir, exist_ok=True)
        
        for file_spec in years:
            filename = file_spec['filename']
            source_file = os.path.join(source_dir, filename)
            dest_file = os.path.join(dest_dir, filename)
            
            if os.path.exists(source_file):
                shutil.copy2(source_file, dest_file)
                file_size = os.path.getsize(dest_file) / (1024 * 1024)
                print(f"  Copied {year}/{filename} ({file_size:.1f} MB)")
                copied_files.append({
                    'year': year,
                    'filename': filename,
                    'source': source_file,
                    'destination': dest_file,
                    'size_mb': round(file_size, 2)
                })
    
    change_source = os.path.join(source_base, 'change_1990_2024')
    change_dest = os.path.join(dest_base, 'change_1990_2024')
    
    if os.path.exists(change_source):
        os.makedirs(change_dest, exist_ok=True)
        
        for change_file in export_plan['change_analysis_outputs']['1990_to_2024']:
            filename = change_file['filename']
            source_file = os.path.join(change_source, filename)
            dest_file = os.path.join(change_dest, filename)
            
            if os.path.exists(source_file):
                shutil.copy2(source_file, dest_file)
                file_size = os.path.getsize(dest_file) / (1024 * 1024)
                print(f"  Copied change_1990_2024/{filename} ({file_size:.1f} MB)")
                copied_files.append({
                    'period': '1990_to_2024',
                    'filename': filename,
                    'source': source_file,
                    'destination': dest_file,
                    'size_mb': round(file_size, 2)
                })
    
    publish_log = {
        'timestamp': datetime.utcnow().isoformat(),
        'source_directory': source_base,
        'destination_directory': dest_base,
        'files_copied': len(copied_files),
        'total_size_mb': round(sum(f['size_mb'] for f in copied_files), 2),
        'copied_files': copied_files
    }
    
    log_path = os.path.join(dest_base, 'publish_log.json')
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, 'w') as f:
        json.dump(publish_log, f, indent=2)
    
    print(f"\nPublishing complete.")
    print(f"Total files published: {len(copied_files)}")
    print(f"Total size: {publish_log['total_size_mb']:.1f} MB")
    print(f"Log written to {log_path}")
    
    return 0

if __name__ == '__main__':
    import sys
    exit_code = publish_assets()
    sys.exit(exit_code)
