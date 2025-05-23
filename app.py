import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import st_folium
import folium


st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    html, body, [class*="css"] {
        background-color: white;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 16px;
    }
    h1, h2, h3, h4 {
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

# Load CV data
cv_file = "CV.xlsx"
cv_data = pd.read_excel(cv_file)
cv_data.rename(columns={"Bezeichnung": "Bezeichnung", "Start": "Start", "Ende": "Finish", "Kategorie": "Kategorie"}, inplace=True)

def format_description(text):
    if pd.isna(text):
        return ""
    return text.replace(" •", "\n•").strip()

cv_data["Formatted Beschreibung"] = cv_data["Beschreibung"].apply(format_description)
position_descriptions = {
    row["Bezeichnung"]: (row["Institution"], row["Formatted Beschreibung"]) for _, row in cv_data.iterrows()
}


analysen_links = {
    "Analyse Laufzeiten vom Auffahrtslauf 2024": "https://www.linkedin.com/pulse/analyse-der-marathon-und-halbmarathon-daten-vom-silvio-oberholzer-euaef/?trackingId=NGnqJvFgQlKk97wAqfZh1w%3D%3D",
    "Power BI Bericht - Passantenfrequenz Stadt St.Gallen": "https://dalix.ch/passantenfrequenz-in-der-st-galler-innenstadt/",
    "Power BI Bericht - Entwicklung Bevölkerung Stadt St.Gallen": "https://dalix.ch/entwicklung-der-bevoelkerung-der-stadt-st-gallen/",
    "Power BI Bericht - Axa Women's Super League": "https://dalix.ch/die-axa-womens-super-league-verabschiedet-sich-in-die-winterpause/",
}

# Load social media
linkedin_url = ""
try:
    social_df = pd.read_excel("Social Media.xlsx")
    linkedin_row = social_df[social_df["Social Media"].str.lower() == "linkedin"]
    if not linkedin_row.empty:
        linkedin_url = linkedin_row.iloc[0]["URL"]
except:
    st.warning("Social Media Datei konnte nicht geladen werden oder fehlt.")

certificates = [
    "Hermes 5.1 Advanced",
    "Certified Project Management Associate IPMA Level D"]

st.title("Lebenslauf Silvio Oberholzer")

with st.sidebar:
    st.subheader("Persönliche Angaben")
    st.markdown("**Silvio Oberholzer**")

    try:
        st.image("images/profilbild.jpg", width=200)
    except:
        st.warning("Bild nicht gefunden. Stelle sicher, dass 'profilbild.jpg' im Projektordner liegt.")

    st.markdown("✉️ silvio_oberholzer@hotmail.com")
    st.markdown("📞 +41 78 917 19 94")
    st.markdown("🎂 6. März 1994")
    st.markdown("📍 Alpsteinstrasse 9, 9050 Appenzell")

    hobbies = ["🎾 Tennis", "🏓 Padel", "🎯 Darts", "🥾 Wandern", "🏃‍♂️ Joggen", "🍳 Kochen"]
    st.markdown("**Hobbies:**<br>" + "<br>".join(hobbies), unsafe_allow_html=True)
    st.markdown(f"[LinkedIn Profil]({linkedin_url})")

    st.subheader("Kenntnisse")
    try:
        kenntnisse_df = pd.read_excel("Kenntnisse.xlsx")
        kenntnisse_filtered = kenntnisse_df.dropna(subset=["quantitative Beurteilung"])

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=kenntnisse_filtered["quantitative Beurteilung"].tolist(),
            theta=kenntnisse_filtered["Kenntnis"].tolist(),
            fill='toself',
            name='Skill-Level'
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",  # transparenter Hintergrund
            plot_bgcolor="rgba(0,0,0,0)",
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True,
                    range=[0, 5],
                    showline=True,
                    linewidth=1,
                    gridcolor="lightgray",
                    linecolor="lightgray",
                    tickfont=dict(color="white", size=12)
                ),
                angularaxis=dict(
                    tickfont=dict(size=13, color="white"),
                    rotation=90,
                    direction="clockwise"
                )
            ),
            font=dict(color="white"),
            showlegend=False,
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)
    except FileNotFoundError:
        st.error(f"Datei 'Kenntnisse.xlsx' nicht gefunden.")

    st.subheader("Datenanalysen & Berichte")

    for titel, link in analysen_links.items():
        st.markdown(f"- [{titel}]({link})")

    st.subheader("Zertifikate")
    for cert in certificates:
        st.markdown(f"- {cert}")


st.subheader("Beruflicher Werdegang und Aus-/Weiterbildungen")

# Gantt-Diagramm mit angepasster Legende
fig = px.timeline(
    cv_data,
    x_start="Start",
    x_end="Finish",
    y="Bezeichnung",
    color="Kategorie",
    color_discrete_sequence=px.colors.qualitative.Set2,
    hover_data=["Institution"]
)

fig.update_yaxes(autorange="reversed", title=None)
fig.update_layout(
    autosize=True,
    font=dict(size=14),
    margin=dict(t=30, b=30, l=20, r=150),
    legend_title_text="",
    legend=dict(
        orientation="h",  # horizontal
        yanchor="bottom",
        y=1.1,  # etwas oberhalb des Plots
        xanchor="center",
        x=0.5
    ))

st.plotly_chart(fig, use_container_width=True)

# Reihenfolge wie im Gantt
type_order = cv_data["Kategorie"].dropna().unique().tolist()

for group in type_order:
    group_data = cv_data[cv_data["Kategorie"] == group].sort_values(by="Start", ascending=False)
    st.markdown(f"### Details {group}")

    for _, row in group_data.iterrows():
        title = f"**{row['Bezeichnung']}** ({row['Start'].date()} – {row['Finish'].date()})"
        st.markdown(title)

        bilddatei = row.get("Bild", "")
        bild_url = f"images/{bilddatei}" if pd.notna(bilddatei) else None

        cols = st.columns([1, 4])

        with cols[0]:
            if bild_url and str(bild_url).lower().endswith((".png", ".jpg", ".jpeg")):
                try:
                    st.image(bild_url, width=150)
                except Exception as e:
                    st.warning(f"Bild konnte nicht geladen werden: {bild_url}")

        with cols[1]:
            st.markdown(f"**Institution:** {row['Institution']}<br>", unsafe_allow_html=True)
            st.markdown(
                f"**Beschreibung:**<br><div style='white-space: pre-wrap'>{row['Formatted Beschreibung']}</div>",
                unsafe_allow_html=True
            )

        st.markdown("---")  # Trennlinie zwischen Stationen

