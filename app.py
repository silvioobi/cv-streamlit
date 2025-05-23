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

        # Werte extrahieren
        werte = kenntnisse_filtered["quantitative Beurteilung"].tolist()
        labels = kenntnisse_filtered["Kenntnis"].tolist()

        # Ersten Punkt am Ende duplizieren
        werte.append(werte[0])
        labels.append(labels[0])

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=werte,
            theta=labels,
            fill='toself',
            name='Skill-Level',
            line=dict(color="#708238", width=3),  # Olivgrün
            marker=dict(size=6)
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5], showgrid=True, gridcolor="lightgrey",
                                tickfont=dict(size=12)),
                angularaxis=dict(tickfont=dict(size=12))
            ),
            showlegend=False,
            paper_bgcolor='#f0f2f6',  # match sidebar
            plot_bgcolor='#f0f2f6',
            font=dict(color='black'),
            height=450
        )

        st.plotly_chart(fig, use_container_width=True)

    except FileNotFoundError:
        st.error("Datei 'Kenntnisse.xlsx' nicht gefunden.")

        st.plotly_chart(fig, use_container_width=True)
    except FileNotFoundError:
        st.error(f"Datei 'Kenntnisse.xlsx' nicht gefunden.")

    st.subheader("Datenanalysen & Berichte")

    for titel, link in analysen_links.items():
        st.markdown(f"- [{titel}]({link})")


st.subheader("Beruflicher Werdegang und Aus-/Weiterbildungen")

category_order = cv_data["Kategorie"].dropna().unique().tolist()

group_lines = []
current_y = 0
for cat in category_order:
    count = cv_data[cv_data["Kategorie"] == cat].shape[0]
    current_y += count
    group_lines.append(current_y - 0.5)  # Y-Position für horizontale Linie

fig = px.timeline(
    cv_data,
    x_start="Start",
    x_end="Finish",
    y="Bezeichnung",
    color="Kategorie",
    #color_discrete_sequence=px.colors.qualitative.Set2,
    color_discrete_sequence=[
            "#708238",  # Olive
            "#8A9A5B",  # Graugrün
            "#A3C1AD",  # Helloliv
            "#B6C96D",  # Soft Green
            "#CDE5A7",  # Pastellgrün
            "#556B2F"   # Dunkeloliv
        ],
    hover_data=["Institution"]
)

fig.update_yaxes(autorange="reversed", title=None)
fig.update_layout(
    autosize=True,
    font=dict(color="black", size=14),
    margin=dict(t=30, b=30, l=20, r=150),
    legend_title_text="",
    legend=dict(
        orientation="h",  # horizontal
        yanchor="bottom",
        y=1.1,  # etwas oberhalb des Plots
        xanchor="center",
        x=0.5
    ))

fig.update_xaxes(
    tickfont=dict(color="black"),
    title_font=dict(color="black")
)
fig.update_yaxes(
    tickfont=dict(color="black"),
    title_font=dict(color="black")
)


for y_pos in group_lines[:-1]:  # letzte Linie nicht nötig
    fig.add_shape(
        type="line",
        x0=-1,
        x1=1,
        y0=y_pos,
        y1=y_pos,
        xref='paper',
        yref='y',
        line=dict(color="lightgrey", width=1, dash="dot")
    )

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

