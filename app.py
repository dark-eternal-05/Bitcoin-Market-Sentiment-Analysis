import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Trader Sentiment Analyzer", layout="wide")

st.title("📈 Trader Performance vs Bitcoin Market Sentiment")

# File uploads
fg_file = st.file_uploader("Upload Fear & Greed Index CSV", type="csv")
trades_file = st.file_uploader("Upload Trader Historical Data CSV", type="csv")

if fg_file and trades_file:
    # Load data
    fg_df = pd.read_csv(fg_file)
    trades_df = pd.read_csv(trades_file)

    # Convert dates
    fg_df['date'] = pd.to_datetime(fg_df['date'])
    trades_df['trade_datetime'] = pd.to_datetime(trades_df['Timestamp IST'], dayfirst=True)
    trades_df['trade_date'] = trades_df['trade_datetime'].dt.normalize()

    # Merge sentiment with trades
    merged_df = pd.merge(trades_df, fg_df[['date', 'classification']], left_on='trade_date', right_on='date', how='left')
    merged_df.drop(columns=['date'], inplace=True)

    # Sidebar filters
    selected_class = st.sidebar.multiselect("Filter by Sentiment", merged_df['classification'].unique(), default=merged_df['classification'].unique())

    filtered_df = merged_df[merged_df['classification'].isin(selected_class)]

    st.subheader("Sample of Merged Data")
    st.dataframe(filtered_df.head(10))

    # ---- ANALYSIS ----
    st.markdown("## 📊 PnL Summary by Sentiment")
    pnl_stats = filtered_df.groupby('classification').agg(
        total_trades=('Closed PnL', 'count'),
        avg_pnl=('Closed PnL', 'mean'),
        median_pnl=('Closed PnL', 'median'),
        total_pnl=('Closed PnL', 'sum')
    ).sort_values(by='avg_pnl', ascending=False)

    st.dataframe(pnl_stats)

    # ---- PLOT 1: Trade Side Distribution ----
    st.markdown("## 🔄 Trade Side Distribution")
    side_dist = filtered_df.groupby(['classification', 'Side']).size().unstack().fillna(0)
    st.bar_chart(side_dist)

    # ---- PLOT 2: Daily PnL Trend ----
    st.markdown("## 📈 Daily Total PnL Over Time")
    daily_pnl = filtered_df.groupby('trade_date')['Closed PnL'].sum().reset_index()
    daily_pnl = daily_pnl.merge(fg_df[['date', 'classification']], left_on='trade_date', right_on='date', how='left')
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=daily_pnl, x='trade_date', y='Closed PnL', hue='classification', ax=ax)
    ax.set_title("Total PnL Per Day by Sentiment")
    ax.set_xlabel("Date")
    ax.set_ylabel("Closed PnL")
    st.pyplot(fig)

    # ---- OPTIONAL: Leverage Analysis ----
    if 'Leverage' in filtered_df.columns:
        st.markdown("## 🧮 Leverage Distribution by Sentiment")
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        sns.boxplot(data=filtered_df, x='classification', y='Leverage', ax=ax2)
        ax2.set_title("Leverage Used by Sentiment Classification")
        st.pyplot(fig2)

else:
    st.info("👆 Please upload both CSV files to begin analysis.")
    
# --- STRATEGY INSIGHTS ---
st.markdown("## 🧠 Strategy Suggestions Based on Sentiment")

strategies = []

for sentiment, row in pnl_stats.iterrows():
    avg_pnl = row['avg_pnl']
    trades = row['total_trades']

    if avg_pnl > 0:
        strategies.append(f"📈 On **{sentiment}** days, traders generally perform well (avg PnL: {avg_pnl:.2f}). Consider increasing exposure and using trend-following strategies.")
    elif avg_pnl < 0:
        strategies.append(f"⚠️ On **{sentiment}** days, traders often face losses (avg PnL: {avg_pnl:.2f}). Reduce position size, consider scalping or staying flat.")
    else:
        strategies.append(f"🔄 On **{sentiment}** days, performance is neutral. Maintain balanced strategies and avoid overleveraging.")

if 'Leverage' in filtered_df.columns:
    high_lev = filtered_df.groupby('classification')['Leverage'].mean().idxmax()
    strategies.append(f"📊 Highest average leverage is used during **{high_lev}** days. Use caution to avoid liquidation.")

for strat in strategies:
    st.markdown(f"- {strat}")

