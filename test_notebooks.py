#!/usr/bin/env python3
"""
Test script to verify all notebooks can be parsed without syntax errors
"""

import json
import sys
from pathlib import Path

def test_notebook(notebook_path):
    """Test if notebook can be parsed"""
    print(f"\n{'='*80}")
    print(f"Testing: {notebook_path.name}")
    print('='*80)
    
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb_content = json.load(f)
        
        # Check structure
        if 'cells' not in nb_content:
            print(f"❌ ERROR: No 'cells' key found")
            return False
        
        cells = nb_content['cells']
        print(f"✅ Notebook structure valid")
        print(f"   - Total cells: {len(cells)}")
        
        # Count cell types
        cell_types = {}
        code_cells = 0
        markdown_cells = 0
        
        for i, cell in enumerate(cells):
            cell_type = cell.get('cell_type', 'unknown')
            cell_types[cell_type] = cell_types.get(cell_type, 0) + 1
            
            if cell_type == 'code':
                code_cells += 1
                # Check for basic syntax issues in code cells
                source = ''.join(cell.get('source', []))
                if source.strip():
                    # Check for common issues
                    if '<b-card>' in source or '</b-card>' in source:
                        print(f"⚠️  WARNING: Cell {i+1} contains Vue.js syntax (not Python)")
                        print(f"   First line: {source.split(chr(10))[0][:60]}...")
                    
            elif cell_type == 'markdown':
                markdown_cells += 1
        
        print(f"   - Code cells: {code_cells}")
        print(f"   - Markdown cells: {markdown_cells}")
        print(f"   - Other cells: {len(cells) - code_cells - markdown_cells}")
        
        # Check for required metadata
        if 'metadata' in nb_content:
            print(f"✅ Metadata present")
            if 'kernelspec' in nb_content['metadata']:
                kernel = nb_content['metadata']['kernelspec']
                print(f"   - Kernel: {kernel.get('display_name', 'Unknown')}")
        
        print(f"\n✅ {notebook_path.name} is VALID")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Invalid JSON format")
        print(f"   {str(e)}")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    """Test all notebooks in notebooks directory"""
    notebooks_dir = Path(__file__).parent / 'notebooks'
    
    if not notebooks_dir.exists():
        print(f"❌ ERROR: notebooks directory not found at {notebooks_dir}")
        sys.exit(1)
    
    notebook_files = list(notebooks_dir.glob('*.ipynb'))
    
    if not notebook_files:
        print(f"❌ ERROR: No notebook files found in {notebooks_dir}")
        sys.exit(1)
    
    print(f"\n{'='*80}")
    print(f"TESTING {len(notebook_files)} NOTEBOOKS")
    print('='*80)
    
    results = {}
    for nb_path in sorted(notebook_files):
        results[nb_path.name] = test_notebook(nb_path)
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print('='*80)
    
    passed = sum(1 for v in results.values() if v)
    failed = len(results) - passed
    
    for nb_name, success in sorted(results.items()):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {nb_name}")
    
    print(f"\nTotal: {len(results)} notebooks")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed > 0:
        print(f"\n❌ {failed} notebook(s) have issues")
        sys.exit(1)
    else:
        print(f"\n✅ All notebooks are valid!")
        sys.exit(0)

if __name__ == '__main__':
    main()
