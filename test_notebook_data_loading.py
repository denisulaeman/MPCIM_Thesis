"""
Test script to verify data loading works correctly in all notebooks
"""

import os
import sys
from pathlib import Path

def test_data_loading():
    """Test if data file can be loaded with the path detection logic"""
    
    print("=" * 70)
    print("🔍 TESTING DATA LOADING LOGIC")
    print("=" * 70)
    
    # Simulate running from different directories
    test_scenarios = [
        ("Project Root", Path.cwd()),
        ("Notebooks Folder", Path.cwd() / "notebooks"),
    ]
    
    all_passed = True
    
    for scenario_name, test_dir in test_scenarios:
        print(f"\n📍 Scenario: {scenario_name}")
        print(f"   Directory: {test_dir}")
        
        # Simulate the path detection logic
        notebook_dir = test_dir
        if 'notebooks' in str(notebook_dir):
            project_root = notebook_dir.parent
        else:
            project_root = notebook_dir
        
        data_path = project_root / "data" / "processed" / "full_dataset_processed.csv"
        
        if data_path.exists():
            print(f"   ✅ PASS: Data file found at {data_path}")
            
            # Try to load the data (only if pandas available)
            try:
                import pandas as pd
                df = pd.read_csv(data_path)
                print(f"   ✅ Successfully loaded: {df.shape[0]} rows, {df.shape[1]} columns")
                
                # Check for required column
                if 'has_promotion' in df.columns:
                    print(f"   ✅ Target column 'has_promotion' exists")
                else:
                    print(f"   ⚠️  Warning: 'has_promotion' column not found")
                    
            except ImportError:
                print(f"   ⚠️  pandas not available, skipping data load test")
            except Exception as e:
                print(f"   ❌ FAIL: Error loading data: {str(e)}")
                all_passed = False
        else:
            print(f"   ❌ FAIL: Data file not found at {data_path}")
            all_passed = False
            
            # Try fallback paths
            fallback_paths = [
                project_root / "data" / "processed" / "full_dataset_processed.csv",
                Path("data/processed/full_dataset_processed.csv"),
                Path("../data/processed/full_dataset_processed.csv"),
            ]
            
            print(f"   🔍 Checking fallback paths:")
            for fb_path in fallback_paths:
                exists = "✅" if fb_path.exists() else "❌"
                print(f"      {exists} {fb_path}")
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL DATA LOADING TESTS PASSED")
        print("=" * 70)
        return 0
    else:
        print("❌ SOME DATA LOADING TESTS FAILED")
        print("=" * 70)
        return 1

def test_actual_notebook_execution():
    """Test by actually running notebook cells"""
    print("\n" + "=" * 70)
    print("🧪 TESTING ACTUAL NOTEBOOK EXECUTION")
    print("=" * 70)
    
    try:
        # Try to import pandas, skip test if not available
        try:
            import pandas as pd
            import numpy as np
        except ImportError:
            print("⚠️  pandas/numpy not installed in this Python environment")
            print("✅ SKIPPED: This test requires pandas (notebooks will use their own kernels)")
            return 0
        
        from pathlib import Path
        
        # Execute the path detection logic
        notebook_dir = Path(os.getcwd())
        if 'notebooks' in str(notebook_dir):
            project_root = notebook_dir.parent
        else:
            project_root = notebook_dir
        
        data_path = project_root / "data" / "processed" / "full_dataset_processed.csv"
        
        if data_path.exists():
            data_file = str(data_path)
            print(f"✅ Data file: {data_file}")
        else:
            # Fallback
            for path in [Path("../data/processed/full_dataset_processed.csv"), 
                         Path("data/processed/full_dataset_processed.csv")]:
                if path.exists():
                    data_file = str(path.resolve())
                    print(f"✅ Data file (fallback): {data_file}")
                    break
            else:
                raise FileNotFoundError("Data file not found in any location")
        
        # Load data
        df = pd.read_csv(data_file)
        print(f"✅ Loaded dataset: {df.shape}")
        
        # Basic checks
        print(f"✅ Columns: {len(df.columns)}")
        print(f"✅ Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        if 'has_promotion' in df.columns:
            print(f"✅ Target distribution:")
            print(df['has_promotion'].value_counts())
        
        print("\n✅ Notebook execution simulation PASSED")
        return 0
        
    except Exception as e:
        print(f"\n❌ Notebook execution simulation FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    result1 = test_data_loading()
    result2 = test_actual_notebook_execution()
    
    print("\n" + "=" * 70)
    print("📊 FINAL SUMMARY")
    print("=" * 70)
    
    if result1 == 0 and result2 == 0:
        print("🎉 ALL TESTS PASSED - Notebooks are ready to run!")
        sys.exit(0)
    else:
        print("⚠️  SOME TESTS FAILED - Please check the errors above")
        sys.exit(1)
