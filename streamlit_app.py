"""
清大校園徵才 - 攤位快速定位系統 (Streamlit 網頁版)
可以在手機和電腦上訪問
"""

import streamlit as st
import pandas as pd
import requests
import warnings

# 忽略憑證警告
warnings.filterwarnings('ignore')

# ── 頁面設定 ────────────────────────────────────
st.set_page_config(
    page_title="清大徵才攤位定位",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS 美化 ────────────────────────────────────
st.markdown("""
    <style>
    body {
        background-color: #f0f4f8;
    }
    .main {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton > button {
        background-color: #2196F3;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #0b7dda;
    }
    .result-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

def get_booth_data(url):
    """從網頁爬取企業與攤位資料"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        response.encoding = 'utf-8'
        
        # 使用 pandas 快速解析網頁中的所有表格
        tables = pd.read_html(response.text)
        
        # 尋找包含「攤位編號」的正確表格
        for df in tables:
            # 如果第一列是標題
            if df.iloc[0].astype(str).str.contains("攤位編號").any():
                df.columns = df.iloc[0] # 將第一列設為欄位名稱
                df = df[1:]             # 移除第一列資料
                
            if "攤位編號" in df.columns and "企業名稱" in df.columns:
                # 清理並回傳乾淨的資料表
                return df[["攤位編號", "企業名稱"]].dropna()
                
        return None
        
    except Exception as e:
        st.error(f"❌ 爬取失敗: {e}")
        return None

def locate_booth(booth_no):
    """根據攤位編號轉換為對應的地圖區域與地標"""
    if not isinstance(booth_no, str) or len(booth_no) < 2:
        return "位置未知"
        
    zone = booth_no[0].upper() # 擷取英文字母判斷區域
    
    zones = {
        'A': "🟩 A區 (綠色)：位於下方入口處，靠近名人堂、野台與水漾餐廳。",
        'B': "🟦 B區 (藍色)：位於左下方，蒙民偉樓前方、靠近餐飲區。",
        'C': "🟧 C區 (橘色)：位於中央直線步道，介於 蒙民偉樓/體育館 與 物理館/桌球館 之間。",
        'D': "🟪 D區 (紫色)：位於左側與左上方，圍繞著體育館的周邊道路。",
        'E': "🟨 E區 (黃色)：位於上方大草地與田徑場周邊，靠近主舞台與醫護站。",
    }
    
    return zones.get(zone, "未知區域 (請參考實體地圖)")

# ── 主程式 ────────────────────────────────────
def main():
    # 標題
    st.title("🎓 清大校園徵才 - 攤位快速定位系統")
    st.markdown("---")
    
    # 使用 Streamlit 的快取機制加快資料加載
    @st.cache_data
    def load_data():
        url = "https://careernthu.conf.asia/com_exhibit_list.aspx?lang=cht"
        return get_booth_data(url)
    
    # 加載資料
    with st.spinner("📡 正在獲取企業攤位資料..."):
        df = load_data()
    
    if df is None:
        st.error("❌ 無法獲取資料，請檢查網路連線或聯絡管理員")
        return
    
    st.success(f"✅ 成功載入 {len(df)} 筆企業資料")
    st.markdown("---")
    
    # 搜尋欄位
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "🔍 搜尋企業名稱或攤位編號",
            placeholder="例如：台積電、聯發科、A1...",
            key="search_input"
        )
    
    with col2:
        st.write("")  # 空格對齊
        search_button = st.button("🔎 搜尋", use_container_width=True)
    
    # 執行搜尋
    if search_query or search_button:
        if search_query:
            # 支援模糊搜尋 (大小寫不拘)
            results = df[
                df['企業名稱'].str.contains(search_query, na=False, case=False) | 
                df['攤位編號'].str.contains(search_query, na=False, case=False)
            ]
            
            if results.empty:
                st.warning("⚠️ 找不到符合的資料，請換個關鍵字試試（例如輸入簡稱）")
                
                # 顯示隨機建議
                st.info(f"💡 試試看這些企業：{', '.join(df['企業名稱'].sample(min(3, len(df))).tolist())}")
            else:
                st.markdown(f"### 🎯 搜尋結果 ({len(results)} 筆)")
                
                # 用表格和卡片展示結果
                for idx, (index, row) in enumerate(results.iterrows()):
                    booth = row['攤位編號']
                    company = row['企業名稱']
                    location = locate_booth(booth)
                    
                    # 建立展開式卡片
                    with st.expander(f"🏢 {company} - 攤位 {booth}", expanded=(idx == 0)):
                        col1, col2 = st.columns([2, 2])
                        
                        with col1:
                            st.write(f"**企業名稱：** {company}")
                            st.write(f"**攤位編號：** {booth}")
                        
                        with col2:
                            st.markdown(f"**📍 位置：**  \n{location}")
    
    # ── 側邊欄 - 所有企業列表 ────
    st.markdown("---")
    
    with st.expander("📋 查看所有企業列表", expanded=False):
        # 添加排序选项
        col1, col2 = st.columns(2)
        
        with col1:
            sort_by = st.radio("排序方式", ["企業名稱", "攤位編號"], horizontal=True)
        
        # 排序資料
        if sort_by == "企業名稱":
            sorted_df = df.sort_values("企業名稱")
        else:
            sorted_df = df.sort_values("攤位編號")
        
        # 顯示表格
        st.dataframe(sorted_df, use_container_width=True, hide_index=True)
        
        # 下載 CSV 功能
        csv = sorted_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 下載 CSV",
            data=csv,
            file_name="nthu_career_booths.csv",
            mime="text/csv"
        )
    
    # ── 頁腳 ────
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: gray; font-size: 12px;'>
        🎓 清大校園徵才攤位定位系統 | 最後更新：即時網頁資料  
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
