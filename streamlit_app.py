import pandas as pd
import streamlit as st
import os
import streamlit_authenticator as stauth

def add_new_game(df1, df2):
    mode = st.selectbox("Choose a game mode:", ["", "2 vs 2", "1 vs 1"])
    players = ["Jordina", "Lorenzo", "Iker", "Roman", "Berta", "Aina"]

    if mode == "2 vs 2":
        st.markdown("<h2 style='text-align: center;'>2 vs 2 Match</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center;'>🔵🔴   Team 1   🔵🔴</h3>", unsafe_allow_html=True)
            team1 = st.multiselect("Members:", players, max_selections=2, key="team1")
            if len(team1) < 2:
                st.warning("Select exactly 2 players for Team 1.")
            score_team1 = st.number_input(f"Goals:", min_value=0, step=1, key="score1")

        with col2:
            st.markdown("<h3 style='text-align: center;'>⚪⚪   Team 2   ⚪⚪</h3>", unsafe_allow_html=True)
            available_players_2 = [p for p in players if p not in team1]  
            team2 = st.multiselect("Members:", available_players_2, max_selections=2, key="team2")
            if len(team2) < 2:
                st.warning("Select exactly 2 players for Team 2.")
            score_team2 = st.number_input(f"Goals:", min_value=0, step=1, key="score2")
        
        date = st.date_input("Date of the match")

        if st.button("Record game"):
            if len(team1) == 2 and len(team2) == 2: 
                new_game = pd.DataFrame({
                    "Team 1": f'{team1[0]} & {team1[1]}',
                    "Team 2": f'{team2[0]} & {team2[1]}',
                    "Score": f'{score_team1} - {score_team2}',
                    "Date": [date]
                })
                df = pd.concat([df2, new_game], ignore_index=True)

                df.to_csv(csv_file_2, index=False)
                st.success("Match recorded correctly")
            else:
                st.error("Please, fill all the fields.")


    if mode == "1 vs 1":
        st.markdown("<h2 style='text-align: center;'>1 vs 1 Match</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center;'>🔵🔴   Team 1   🔵🔴</h3>", unsafe_allow_html=True)
            team1 = st.selectbox("Members:", players)
            score_team1 = st.number_input(f"Goals:", min_value=0, step=1, key="score1")

        with col2:
            st.markdown("<h3 style='text-align: center;'>⚪⚪   Team 2   ⚪⚪</h3>", unsafe_allow_html=True)
            available_players_2 = [p for p in players if p not in team1]  
            team2 = st.selectbox("Members:", available_players_2)
            if len(team2) < 2:
                st.warning("Select exactly 2 players for Team 2.")
            score_team2 = st.number_input(f"Goals:", min_value=0, step=1, key="score2")

        date = st.date_input("Date of the match")

        if st.button("Record game"):
            new_game = pd.DataFrame({
                    "Team 1": [team1],
                    "Team 2": [team2],
                    "Score": f'{score_team1} - {score_team2}',
                    "Date": [date]
            })
            df = pd.concat([df1, new_game], ignore_index=True)

            df.to_csv(csv_file_1, index=False)
            st.success("Match recorded correctly")
        

def show_stars(num):
    return "⭐" * num + "☆" * (5 - num)

st.set_page_config(page_title="Futbolín League Hub", layout="wide", page_icon="⚽")
st.markdown(
    "<h1 style='text-align: center;'>Futbolín League Hub ⚽🏆 \n\n AI Lab Barcelona - HP</h1>",
    unsafe_allow_html=True
)
st.write(
    """
    Track all the thrilling matches, results and rankings from the AI Lab’s Futbolín league at HP Barcelona. 
    
    Celebrate your victories, analyze your stats and see who’s dominating the table in this ultimate fusion of fun, competition and teamwork! 
    
    Let the game begin! 🎉
    """
)

tabs = st.tabs(["Overview", "Record new game", "Statistics"])
csv_file_1 = "futbolin_results_1.csv"
csv_file_2 = "futbolin_results_2.csv"
df1 = pd.read_csv(csv_file_1)
df2 = pd.read_csv(csv_file_2)
with tabs[0]:
    members = [
        {"nombre": "Jordina", "imagen": "./users/user.png", "puntuacion": 4},
        {"nombre": "Lorenzo", "imagen": "./users/user.png", "puntuacion": 4},
        {"nombre": "Iker", "imagen": "./users/user.png", "puntuacion": 4},
        {"nombre": "Roman", "imagen": "./users/user.png", "puntuacion": 2},        
        {"nombre": "Berta", "imagen": "./users/user.png", "puntuacion": 3},
        {"nombre": "Aina", "imagen": "./users/user.png", "puntuacion": 2}
    ]

    cols = st.columns(3) 

    for i, persona in enumerate(members):
        cols_index = i%3
        with cols[cols_index]: 
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.image(persona["imagen"], width=150)
            st.write(f"**{persona['nombre']}**")
            st.write(show_stars(persona["puntuacion"]))
            st.markdown("</div>", unsafe_allow_html=True)


    st.header("Upcoming matches")
    st.write("Stay tuned for the next monthly league—it kicks off on March 3rd!")

    st.header("Past matches")
    st.subheader("2 vs 2 Matches")
    if not os.path.exists(csv_file_2):
        df2 = pd.DataFrame(columns=["Team 1", "Team 2", "Score", "Date"])
        df2.to_csv(csv_file_2, index=False)
    st.dataframe(df2)

    st.subheader("1 vs 1 Matches")
    if not os.path.exists(csv_file_1):
        df1 = pd.DataFrame(columns=["Team 1", "Team 2", "Score", "Date"])
        df1.to_csv(csv_file_1, index=False)
    st.dataframe(df1)

with tabs[1]:
    add_new_game(df1, df2)

with tabs[2]:
    st.write("Coming soon...")
