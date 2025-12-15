#!/usr/bin/env python3
"""
Download SLR Reference Papers
=============================
Script to download academic papers used in the Systematic Literature Review.

Note: Some papers may require institutional access or purchase.
This script attempts to download from open-access sources where available.
"""

import os
import requests
import time
from urllib.parse import urlparse

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                          'docs', 'papers', 'slr_references')

# Headers to mimic browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

# Paper references with URLs
PAPERS = {
    # === CORE PROMOTION PREDICTION PAPERS ===
    '[10] Alqahtani_Almaleh_2022': {
        'title': 'Analysis and prediction of employee promotions using machine learning',
        'url': 'https://ieeexplore.ieee.org/document/9943959',
        'doi': '10.1109/ICCI54321.2022.9943959',
        'type': 'ieee',
        'notes': 'Requires IEEE Xplore access'
    },
    '[11] Jafor_2023': {
        'title': 'Employee promotion prediction using improved AdaBoost machine learning approach',
        'url': 'https://pdfs.semanticscholar.org/6902/02d285800b78307dee054258f946fd13902c.pdf',
        'doi': None,
        'type': 'pdf',
        'notes': 'Open access - Semantic Scholar'
    },
    '[12] Shafie_2023': {
        'title': 'Prediction of employee promotion using hybrid sampling method with machine learning architecture',
        'url': 'https://ir.uitm.edu.my/id/eprint/77298/',
        'doi': None,
        'type': 'repository',
        'notes': 'UiTM Institutional Repository'
    },
    '[13] Ilwani_Nassreddine_2023': {
        'title': 'Machine learning application on employee promotion',
        'url': 'https://journals.mesopotamian.press/index.php/cs/article/view/91',
        'doi': '10.58496/MJCSC/2023/012',
        'type': 'open_journal',
        'pdf_url': 'https://journals.mesopotamian.press/index.php/cs/article/download/91/69',
        'notes': 'Open access journal'
    },
    '[14] Wang_2024': {
        'title': 'Prediction and analysis of employee promotions using machine learning',
        'url': 'https://ieeexplore.ieee.org/document/10904438',
        'doi': None,
        'type': 'ieee',
        'notes': 'Requires IEEE Xplore access'
    },
    '[15] Bhattacharya_Choudhary_2023': {
        'title': 'Explainable AI for predictive analytics on employee promotion',
        'url': 'https://ieeexplore.ieee.org/document/10393141',
        'doi': '10.1109/ICIT58056.2023.10393141',
        'type': 'ieee',
        'notes': 'Requires IEEE Xplore access'
    },
    
    # === XAI IN HR PAPERS ===
    '[22] Marin_Diaz_2023': {
        'title': 'Analyzing employee attrition using explainable AI for strategic HR decision-making',
        'url': 'https://www.mdpi.com/2227-7390/11/22/4677',
        'doi': '10.3390/math11224677',
        'type': 'mdpi',
        'pdf_url': 'https://www.mdpi.com/2227-7390/11/22/4677/pdf',
        'notes': 'Open access - MDPI'
    },
    '[23] Das_2022': {
        'title': 'Explainable AI for predictive analytics on employee attrition',
        'url': 'https://link.springer.com/chapter/10.1007/978-3-031-27609-5_12',
        'doi': '10.1007/978-3-031-27609-5_12',
        'type': 'springer',
        'notes': 'Requires Springer access'
    },
    '[24] Abonamah_2022': {
        'title': 'Explainable artificial intelligence in human resources: A computational study',
        'url': 'https://ieeexplore.ieee.org/document/10041624',
        'doi': '10.1109/ICDABI56818.2022.10041624',
        'type': 'ieee',
        'notes': 'Requires IEEE Xplore access'
    },
    '[25] Al_Akasheh_2024': {
        'title': 'Enhancing the prediction of employee turnover with knowledge graphs and explainable AI',
        'url': 'https://ieeexplore.ieee.org/document/10538112',
        'doi': '10.1109/ACCESS.2024.3404568',
        'type': 'ieee_access',
        'pdf_url': 'https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10538112',
        'notes': 'IEEE Access - Open access'
    },
    '[26] Baum_2023': {
        'title': 'The explanation matters: Enhancing AI adoption in human resource management',
        'url': 'https://aisel.aisnet.org/pacis2023/17/',
        'doi': None,
        'type': 'ais',
        'notes': 'Open access - AIS Electronic Library'
    },
    
    # === KNOWLEDGE GRAPH PAPERS ===
    '[35] Qin_2025': {
        'title': 'A comprehensive survey of artificial intelligence techniques for talent analytics',
        'url': 'https://ieeexplore.ieee.org/document/11027075',
        'doi': '10.1109/JPROC.2024.3515782',
        'type': 'ieee',
        'notes': 'Requires IEEE Xplore access'
    },
    '[36] Yang_2023': {
        'title': 'Contextualized knowledge graph embedding for explainable talent training course recommendation',
        'url': 'https://dl.acm.org/doi/10.1145/3597022',
        'doi': '10.1145/3597022',
        'type': 'acm',
        'notes': 'Requires ACM Digital Library access'
    },
    '[37] Konstantinidis_2022': {
        'title': 'Knowledge-driven unsupervised skills extraction for graph-based talent matching',
        'url': 'https://dl.acm.org/doi/10.1145/3549737.3549769',
        'doi': '10.1145/3549737.3549769',
        'type': 'acm',
        'notes': 'Requires ACM Digital Library access'
    },
    '[38] Yang_Shen_2025': {
        'title': 'Knowledge graph construction and talent competency prediction for human resource management',
        'url': 'https://www.sciencedirect.com/science/article/pii/S1110016825002194',
        'doi': '10.1016/j.aej.2024.11.081',
        'type': 'elsevier',
        'notes': 'Requires ScienceDirect access'
    },
    '[47] Hogan_2021': {
        'title': 'Knowledge graphs',
        'url': 'https://dl.acm.org/doi/10.1145/3447772',
        'doi': '10.1145/3447772',
        'type': 'acm',
        'pdf_url': 'https://arxiv.org/pdf/2003.02320.pdf',
        'notes': 'ArXiv preprint available'
    },
    
    # === SHAP/LIME FOUNDATIONAL PAPERS ===
    '[39] Lundberg_Lee_2017': {
        'title': 'A unified approach to interpreting model predictions',
        'url': 'https://papers.nips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html',
        'doi': None,
        'type': 'neurips',
        'pdf_url': 'https://papers.nips.cc/paper_files/paper/2017/file/8a20a8621978632d76c43dfd28b67767-Paper.pdf',
        'notes': 'Open access - NeurIPS'
    },
    '[40] Ribeiro_2016': {
        'title': 'Why should I trust you?: Explaining the predictions of any classifier (LIME)',
        'url': 'https://dl.acm.org/doi/10.1145/2939672.2939778',
        'doi': '10.1145/2939672.2939778',
        'type': 'acm',
        'pdf_url': 'https://arxiv.org/pdf/1602.04938.pdf',
        'notes': 'ArXiv preprint available'
    },
    '[41] Vimbi_2024': {
        'title': 'Interpreting AI models: A systematic review on LIME and SHAP in Alzheimer detection',
        'url': 'https://link.springer.com/article/10.1186/s40708-024-00222-1',
        'doi': '10.1186/s40708-024-00222-1',
        'type': 'springer_open',
        'pdf_url': 'https://link.springer.com/content/pdf/10.1186/s40708-024-00222-1.pdf',
        'notes': 'Open access - Springer'
    },
    
    # === ML ALGORITHM PAPERS ===
    '[43] Chen_Guestrin_2016': {
        'title': 'XGBoost: A scalable tree boosting system',
        'url': 'https://dl.acm.org/doi/10.1145/2939672.2939785',
        'doi': '10.1145/2939672.2939785',
        'type': 'acm',
        'pdf_url': 'https://arxiv.org/pdf/1603.02754.pdf',
        'notes': 'ArXiv preprint available'
    },
    
    # === IMBALANCED DATA PAPERS ===
    '[29] Wongvorachan_2023': {
        'title': 'A comparison of undersampling, oversampling, and SMOTE methods',
        'url': 'https://www.mdpi.com/2078-2489/14/1/54',
        'doi': '10.3390/info14010054',
        'type': 'mdpi',
        'pdf_url': 'https://www.mdpi.com/2078-2489/14/1/54/pdf',
        'notes': 'Open access - MDPI'
    },
    '[30] Dablain_2022': {
        'title': 'DeepSMOTE: Fusing deep learning and SMOTE for imbalanced data',
        'url': 'https://ieeexplore.ieee.org/document/9694621',
        'doi': '10.1109/TNNLS.2021.3136503',
        'type': 'ieee',
        'notes': 'Requires IEEE Xplore access'
    },
    '[31] Pradipta_2021': {
        'title': 'SMOTE for handling imbalanced data problem: A review',
        'url': 'https://ieeexplore.ieee.org/document/9632912',
        'doi': '10.1109/ICIC54025.2021.9632912',
        'type': 'ieee',
        'notes': 'Requires IEEE Xplore access'
    },
    
    # === HR ANALYTICS SURVEY PAPERS ===
    '[4] Garg_2022': {
        'title': 'A review of machine learning applications in human resource management',
        'url': 'https://www.emerald.com/insight/content/doi/10.1108/IJPPM-08-2020-0427/full/html',
        'doi': '10.1108/IJPPM-08-2020-0427',
        'type': 'emerald',
        'notes': 'Requires Emerald access'
    },
    '[28] Fallucchi_2020': {
        'title': 'Predicting employee attrition using machine learning techniques',
        'url': 'https://www.mdpi.com/2073-431X/9/4/86',
        'doi': '10.3390/computers9040086',
        'type': 'mdpi',
        'pdf_url': 'https://www.mdpi.com/2073-431X/9/4/86/pdf',
        'notes': 'Open access - MDPI'
    },
}


def download_paper(paper_id, paper_info, output_dir):
    """Download a single paper if possible."""
    filename = f"{paper_id.replace(' ', '_').replace('[', '').replace(']', '')}.pdf"
    filepath = os.path.join(output_dir, filename)
    
    # Check if already downloaded
    if os.path.exists(filepath):
        print(f"  ⏭  Already exists: {filename}")
        return True
    
    # Try to download from pdf_url if available
    pdf_url = paper_info.get('pdf_url')
    if pdf_url:
        try:
            print(f"  📥 Downloading: {paper_info['title'][:60]}...")
            response = requests.get(pdf_url, headers=HEADERS, timeout=30, allow_redirects=True)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'pdf' in content_type or response.content[:4] == b'%PDF':
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"  ✅ Downloaded: {filename}")
                    return True
                else:
                    print(f"  ⚠️  Not a PDF file")
            else:
                print(f"  ❌ HTTP {response.status_code}")
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:50]}")
    else:
        print(f"  ℹ️  No direct PDF: {paper_info['notes']}")
    
    return False


def create_reference_index(papers, output_dir):
    """Create an index file of all references."""
    index_path = os.path.join(output_dir, 'REFERENCE_INDEX.md')
    
    with open(index_path, 'w') as f:
        f.write("# SLR Reference Papers Index\n\n")
        f.write("This document lists all papers referenced in the Systematic Literature Review.\n\n")
        f.write("---\n\n")
        
        # Group by category
        categories = {
            'Core Promotion Prediction': ['[10]', '[11]', '[12]', '[13]', '[14]', '[15]'],
            'XAI in HR': ['[22]', '[23]', '[24]', '[25]', '[26]'],
            'Knowledge Graphs': ['[35]', '[36]', '[37]', '[38]', '[47]'],
            'SHAP/LIME Foundations': ['[39]', '[40]', '[41]'],
            'ML Algorithms': ['[43]'],
            'Imbalanced Data': ['[29]', '[30]', '[31]'],
            'HR Analytics': ['[4]', '[28]'],
        }
        
        for category, refs in categories.items():
            f.write(f"## {category}\n\n")
            for paper_id, info in papers.items():
                ref_num = paper_id.split(']')[0] + ']'
                if ref_num in refs:
                    f.write(f"### {paper_id}\n")
                    f.write(f"- **Title**: {info['title']}\n")
                    f.write(f"- **URL**: {info['url']}\n")
                    if info.get('doi'):
                        f.write(f"- **DOI**: {info['doi']}\n")
                    f.write(f"- **Access**: {info['notes']}\n")
                    f.write("\n")
            f.write("---\n\n")
    
    print(f"\n📋 Reference index created: {index_path}")


def main():
    print("\n" + "="*70)
    print("SLR Reference Papers Downloader")
    print("="*70 + "\n")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    downloaded = 0
    skipped = 0
    failed = 0
    
    for paper_id, info in PAPERS.items():
        print(f"\n[{paper_id}]")
        if download_paper(paper_id, info, OUTPUT_DIR):
            downloaded += 1
        elif info.get('pdf_url'):
            failed += 1
        else:
            skipped += 1
        time.sleep(1)  # Be nice to servers
    
    # Create reference index
    create_reference_index(PAPERS, OUTPUT_DIR)
    
    print("\n" + "="*70)
    print("Summary")
    print("="*70)
    print(f"  ✅ Downloaded: {downloaded}")
    print(f"  ⏭️  Skipped (no direct PDF): {skipped}")
    print(f"  ❌ Failed: {failed}")
    print(f"\n📁 Output directory: {OUTPUT_DIR}")
    print("\n" + "="*70)
    print("\n⚠️  Note: Some papers require institutional access.")
    print("   Please download manually from:")
    print("   - IEEE Xplore (requires subscription)")
    print("   - Springer (requires subscription)")
    print("   - ACM Digital Library (requires subscription)")
    print("   - Emerald Insight (requires subscription)")


if __name__ == "__main__":
    main()
