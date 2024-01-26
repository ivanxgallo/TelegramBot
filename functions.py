import itertools

# --------------- DEFINING SOME VARIABLES -------------------#
HELP_TEXT = '''
Este Bot es propiedad de VoludosInk.
Está diseñado para simplificar la
creación de equipos en futbolito.

El modo de uso es la siguiente:
Se debe ingresar una lista numerada de nombres.
Este es un ejemplo de mensaje a ingresar:

1. jugador1
2. jugador2
.
.
.
14. jugador14

Este Bot retornará los equipos más equilibrados que encuentre.
'''

players = [
    {"nombre": "Vito", "defensa": 5, "medio": 8, "ataque": 7},
    {"nombre": "Dolo", "defensa": 5, "medio": 5, "ataque": 4},
    {"nombre": "Valenzuela", "defensa": 8, "medio": 7, "ataque": 5},
    {"nombre": "Jano", "defensa": 7, "medio": 5, "ataque": 4},
    {"nombre": "Capullo", "defensa": 7, "medio": 6, "ataque": 6},
    {"nombre": "Reyes", "defensa": 3, "medio": 4, "ataque": 7},
    {"nombre": "Migue", "defensa": 6, "medio": 7, "ataque": 7},
    {"nombre": "Rodro", "defensa": 5, "medio": 6, "ataque": 9},
    {"nombre": "Nacho", "defensa": 5, "medio": 7, "ataque": 9},
    {"nombre": "Gallo", "defensa": 9, "medio": 8, "ataque": 7},
    {"nombre": "Koke", "defensa": 5, "medio": 6, "ataque": 6},
    {"nombre": "Juanka", "defensa": 6, "medio": 7, "ataque": 7},
    {"nombre": "Arquero", "defensa": 8, "medio": 6, "ataque": 3},
    {"nombre": "Adolfo", "defensa": 9, "medio": 5, "ataque": 2}
]

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
        message += f"{id+1}. {player['nombre']} \n"

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
    selected_players = [player for player in players_list if player["nombre"].lower() in list_names]

    return selected_players


def calculate_optimal_team(players):
    best_difference = float('inf')
    best_combination = None

    # Generate all possible combinations of teams
    combinations = list(itertools.combinations(players, int(len(players)/2)))

    for team1 in combinations:
        team2 = [player for player in players if player not in team1]

        # Calculate the total skills of each team
        skills_team1 = sum(jugador["defensa"] + jugador["medio"] + jugador["ataque"] for jugador in team1)
        skills_team2 = sum(jugador["defensa"] + jugador["medio"] + jugador["ataque"] for jugador in team2)

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
        message += f"{i+1}. {p['nombre']}\n"

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message)
