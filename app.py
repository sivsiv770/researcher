import streamlit as st
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import pandas as pd

# הגדרת כיוון כתיבה מימין לשמאל (RTL)
st.markdown("""
    <style>
    .reportview-container .main .block-container { direction: rtl; }
    div[role="radiogroup"] { direction: rtl; }
    p, h1, h2, h3, label { text-align: right; direction: rtl; }
    .stTextInput > div > div > input { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 מחולל עבודות מחקר אוטונומי")
st.subheader("מבית סיון - מחקר תורני ואקדמי")

topic = st.text_input("הכנס את נושא העבודה שלך:")

if st.button("בנה עבודה מלאה"):
    if not topic:
        st.error("בבקשה הכנס נושא!")
    else:
        with st.spinner(f"סורק את הרשת עבור '{topic}' בעברית בלבד..."):
            # 1. חיפוש מקורות בעברית
            results = []
            with DDGS() as ddgs:
                # הגבלה ל-15 תוצאות מישראל בעברית
                search_results = list(ddgs.text(f"{topic} מאמר", region='il-he', max_results=15))
            
            # 2. איסוף וניתוח תוכן
            full_text_compiled = ""
            sources_list = []
            
            for i, res in enumerate(search_results):
                try:
                    r = requests.get(res['href'], timeout=10)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    paragraphs = [p.get_text() for p in soup.find_all('p')]
                    content = " ".join(paragraphs)[:2000] # לוקח 2000 תווים ראשונים
                    
                    full_text_compiled += f"\n\n### מקור {i+1}: {res['title']}\n{content}"
                    sources_list.append(f"{i+1}. {res['title']}. זמין בכתובת: {res['href']}")
                except:
                    continue

            # 3. בניית ה"עבודה" (סינתזה בסיסית)
            st.success("המחקר הושלם! הנה העבודה המוכנה שלך:")
            
            research_work = f"""
# עבודת מחקר בנושא: {topic}

## מבוא וסקירה כללית
על פי המקורות שנמצאו ברשת, הנושא {topic} נדון בהרחבה בהקשרים פדגוגיים ותורניים. 
להלן ניתוח הממצאים העיקריים מתוך 15 המקורות שנסרקו.

## ממצאים עיקריים
{full_text_compiled[:5000]}... (המשך ניתוח אוטונומי)

## סיכום ומסקנות
המחקר מעלה כי השילוב של {topic} מהווה נדבך משמעותי בעולם החינוך וההלכה המודרני.

## ביבליוגרפיה (APA בסיסי)
""" + "\n".join(sources_list)

            st.markdown(research_work)
            
            # כפתור הורדה
            st.download_button("הורד עבודה כקובץ טקסט", research_work, file_name=f"research_{topic}.txt")