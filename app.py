#(MAIN STREAMLIT APPLICATION - PART 1)
import streamlit as st
import os
from utils.contract_parser import extract_text_from_file
from utils.nlp_analyzer import ContractAnalyzer
from utils.risk_scorer import RiskAssessment
import json
from datetime import datetime

st.set_page_config(
    page_title="Contract Analysis Bot",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Contract Analysis & Risk Assessment Bot")
st.markdown("**AI-Powered Legal Assistant for SMEs**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("OpenAI API Key (Optional)", type="password")
    st.markdown("---")
    st.markdown("### 📚 Supported Formats")
    st.markdown("- PDF\n- DOCX\n- TXT")

# File uploader
uploaded_file = st.file_uploader(
    "Upload Contract Document", 
    type=['pdf', 'txt', 'docx']
)

if uploaded_file:
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    with st.spinner("Extracting text..."):
        contract_text = extract_text_from_file(file_path)
    
    if contract_text:
        st.success("✅ Text extracted successfully!")
        
        analyzer = ContractAnalyzer()
        risk_assessor = RiskAssessment()
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📝 Summary", 
            "🔍 Analysis", 
            "⚠️ Risk Assessment",
            "📊 Entities",
            "💡 Recommendations"
        ])
        
        with tab1:
            st.header("Contract Summary")
            contract_type = analyzer.classify_contract_type(contract_text)
            st.subheader(f"Type: {contract_type}")
            
            summary_points = analyzer.generate_summary(contract_text)
            for point in summary_points:
                st.markdown(f"- {point}")
        
        with tab2:
            st.header("Clause Analysis")
            clauses = analyzer.extract_clauses(contract_text)
            
            for idx, clause in enumerate(clauses, 1):
                with st.expander(f"Clause {idx}"):
                    st.markdown(f"**Text:** {clause['text'][:200]}...")
                    st.markdown(f"**Explanation:** {clause['explanation']}")
                    clause_type = analyzer.identify_clause_type(clause['text'])
                    st.info(f"**Type:** {clause_type}")
        
        with tab3:
            st.header("Risk Assessment")
            risk_report = risk_assessor.assess_contract_risk(contract_text, analyzer)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                risk_color = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
                st.metric("Risk Level", 
                    f"{risk_color[risk_report['overall_risk']]} {risk_report['overall_risk']}")
            with col2:
                st.metric("Risk Score", f"{risk_report['risk_score']}/100")
            with col3:
                st.metric("High-Risk Items", risk_report['high_risk_count'])
            
            st.markdown("---")
            st.subheader("⚠️ Risk Factors")
            for risk in risk_report['risk_factors']:
                with st.expander(f"{risk['severity']} - {risk['type']}"):
 
                   st.markdown(f"**Issue:** {risk['description']}")
                   st.markdown(f"**Impact:** {risk['impact']}")

        with tab4:
            st.header("Extracted Entities")
            entities = analyzer.extract_entities(contract_text)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("👥 Parties")
                for party in entities.get('parties', [])[:5]:
                    st.markdown(f"- {party}")
                
                st.subheader("💰 Financial Amounts")
                for amount in entities.get('amounts', [])[:5]:
                    st.markdown(f"- {amount}")
            
            with col2:
                st.subheader("📅 Dates")
                for date in entities.get('dates', [])[:5]:
                    st.markdown(f"- {date}")
                
                st.subheader("⚖️ Jurisdiction")
                for jurisdiction in entities.get('jurisdiction', [])[:5]:
                    st.markdown(f"- {jurisdiction}")
        
        with tab5:
            st.header("Recommendations")
            
            st.subheader("🚩 Unfavorable Clauses")
            unfavorable = risk_assessor.identify_unfavorable_clauses(contract_text)
            for clause in unfavorable:
                with st.expander(f"⚠️ {clause['title']}"):
                    st.markdown(f"**Issue:** {clause['issue']}")
                    st.markdown(f"**Alternative:** {clause['alternative']}")
            
            st.markdown("---")
            st.subheader("📄 Export Report")
            
            full_report = {
                "contract_type": contract_type,
                "analysis_date": datetime.now().isoformat(),
                "risk_assessment": risk_report,
                "entities": entities
            }
            
            st.download_button(
                label="📥 Download JSON Report",
                data=json.dumps(full_report, indent=2),
                file_name="contract_report.json",
                mime="application/json"
            )
        
        os.remove(file_path)
    else:
        st.error("❌ Failed to extract text")

st.markdown("---")
st.markdown("Built for **Career Carnival Hackathon 2026**")




        

