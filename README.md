
# 📈 Trader Sentiment Analyzer

Analyze trader performance against **Bitcoin market sentiment** (Fear & Greed Index) using interactive visualizations and intelligent strategy suggestions. Built with **Streamlit** for easy use.

---

## 🚀 Features

- 📤 Upload historical trade data and Fear-Greed sentiment CSVs
- 📊 Get summary statistics: PnL, trade volume, leverage
- 🔄 Visualize BUY/SELL distribution by sentiment
- 📈 Track daily PnL over time with sentiment overlay
- 🧠 Auto-generated strategy insights
- ☁️ Deployable via Streamlit Cloud or Docker

---

## 🗂️ Example Dataset Format

### 1. Fear & Greed Index (`fear_greed_index.csv`)
```csv
date,value,classification
2024-06-01,45,Greed
2024-06-02,20,Fear
...
```

### 2. Historical Trader Data (`historical_data.csv`)
```csv
Timestamp IST,Coin,Execution Price,Size USD,Side,Closed PnL,...
02-12-2024 22:50,@107,7.9769,7872.16,BUY,50.75,...
```

---

## 🛠️ Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/trader-sentiment-analyzer.git
cd trader-sentiment-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

---

## 📌 Project Structure

```
.
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
└── README.md               # Project info
```

---

## 💡 Sample Insights Delivered

- Greed days show 2.3x higher avg PnL → use breakout strategies.
- Extreme Fear → lower leverage, fewer trades → apply risk-off tactics.
- Trader behavior shifts align closely with market sentiment.
