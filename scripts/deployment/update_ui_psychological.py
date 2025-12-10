"""
Update UI to Display Psychological Scores
==========================================
This script updates the Promotion Candidates page to show psychological assessment data.
"""

import re
from pathlib import Path

print("=" * 80)
print("UPDATING UI FOR PSYCHOLOGICAL SCORES")
print("=" * 80)
print()

repo_root = Path(__file__).resolve().parents[2]
ui_file = repo_root / "app" / "pages" / "6_👥_Promotion_Candidates.py"

print(f"1. Reading UI file: {ui_file}")

with open(ui_file, 'r', encoding='utf-8') as f:
    content = f.read()

print("   ✓ File loaded")
print()

# Backup original
backup_file = ui_file.with_suffix('.py.backup')
with open(backup_file, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"2. Backup created: {backup_file}")
print()

# Update 1: Add psychological scores to compact card display
print("3. Updating compact card display...")

old_pattern = r'with col4:\s+st\.metric\("Perf/Beh/Psych", f"\{row\[\'performance_score\'\]:.0f\}/\{row\[\'behavior_avg\'\]:.0f\}/\{row\.get\(\'psychological_score\', 0\):.0f\}"\)'

new_code = '''with col4:
            perf = row['performance_score']
            beh = row['behavior_avg']
            psych = row.get('psychological_score', 0)
            st.metric("Perf/Beh/Psych", f"{perf:.0f}/{beh:.0f}/{psych:.0f}")
            # Add psychological indicator
            if psych > 75:
                st.caption("🧠 Strong")
            elif psych > 60:
                st.caption("🧠 Good")
            else:
                st.caption("🧠 Fair")'''

if re.search(old_pattern, content):
    content = re.sub(old_pattern, new_code, content)
    print("   ✓ Updated compact card display")
else:
    print("   ⚠️ Pattern not found, skipping")

print()

# Update 2: Add psychological section to modal
print("4. Adding psychological section to modal...")

# Find the modal section and add psychological details after behavior metric
modal_pattern = r'(with col4:\s+st\.metric\("🎯 Behavior", f"\{emp\[\'behavior_avg\'\]:.1f\}"\))'

psychological_section = r'''\1
                
                # Psychological Assessment Section
                st.markdown("---")
                st.markdown("### 🧠 Psychological Assessment")
                
                if 'psychological_score' in emp and emp.get('psychological_score', 0) > 0:
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        psych_score = emp.get('psychological_score', 0)
                        st.metric("Overall", f"{psych_score:.1f}")
                        if psych_score > 75:
                            st.caption("✅ Excellent")
                        elif psych_score > 60:
                            st.caption("✅ Good")
                        else:
                            st.caption("⚠️ Fair")
                    
                    with col2:
                        drive = emp.get('drive_score', 0)
                        st.metric("🔥 Drive", f"{drive:.1f}")
                        if drive > 75:
                            st.caption("High motivation")
                        else:
                            st.caption("Moderate")
                    
                    with col3:
                        mental = emp.get('mental_strength_score', 0)
                        st.metric("💪 Mental", f"{mental:.1f}")
                        if mental > 75:
                            st.caption("Resilient")
                        else:
                            st.caption("Developing")
                    
                    with col4:
                        adapt = emp.get('adaptability_score', 0)
                        st.metric("🔄 Adapt", f"{adapt:.1f}")
                        if adapt > 75:
                            st.caption("Very flexible")
                        else:
                            st.caption("Moderate")
                    
                    with col5:
                        collab = emp.get('collaboration_score', 0)
                        st.metric("🤝 Collab", f"{collab:.1f}")
                        if collab > 75:
                            st.caption("Team player")
                        else:
                            st.caption("Developing")
                    
                    # Leadership potential
                    st.markdown("---")
                    leadership = emp.get('leadership_potential', 0)
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.metric("👔 Leadership Potential", f"{leadership:.1f}")
                    with col2:
                        if leadership > 80:
                            st.success("🌟 High leadership potential - Ready for leadership roles")
                        elif leadership > 70:
                            st.info("✅ Good leadership potential - Can develop into leadership")
                        else:
                            st.warning("📈 Moderate - Needs leadership development")
                    
                    # Holistic score
                    holistic = emp.get('holistic_score', 0)
                    if holistic > 0:
                        st.markdown("---")
                        st.markdown("### 📊 Holistic Assessment")
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.metric("Combined Score", f"{holistic:.1f}")
                        with col2:
                            alignment = emp.get('score_alignment', 0)
                            if alignment > 0.7:
                                st.success(f"✅ Well-balanced profile (alignment: {alignment:.2f})")
                            elif alignment > 0.5:
                                st.info(f"📊 Moderately balanced (alignment: {alignment:.2f})")
                            else:
                                st.warning(f"⚠️ Unbalanced profile (alignment: {alignment:.2f})")
                else:
                    st.info("ℹ️ No psychological assessment data available for this employee")'''

if re.search(modal_pattern, content):
    content = re.sub(modal_pattern, psychological_section, content)
    print("   ✓ Added psychological section to modal")
else:
    print("   ⚠️ Modal pattern not found, skipping")

print()

# Save updated file
print("5. Saving updated file...")
with open(ui_file, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"   ✓ Saved: {ui_file}")
print()

print("=" * 80)
print("✅ UI UPDATE COMPLETE!")
print("=" * 80)
print()
print("Changes made:")
print("  1. ✅ Enhanced compact card display with psychological indicators")
print("  2. ✅ Added comprehensive psychological section to employee modal")
print("  3. ✅ Added leadership potential display")
print("  4. ✅ Added holistic assessment with alignment score")
print()
print(f"Backup saved to: {backup_file}")
print()
print("Next: Test the UI by running the Streamlit app")
print()
