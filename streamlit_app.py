import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# ---- minimal dark theme (cyan accent, thin outline) ----
st.markdown("""
<style>
html, body, [data-testid="stApp"] { background:#0a0a0a; color:#e8e8e8; }
[data-testid="stHeader"] { background:#0a0a0a; }
.stButton>button { background:#111; color:#e8e8e8; border:1px solid #2a2a2a; }
.stButton>button:hover { border-color:#3ad6e0; color:#3ad6e0; }
h1,h2,h3 { font-weight:600; }
.css-1v0mbdj { border:1px solid #2a2a2a; }
.stSlider>div>div { color:#3ad6e0; }
</style>
""", unsafe_allow_html=True)

st.title("Aquila Auto-Resolve Explorer")
st.caption("IAT 461 Final Project - interactive companion to the notebook (optional +10% Streamlit bonus)")

# ============ load + build the SAME model as the notebook ============
@st.cache_resource
def load_models():
    df = pd.read_csv("battles.csv")
    units = pd.read_csv("unit_roster.csv")

    ATT = ["att_heavy_infantry","att_spearmen","att_sword_infantry","att_archers",
           "att_skirmishers","att_light_cavalry","att_shock_cavalry","att_artillery"]
    DEF = ["def_heavy_infantry","def_spearmen","def_sword_infantry","def_archers",
           "def_skirmishers","def_light_cavalry","def_shock_cavalry","def_artillery"]

    X = df.copy()
    X["y"] = (df["outcome"] == "attacker").astype(int)
    X["att_total"] = X[ATT].sum(axis=1)
    X["def_total"] = X[DEF].sum(axis=1)
    X["total_ratio"] = X["att_total"] / (X["def_total"] + 1e-9)
    X["total_diff"] = X["att_total"] - X["def_total"]
    X["gen_diff"] = X["att_general_rating"] - X["def_general_rating"]
    X["morale_diff"] = X["att_avg_morale"] - X["def_avg_morale"]
    X["fatigue"] = X["att_fatigue"] / 100.0
    X["fortified"] = X["def_fortified"]
    X["att_spear_def_cav"] = X["att_spearmen"] * (X["def_light_cavalry"] + X["def_shock_cavalry"])
    X["att_cav_def_archer"] = (X["att_light_cavalry"] + X["att_shock_cavalry"]) * X["def_archers"]
    feat_cols = (ATT + DEF +
                 ["att_total","def_total","total_ratio","total_diff",
                  "gen_diff","morale_diff","fatigue","fortified",
                  "att_spear_def_cav","att_cav_def_archer"])
    F = pd.concat([X[feat_cols],
                   pd.get_dummies(X["terrain"], prefix="terrain"),
                   pd.get_dummies(X["weather"], prefix="weather")], axis=1)
    y = X["y"].values
    FEATURE_COLS = list(F.columns)

    scaler = StandardScaler().fit(F)
    model = LogisticRegression(max_iter=2000).fit(scaler.transform(F), y)

    # role audit
    vec = TfidfVectorizer(stop_words="english", max_features=300)
    M = vec.fit_transform(units["description"].astype(str))
    km = KMeans(n_clusters=6, random_state=461, n_init=10)
    units["cluster"] = km.fit_predict(M)
    ct = pd.crosstab(units["cluster"], units["advertised_role"])
    dominant = ct.idxmax(axis=1)
    purity = ct.max(axis=1) / ct.sum(axis=1)
    agreement = (dominant[units["cluster"].values] == units["advertised_role"].values).mean()

    return dict(df=df, units=units, ATT=ATT, DEF=DEF, feat_cols=feat_cols,
                FEATURE_COLS=FEATURE_COLS, scaler=scaler, model=model,
                vec=vec, km=km, ct=ct, dominant=dominant, purity=purity,
                agreement=agreement, terrain_cats=sorted(df["terrain"].unique()),
                weather_cats=sorted(df["weather"].unique()))

M = load_models()

# ============ nav ============
page = st.sidebar.radio("Go to", ["Battle Outcome Predictor", "Unit Role Auditor"])
st.sidebar.markdown("---")
st.sidebar.caption("Built to mirror the notebook's two analyses. "
                   "Model = logistic regression, 80% held-out accuracy.")

if page == "Battle Outcome Predictor":
    st.header("Battle Outcome Predictor")
    st.write("Set up a battle. The model predicts who wins and how confident it is. "
             "The flat troop-count rule is shown for comparison.")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Attacker")
        att = {col: st.number_input(f"{col.replace('att_','')}", 0, 50, 5, key="a_"+col)
               for col in M["ATT"]}
        att_gen = st.slider("general rating", 1, 5, 3, key="ag")
        att_mor = st.slider("avg morale", 0, 100, 55, key="am")
        att_fat = st.slider("fatigue", 0, 100, 10, key="af")
    with c2:
        st.subheader("Defender")
        deff = {col: st.number_input(f"{col.replace('def_','')}", 0, 50, 5, key="d_"+col)
                for col in M["DEF"]}
        def_gen = st.slider("general rating", 1, 5, 2, key="dg")
        def_mor = st.slider("avg morale", 0, 100, 60, key="dm")
        fortified = st.checkbox("defender fortified", key="dfort")

    terrain = st.selectbox("terrain", M["terrain_cats"])
    weather = st.selectbox("weather", M["weather_cats"])

    # build feature row
    row = {c: 0.0 for c in M["FEATURE_COLS"]}
    for c in M["ATT"]: row[c] = att[c]
    for c in M["DEF"]: row[c] = deff[c]
    att_total = sum(att.values()); def_total = sum(deff.values())
    row["att_total"] = att_total
    row["def_total"] = def_total
    row["total_ratio"] = att_total / (def_total + 1e-9)
    row["total_diff"] = att_total - def_total
    row["gen_diff"] = att_gen - def_gen
    row["morale_diff"] = att_mor - def_mor
    row["fatigue"] = att_fat / 100.0
    row["fortified"] = int(fortified)
    row["att_spear_def_cav"] = att["att_spearmen"] * (deff["def_light_cavalry"] + deff["def_shock_cavalry"])
    row["att_cav_def_archer"] = (att["att_light_cavalry"] + att["att_shock_cavalry"]) * deff["def_archers"]
    row["terrain_" + terrain] = 1.0
    row["weather_" + weather] = 1.0

    X = pd.DataFrame([row])[M["FEATURE_COLS"]]
    p_att = M["model"].predict_proba(M["scaler"].transform(X))[0][1]
    p_def = 1 - p_att
    model_call = "attacker" if p_att >= 0.5 else "defender"
    conf = max(p_att, p_def)
    flat_call = "attacker" if att_total > def_total else "defender"

    colA, colB, colC = st.columns(3)
    colA.metric("Model says", f"{model_call}", f"{max(p_att,p_def)*100:.0f}% confident")
    colB.metric("Attacker win prob", f"{p_att*100:.0f}%")
    colC.metric("Flat troop rule", flat_call)

    # win-probability bar chart (toss-up line in the middle)
    fig = go.Figure(go.Bar(
        x=["Attacker", "Defender"],
        y=[p_att*100, p_def*100],
        marker_color=["#3ad6e0", "#e0524a"],
        text=[f"{p_att*100:.0f}%", f"{p_def*100:.0f}%"],
        textposition="outside"))
    fig.add_hline(y=50, line_color="#888888", line_dash="dash",
                  annotation_text="toss-up (50%)", annotation_font_color="#888888")
    fig.update_layout(paper_bgcolor="#0a0a0a", plot_bgcolor="#0a0a0a",
                      font_color="#e8e8e8", height=320, yaxis_range=[0, 100],
                      yaxis_title="Win probability (%)", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    if conf >= 0.75:
        st.success(f"Confident ({conf*100:.0f}%): game can auto-resolve this one.")
    else:
        st.warning(f"Close call ({conf*100:.0f}%): hand this one back to the player.")

elif page == "Unit Role Auditor":
    st.header("Unit Role Auditor")
    st.write(f"Clustering unit descriptions (TF-IDF + KMeans, 6 groups) vs the 6 advertised "
             f"marketing labels. Overall agreement: **{M['agreement']*100:.1f}%**.")

    ct = M["ct"].copy()
    ct.index = [f"Group {i}" for i in ct.index]
    fig = px.imshow(ct.values,
                    labels=dict(x="Advertised role", y="Computer group", color="count"),
                    x=list(ct.columns), y=list(ct.index),
                    color_continuous_scale="Teal")
    fig.update_layout(paper_bgcolor="#0a0a0a", plot_bgcolor="#0a0a0a", font_color="#e8e8e8", height=360)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Try a description")
    desc = st.text_area("Paste or type a unit description:",
                        "Commanders value them for drive deep and devastating impact. "
                        "On the field they rely on shatter the formation and overrun.")
    if st.button("Cluster it"):
        v = M["vec"].transform([desc])
        cl = int(M["km"].predict(v)[0])
        role = M["dominant"].get(cl, "?")
        pur = M["purity"].get(cl, 0)
        st.write(f"Assigned to **Group {cl}** → mostly **{role}** (purity {pur:.0%})")

    st.subheader("Per-group purity")
    purity_df = pd.DataFrame({"group":[f"Group {i}" for i in M["purity"].index],
                              "dominant_role":M["dominant"].values,
                              "purity":M["purity"].values})
    st.dataframe(purity_df, use_container_width=True)
