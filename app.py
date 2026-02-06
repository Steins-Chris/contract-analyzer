import streamlit as st
import PyPDF2
import io

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_contract(text):
    # Simple analysis
    word_count = len(text.split())
    
    # Check for common risk keywords
    risk_keywords = ['penalty', 'liability', 'termination', 'indemnify', 'breach', 'default']
    found_risks = [word for word in risk_keywords if word.lower() in text.lower()]
    
    risk_score = len(found_risks) * 10
    if risk_score > 50:
        risk_level = "High"
    elif risk_score > 25:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    return {
        'word_count': word_count,
        'risk_keywords': found_risks,
        'risk_score': min(risk_score, 100),
        'risk_level': risk_level
    }

st.set_page_config(page_title="Contract Analyzer", page_icon="📄", layout="wide")

st.title("📄 Contract Analysis & Risk Assessment Bot")
st.markdown("### AI-powered legal assistant for SMEs")
st.markdown("---")

with st.sidebar:
    st.header("About")
    st.info(
        "This tool helps analyze contracts and identify potential risks.\n\n"
        "**Features:**\n"
        "- PDF contract upload\n"
        "- Risk keyword detection\n"
        "- Risk scoring\n\n"
        "**Career Carnival Hackathon 2026**"
    )

uploaded_file = st.file_uploader("Upload Contract (PDF)", type=['pdf'])

if uploaded_file:
    with st.spinner('Analyzing contract...'):
        # Extract text
        text = extract_text_from_pdf(uploaded_file)
        
        # Analyze
        results = analyze_contract(text)
        
        st.success('Analysis complete!')
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Word Count", results['word_count'])
        
        with col2:
            st.metric("Risk Score", f"{results['risk_score']}/100")
        
        with col3:
            risk_color = "🔴" if results['risk_level'] == "High" else "🟡" if results['risk_level'] == "Medium" else "🟢"
            st.metric("Risk Level", f"{risk_color} {results['risk_level']}")
        
        st.markdown("---")
        
        if results['risk_keywords']:
            st.subheader("⚠️ Risk Keywords Detected")
            st.write(", ".join(results['risk_keywords']))
        
        with st.expander("View Contract Text"):
            st.text_area("Contract Content", text, height=300)
else:
    st.info("👆 Please upload a PDF contract to begin analysis")
