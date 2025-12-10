"""
Script to validate notebook syntax and imports
Tests all notebooks in the notebooks/ folder for syntax errors
"""

import ast
import json
import sys
from pathlib import Path

def extract_python_code_from_notebook(notebook_path):
    """Extract Python code cells from a Jupyter notebook"""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse as JSON (standard ipynb format)
    try:
        notebook = json.loads(content)
        python_cells = []
        
        for cell in notebook.get('cells', []):
            if cell.get('cell_type') == 'code':
                # Get source code
                source = cell.get('source', [])
                if isinstance(source, list):
                    code = ''.join(source)
                else:
                    code = source
                
                # Skip magic commands and shell commands
                lines = []
                for line in code.split('\n'):
                    if line.strip().startswith('!') or line.strip().startswith('%'):
                        continue
                    # Skip Google Colab specific imports
                    if 'from google.colab import' in line:
                        continue
                    if 'files.upload()' in line:
                        continue
                    lines.append(line)
                
                cleaned_code = '\n'.join(lines)
                if cleaned_code.strip():
                    python_cells.append(cleaned_code)
        
        return python_cells
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing {notebook_path}: {e}")
        return []

def check_syntax(code, cell_num):
    """Check Python syntax for a code cell"""
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, f"Cell {cell_num}: Line {e.lineno}: {e.msg}"

def test_notebook(notebook_path):
    """Test a single notebook"""
    print(f"\n{'='*70}")
    print(f"📓 Testing: {notebook_path.name}")
    print('='*70)
    
    cells = extract_python_code_from_notebook(notebook_path)
    
    if not cells:
        print("⚠️  No Python code cells found or notebook format error")
        return False
    
    print(f"✅ Found {len(cells)} Python code cells")
    
    errors = []
    for i, cell_code in enumerate(cells, 1):
        is_valid, error = check_syntax(cell_code, i)
        if not is_valid:
            errors.append(error)
            print(f"❌ {error}")
    
    if not errors:
        print(f"✅ All {len(cells)} cells have valid Python syntax!")
        return True
    else:
        print(f"\n❌ Found {len(errors)} syntax error(s)")
        return False

def main():
    """Main testing function"""
    notebooks_dir = Path(__file__).parent / "notebooks"
    
    if not notebooks_dir.exists():
        print(f"❌ Notebooks directory not found: {notebooks_dir}")
        sys.exit(1)
    
    # Find all notebook files
    notebooks = list(notebooks_dir.glob("*.ipynb"))
    
    if not notebooks:
        print(f"❌ No notebooks found in {notebooks_dir}")
        sys.exit(1)
    
    print(f"🔍 Found {len(notebooks)} notebook(s) to test")
    
    results = {}
    for notebook in notebooks:
        results[notebook.name] = test_notebook(notebook)
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 SUMMARY")
    print('='*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n{'='*70}")
    print(f"Results: {passed}/{total} notebooks passed")
    print('='*70)
    
    if passed == total:
        print("🎉 All notebooks passed syntax validation!")
        sys.exit(0)
    else:
        print("⚠️  Some notebooks have syntax errors")
        sys.exit(1)

if __name__ == "__main__":
    main()
