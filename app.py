import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors as mpc
import streamlit as st
plt.style.use("https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle")
st.set_page_config(layout='wide')


@st.cache_data
def load_data(model_name):
    return pd.read_csv(model_name)

df = load_data("matches.csv")
dff = load_data("deliveries.csv")

print(df.head())
st.markdown("<h1 style='text-align:center;margin-bottom:30px'>IPL Data Analysis 2008 - 2019</h1>",unsafe_allow_html=True)

df['date'] = np.where(df['date'].str.contains('/'), pd.to_datetime(df['date']), pd.to_datetime(df['date'], dayfirst=True))

col1,col2,col23= st.columns(3)
with col1:
    st.subheader("IPL trophies Won by teams")
with col2:
    st.markdown("#### Mumbai Indians team won 4 IPL trophies which is highest of all time, following Chennai Super Kings 3 times and Kolkata Knight Riders 2 times")

with col23:
    @st.cache_data
    def winner_wise_year():
        winners = {}
        for year in range(2008,2020):
            if year==2019:
                continue
            else:
                lst = list(df.loc[df['season']==year].tail(1)['winner'])[0]
                if lst in winners.keys():
                    winners[lst] += 1
                else:
                    winners[lst] = 1
        winners[df.loc[df['season']==2019].loc[df['date'].idxmax()]['winner']] += 1
        dict = {
            'team':list(winners.keys()),
            'No of IPL trophies':list(winners.values())
        }
        champions = pd.DataFrame(dict)
        champions.sort_values(by='No of IPL trophies',inplace=True)
        fig = plt.figure()
        win_plot = plt.bar(champions['team'],champions['No of IPL trophies'],ec='darkblue')
        plt.bar_label(win_plot,labels=list(winners.values()).sort(),label_type='edge')
        plt.xticks(champions['team'],rotation='vertical')
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=10)
        st.pyplot(fig)
        return champions.set_index('team')
    champs = winner_wise_year() 
    with col1:
        # champs = champions.set_index('team')
        champs.index.name = 'team'
        st.write(champs)

st.write('---')


col3,col4,col43 = st.columns([1.5,1,1])

with col4:
    st.write("<h3>There are total 752 IPL matches played from 2008 to 2019</h3> ",unsafe_allow_html=True)
    st.write("<h3>We can See that in 2011,2012 and 2013 there are more matches have been played because there were total 10 teams on the other hand in other seasons there are only 8 teams registered</h3> ",unsafe_allow_html=True)
with col43:
    st.subheader("Total Number of Matches played in each season")
with col3:
    @st.cache_data
    def per_season_matches():
        matches_per_season = df.groupby('season')['id'].count()
        matches_per_season = pd.DataFrame(matches_per_season)
        matches_per_season.reset_index(inplace=True)
        fig = plt.figure()
        matches_plot = plt.barh(matches_per_season['season'],matches_per_season['id'],ec='darkblue')
        plt.bar_label(matches_plot,labels=matches_per_season['id'],label_type='edge')
        plt.title('Total Matches per Season')
        st.pyplot(fig)
        return matches_per_season
    tab = per_season_matches()
    with col43:
        st.table(tab)

st.write('---')
col5,col6 = st.columns(2)
with col5:
    st.subheader("Toss Decisions made by teams in between 2008 and 2019")
with col6:
    @st.cache_data
    def toss_decisions():
        # matches_per_season = df.groupby('season').id.count()
        toss_decision_percentage = df.groupby('season').toss_decision.value_counts()
        season = [i for i in range(2008,2020)]
        # for i in range(2008,2020):
        #     season.append(i)
        field = []
        bat = []
        for i in list(toss_decision_percentage.index):
            if i[1] == 'bat':
                bat.append(toss_decision_percentage[i])
            else :
                field.append(toss_decision_percentage[i])
                
        print(season)
        print(bat)
        print(field)
        fig = plt.figure()
        bat_plot = plt.bar(np.array(season)-0.2,bat,width=0.40,label='batting',ec='darkblue')
        bowl_plot = plt.bar(np.array(season)+0.2,field,width=0.40,label='fielding',ec='red')
        plt.legend()
        plt.show()
        st.pyplot(fig)
        return pd.DataFrame({
                'season':season,
                "batting":bat,
                "fielding":field
            })
    dd = toss_decisions()
    with col5:
        col12,col13 = st.columns(2)
        with col12:
            st.table(dd)
        
        with col13:
            st.markdown(">### We can Clearly See that since last 6 years All the teams prefer to bowl first")


st.write('---')

col9,col10 = st.columns(2)

with col9:
    @st.cache_data
    def win_by_toss():
        won_by_toss = df[['season','team1','team2','toss_winner','winner']]
        toss_winner = won_by_toss.loc[df['toss_winner'] == df['winner']]
        toss_wins = toss_winner.groupby('season').count()['winner']
        toss_lose = won_by_toss[df['toss_winner']!=df['winner']]
        toss_loss = toss_lose.groupby('season').count()['winner']
        seasons = [x for x in range(2008,2020)]
        won_by_toss = toss_wins.tolist()
        won_by_defend = toss_loss.tolist()
        fig = plt.figure()
        plt.bar(np.array(seasons)-0.2,won_by_toss,width=0.40,label='Matches won after winning toss')
        plt.bar(np.array(seasons)+0.2,won_by_defend,width=0.40,label='Matches won after losing toss')
        plt.legend()
        plt.show()
        st.pyplot(fig)
    win_by_toss()
with col10:
    @st.cache_data
    def data_win_by_toss():
        won_by_toss = df[['season','team1','team2','toss_winner','winner']]
        toss_winner = won_by_toss.loc[df['toss_winner'] == df['winner']]
        toss_wins = toss_winner.groupby('season').count()['winner']
        toss_lose = won_by_toss[df['toss_winner']!=df['winner']]
        toss_loss = toss_lose.groupby('season').count()['winner']
        seasons = [x for x in range(2008,2020)]
        won_by_toss = toss_wins.tolist()
        won_by_defend = toss_loss.tolist()
        st.subheader("Matches Won after Winning the Toss")
        st.markdown("### Some Observations we can do from the visualizations: ")
        st.write(">There are many few seasons like 2008,2012,2013,2015 in which There are more teams who won matches after losing toss")
        st.write(">There is only one year 2014 in which 60 matches were played from that exact 30 matches won by winning toss")
        st.write(">from 2008 to 2019 total {} matches have been played in IPL out of which {} matches are won after winning the toss and {} matches are won after losing the toss".format(np.array(won_by_toss).sum()+np.array(won_by_defend).sum(),np.array(won_by_toss).sum(),np.array(won_by_defend).sum()))
        st.write(">The winning percentage of team which won the toss is 52.26% and the winning percentage of the team who lose the toss is 47.73%")
    data_win_by_toss()




st.write('---')

st.write(" <h2 style='text-align:center;' >Matches Won By Each Team in Each Season</h2> ",unsafe_allow_html=True)

col7,col8,col37 = st.columns(3)

with col7:
    @st.cache_data
    def per_year_winnings(year_select):
        year_1 = df.loc[df['season']==year_select]
        year_winners = year_1.groupby(by='winner')['id'].count()
        year_winners.rename('Number of Winnings',inplace=True)
        year_winners.sort_values(inplace=True)
        fig = plt.figure()
        teams = list(year_winners.index)
        plt.title("Matches won by each team per year")
        plt.xlabel("number of wins")
        plt.ylabel("Teams")
        plt.barh(teams,width=list(year_winners.values))
        st.pyplot(fig)
        return teams[len(teams)-1]
    # def per_year_winnings(year_select):
    year_select = st.slider('Select Year',min_value=2008,max_value=2019,value=2008,key='year_value')
    print(year_select)
    high_team = per_year_winnings(year_select)
    st.write(high_team)
    @st.cache_data
    def runNwickets(year,team):
        win_per_year = df[df['season']==year]
        win_per_year = win_per_year[win_per_year['winner']==team]
        win_by_runs = win_per_year[win_per_year['win_by_runs']>0]
        win_by_runs = win_by_runs.sort_values(by='win_by_runs',ascending=False)
        win_by_runs = win_by_runs[['team1','team2','win_by_runs']]
        win_by_wickets = win_per_year[win_per_year['win_by_wickets']>0]
        win_by_wickets = win_by_wickets.sort_values(by='win_by_wickets',ascending=False)
        win_by_wickets = win_by_wickets[['team1','team2','win_by_wickets']]
        l1 = 5
        l2=5
        l1 = min(l1,len(win_by_wickets))
        l2 = min(l2,len(win_by_runs))
        win_by_wickets = win_by_wickets.head(l1)
        win_by_runs = win_by_runs.head(l2)
        return win_by_runs,win_by_wickets

with col8:
    winRuns,winWickets = runNwickets(year_select,high_team)
    st.subheader("Top Matches in Which {} won by runs".format(high_team))
    st.table(winRuns)
with col37:
    st.subheader("Top Matches in Which {} won by wickets".format(high_team))
    st.table(winWickets)


    

st.write("---")

st.markdown("<h1 style='text-align:center;'>Detailed Analysis of Any One Match</h1>",unsafe_allow_html=True)
col11,col12,col13 = st.columns([1,1,2])


with col11:
    year_slider = st.slider("Select year",min_value=2008,max_value=2019)

    @st.cache_data
    def select_team1(year_slider):
        return df.loc[df['season']==year_slider]['team1'].unique().tolist()
    team1_list = select_team1(year_slider)
    team1 = st.selectbox("Select Team1",options=team1_list)

    @st.cache_data
    def select_team2(year_slider,team1):
        opposition = df.loc[(df['season']==year_slider) & ((df['team1']==team1) | (df['team2']==team1))]
        opposition_list = set({})
        for team in opposition['team1']:
            if team!=team1:
                opposition_list.add(team)
        for team in opposition['team2']:
            if team!=team1:
                opposition_list.add(team)
        return list(opposition_list)
    
    team2_list = select_team2(year_slider,team1)
    team2 = st.selectbox("Select Team2",options=team2_list)

    @st.cache_data
    def select_date(year_slider,team1,team2):
        opposition = df.loc[(df['season']==year_slider) & ((df['team1']==team1) | (df['team2']==team1))]
        date_list = opposition.loc[(opposition['team1']==team2) | (opposition['team2']==team2)]
        date_lst = []
        for dt in date_list['date']:
            date_lst.append(str(dt))
        return date_lst
    date_list = select_date(year_slider,team1,team2)
    print(date_list)
    # if len(date_list)>0:
    match = st.selectbox("Select Date",options=date_list)
    print(year_slider)
    print(team1)
    print(team2)
    print(match)
    with col12:
        mid = df[((df['date']==match) & (((df['team1']==team1) & (df['team2']==team2)) | ((df['team1']==team2) & (df['team2']==team1))))]
        match1 = dff[dff['match_id']==mid['id'].tolist()[0]]
        st.subheader("General Analysis about this match")
        st.write(">This Particular Match was Played at {} in {}".format(mid['city'].tolist()[0],mid['venue'].tolist()[0]))
        if(mid['toss_decision'].tolist()[0] == 'bat'):
            st.write(">{} won the toss and chose to bat first".format(mid['toss_winner'].tolist()[0]))
        else:
            st.write(">{} won the toss and chose to bowl first".format(mid['toss_winner'].tolist()[0]))

        if (mid['win_by_runs'].tolist()[0])>0:
            st.write(">{} won this match by {} runs".format(mid['winner'].tolist()[0],mid['win_by_runs'].tolist()[0]))
            # st.write(">")
        else:
            st.write(">{} won this match by {} wickets".format(mid['winner'].tolist()[0],mid['win_by_wickets'].tolist()[0]))
        st.write(">{} is the Man of the Match for this match".format(mid['player_of_match'].tolist()[0]))
    with col13:
        match1 = dff[dff['match_id']==mid['id'].tolist()[0]]
        in1 =  match1[match1['inning']==1]
        in2 = match1[match1['inning']==2]
        run_by_team1 = in1.groupby('over').sum()['total_runs'].cumsum().values.tolist()
        run_by_team2 = in2.groupby('over').sum()['total_runs'].cumsum().values.tolist()
        fig =plt.figure()
        plt.plot(list(range(1,len(run_by_team1)+1)),run_by_team1,label="{}".format(in1['batting_team'].unique().tolist()[0]))
        plt.plot(list(range(1,len(run_by_team2)+1)),run_by_team2,label="{}".format(in2['batting_team'].unique().tolist()[0]))
        plt.title("Run Chase between the teams")
        plt.xlabel("Overs")
        plt.ylabel("Run after each over")
        plt.legend()
        mpc.cursor(hover=True)
        st.pyplot(fig)


st.markdown("<h1 style='text-align:center;'>Detailed Scoreboard</h1>",unsafe_allow_html=True)

col14,col15 = st.columns(2)
with col14:
    team_in1 = match1[match1['inning']==1]
    team1_bowling = team_in1.groupby('bowler').agg({'total_runs':'sum','player_dismissed':'count'})
    team1_bowling.columns = ['runs given','wickets taken']
    team1_batting = team_in1.groupby('batsman').agg({'ball':'count','total_runs':'sum'})
    if mid['season'].tolist()[0]==2019:
        team1_batting = team_in1.groupby('batsman').agg({'ball':'count','batsman_runs':'sum'})
    team1_total = team_in1.groupby("over").sum()['total_runs']
    if mid['season'].tolist()[0]==2019:
        team1_total = team_in1.groupby("over").sum()['batsman_runs']
    team1_total.sum()
    team1_wickets = team_in1.groupby("over").count().sum()['player_dismissed']
    # team1_wickets
    st.markdown("<h3 style='text-align:center'>{}</h3>".format(team_in1['batting_team'].unique().tolist()[0]),unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center'>Total Scored: {}/{}</h3>".format(team1_total.sum(),team1_wickets),unsafe_allow_html=True)

    col22,col23 = st.columns(2)
    with col22:
        st.markdown("### Batting Score")
        st.write(team1_batting)
    with col23:
        st.write("### Bowling")
        st.write(team1_bowling)



with col15:
    team_in2 = match1[match1['inning']==2]
    team2_bowling = team_in2.groupby('bowler').agg({'total_runs':'sum','player_dismissed':'count'})
    team2_bowling.columns = ['runs given','wickets taken']
    team2_batting = team_in2.groupby('batsman').agg({'ball':'count','total_runs':'sum'})
    if mid['season'].tolist()[0]==2019:
        team2_batting = team_in2.groupby('batsman').agg({'ball':'count','batsman_runs':'sum'})
    team2_total = team_in2.groupby("over").sum()['total_runs']
    if mid['season'].tolist()[0]==2019:
        team2_total = team_in2.groupby("over").sum()['batsman_runs']
    team2_wickets = team_in2.groupby("over").count().sum()['player_dismissed']
    st.markdown("<h3 style='text-align:center'>{}</h3>".format(team_in2['batting_team'].unique().tolist()[0]),unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center'>Total Scored: {}/{}</h3>".format(team2_total.sum(),team2_wickets),unsafe_allow_html=True)
    col22,col23 = st.columns(2)
    with col22:
        st.markdown("### Batting Score")
        st.write(team2_batting)
    with col23:
        st.write("### Bowling")
        st.write(team2_bowling)


st.write("---")

col31,col32,col33 = st.columns(3)
with col31:
    @st.cache_data
    def top_hitters(year):
        year_wise_bowler = df[df['season']==year]['id'].tolist()
        top_bowlers = dff[dff['match_id'].isin(year_wise_bowler)].groupby('batsman').sum().sort_values(by='batsman_runs',ascending=False)['batsman_runs']
        top_batters = top_bowlers.head(15)
        batters = top_batters.index.tolist()
        runs_by_batters= top_batters.values.tolist()
        # plt.barh()
        dct = {
            'batsman':batters,
            'runs':runs_by_batters
        }
        DF = pd.DataFrame(dct).sort_values(by='runs')
        fig = plt.figure()
        plt.barh('batsman','runs',data=DF)
        st.pyplot(fig)
        return batters[0],runs_by_batters[0],year
    
    slt_year = st.slider("Season",min_value=2008,max_value=2019,value=2008,key='key13')
    x,y,z = top_hitters(slt_year)


with col33:
    st.subheader("Some Of top Innings Played by {} in Season {}".format(x,z))
    year_wise_bowler = df[df['season']==z]['id'].tolist()
    year_wise_bowler = dff[dff['match_id'].isin(year_wise_bowler)]
    purple_cp = year_wise_bowler[year_wise_bowler['batsman']==x].groupby(['match_id','batting_team','bowling_team']).agg({'ball':'count','batsman_runs':'sum'}).reset_index()
    purple_cp.sort_values(by='batsman_runs',ascending=False,inplace=True)
    purple_cp = purple_cp[purple_cp['batsman_runs']>50]
    purple_cp.drop(['match_id'],axis=1,inplace=True)
    purple_cp.columns = ['Bowling Team','Batting Team','ball','Runs']
    st.table(purple_cp)
with col32:
    st.subheader("Analysis of Orange Cap in Season {}".format(z))
    ids = df[df['season']==slt_year]['id'].tolist()
    matches_id = dff[dff['match_id'].isin(ids)]
    sixes = matches_id[matches_id['batsman']==x].groupby(matches_id['batsman_runs']==6).count()['batsman_runs'][True]
    fours = matches_id[matches_id['batsman']==x].groupby(matches_id['batsman_runs']==4).count()['batsman_runs'][True]
    fifties = matches_id[matches_id['batsman']==x].groupby('match_id').sum().reset_index()
    team = matches_id[matches_id['batsman']==x]['batting_team'].unique().tolist()[0]
    fast_fifty = matches_id[matches_id['batsman']==x].groupby(['match_id','batting_team','bowling_team']).agg({'ball':'count','batsman_runs':'sum'})
    fast_fifty.reset_index(inplace=True)
    fast_fifty['diff'] = fast_fifty['batsman_runs'].sub(fast_fifty['ball'])
    fast_fifty.sort_values(by='diff',ascending=False,inplace=True)
    fast_fifty = fast_fifty[fast_fifty['batsman_runs']>=50]
    fast_fifty.drop(['diff'],axis=1,inplace=True)
    fast_fifty.drop(['match_id'],axis=1,inplace=True)
    st.write("> <h3>{}</h3> was the Orange Cap Holder in season {} ".format(x,z),unsafe_allow_html=True)
    st.write("> He was Played for <b>{}</b> in season {}".format(team,z),unsafe_allow_html=True)
    st.write("> {} scored <b>{}</b> runs in Season {}".format(x,y,z),unsafe_allow_html=True)
    st.write("> {} scored <b>{} 6's</b> and <b>{} 4's</b> in season {}".format(x,sixes,fours,z),unsafe_allow_html=True)
    st.write("> He also Scored <b>{}</b> Fifty and <b>{}</b> centuries in season {}".format(len(fifties[fifties['batsman_runs']>50]),len(fifties[fifties['batsman_runs']>99]),z),unsafe_allow_html=True)
    # st.table(fast_fifty)
    

st.write("---")

col34,col35,col36 = st.columns([1,1.5,1])
with col36:
    @st.cache_data
    def year_wise_bowlers(year):
        year_wise_bowler = df[df['season']==year]['id'].tolist()
        top_bowlers = dff[dff['match_id'].isin(year_wise_bowler)].groupby('bowler').count().sort_values(by='player_dismissed',ascending=False)['player_dismissed']
        top_bowlers = top_bowlers.head(15)
        bowlers = top_bowlers.index.tolist()
        wickets_by_bowlers= top_bowlers.values.tolist()
        # plt.barh()
        dct = {
            'bowlers':bowlers,
            'wickets':wickets_by_bowlers
        }
        DF = pd.DataFrame(dct).sort_values(by='wickets')
        fig = plt.figure()
        plt.barh('bowlers','wickets',data=DF)
        st.pyplot(fig)
        return bowlers[0],wickets_by_bowlers[0],year
    slt_year12 = st.slider("Season",min_value=2008,max_value=2019,value=2008,key='key3')
    bowler,wckts,seasn = year_wise_bowlers(slt_year12)

with col35:
    st.subheader("Some Of top Innings Played by {} in Season {}".format(bowler,seasn))
    year_wise_bowler = df[df['season']==seasn]['id'].tolist()
    year_wise_bowler = dff[dff['match_id'].isin(year_wise_bowler)]
    purple_cp = year_wise_bowler[year_wise_bowler['bowler']==bowler].groupby(['match_id','bowling_team','batting_team']).agg({'total_runs':'sum','player_dismissed':'count'}).reset_index()
    purple_cp.sort_values(by='player_dismissed',ascending=False,inplace=True)
    purple_cp = purple_cp[purple_cp['player_dismissed']>1]
    purple_cp.drop(['match_id'],axis=1,inplace=True)
    purple_cp.columns = ['Bowling Team','Batting Team','Runs given','Wickets Taken']
    st.table(purple_cp)


with col34:
    ids = df[df['season']==seasn]['id'].tolist()
    matches_id = dff[dff['match_id'].isin(ids)]
    team = matches_id[matches_id['bowler']==bowler]['bowling_team'].unique().tolist()[0]
    runs_given = year_wise_bowler.groupby(year_wise_bowler['bowler']==bowler).agg({'total_runs':'sum','player_dismissed':'count'})['total_runs'][True]
    st.subheader("Analysis of Purple Cap Holder in Season {}".format(seasn))
    st.write("> <h3>{}</h3> was the Purple Cap Holder in Season {}".format(bowler,seasn),unsafe_allow_html=True)
    st.write("> He Played for <b>{}</b> team in Season {}".format(team,seasn),unsafe_allow_html=True)
    st.write("> He took <b>{}</b> wickets by giving only {} runs for {} in Season {}".format(wckts,runs_given,team,seasn),unsafe_allow_html=True)


st.write('---')
st.markdown("# <div style='text-align:center;'>Conclusion</div>",unsafe_allow_html=True)

st.write("> I tried to analyze Datasets <a href='https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020?select=IPL+Matches+2008-2020.csv'>matches.csv</a> and  <a href='https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020?select=IPL+Matches+2008-2020.csv'>deliveries.csv</a> available on Kaggle",unsafe_allow_html=True)
