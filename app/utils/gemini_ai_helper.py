"""
Gemini AI Helper for HR Decision Support
Integrates Google Gemini AI for natural language generation and analysis
"""

import os
import google.generativeai as genai
from typing import Dict, List, Optional
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiAIHelper:
    """Helper class for Gemini AI integration"""
    
    def __init__(self):
        """Initialize Gemini AI"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Use Gemini 2.5 Flash - latest and fastest model
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.available = True
        else:
            self.model = None
            self.available = False
    
    def is_available(self) -> bool:
        """Check if Gemini AI is available"""
        return self.available
    
    def generate_employee_analysis(self, employee_data: Dict, ml_confidence: float = None) -> str:
        """
        Generate comprehensive employee analysis using Gemini AI
        
        Args:
            employee_data: Dictionary containing employee information
            ml_confidence: ML model confidence score (0-1)
        
        Returns:
            AI-generated analysis text in Indonesian
        """
        if not self.available:
            return "Gemini AI tidak tersedia. Silakan konfigurasi GEMINI_API_KEY."
        
        # Format confidence level
        confidence_text = ""
        if ml_confidence:
            if ml_confidence >= 0.9:
                confidence_text = f"Model Machine Learning memiliki tingkat kepercayaan SANGAT TINGGI ({ml_confidence:.1%}) terhadap prediksi ini."
            elif ml_confidence >= 0.75:
                confidence_text = f"Model Machine Learning memiliki tingkat kepercayaan TINGGI ({ml_confidence:.1%}) terhadap prediksi ini."
            elif ml_confidence >= 0.6:
                confidence_text = f"Model Machine Learning memiliki tingkat kepercayaan SEDANG ({ml_confidence:.1%}) terhadap prediksi ini."
            else:
                confidence_text = f"Model Machine Learning memiliki tingkat kepercayaan RENDAH ({ml_confidence:.1%}) terhadap prediksi ini."
        
        prompt = f"""
        Anda adalah seorang ahli HR Analytics yang berpengalaman. Analisis profil karyawan ini dan berikan penilaian komprehensif dalam BAHASA INDONESIA.
        
        PENTING: Gunakan data Machine Learning berikut sebagai DASAR UTAMA analisis Anda. Jangan membuat asumsi di luar data yang diberikan.
        
        HASIL PREDIKSI MACHINE LEARNING:
        - Probabilitas Promosi: {employee_data.get('promotion_probability', 0):.1%}
        {confidence_text}
        
        PROFIL KARYAWAN:
        - Nama: {employee_data.get('name', 'Unknown')}
        - Masa Kerja: {employee_data.get('tenure_years', 0):.1f} tahun
        
        SKOR KINERJA (Skala 0-100):
        - Skor Performa: {employee_data.get('performance_score', 0):.1f}/100
        - Skor Perilaku: {employee_data.get('behavior_avg', 0):.1f}/100
        - Skor Psikologis: {employee_data.get('psychological_score', 0):.1f}/100
        - Potensi Kepemimpinan: {employee_data.get('leadership_potential', 0):.1f}/100
        
        DETAIL PSIKOLOGIS:
        - Drive & Motivasi: {employee_data.get('drive_score', 0):.1f}/100
        - Adaptabilitas: {employee_data.get('adaptability_score', 0):.1f}/100
        - Kekuatan Mental: {employee_data.get('mental_strength_score', 0):.1f}/100
        - Kolaborasi: {employee_data.get('collaboration_score', 0):.1f}/100
        
        Berikan analisis dalam format berikut (DALAM BAHASA INDONESIA):
        
        ## 📊 Penilaian Keseluruhan
        [2-3 paragraf yang menjelaskan hasil prediksi ML dan profil karyawan secara keseluruhan. Jelaskan MENGAPA model ML memberikan probabilitas tersebut berdasarkan skor-skor yang ada.]
        
        ## 💪 Kekuatan Utama
        [Identifikasi 3-4 kekuatan berdasarkan SKOR TERTINGGI dari data. Sebutkan angka spesifik.]
        - [Kekuatan 1 dengan skor]
        - [Kekuatan 2 dengan skor]
        - [Kekuatan 3 dengan skor]
        - [Kekuatan 4 dengan skor]
        
        ## 📈 Area Pengembangan
        [Identifikasi 2-3 area yang perlu ditingkatkan berdasarkan SKOR TERENDAH dari data. Sebutkan angka spesifik.]
        - [Area 1 dengan skor dan target]
        - [Area 2 dengan skor dan target]
        - [Area 3 dengan skor dan target]
        
        ## 🎯 Kesiapan Promosi
        [Berikan penilaian kesiapan promosi berdasarkan PROBABILITAS ML dan skor keseluruhan. Jelaskan apakah karyawan ini siap, hampir siap, atau perlu pengembangan lebih lanjut.]
        
        ## 🚀 Rekomendasi Aksi
        [Berikan 4-5 rekomendasi SPESIFIK dan TERUKUR yang akan meningkatkan probabilitas promosi. Setiap rekomendasi harus mencakup: aksi konkret, timeline, dan estimasi dampak terhadap probabilitas promosi.]
        
        PENTING:
        - Gunakan bahasa Indonesia yang profesional dan mudah dipahami
        - Semua analisis HARUS berdasarkan data ML yang diberikan
        - Sebutkan angka-angka spesifik dari data
        - Berikan rekomendasi yang actionable dan terukur
        - Jangan membuat asumsi di luar data yang tersedia
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating analysis: {str(e)}"
    
    def generate_personalized_recommendations(self, employee_data: Dict, 
                                             feature_contributions: List[Dict],
                                             ml_confidence: float = None) -> str:
        """
        Generate personalized development recommendations using Gemini AI
        
        Args:
            employee_data: Employee information
            feature_contributions: Top contributing features from ML
            ml_confidence: ML model confidence
        
        Returns:
            AI-generated recommendations in Indonesian
        """
        if not self.available:
            return "Gemini AI tidak tersedia."
        
        # Format feature contributions with Indonesian names
        feature_name_map = {
            'tenure_years': 'Masa Kerja',
            'performance_score': 'Skor Performa',
            'behavior_avg': 'Skor Perilaku',
            'psychological_score': 'Skor Psikologis',
            'leadership_potential': 'Potensi Kepemimpinan',
            'drive_score': 'Drive & Motivasi',
            'adaptability_score': 'Adaptabilitas',
            'mental_strength_score': 'Kekuatan Mental',
            'collaboration_score': 'Kolaborasi'
        }
        
        features_text = "\n".join([
            f"- {feature_name_map.get(feat['feature'], feat['feature'])}: {feat['contribution']:.1%} kontribusi terhadap prediksi"
            for feat in feature_contributions[:5]
        ])
        
        prompt = f"""
        Anda adalah seorang HR Development Coach yang berpengalaman. Buat rencana pengembangan personal yang SPESIFIK dan TERUKUR dalam BAHASA INDONESIA.
        
        HASIL MACHINE LEARNING:
        - Karyawan: {employee_data.get('name', 'Unknown')}
        - Probabilitas Promosi Saat Ini: {employee_data.get('promotion_probability', 0):.1%}
        
        FAKTOR-FAKTOR YANG PALING BERPENGARUH (dari Model ML):
        {features_text}
        
        SKOR SAAT INI:
        - Performa: {employee_data.get('performance_score', 0):.1f}/100
        - Perilaku: {employee_data.get('behavior_avg', 0):.1f}/100
        - Psikologis: {employee_data.get('psychological_score', 0):.1f}/100
        - Kepemimpinan: {employee_data.get('leadership_potential', 0):.1f}/100
        
        Buat rencana pengembangan dalam format berikut (BAHASA INDONESIA):
        
        ## 🎯 Target Pengembangan
        [Tetapkan target peningkatan probabilitas promosi yang realistis berdasarkan data ML. Contoh: "Meningkatkan probabilitas promosi dari X% menjadi Y% dalam 6 bulan"]
        
        ## ⚡ Aksi Segera (1-3 Bulan)
        [Berikan 3-4 aksi konkret yang fokus pada faktor dengan kontribusi TERTINGGI dari ML. Setiap aksi harus mencakup:]        - Aksi spesifik
        - Timeline jelas
        - Estimasi dampak terhadap skor dan probabilitas promosi
        - Cara mengukur keberhasilan
        
        ## 📅 Tujuan Jangka Pendek (3-6 Bulan)
        [Berikan 2-3 tujuan yang akan meningkatkan skor pada area yang masih lemah. Setiap tujuan harus terukur dan realistis.]
        
        ## 🚀 Pengembangan Jangka Panjang (6-12 Bulan)
        [Berikan 2-3 program pengembangan strategis yang akan meningkatkan probabilitas promosi secara signifikan.]
        
        ## 📚 Rekomendasi Pelatihan & Mentoring
        [Berikan rekomendasi pelatihan atau mentoring SPESIFIK yang sesuai dengan gap yang teridentifikasi dari data ML.]
        
        PENTING:
        - Semua rekomendasi HARUS berdasarkan faktor-faktor ML yang diberikan
        - Fokus pada faktor dengan kontribusi tertinggi untuk hasil maksimal
        - Berikan angka target yang spesifik dan terukur
        - Estimasi dampak harus realistis berdasarkan data
        - Gunakan bahasa Indonesia yang profesional
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating recommendations: {str(e)}"
    
    def explain_prediction(self, employee_data: Dict, 
                          feature_contributions: List[Dict]) -> str:
        """
        Generate natural language explanation of prediction using Gemini AI
        
        Args:
            employee_data: Employee information
            feature_contributions: Feature contributions
        
        Returns:
            AI-generated explanation
        """
        if not self.available:
            return "Gemini AI not available."
        
        prob = employee_data.get('promotion_probability', 0)
        
        # Format top 3 features
        top_features = "\n".join([
            f"- {feat['feature']}: {feat['contribution']:.1%}"
            for feat in feature_contributions[:3]
        ])
        
        # Format top features with Indonesian names
        feature_name_map = {
            'tenure_years': 'Masa Kerja',
            'performance_score': 'Skor Performa',
            'behavior_avg': 'Skor Perilaku',
            'psychological_score': 'Skor Psikologis',
            'leadership_potential': 'Potensi Kepemimpinan',
            'drive_score': 'Drive & Motivasi',
            'adaptability_score': 'Adaptabilitas',
            'mental_strength_score': 'Kekuatan Mental',
            'collaboration_score': 'Kolaborasi'
        }
        
        top_features = "\n".join([
            f"- {feature_name_map.get(feat['feature'], feat['feature'])}: {feat['contribution']:.1%} kontribusi"
            for feat in feature_contributions[:5]
        ])
        
        prompt = f"""
        Anda adalah seorang ahli HR Analytics. Jelaskan prediksi promosi ini dengan bahasa yang JELAS dan MUDAH DIPAHAMI dalam BAHASA INDONESIA.
        
        HASIL PREDIKSI MACHINE LEARNING:
        - Karyawan: {employee_data.get('name', 'Unknown')}
        - Probabilitas Promosi: {prob:.1%}
        
        FAKTOR-FAKTOR UTAMA YANG MEMPENGARUHI PREDIKSI (dari Model ML):
        {top_features}
        
        DATA KARYAWAN:
        - Performa: {employee_data.get('performance_score', 0):.1f}/100
        - Perilaku: {employee_data.get('behavior_avg', 0):.1f}/100
        - Psikologis: {employee_data.get('psychological_score', 0):.1f}/100
        - Kepemimpinan: {employee_data.get('leadership_potential', 0):.1f}/100
        - Masa Kerja: {employee_data.get('tenure_years', 0):.1f} tahun
        
        Berikan penjelasan dalam format berikut (BAHASA INDONESIA):
        
        ## 🎯 Hasil Prediksi
        [Jelaskan probabilitas promosi dan tingkat kepercayaan model ML terhadap prediksi ini. Gunakan bahasa yang mudah dipahami.]
        
        ## 🔍 Mengapa Prediksi Ini Diberikan?
        [Jelaskan secara detail MENGAPA model ML memberikan probabilitas ini. Fokus pada 3-5 faktor dengan kontribusi tertinggi. Jelaskan bagaimana setiap faktor mempengaruhi prediksi. Sebutkan angka-angka spesifik dari data.]
        
        ## 📊 Apa Arti Prediksi Ini?
        [Jelaskan konteks dan makna dari probabilitas ini untuk karyawan. Apakah ini probabilitas tinggi, sedang, atau rendah? Bagaimana posisi karyawan dibandingkan kandidat lain?]
        
        ## 💡 Langkah Selanjutnya
        [Berikan 3-4 langkah konkret yang dapat dilakukan karyawan untuk meningkatkan probabilitas promosi, berdasarkan faktor-faktor ML yang teridentifikasi.]
        
        PENTING:
        - Gunakan bahasa Indonesia yang profesional namun mudah dipahami
        - Semua penjelasan HARUS berdasarkan data dan faktor ML yang diberikan
        - Sebutkan angka-angka spesifik untuk mendukung penjelasan
        - Fokus pada faktor dengan kontribusi tertinggi
        - Berikan penjelasan yang objektif dan data-driven
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating explanation: {str(e)}"
    
    def compare_candidates(self, candidate1: Dict, candidate2: Dict) -> str:
        """
        Generate AI comparison between two candidates
        
        Args:
            candidate1: First candidate data
            candidate2: Second candidate data
        
        Returns:
            AI-generated comparison
        """
        if not self.available:
            return "Gemini AI not available."
        
        prompt = f"""
        You are an HR decision support analyst. Compare these two promotion candidates.
        
        Candidate 1: {candidate1.get('name', 'Unknown')}
        - Promotion Probability: {candidate1.get('promotion_probability', 0):.1%}
        - Performance: {candidate1.get('performance_score', 0):.1f}
        - Behavior: {candidate1.get('behavior_avg', 0):.1f}
        - Psychological: {candidate1.get('psychological_score', 0):.1f}
        - Leadership: {candidate1.get('leadership_potential', 0):.1f}
        - Tenure: {candidate1.get('tenure_years', 0):.1f} years
        
        Candidate 2: {candidate2.get('name', 'Unknown')}
        - Promotion Probability: {candidate2.get('promotion_probability', 0):.1%}
        - Performance: {candidate2.get('performance_score', 0):.1f}
        - Behavior: {candidate2.get('behavior_avg', 0):.1f}
        - Psychological: {candidate2.get('psychological_score', 0):.1f}
        - Leadership: {candidate2.get('leadership_potential', 0):.1f}
        - Tenure: {candidate2.get('tenure_years', 0):.1f} years
        
        Provide:
        1. Side-by-side comparison of strengths
        2. Key differentiators
        3. Which candidate is better suited for promotion and why
        4. Considerations for the decision
        
        Be objective, balanced, and data-driven.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating comparison: {str(e)}"
    
    def generate_what_if_insight(self, employee_data: Dict, 
                                 feature: str, current_value: float, 
                                 new_value: float, impact: float) -> str:
        """
        Generate insight for what-if scenario using Gemini AI
        
        Args:
            employee_data: Employee data
            feature: Feature being changed
            current_value: Current value
            new_value: New value
            impact: Predicted impact on probability
        
        Returns:
            AI-generated insight
        """
        if not self.available:
            return "Gemini AI not available."
        
        prompt = f"""
        You are an HR development advisor. Provide insight on this development scenario.
        
        Employee: {employee_data.get('name', 'Unknown')}
        Current Promotion Probability: {employee_data.get('promotion_probability', 0):.1%}
        
        Scenario: Improve {feature} from {current_value:.1f} to {new_value:.1f}
        Predicted Impact: {impact:+.1%} change in promotion probability
        
        Provide:
        1. What this improvement means in practical terms
        2. How to achieve this improvement (2-3 specific actions)
        3. Realistic timeline for this improvement
        4. Additional benefits beyond promotion probability
        
        Be practical and encouraging. Keep it concise (2-3 paragraphs).
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating insight: {str(e)}"
    
    def generate_team_insights(self, team_data: List[Dict]) -> str:
        """
        Generate insights about a team or group of candidates
        
        Args:
            team_data: List of employee data dictionaries
        
        Returns:
            AI-generated team insights
        """
        if not self.available:
            return "Gemini AI not available."
        
        # Calculate team statistics
        avg_prob = sum(e.get('promotion_probability', 0) for e in team_data) / len(team_data)
        avg_perf = sum(e.get('performance_score', 0) for e in team_data) / len(team_data)
        avg_lead = sum(e.get('leadership_potential', 0) for e in team_data) / len(team_data)
        
        prompt = f"""
        You are an HR analytics expert. Analyze this group of {len(team_data)} promotion candidates.
        
        Team Statistics:
        - Average Promotion Probability: {avg_prob:.1%}
        - Average Performance Score: {avg_perf:.1f}
        - Average Leadership Potential: {avg_lead:.1f}
        - Number of Candidates: {len(team_data)}
        
        Top 3 Candidates:
        {chr(10).join([f"- {e.get('name', 'Unknown')}: {e.get('promotion_probability', 0):.1%}" for e in team_data[:3]])}
        
        Provide:
        1. Overall team readiness assessment
        2. Patterns or trends you notice
        3. Succession planning recommendations
        4. Talent development priorities
        5. Risk areas to address
        
        Be strategic and actionable. Think about organizational needs.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating team insights: {str(e)}"


# Singleton instance
_gemini_helper = None

def get_gemini_helper() -> GeminiAIHelper:
    """Get or create Gemini AI helper instance"""
    global _gemini_helper
    if _gemini_helper is None:
        _gemini_helper = GeminiAIHelper()
    return _gemini_helper


# Example usage
if __name__ == "__main__":
    print("Gemini AI Helper for HR Decision Support")
    print("=" * 80)
    
    helper = get_gemini_helper()
    
    if helper.is_available():
        print("✅ Gemini AI is available and ready!")
        print()
        print("Features:")
        print("1. ✅ Employee Analysis")
        print("2. ✅ Personalized Recommendations")
        print("3. ✅ Prediction Explanations")
        print("4. ✅ Candidate Comparisons")
        print("5. ✅ What-If Insights")
        print("6. ✅ Team Insights")
    else:
        print("❌ Gemini AI not available")
        print("💡 Please set GEMINI_API_KEY in .env file")
