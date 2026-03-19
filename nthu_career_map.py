import pandas as pd
import requests
import warnings

# 忽略憑證警告（有些學術/活動網站的 SSL 憑證可能會引起警告）
warnings.filterwarnings('ignore')

def get_booth_data(url):
    print("網頁資料爬取中，請稍候...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, verify=False)
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
                
        print("❌ 找不到符合的表格，網頁結構可能已更動。")
        return None
        
    except Exception as e:
        print(f"❌ 爬取失敗: {e}")
        return None

def locate_booth(booth_no):
    """根據你提供的圖片邏輯，將攤位編號轉換為對應的地圖區域與地標"""
    if not isinstance(booth_no, str) or len(booth_no) < 2:
        return "位置未知"
        
    zone = booth_no[0].upper() # 擷取英文字母判斷區域
    
    if zone == 'A':
        return "🟩 A區 (綠色)：位於下方入口處，靠近名人堂、野台與水漾餐廳。"
    elif zone == 'B':
        return "🟦 B區 (藍色)：位於左下方，蒙民偉樓前方、靠近餐飲區。"
    elif zone == 'C':
        return "🟧 C區 (橘色)：位於中央直線步道，介於 蒙民偉樓/體育館 與 物理館/桌球館 之間。"
    elif zone == 'D':
        return "🟪 D區 (紫色)：位於左側與左上方，圍繞著體育館的周邊道路。"
    elif zone == 'E':
        return "🟨 E區 (黃色)：位於上方大草地與田徑場周邊，靠近主舞台與醫護站。"
    else:
        return "未知區域 (請參考實體地圖)"

def main():
    url = "https://careernthu.conf.asia/com_exhibit_list.aspx?lang=cht"
    df = get_booth_data(url)
    
    if df is not None:
        print(f"✅ 成功抓取 {len(df)} 筆企業攤位資料！\n")
        print("="*40)
        print(" 🎓 清大校園徵才 - 攤位快速定位系統 🎓")
        print("="*40)
        
        while True:
            query = input("\n🔍 請輸入想尋找的「企業名稱」或「攤位編號」(輸入 q 離開): ")
            if query.lower() == 'q':
                print("祝你求職順利！掰掰 👋")
                break
                
            # 支援模糊搜尋 (大小寫不拘)
            results = df[df['企業名稱'].str.contains(query, na=False, case=False) | 
                         df['攤位編號'].str.contains(query, na=False, case=False)]
            
            if results.empty:
                print("⚠️ 找不到符合的資料，請換個關鍵字（例如輸入簡稱「台積電」或「聯發科」）試試。")
            else:
                print("\n🎯 搜尋結果與地圖對應：")
                for index, row in results.iterrows():
                    booth = row['攤位編號']
                    company = row['企業名稱']
                    location = locate_booth(booth)
                    
                    print(f"▶ 🏢 企業：{company}")
                    print(f"  📍 攤位：{booth}")
                    print(f"  🗺️ 位置：{location}")
                    print("-" * 30)

if __name__ == "__main__":
    main()