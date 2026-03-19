"""啟動器：以無視窗模式運行 AirPods Battery Monitor。"""
import runpy
import os
import sys

# 確保工作目錄為腳本所在資料夾
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 引入並執行主程式
runpy.run_path("show_airpods_battery.py", run_name="__main__")
