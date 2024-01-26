# -*- coding: utf-8 -*-
import itertools
import pandas as pd

# --------------- DEFINING SOME VARIABLES -------------------#
HELP_TEXT = '''
# - Este Bot es propiedad de VoludosInk - #

Está diseñado para simplificar la
creación de equipos en futbolito.

El modo de uso es la siguiente:
Se debe ingresar una lista de nombres.
Esta lista debe contener solo un jugador por línea.
(No es necesario que los jugadores estén numerados)
Este es un ejemplo de mensaje a ingresar:

1. jugador1
2. jugador2
.
.
.
14. jugador14

Este Bot retornará los equipos más equilibrados que encuentre.

Se recomienda primero mandar "/players" y ver qué jugadores
hay disponibles con sus respectivos nombres (o alias).
'''

df = pd.read_excel("Fushibola.xlsx")
players = df.to_dict(orient="records")

# -------------------- DEFINING SOME FUNCTIONS ----------------------- #

def starter(update, context):
    user = update.effective_user
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Hola {user.mention_html()}!',
        parse_mode='HTML',
    )


def helper(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=HELP_TEXT)


def dict2text(player_dict):
    message = ""
    for id, player in enumerate(player_dict):
        message += f"{id+1}. {player['Alias']} \n"

    return message


def analyzer(update, context):
    # Obtén el texto del mensaje
    message = update.message.text

    players_dict = filter_players(message, players)

    team1, team2 = calculate_optimal_team(players_dict)

    msg = ""
    for i, team in enumerate([team1, team2]):
        msg += f"El equipo {i+1} es:\n"
        msg += f"{dict2text(team)}\n"

    # Envía el resultado del análisis como respuesta
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg
    )


def filter_players(selected_names_str, players_list):
    list_names = selected_names_str.lower()
    selected_players = [player for player in players_list if player["Alias"].lower() in list_names]

    return selected_players


def calculate_optimal_team(players):
    best_difference = float('inf')
    best_combination = None

    # Generate all possible combinations of teams
    combinations = list(itertools.combinations(players, int(len(players)/2)))

    for team1 in combinations:
        team2 = [player for player in players if player not in team1]

        # Calculate the total skills of each team
        skills_team1 = sum(player["Defensa"] + player["Medio Campo"] + player["Ataque"] + player["Stamina"] + player["Pase"] for player in team1)
        skills_team2 = sum(player["Defensa"] + player["Medio Campo"] + player["Ataque"] + player["Stamina"] + player["Pase"] for player in team2)

        # Calculate the difference between the skills of the two teams
        difference = abs(skills_team1 - skills_team2)

        # Update the best combination if the difference is smaller
        if difference < best_difference:
            best_difference = difference
            best_combination = (team1, team2)

    return best_combination

def show_players(update, context):
    message = "Listado de jugadores en la base de datos:\n\n"
    for i, p in enumerate(players):
        message += f"{i+1}. {p['Alias']}: \t {p['Posición en el campo']}\n"

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message)
