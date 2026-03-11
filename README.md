import streamlit as st
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

# הגדרת כיוון כתיבה מימין לשמאל (RTL)
st.markdown("""
    <style>
    body { direction: rtl; text-align: right; }
    .stTextInput > div > div > input { direction: rtl; text-align: right; }
    .stMarkdown, .stText, p, h1, h2, h3 { direction: rtl; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 מחולל עבודות מחקר אוטונומי")
st.subheader("מבית סיון - מחקר תורני ואקדמי")

topic = st.text_input("הכנס את נושא העבודה שלך:")

if st.button("בנה עבודה מלאה"):
    if not topic:
        st.error("בבקשה הכנס נושא!")
    else:
        with st.spinner(f"סורק את הרשת עבור '{topic}'..."):
            results = []
            with DDGS() as ddgs:
                # מחפש 15 מקורות בעברית
                search_results = list(ddgs.text(f"{topic} מאמר אקדמי", region='il-he', max_results=15))
            
            summary_content = ""
            sources_list = []
            
            for i, res in enumerate(search_results):
                try:
                    r = requests.get(res['href'], timeout=10)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    text = " ".join([p.get_text() for p in soup.find_all('p')])[:1000]
                    summary_content += f"\n\n### {res['title']}\n{text}...\n"
                    sources_list.append(f"{i+1}. {res['title']}. קישור: {res['href']}")
                except: continue

            st.success("המחקר הושלם!")
            full_report = f"# עבודה בנושא: {topic}\n\n## סקירת מקורות\n{summary_content}\n\n## ביבליוגרפיה\n" + "\n".join(sources_list)
            st.markdown(full_report)
            st.download_button("הורד עבודה כקובץ TXT", full_report, file_name=f"{topic}.txt")
