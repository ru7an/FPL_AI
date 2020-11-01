def new_data(player, playern1, playern2, playern3, playern4, playern5):
    import pandas as pd
    import numpy as np

    new_data = pd.read_csv('https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2020-21/gws/merged_gw.csv')
    data_team_no = pd.read_csv('teams20_21.csv')
    fixtures = pd.read_csv('fixtures.csv')
    
    new_data[['opp_goals_scored','opp_goals_conceded', 'opp_clean_sheets', 'opp_total_points']] = None
    features = features = ['ict_index', 'threat', 'creativity', 'was_home', 'opp_goals_scored','opp_goals_conceded', 'opp_clean_sheets', 'opp_total_points']
    target = ['total_points']

    if playern1 != '':
        playern1 = ' ' + str(playern1)

    if playern2 != '':
        playern2 = ' ' + str(playern2)

    if playern3 != '':
        playern3 = ' ' + str(playern3)

    if playern4 != '':
        playern4 = ' ' + str(playern4)

    if playern5 != '':
        playern5 = ' ' + str(playern5)

    player = str(player)+str(playern1)+str(playern2)+str(playern3)+str(playern4)+str(playern5)

    def player_name():
        pl_ds = pd.read_csv('player.csv')
        for i in pl_ds['surname_lower']:
            if i == player:
                player_name = pl_ds.loc[pl_ds['surname_lower']==player]
                name = player_name['player_name']
                return name.values[0]
        for i in pl_ds['surname']:
            if i == player:
                player_name = pl_ds.loc[pl_ds['surname']==player]
                name = player_name['player_name']
                return name.values[0]
        for i in pl_ds['firstname_lower']:
            if i == player:
                player_name = pl_ds.loc[pl_ds['firstname_lower']==player]
                name = player_name['player_name']
                return name.values[0]
        for i in pl_ds['firstname']:
            if i == player:
                player_name = pl_ds.loc[pl_ds['firstname']==player]
                name = player_name['player_name']
                return name.values[0]

        for i in pl_ds['player_name']:
            if i == player:
                player_name = pl_ds.loc[pl_ds['player_name']==player]
                name = player_name['player_name']
                return name.values[0]

    X_new = new_data.loc[new_data['name']==player_name()]
    X_new_data = X_new[features]    

    z0 = np.mean(X_new_data)
    z0_df = pd.DataFrame(z0).transpose()

    team_name = X_new['team'].unique()[-1]
    round0 = max(X_new['round'])+1
    opp_fix = fixtures.loc[fixtures['Round']==round0]
    opp_fix = opp_fix.reset_index(drop=True)
    for i in range(len(opp_fix)):
        if opp_fix['Team 1'][i]==team_name:
            was_home = True
            opponent = opp_fix['Team 2'][i]
            break
        elif opp_fix['Team 2'][i]==team_name:
            was_home = False
            opponent = opp_fix['Team 1'][i]
            break
        else:
            pass

    df_team = new_data.loc[new_data['team']==opponent]
    df = df_team[['goals_scored', 'goals_conceded', 'clean_sheets', 'total_points']]
    z = np.sum(df, axis=0)/max(df_team['GW'])
    z_df = pd.DataFrame(z).transpose()
    z0_df['was_home'] = was_home
    z0_df['opp_goals_scored'] = z_df['goals_scored']
    z0_df['opp_goals_conceded'] = z_df['goals_conceded']
    z0_df['opp_clean_sheets'] = z_df['clean_sheets']
    z0_df['opp_total_points'] = z_df['total_points']
    next_fix = z0_df
    
    player_name = player_name()
    return (next_fix, player_name, team_name, opponent)