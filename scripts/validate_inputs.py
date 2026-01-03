import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime

def read_yaml_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def validate_file_exists(file_path):
    return os.path.isfile(file_path)

def get_file_size_mb(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)

def try_read_raster_metadata(file_path):
    try:
        import rasterio
        with rasterio.open(file_path) as src:
            return {
                'width': src.width,
                'height': src.height,
                'count': src.count,
                'dtype': str(src.dtypes[0]),
                'crs': str(src.crs)
            }
    except ImportError:
        return None
    except Exception:
        return None

def validate_inputs():
    config = read_yaml_config('configs/pipeline_config.yaml')
    
    validation_report = {
        'timestamp': datetime.utcnow().isoformat(),
        'status': 'passed',
        'checks': []
    }
    
    raw_data_dir = config['data_input']['raw_data_directory']
    input_files = config['data_input']['input_files']
    
    print("Validating input data structure...")
    
    missing_files = []
    valid_files = []
    
    for year, year_config in input_files.items():
        print(f"\nChecking {year} ({year_config['sensor']}) imagery:")
        
        bands = year_config['bands']
        file_pattern = year_config['file_pattern']
        
        for band in bands:
            filename = file_pattern.replace('{band}', str(band))
            filepath = os.path.join(raw_data_dir, filename)
            
            if validate_file_exists(filepath):
                file_size = get_file_size_mb(filepath)
                print(f"  Band {band}: Found ({file_size:.1f} MB)")
                
                metadata = try_read_raster_metadata(filepath)
                if metadata:
                    print(f"    Metadata: {metadata['width']}x{metadata['height']}, {metadata['count']} bands, {metadata['dtype']}, {metadata['crs']}")
                
                valid_files.append({
                    'year': year,
                    'band': band,
                    'filename': filename,
                    'size_mb': file_size,
                    'metadata': metadata
                })
            else:
                print(f"  Band {band}: NOT FOUND")
                missing_files.append({
                    'year': year,
                    'band': band,
                    'filename': filename,
                    'path': filepath
                })
    
    if missing_files:
        validation_report['status'] = 'failed'
        validation_report['missing_files'] = missing_files
        print(f"\nValidation FAILED: {len(missing_files)} file(s) missing")
    else:
        print(f"\nValidation PASSED: All {len(valid_files)} required files present")
    
    validation_report['valid_files_count'] = len(valid_files)
    validation_report['missing_files_count'] = len(missing_files)
    
    report_output = 'outputs/validation_report.txt'
    os.makedirs(os.path.dirname(report_output), exist_ok=True)
    
    with open(report_output, 'w') as f:
        f.write("Input Validation Report\n")
        f.write("======================\n\n")
        f.write(f"Timestamp: {validation_report['timestamp']}\n")
        f.write(f"Status: {validation_report['status'].upper()}\n\n")
        f.write(f"Valid Files: {validation_report['valid_files_count']}\n")
        f.write(f"Missing Files: {validation_report['missing_files_count']}\n\n")
        
        if missing_files:
            f.write("Missing Files:\n")
            for item in missing_files:
                f.write(f"  {item['year']} Band {item['band']}: {item['path']}\n")
    
    print(f"\nValidation report written to {report_output}")
    
    if missing_files:
        return 2
    else:
        return 0

if __name__ == '__main__':
    exit_code = validate_inputs()
    sys.exit(exit_code)
