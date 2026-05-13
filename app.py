import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# plotly imported after streamlit to avoid cloud module resolution issues
import plotly.graph_objects as go

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinSight · Personal Finance",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stAppViewContainer"], [data-testid="stMain"], .block-container {
    background: #0d0f14 !important;
}
.block-container { padding-top: 1.5rem !important; max-width: 1280px !important; }

body, p, span, div, label { color: #e2e0db; font-family: 'DM Sans', sans-serif; }

.stTextInput > label { color: #9a9890 !important; font-size: 13px !important; }
.stTextInput input {
    background: #1a1c24 !important;
    border: 1px solid #2e3040 !important;
    border-radius: 10px !important;
    color: #e2e0db !important;
}
.stTextInput input:focus {
    border-color: #5ce89b !important;
    box-shadow: 0 0 0 2px rgba(92,232,155,0.15) !important;
}

.stButton > button {
    background: #5ce89b !important;
    color: #0d0f14 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    width: 100% !important;
}
.stButton > button:hover { background: #3fd47f !important; }

[data-testid="stMetric"] {
    background: #161820 !important;
    border: 1px solid #23253a !important;
    border-radius: 14px !important;
    padding: 18px 20px !important;
}
[data-testid="stMetricLabel"] p { color: #7a7870 !important; font-size: 12px !important; }
[data-testid="stMetricValue"]   { color: #e2e0db !important; }

[data-testid="stSidebar"] { display: none !important; }

hr { border-color: #23253a !important; }

.stTabs [data-baseweb="tab-list"] {
    background: #161820;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: #7a7870;
    font-size: 13px;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: #1f2135 !important;
    color: #e2e0db !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
for k, v in [("page", "signin"), ("user_name", ""), ("user_email", "")]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Data ───────────────────────────────────────────────────────────────────────
@st.cache_data
def get_portfolio():
    np.random.seed(42)
    dates = pd.date_range(end=datetime.today(), periods=180, freq="D")
    rets  = np.random.normal(0.0008, 0.012, 180)
    vals  = 50000 * np.cumprod(1 + rets)
    return pd.DataFrame({"date": dates, "value": vals})

@st.cache_data
def get_cashflow():
    np.random.seed(7)
    months = pd.date_range(end=datetime.today(), periods=12, freq="ME")
    return pd.DataFrame({
        "month":   months,
        "income":  np.random.uniform(6200, 9000, 12),
        "expense": np.random.uniform(3800, 6200, 12),
    })

HOLDINGS = [
    {"ticker": "AAPL",  "name": "Apple Inc.",      "shares": 15,  "price": 189.45, "chg": +1.23},
    {"ticker": "MSFT",  "name": "Microsoft Corp.", "shares": 8,   "price": 415.20, "chg": +0.88},
    {"ticker": "NVDA",  "name": "NVIDIA Corp.",    "shares": 5,   "price": 875.60, "chg": +3.41},
    {"ticker": "GOOGL", "name": "Alphabet Inc.",   "shares": 10,  "price": 175.90, "chg": -0.54},
    {"ticker": "BTC",   "name": "Bitcoin",         "shares": 0.5, "price": 67400,  "chg": +2.10},
]

BUDGET = [
    {"cat": "Housing",       "spent": 1850, "limit": 2000, "color": "#40a9ff"},
    {"cat": "Food",          "spent": 680,  "limit": 700,  "color": "#5ce89b"},
    {"cat": "Transport",     "spent": 310,  "limit": 400,  "color": "#fbbf24"},
    {"cat": "Subscriptions", "spent": 145,  "limit": 150,  "color": "#a78bfa"},
    {"cat": "Shopping",      "spent": 490,  "limit": 350,  "color": "#f87171"},
    {"cat": "Healthcare",    "spent": 120,  "limit": 300,  "color": "#34d399"},
]

PLOT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#7a7870", size=11),
    margin=dict(t=10, b=10, l=10, r=10),
    hovermode="x unified",
)

def section(title, sub=""):
    html = f"<div style='font-family:Syne,sans-serif;font-size:15px;font-weight:700;color:#e2e0db;margin-bottom:2px'>{title}</div>"
    if sub:
        html += f"<div style='font-size:12px;color:#5a5856;margin-bottom:8px'>{sub}</div>"
    st.markdown(html, unsafe_allow_html=True)

def google_btn(label):
    st.markdown(f"""
    <div style='background:#1a1c24;border:1px solid #2e3040;border-radius:10px;
         padding:11px 16px;font-size:14px;font-weight:500;color:#e2e0db;
         display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:4px'>
      <svg width='16' height='16' viewBox='0 0 18 18'>
        <path fill='#EA4335' d='M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z'/>
        <path fill='#4285F4' d='M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 0 0 9 18z'/>
        <path fill='#FBBC05' d='M3.964 10.71A5.41 5.41 0 0 1 3.682 9c0-.593.102-1.17.282-1.71V4.958H.957A8.996 8.996 0 0 0 0 9c0 1.452.348 2.827.957 4.042l3.007-2.332z'/>
        <path fill='#34A853' d='M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 0 0 .957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z'/>
      </svg>
      {label}
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIGN IN
# ══════════════════════════════════════════════════════════════════════════════
def page_signin():
    _, mid, _ = st.columns([1, 1.1, 1])
    with mid:
        st.markdown("""
        <div style='text-align:center;padding:28px 0 18px'>
          <div style='font-family:Syne,sans-serif;font-size:30px;font-weight:800;color:#5ce89b'>
            Fin<span style='color:#e2e0db'>Sight</span></div>
          <div style='font-size:13px;color:#5a5856;margin-top:6px'>Personal finance intelligence</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='font-family:Syne,sans-serif;font-size:18px;font-weight:700;color:#e2e0db;margin-bottom:14px'>Sign in to your account</div>", unsafe_allow_html=True)

        google_btn("Continue with Google")
        if st.button("Continue with Google", key="g_si"):
            st.session_state.user_name = "Google User"
            st.session_state.page = "dashboard"
            st.rerun()

        st.markdown("<div style='text-align:center;color:#3a3c4a;font-size:12px;margin:12px 0'>— or sign in with email —</div>", unsafe_allow_html=True)

        email = st.text_input("Email address", placeholder="you@example.com", key="si_em")
        pwd   = st.text_input("Password",      placeholder="••••••••",        type="password", key="si_pw")

        if st.button("Sign In →", key="si_btn"):
            if email and pwd:
                st.session_state.user_name  = email.split("@")[0].capitalize()
                st.session_state.user_email = email
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Please enter your email and password.")

        st.markdown("<hr style='margin:18px 0'>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;font-size:13px;color:#5a5856;margin-bottom:8px'>Don't have an account?</div>", unsafe_allow_html=True)
        if st.button("Create a free account", key="to_su"):
            st.session_state.page = "signup"
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# SIGN UP
# ══════════════════════════════════════════════════════════════════════════════
def page_signup():
    _, mid, _ = st.columns([1, 1.1, 1])
    with mid:
        st.markdown("""
        <div style='text-align:center;padding:28px 0 18px'>
          <div style='font-family:Syne,sans-serif;font-size:30px;font-weight:800;color:#5ce89b'>
            Fin<span style='color:#e2e0db'>Sight</span></div>
          <div style='font-size:13px;color:#5a5856;margin-top:6px'>Create your account</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='font-family:Syne,sans-serif;font-size:18px;font-weight:700;color:#e2e0db;margin-bottom:14px'>Get started for free</div>", unsafe_allow_html=True)

        google_btn("Sign up with Google")
        if st.button("Sign up with Google", key="g_su"):
            st.session_state.user_name = "Google User"
            st.session_state.page = "dashboard"
            st.rerun()

        st.markdown("<div style='text-align:center;color:#3a3c4a;font-size:12px;margin:12px 0'>— or sign up with email —</div>", unsafe_allow_html=True)

        name  = st.text_input("Full name",        placeholder="Alex Johnson",      key="su_nm")
        email = st.text_input("Email address",    placeholder="you@example.com",   key="su_em")
        pwd   = st.text_input("Password",         placeholder="Min. 8 characters", type="password", key="su_pw")
        pwd2  = st.text_input("Confirm password", placeholder="Repeat password",   type="password", key="su_pw2")

        if st.button("Create Account →", key="su_btn"):
            if not all([name, email, pwd, pwd2]):
                st.error("Please fill in all fields.")
            elif pwd != pwd2:
                st.error("Passwords do not match.")
            elif len(pwd) < 8:
                st.error("Password must be at least 8 characters.")
            else:
                st.session_state.user_name  = name.split()[0]
                st.session_state.user_email = email
                st.session_state.page = "dashboard"
                st.rerun()

        st.markdown("<hr style='margin:18px 0'>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;font-size:13px;color:#5a5856;margin-bottom:8px'>Already have an account?</div>", unsafe_allow_html=True)
        if st.button("Back to Sign In", key="to_si"):
            st.session_state.page = "signin"
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    name      = st.session_state.user_name or "User"
    portfolio = get_portfolio()
    cashflow  = get_cashflow()

    cur_val        = portfolio["value"].iloc[-1]
    total_invested = 48_200
    total_gain     = cur_val - total_invested
    gain_pct       = total_gain / total_invested * 100
    month_ret      = (cur_val - portfolio["value"].iloc[-30]) / portfolio["value"].iloc[-30] * 100
    net_worth      = cur_val + 12_400

    # Topbar
    tl, tm, tr = st.columns([1, 3, 1])
    with tl:
        st.markdown("<div style='font-family:Syne,sans-serif;font-size:22px;font-weight:800;color:#5ce89b;padding:8px 0'>Fin<span style='color:#e2e0db'>Sight</span></div>", unsafe_allow_html=True)
    with tm:
        st.markdown("<div style='display:flex;gap:28px;justify-content:center;align-items:center;padding:12px 0;font-size:13px;color:#5a5856'><b style='color:#e2e0db'>Overview</b><span>Portfolio</span><span>Budget</span><span>Reports</span></div>", unsafe_allow_html=True)
    with tr:
        st.markdown(f"<div style='text-align:right;font-size:13px;color:#7a7870;padding:4px 0'>👤 {name}</div>", unsafe_allow_html=True)
        if st.button("Sign Out", key="logout"):
            st.session_state.page = "signin"
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("💰 Net Worth",       f"${net_worth:,.0f}",  f"+{gain_pct:.1f}% all time")
    k2.metric("📈 Portfolio Value", f"${cur_val:,.0f}",    f"+{month_ret:.1f}% this month")
    k3.metric("📊 Total Gain",      f"${total_gain:,.0f}", "Since inception")
    k4.metric("🎯 Savings Rate",    "28.4%",               "+2.1 pp vs last month")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["  📈  Portfolio  ", "  💵  Cash Flow  ", "  🎯  Budget  "])

    # ── Portfolio tab ──
    with tab1:
        ca, cb = st.columns([2, 1], gap="large")
        with ca:
            section("Portfolio Performance", "180-day history · daily close")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=portfolio["date"], y=portfolio["value"],
                mode="lines", line=dict(color="#5ce89b", width=2.2),
                fill="tozeroy", fillcolor="rgba(92,232,155,0.06)",
                hovertemplate="<b>$%{y:,.0f}</b><br>%{x|%b %d, %Y}<extra></extra>",
            ))
            fig.update_layout(height=260,
                xaxis=dict(showgrid=False, color="#5a5856"),
                yaxis=dict(showgrid=True, gridcolor="#1e2030", tickformat="$,.0f", color="#5a5856"),
                **PLOT_BASE)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with cb:
            section("Asset Allocation", "By class")
            fig2 = go.Figure(go.Pie(
                labels=["US Equity","Crypto","Intl","Cash","Bonds"],
                values=[52, 18, 14, 10, 6], hole=0.6,
                marker=dict(colors=["#5ce89b","#fbbf24","#40a9ff","#a78bfa","#f87171"],
                            line=dict(color="#0d0f14", width=2)),
                textinfo="none",
                hovertemplate="<b>%{label}</b>: %{value}%<extra></extra>",
            ))
            fig2.update_layout(height=260,
                legend=dict(font=dict(size=11, color="#7a7870"), bgcolor="rgba(0,0,0,0)",
                            orientation="v", x=0.72, y=0.5),
                **PLOT_BASE)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        section("Top Holdings", "Current positions")

        hdr = st.columns([1.4, 2.6, 1.5, 1.5, 1.2])
        for i, lbl in enumerate(["Ticker","Name","Value","Price","24h Chg"]):
            hdr[i].markdown(f"<span style='font-size:11px;color:#5a5856;text-transform:uppercase;letter-spacing:0.5px'>{lbl}</span>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

        for h in HOLDINGS:
            val = h["shares"] * h["price"]
            cc  = "#5ce89b" if h["chg"] >= 0 else "#f87171"
            sg  = "+" if h["chg"] >= 0 else ""
            rc  = st.columns([1.4, 2.6, 1.5, 1.5, 1.2])
            rc[0].markdown(f"<b style='font-family:Syne,sans-serif;color:#e2e0db'>{h['ticker']}</b>", unsafe_allow_html=True)
            rc[1].markdown(f"<span style='font-size:13px;color:#7a7870'>{h['name']}</span>", unsafe_allow_html=True)
            rc[2].markdown(f"<span style='font-size:13px;color:#e2e0db;font-weight:500'>${val:,.0f}</span>", unsafe_allow_html=True)
            rc[3].markdown(f"<span style='font-size:13px;color:#7a7870'>${h['price']:,.2f}</span>", unsafe_allow_html=True)
            rc[4].markdown(f"<span style='font-size:13px;font-weight:600;color:{cc}'>{sg}{h['chg']}%</span>", unsafe_allow_html=True)

    # ── Cash Flow tab ──
    with tab2:
        cf1, cf2 = st.columns(2, gap="large")
        months_lbl = cashflow["month"].dt.strftime("%b")

        with cf1:
            section("Income vs Expenses", "Last 12 months")
            fig3 = go.Figure()
            fig3.add_trace(go.Bar(x=months_lbl, y=cashflow["income"],  name="Income",
                                  marker_color="#5ce89b", hovertemplate="Income: $%{y:,.0f}<extra></extra>"))
            fig3.add_trace(go.Bar(x=months_lbl, y=cashflow["expense"], name="Expenses",
                                  marker_color="#f87171", hovertemplate="Expense: $%{y:,.0f}<extra></extra>"))
            fig3.update_layout(height=280, barmode="group", bargap=0.2,
                xaxis=dict(showgrid=False, color="#5a5856"),
                yaxis=dict(showgrid=True, gridcolor="#1e2030", tickformat="$,.0f", color="#5a5856"),
                legend=dict(font=dict(size=11, color="#7a7870"), bgcolor="rgba(0,0,0,0)",
                            orientation="h", x=0, y=1.1),
                **PLOT_BASE)
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

        with cf2:
            section("Monthly Net Savings", "Income minus expenses")
            net    = cashflow["income"] - cashflow["expense"]
            colors = ["#5ce89b" if v >= 0 else "#f87171" for v in net]
            fig4   = go.Figure(go.Bar(x=months_lbl, y=net, marker_color=colors,
                                      hovertemplate="Net: $%{y:,.0f}<extra></extra>"))
            fig4.update_layout(height=280,
                xaxis=dict(showgrid=False, color="#5a5856"),
                yaxis=dict(showgrid=True, gridcolor="#1e2030", tickformat="$,.0f", color="#5a5856"),
                **PLOT_BASE)
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        avg_inc  = cashflow["income"].mean()
        avg_exp  = cashflow["expense"].mean()
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Avg Monthly Income",  f"${avg_inc:,.0f}")
        s2.metric("Avg Monthly Expense", f"${avg_exp:,.0f}")
        s3.metric("Avg Net Savings",     f"${avg_inc - avg_exp:,.0f}")
        s4.metric("Best Savings Month",  f"${(cashflow['income'] - cashflow['expense']).max():,.0f}")

    # ── Budget tab ──
    with tab3:
        b1, b2 = st.columns(2, gap="large")

        with b1:
            section("Monthly Budget Tracker", "May 2026 · spending vs limits")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            for b in BUDGET:
                pct  = min(b["spent"] / b["limit"] * 100, 100)
                over = b["spent"] > b["limit"]
                bc   = "#f87171" if over else b["color"]
                stxt = f"⚠ Over ${b['spent']-b['limit']}" if over else f"${b['limit']-b['spent']} left"
                sclr = "#f87171" if over else "#5a5856"
                st.markdown(f"""
                <div style='margin-bottom:18px'>
                  <div style='display:flex;justify-content:space-between;margin-bottom:6px;font-size:13px'>
                    <span style='color:#e2e0db;font-weight:500'>{b['cat']}</span>
                    <span style='color:#7a7870'>${b['spent']}
                      <span style='color:#3a3c4a'>/ ${b['limit']}</span>
                      &nbsp;<span style='color:{sclr}'>{stxt}</span>
                    </span>
                  </div>
                  <div style='background:#1e2030;border-radius:99px;height:6px;overflow:hidden'>
                    <div style='background:{bc};width:{pct}%;height:100%;border-radius:99px'></div>
                  </div>
                </div>""", unsafe_allow_html=True)

        with b2:
            section("Spending by Category", "This month")
            fig5 = go.Figure(go.Bar(
                x=[b["spent"] for b in BUDGET],
                y=[b["cat"]   for b in BUDGET],
                orientation="h",
                marker=dict(color=[b["color"] for b in BUDGET], line=dict(color="rgba(0,0,0,0)")),
                hovertemplate="<b>%{y}</b>: $%{x:,.0f}<extra></extra>",
            ))
            fig5.update_layout(height=320,
                xaxis=dict(showgrid=True, gridcolor="#1e2030", tickformat="$,.0f", color="#5a5856"),
                yaxis=dict(showgrid=False, color="#9a9890"),
                **PLOT_BASE)
            st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})

            total_spent = sum(b["spent"] for b in BUDGET)
            total_limit = sum(b["limit"] for b in BUDGET)
            st.markdown(f"""
            <div style='background:#161820;border:1px solid #23253a;border-radius:12px;padding:16px 20px;margin-top:12px'>
              <div style='font-size:11px;color:#5a5856;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px'>Total Budget Used</div>
              <div style='font-family:Syne,sans-serif;font-size:26px;font-weight:700;color:#e2e0db'>{total_spent/total_limit*100:.0f}%</div>
              <div style='font-size:12px;color:#7a7870;margin-top:4px'>${total_spent:,.0f} of ${total_limit:,.0f}</div>
            </div>""", unsafe_allow_html=True)

# ── Router ─────────────────────────────────────────────────────────────────────
if st.session_state.page == "signin":
    page_signin()
elif st.session_state.page == "signup":
    page_signup()
else:
    page_dashboard()
