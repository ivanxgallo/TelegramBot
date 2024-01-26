import numpy as np
import pandas as pd
import random as rd
from itertools import combinations



def score_calculator_1(team, players):
    sum = 0
    for i in team:
        D = players[i]["defensa"]
        M = players[i]["medio"]
        A = players[i]["ataque"]

        prom = (D+M+A)/3
        sum += prom

    return sum/len(team)

def score_calculator_2(team, players):
    D_sum   = 0
    M_sum   = 0
    A_sum   = 0
    n_team  = len(team)
    for i in team:
        D = players[i]["defensa"]
        M = players[i]["medio"]
        A = players[i]["ataque"]

        D_sum += D
        M_sum += M
        A_sum += A

    D_prom = D_sum/n_team
    M_prom = M_sum/n_team
    A_prom = A_sum/n_team

    return (D_prom + M_prom + A_prom)/3.

def score_calculator_3(team, players):
    D_sum   = 0
    M_sum   = 0
    A_sum   = 0
    n_team  = len(team)
    for i in team:
        D = players[i]["defensa"]
        M = players[i]["medio"]
        A = players[i]["ataque"]

        D_sum += D
        M_sum += M
        A_sum += A

    D_prom = D_sum/n_team
    M_prom = M_sum/n_team
    A_prom = A_sum/n_team

    return (D_prom*M_prom*A_prom)**(1/3.)

def score_calculator_4(team, players):
    D_mul   = 1.
    M_mul   = 1.
    A_mul   = 1.
    n_team  = len(team)
    for i in team:
        D = players[i]["defensa"]
        M = players[i]["medio"]
        A = players[i]["ataque"]

        D_mul *= D
        M_mul *= M
        A_mul *= A

    D_prom = (D_mul)**(1./n_team)
    M_prom = (M_mul)**(1./n_team)
    A_prom = (A_mul)**(1./n_team)

    return (D_prom*M_prom*A_prom)**(1./3.)


def complementary_list(lst, sub_lst):
    return list(set(lst) - set(sub_lst))

def generate_sublists(lst, m):
    # It returns a list which contains all possible sublists with m elements
    sublists = []
    for comb in combinations(lst, m):
        if comb not in sublists:
            sublists.append(list(comb))
    return sublists



class OptimizeTeam(object):
    def __init__(self, players = []):

        self.players                =       players
        self.player_labels          =       list(range(len(players)))
        self.n_team_players         =       int(len(players)/2)
        self.team_labels            =       None
        self.initial_random_teams   =       None
        self.score_opt_teams        =       None
        self.score_disp_teams       =       None
        self.initial_scores         =       []
        self.opt_teams              =       []
        self.disp_teams             =       []


    def set_first_sample(self, fact = 0.1):
        combinations                =   generate_sublists(self.player_labels, self.n_team_players)
        n_sample                    =   int(len(combinations)*fact)
        self.initial_random_teams   =   rd.sample(combinations, k = n_sample)


    def score_teams_calculator(self):
        complementary_teams         =   []
        self.initial_scores         =   []
        for t in self.initial_random_teams:
            complementary_teams.append(complementary_list(self.player_labels, t))

        for i, t in enumerate(self.initial_random_teams):
            team1_score     =   score_calculator_3(t, self.players)
            team2_score     =   score_calculator_3(complementary_teams[i], self.players)
            score_diff      =   abs(team1_score - team2_score)
            self.initial_scores.append(score_diff)


    def get_opt_teams(self):
        idx             =   self.initial_scores.index(min(self.initial_scores))
        score           =   self.initial_scores[idx]
        team1_labels    =   self.initial_random_teams[idx]
        team2_labels    =   complementary_list(self.player_labels, self.initial_random_teams[idx])
        team1           =   [self.players[player] for player in team1_labels]
        team2           =   [self.players[player] for player in team2_labels]
        self.opt_teams  =   [team1_labels, team2_labels]
        self.score_opt_teams = score

        return  (team1, team2, score)


    def get_disp_teams(self):
        idx             =   self.initial_scores.index(max(self.initial_scores))
        score           =   self.initial_scores[idx]
        team1_labels    =   self.initial_random_teams[idx]
        team2_labels    =   complementary_list(self.player_labels, self.initial_random_teams[idx])
        team1           =   [self.players[player] for player in team1_labels]
        team2           =   [self.players[player] for player in team2_labels]
        self.disp_teams =   [team1_labels, team2_labels]
        self.score_disp_teams = score

        return  (team1, team2, score)


    def show_opt_teams(self, fact=1):
        self.set_first_sample(fact=fact)
        self.score_teams_calculator()
        t1, t2, score = self.get_opt_teams()
        print("Con un score de: ", score, ", un resultado optimo podría ser...")
        print(f"El equipo 1 (prom = {score_calculator_3(self.opt_teams[0], self.players)}) es:")
        for i, t in enumerate(t1):
            print(i+1, ". ", t["nombre"])
        print(f"El equipo 2 (prom = {score_calculator_3(self.opt_teams[1], self.players)}) es:")
        for i, t in enumerate(t2):
            print(i+1, ". ", t["nombre"])

    def show_disp_teams(self, fact=1):
        self.set_first_sample(fact=fact)
        self.score_teams_calculator()
        t1, t2, score = self.get_disp_teams()
        print("Con un score de: ", score, ", el resultado más disparejo es...")
        print(f"El equipo 1 (prom = {score_calculator_3(self.disp_teams[0], self.players)}) es:")
        for i, t in enumerate(t1):
            print(i+1, ". ", t["nombre"])
        print(f"El equipo 2 (prom = {score_calculator_3(self.disp_teams[1], self.players)}) es:")
        for i, t in enumerate(t2):
            print(i+1, ". ", t["nombre"])




