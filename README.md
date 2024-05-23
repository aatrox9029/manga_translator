# 漫畫翻譯器 日->中
 Only supports Japanese to Chinese.  
僅支援日文轉換成中文繁體/簡體  
效果為將輸入圖片自動翻譯為中文  
請確保已安裝python，盡可能使用虛擬環境(Anaconda)執行  
推薦python版本為3.10.6  
**※※第一次使用請先執行First_Run_Run_This.bat此檔案※※**  

下載解壓後使用win+R 輸入cmd開啟命令提示字元視窗  
輸入 `cd /d "解壓後資料夾所在路徑"`  
`pip install -r requirements.txt `  
將需要翻譯圖片放至Input資料夾，執行程式碼後，翻譯好的圖片會在Output資料夾  
`python manga_translator.py`  
等待一下即可翻譯完成  

在config.txt可以指定要翻譯的語言(繁體或簡體中文)，字體也能選擇，請確保語言與字體是符合的  
zh-TW 為繁體 zh-CN 為簡體  
