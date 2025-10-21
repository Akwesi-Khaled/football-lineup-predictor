
import streamlit as st
import plotly.graph_objects as go

def show_fixture_table(df):
    if df is None or df.empty:
        st.write('No fixtures found')
        return
    cols = ['fixture.id','fixture.date','teams.home.name','teams.away.name','league.name']
    available = [c for c in cols if c in df.columns]
    st.dataframe(df[available].sort_values('fixture.date'))

def show_prob_metrics(p):
    st.metric('Home win', f"{p['p_home']*100:.1f}%")
    st.metric('Draw', f"{p['p_draw']*100:.1f}%")
    st.metric('Away win', f"{p['p_away']*100:.1f}%")
    fig = go.Figure(data=[go.Bar(x=['Home','Draw','Away'], y=[p['p_home'], p['p_draw'], p['p_away']])])
    st.plotly_chart(fig, use_container_width=True)
