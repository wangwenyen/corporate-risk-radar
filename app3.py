import streamlit as st
import pandas as pd
import math
import plotly.graph_objects as go
import plotly.express as px


# ---------------------------
# Language Dictionary
# ---------------------------

LANG = {

    "中文": {

        "title": "企業風控雷達",
        "subtitle": "企業破產預警系統",

        "input_header": "輸入財務資料",
        "cash": "現金",
        "ar": "應收帳款",
        "credit": "可用授信額度",
        "burn": "每月現金流支出",
        "industry": "產業類型",

        "analyze": "分析風險",

        "dashboard": "風險儀表板",

        "liquidity": "總流動資金",
        "survival": "現金流生存月數",
        "bankruptcy": "破產機率",

        "risk_gauge": "破產風險儀表板",
        "survival_gauge": "現金流生存儀表板",

        "risk_radar": "企業風險雷達",

        "benchmark": "產業風險基準",

        "company": "本公司",
        "industry_avg": "產業平均",

        "forecast": "12個月破產機率預測",

        "advisor": "AI風險建議"

    },


    "English": {

        "title": "Corporate Risk Radar",
        "subtitle": "Enterprise Bankruptcy Early Warning System",

        "input_header": "Input Financial Data",
        "cash": "Cash on Hand",
        "ar": "Accounts Receivable",
        "credit": "Credit Line Available",
        "burn": "Monthly Burn Rate",
        "industry": "Industry",

        "analyze": "Analyze Risk",

        "dashboard": "Risk Dashboard",

        "liquidity": "Total Liquidity",
        "survival": "Cash Flow Survival (Months)",
        "bankruptcy": "Bankruptcy Probability",

        "risk_gauge": "Bankruptcy Risk Gauge",
        "survival_gauge": "Cash Flow Survival Gauge",

        "risk_radar": "Corporate Risk Radar",

        "benchmark": "Industry Benchmark",

        "company": "Your Company",
        "industry_avg": "Industry Average",

        "forecast": "12 Month Bankruptcy Forecast",

        "advisor": "AI Risk Advisor"

    }

}


# ---------------------------
# Industry Options
# ---------------------------

INDUSTRY_OPTIONS = {

    "中文": ["製造業","零售業","科技業","營造業"],

    "English": ["Manufacturing","Retail","Tech","Construction"]

}


# ---------------------------
# Industry Benchmark
# ---------------------------

BENCHMARK = {

    "製造業":10,
    "零售業":6,
    "科技業":14,
    "營造業":8,

    "Manufacturing":10,
    "Retail":6,
    "Tech":14,
    "Construction":8

}


# ---------------------------
# Page Setup
# ---------------------------

st.set_page_config(page_title="Corporate Risk Radar", layout="wide")


# ---------------------------
# Language Selection
# ---------------------------

lang = st.sidebar.selectbox("Language / 語言",["中文","English"])

T = LANG[lang]


# ---------------------------
# Title
# ---------------------------

st.title(T["title"])

st.subheader(T["subtitle"])


# ---------------------------
# Sidebar Input
# ---------------------------

st.sidebar.header(T["input_header"])

cash = st.sidebar.number_input(T["cash"],0,100000000,5000000)

ar = st.sidebar.number_input(T["ar"],0,100000000,3000000)

credit = st.sidebar.number_input(T["credit"],0,100000000,2000000)

burn = st.sidebar.number_input(T["burn"],1,10000000,1000000)

industry = st.sidebar.selectbox(

    T["industry"],

    INDUSTRY_OPTIONS[lang]

)


# ---------------------------
# Excel Upload
# ---------------------------

uploaded_file = st.sidebar.file_uploader("Upload Excel", type=["xlsx"])

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    cash = int(df["Cash"][0])
    ar = int(df["AccountsReceivable"][0])
    credit = int(df["CreditLine"][0])
    burn = int(df["BurnRate"][0])

    st.sidebar.success("Excel Loaded")

    st.sidebar.write("Cash:", cash)
    st.sidebar.write("AR:", ar)
    st.sidebar.write("Credit:", credit)
    st.sidebar.write("Burn:", burn)


# ---------------------------
# Risk Model
# ---------------------------

def survival_months(liquidity,burn):

    return round(liquidity/burn,2)


def bankruptcy_probability(survival):

    alpha = 2.5

    beta = -0.35

    z = alpha + beta*survival

    p = 1/(1+math.exp(-z))

    return round(p*100,2)


# ---------------------------
# Run Analysis
# ---------------------------

if st.sidebar.button(T["analyze"]):


    liquidity = cash + ar + credit

    survival = survival_months(liquidity,burn)

    probability = bankruptcy_probability(survival)


    st.header(T["dashboard"])


    col1,col2,col3 = st.columns(3)

    col1.metric(T["liquidity"], liquidity)

    col2.metric(T["survival"], survival)

    col3.metric(T["bankruptcy"], probability)


    # ---------------------------
    # Bankruptcy Gauge
    # ---------------------------

    st.subheader(T["risk_gauge"])

    fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=probability,

        title={"text":T["bankruptcy"]},

        gauge={

            "axis":{"range":[0,100]},

            "steps":[

                {"range":[0,30],"color":"green"},

                {"range":[30,60],"color":"yellow"},

                {"range":[60,100],"color":"red"}

            ]

        }

    ))

    st.plotly_chart(fig,use_container_width=True)


    # ---------------------------
    # Survival Gauge
    # ---------------------------

    st.subheader(T["survival_gauge"])

    fig2 = go.Figure(go.Indicator(

        mode="gauge+number",

        value=survival,

        title={"text":T["survival"]},

        gauge={

            "axis":{"range":[0,24]},

            "steps":[

                {"range":[0,6],"color":"red"},

                {"range":[6,12],"color":"yellow"},

                {"range":[12,24],"color":"green"}

            ]

        }

    ))

    st.plotly_chart(fig2,use_container_width=True)


    # ---------------------------
    # Corporate Risk Radar
    # ---------------------------

    st.subheader(T["risk_radar"])

    liquidity_score = min(liquidity/10000000*100,100)

    survival_score = min(survival/24*100,100)

    risk_score = 100 - probability

    stability_score = (liquidity_score+survival_score)/2


    radar_df = pd.DataFrame({

        "Metric":["Liquidity","CashFlow","Risk","Stability"],

        "Value":[liquidity_score,survival_score,risk_score,stability_score]

    })


    fig3 = px.line_polar(

        radar_df,

        r="Value",

        theta="Metric",

        line_close=True

    )

    fig3.update_traces(fill="toself")

    st.plotly_chart(fig3,use_container_width=True)


    # ---------------------------
    # Benchmark
    # ---------------------------

    st.subheader(T["benchmark"])

    benchmark = BENCHMARK[industry]


    compare_df = pd.DataFrame({

        "Type":[T["company"],T["industry_avg"]],

        "Value":[survival,benchmark]

    })


    fig4 = px.bar(compare_df,x="Type",y="Value")

    st.plotly_chart(fig4,use_container_width=True)


    # ---------------------------
    # Forecast
    # ---------------------------

    st.subheader(T["forecast"])


    months = list(range(1,13))

    forecast = []

    for m in months:

        future = max(survival-m,0)

        forecast.append(bankruptcy_probability(future))


    forecast_df = pd.DataFrame({

        "Month":months,

        "Risk":forecast

    })


    fig5 = px.line(forecast_df,x="Month",y="Risk",markers=True)

    st.plotly_chart(fig5,use_container_width=True)


    # ---------------------------
    # AI Advisor
    # ---------------------------

    st.header(T["advisor"])


    if survival < 6:

        st.error("High liquidity risk. Reduce cost immediately.")

    elif survival < 12:

        st.warning("Moderate financial risk. Monitor cash flow.")

    else:

        st.success("Healthy financial condition.")