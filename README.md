# AI-NSE-Stock-Analyzer with Langchain & ScreenerAPI
<p align="center">
<img src="https://github.com/user-attachments/assets/f82f29ed-5929-4954-879e-e1582b0dd1a0" width="500"/>
</p>

## About The Project:
AI-Stock-Analyzer is a generative AI webapp for performing fundamental analysis of the NSE stock market data. This project was developed using Streamlit LangChain and Gemini Flash for the LLM. Used selenium python to webscrape screencer website for stock data and to create API. `Disclaimer: Don't use trust this blindly, only for pro-noobies or later`
<br>

https://github.com/user-attachments/assets/36447d2c-1379-4426-871c-191090ff678d

## How to Run:
#### 1. Clone the repository:
   - ```
     git clone https://github.com/harshitv804/AI-Stock-Analyzer.git
     ```
#### 2. Install necessary packages:
   - ```
     pip install -r requirements.txt
     ```
#### 3. Add Google Gemini API key to the `.env` file.
#### 4. Run `streamlit run stock_analyse.py`.

## Customization Features:
- You can fetch data if you have an Screener Account for adding more metrics. To do that add your login credintials inside the class shown below:
```py
  StockScreenerScraper(login_email='LOGIN_EMAIL',login_pass='LOGIN_PASS')
```
https://github.com/harshitv804/AI-Stock-Analyzer/blob/b97bd4aafcaae60fa7b7b95eeabd551e966e226f/stock_analyse.py#L33

## Contact:
If you have any questions or feedback, please raise an [github issue](https://github.com/harshitv804/LawGPT/issues).
