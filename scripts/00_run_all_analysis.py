"""
Quick Start: Run All Job Level Analysis
========================================

Script ini menjalankan semua analisis secara berurutan:
1. Job Level Analysis
2. Promotion Prediction Model
3. Succession Planning

Author: Denis Ulaeman
Date: Dec 2025
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"

print("="*80)
print("JOB LEVEL ANALYSIS - COMPLETE PIPELINE")
print("="*80)
print(f"\nStart Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Working Directory: {BASE_DIR}")
print("\n" + "="*80)

# List of scripts to run
scripts = [
    ("01_job_level_analysis.py", "Job Level Analysis & Feature Engineering"),
    ("04_integrated_feature_engineering.py", "Integrated Feature Engineering (ALL Features)"),
    ("05_advanced_promotion_prediction.py", "Advanced Promotion Prediction Model"),
    ("03_succession_planning.py", "Succession Planning & Talent Pool Analysis")
]

results = []

for script_file, description in scripts:
    print(f"\n{'='*80}")
    print(f"RUNNING: {description}")
    print(f"Script: {script_file}")
    print(f"{'='*80}\n")
    
    script_path = SCRIPTS_DIR / script_file
    
    if not script_path.exists():
        print(f"❌ ERROR: Script not found: {script_path}")
        results.append((script_file, "FAILED", "Script not found"))
        continue
    
    try:
        # Run the script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        # Print output
        print(result.stdout)
        
        if result.returncode == 0:
            print(f"\n✅ SUCCESS: {description} completed")
            results.append((script_file, "SUCCESS", "Completed successfully"))
        else:
            print(f"\n❌ ERROR: {description} failed")
            print(f"Error output:\n{result.stderr}")
            results.append((script_file, "FAILED", result.stderr[:200]))
            
    except subprocess.TimeoutExpired:
        print(f"\n⏱️ TIMEOUT: {description} exceeded 5 minutes")
        results.append((script_file, "TIMEOUT", "Exceeded 5 minutes"))
        
    except Exception as e:
        print(f"\n❌ EXCEPTION: {description} raised an error")
        print(f"Error: {str(e)}")
        results.append((script_file, "EXCEPTION", str(e)[:200]))

# Summary
print("\n" + "="*80)
print("PIPELINE EXECUTION SUMMARY")
print("="*80)
print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\nResults:")
print("-"*80)

success_count = 0
for script, status, message in results:
    status_icon = "✅" if status == "SUCCESS" else "❌"
    print(f"{status_icon} {script:<40} {status}")
    if status != "SUCCESS":
        print(f"   Message: {message}")
    else:
        success_count += 1

print("-"*80)
print(f"\nTotal: {len(results)} scripts")
print(f"Success: {success_count}")
print(f"Failed: {len(results) - success_count}")

if success_count == len(results):
    print("\n🎉 All analyses completed successfully!")
    print("\nNext steps:")
    print("1. Check results/ folder for outputs")
    print("2. Review visualizations and reports")
    print("3. Validate findings with domain experts")
    print("4. Use insights for thesis writing")
else:
    print("\n⚠️  Some analyses failed. Please check error messages above.")

print("\n" + "="*80)
print("Pipeline execution complete!")
print("="*80)
