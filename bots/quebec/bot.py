import random
import re
import spacy
from tabulate import tabulate

# functions
def process_name_action(msg):
    '''
    Function used to find name is user message. This function does not flawlessly detect names.
        Args: msg (str)
        Returns: user name (str) only if all other words in msg
    Call: below if statement, use to find name to insert to bots response: name = name_process([last_user_message])
    '''
    for elem in msg:
        mytokens = nlp(elem)
        name = [word.lemma_.lower().strip() for word in mytokens if word.pos_ != "PUNCT" and word.text.lower() not in stopwords]
    return name


def is_cursed(msg):
    '''
    Detects cursewords in user messages
    Call: if is_cursed([last_user_message]) == False
        Args: msg (str)
        Returns: True/False (bool), True if there are cursewords in user message and False if there are none
    '''
    for elem in msg:
        mytokens = nlp(elem)
        cw = [word.lemma_.lower().strip() for word in mytokens if word.text.lower() in cursewords]
    # cursewords is/are present in msg
    if cw != []:
        return True
    # no cursewords in msg
    return False


# use states to navigate through chat
possible_states = ["state_0", "state_1", "state_2", "state_3", "state_4", "state_5", "state_6", "state_7"]
current_state = None
cb_gender = None
cb_name = None
cb_preferences = None
cb_dislikes = None
cb_dislikes_short = None
possible_dislikes = []
suggestion = None
student_name = None
action = None
x = None

# list of activities with tuple (activity, category, activity_in_short)
###### TO DO: adjust sport & culture into infinitive ###########
activities_list = [("faire une randonnée dans le parc national de la Jacques-Cartier", "sport", "jacquescartier", "Randonnée - Jacques-Cartier"),
    ("faire une randonnée guidée dans le parc de la Gatineau", "sport", "gatineau", "Randonnée guidée - Gatineau"),
    ("faire du ski", "sport", "ski", "Ski"), ("faire du snowboard", "sport", "snowboard", "Snowboard"), ("faire de la luge", "sport", "luge", "Luge"),
    ("faire une excursion en motoneige", "sport", "motoneige", "Excursion en montoneige"),
    ("faire une excursion en traîneau à chiens à Mont-Tremblant", "sport", "traîneau", "Excursion en traîneau à chiens"),
    ("faire du rafting en eaux vives sur la rivière Rouge", "sport", "rafting", "Rafting sur Rouge"),
    ("faire de la natation au Centre aquatique Desjardins", "sport", "natation", "Natation au Desjardins"),
    ("faire du canoë sur glace sur le fleuve Saint-Laurent", "sport", "canoë", "Canoë sur glace"),
    ("faire du benji", "sport", "benji", "Benji"), ("faire un tour de tyrolienne sur Mont Tremblant", "sport", "tyrolienne", "Tyorlienne sur Mont Tremblant"),
    ("faire de l'escalade sur Mont Catherine", "sport", "escalade", "Escalade - Mont Catherine"),
    ("aller au club de Trampoline Acrosport Barani", "sport", "trampoline", "Trampoline - Acrosport Barani"),
    ("jouer au tennis", "sport", "tennis", "Tennis"), ("faire un tour du vélo", "sport", "vélo", "Tour du vélo"),
    ("faire du yoga", "sport", "yoga", "Yoga"), ("jouer au paintball à Barkmere", "sport", "paintball", "Paintball à Barkmere"),
    ("aller à l’académie de karting", "sport", "kart", "Karting"), ("faire une promenade", "sport", "promenade", "Promenade"),
    ("faire une balade", "sport", "balade", "Balade"),

    ("aller au Musée de la nature et des sciences de Sherbrooke", "culture", "sherbrooke", "Musée - Sherbrooke"),
    ("aller au Musée du squelette", "culture", "squelette", "Musée - Squelette"), ("aller au Musée du Fjord", "culture", "fjord", "Musée - Fjord"),
    ("visiter le Zoo sauvage de Saint-Félicien", "culture", "zoo", "Zoo sauvage"), ("aller au Musée maritime de Charlevoix", "culture", "charlevoix", "Musée Charlevoix"),
    ("aller au Musée de la civilisation", "culture", "civilisation", " Musée - Civilisation"),
    ("visiter le lieu historique Fort-Lennox", "culture", "fortlennox", "Fort-Lennox"),
    ("visiter le lieu historique Forts-de-Lévis", "culture", "fortsdelévis", "Forts-de-Lévis"), ("regarder un film au cinéma", "culture", "cinéma", "Cinéma"),
    ("aller au Festival d’été de Québec", "culture", "festival", "Festival d'éte"),
    ("aller au Festival international de jazz de Montréal", "culture", "jazz", "Festival international de jazz"),
    ("visiter le Musée national des beaux-arts du Québec", "culture", "beauxarts", "Musée - Beaux-arts"),
    ("visiter le Centre d’art Diane-Dufresne", "culture", "dianedufresne", "Centre d'art - Diane Dufresne"),
    ("visiter le Centre des arts contemporains du Québec à Sorel-Tracy", "culture", "soreltracy", "Centre des arts - Sorel-Tracy"),
    ("visiter la Cinémathèque québécoise", "culture", "cinémathèque", "Cinémathèque"),

    ("aller à la fête au centre de jeunes", "social", "fête", "Fete au centre de jeunes"), ("aller dans une Escape Room", "social", "escape", "Escape Room"),
    ("jouer Mario Kart", "social", "mario", "Mario Kart"), ("jouer aux cartes", "social", "cartes", "Jeux de cartes"), ("jouer au billard", "social", "billard", "Billard"),
    ("jouer au lasertag", "social", "lasertag", "Lasertag"), ("aller au parc de loisirs", "social", "loisirs", "Parc de loisirs"),
    ("aller à un marché aux puces", "social", "marché", "Marché aux puces"), ("réaliser un court-métrage", "social", "courtmétrage", "Court-métrange"),
    ("faire un dîner de différentes cultures", "social", "dîner", "Dîner interculturel"),
    ("faire du shopping", "social", "shopping", "Shopping"), ("faire des biscuits", "social", "biscuits", "Biscuits")]


# possible names of chatbot
names = {"female": ["Jade", "Louise", "Alice", "Emma", "Chloé", "Adeline", "Aurelie",
"Camille", "Charlotte", "Florence", "Julie", "Margaux", "Manon", "Zoé"],
"male": ["Gabriel", "Jules", "Noel", "Louis", "Mathéo", "André", "Hugo",
"Éthan", "Thomas", "Maxime", "Clément", "Jean", "David", "Pascal"]}
names_keys = names.keys()
names_keys = list(names_keys)

plan = {' ': ['Matin', 'Midi', 'Soir'],
        'Lundi': ["Arrivée", "Tour de la ville", "Tour de la ville"],
        'Mardi': ["École", None, None],
        'Mercredi': ["École", None, None],
        'Jeudi': ["École", None, None],
        'Vendredi': ["École", None, "Fête d'adieu"],
        'Samedi': ["Adieu", "Départ", "Départ"]}

cursewords = ["putain", "merde", "connard", "connasse", "hure", "hurensohn", "scheiße", "arschloch", "schlampe"]
# TO DO: adjust so that only lemmas (or stems) have to be written here
stopwords = ["de", "je", "suis", "m'", "mappelle", "appelle", "mapele", "mapelle", "mappele", "apele", "apelle", "appele", "bonjour",
            "mon", "ton", "nom", "est", "salut", "moi", "partenaire", "allemagne", "allemand", "osnabrück", "de", "d'", "du", "et", "échange",
            "faire", "aller", "aimer", "bien", "sur", "sûr", "visiter", "on", "nous", "tu", "j'", "aimerais", "mardi", "le", "l'",
            "vouloir", "veux", "voulons", "voudrais", "beaucoup"]
nlp = spacy.load("fr_core_news_sm")

class Bot:
    '''
    To DO:
    - save information on sport, culture, social in order to adjust proposed suggestions
    '''

    name = 'Québec' # change to random name from list
    avatar = 'avatar/quebec-city.jpeg' # picture from quebec


    def welcome(self, session):
        '''
        This is the first called function when starting the chat with the bot.
        It creates a chatbot personality with gender, name and activity preferences/dislikes
        Returns: (str) welcoming statement which is adjusted to the chatbots gender and name
        '''
        global cb_gender
        global cb_name
        global cb_preferences
        global cb_dislikes
        global cb_dislikes_short
        global current_state
        global possible_states
        global activities_list
        global possible_dislikes

        session.bot.online = "online"
        session.bot.save()
        ################ create bot identity ######################
        # choose random gender of chatbot
        cb_gender = random.choice(names_keys)
        # choose random name of chatbot
        cb_name = random.choice(names[cb_gender])


        # determine preferences of chatbot
        cb_preferences = random.sample(activities_list, 20)

        # only allow non preferred activities to be dislikes
        for elem in activities_list:
            if elem in cb_preferences:
                pass
            else:
                possible_dislikes.append(elem)

        # determine dislikes of chatbot
        cb_dislikes = random.sample(possible_dislikes, 20)
        cb_dislikes_short = [dislike[2] for dislike in cb_dislikes]
        print(cb_dislikes_short, "DISLIKES")

        current_state = possible_states[0]
        # incorporate gender into chatbots welcome statement
        if cb_gender == "male":
            return """Salut! Je suis {}, ton partenaire d'échange.
            Quel est ton nom ?""".format(cb_name)
        elif cb_gender == "female":
            return """Salut! Je suis {}, ta partenaire d'échange.
            Quel est ton nom ?""".format(cb_name)
        else:
            return "Something went wrong"

    def chat(self, last_user_message, session):
        # einfach alles an code in dieser methode schreiben
        # generell wichtig: versuchen auf unklarheiten, negierung, rechtscreibfehler, etc. mit ablenkungen reagiern
        global current_state
        global cb_preferences
        global suggestion
        global cb_dislikes
        global cb_dislikes_short
        global student_name
        global plan

        try:
            # check message for cursewords
            # return """Bitte freundlich bleiben und die Frage beantworten."""
            if is_cursed([last_user_message]) == True:
                return "S'il te plaît, reste aimable et réponds à la dernière question!"
            ######## 0 ########
            # state_0
            elif current_state == possible_states[0] and (process_name_action([last_user_message]) != []): # Eingabe korrekt: die Funktion process_name_action hat einen Namen gefunden
                student_name = process_name_action([last_user_message])[0].capitalize()
                if cb_gender == "male":
                    current_state = possible_states[1]
                    return """Salut {}! Je suis heureux de faire ta connaissance !
                    J'attends ton arrivée avec beaucoup d'impatience. Es-tu déjà allé.e au Québec?""".format(student_name)
                elif cb_gender == "female":
                    current_state = possible_states[1]
                    return """Salut {}! Je suis heureuse de faire ta connaissance !
                    J'attends ton arrivée avec beaucoup d'impatience. Es-tu déjà allé.e au Québec?""".format(student_name)
            elif current_state == possible_states[0]: # && Eingabe ungültig
                return """Tu t'appelles comment ?"""

            ######## 1 ########
            # use regex to detect yes and no
            # state_1
            elif current_state == possible_states[1] and re.search('O|oui', last_user_message) != None: # Eingabe korrekt: Oui
                current_state = possible_states[2]
                return """C'est cool! Alors, planifions ta visite le mois prochain.\nEst-ce que tu préfères des activités sportives, culturelles ou sociales ?"""
            elif current_state == possible_states[1] and re.search('N|non', last_user_message) != None: # Eingabe korrekt: Non
                current_state = possible_states[2]
                return """C'est dommage! Mais alors, je peux te montrer beaucoup de nouvelles choses. \n Alors, planifions ta visite le mois prochain.
                Est-ce que tu préfères des activités sportives, culturelles ou sociales ?"""
            elif current_state == possible_states[1]: # && Eingabe ungültig
                return """Es-tu déjà allé.e au Québec ? Dis-moi si c'est oui ou non, s'il te plaît.""" # TO DO (optional): Liste anlegen und random Frage generieren

            ######## 2 ########
            # use regex to detect sport and culture and social
            # state_2
            elif current_state == possible_states[2] and re.search('S|sport', last_user_message) != None: # Eingabe korrekt: sport
                current_state = possible_states[3]
                index, suggestion = [(i, pref[0]) for i, pref in enumerate(cb_preferences) if pref[1] == "sport"].pop(0)
                _, _, _, action = cb_preferences.pop(index)
                plan["Mercredi"][1] = action
                plan["Mercredi"][2] = action
                return """C'est super! On peut {} le mercredi.
                J'aimerais bien aussi te montrer ma ville le lundi après ton arrivée. Qu'est-ce qu'on va faire le mardi ?""".format(suggestion)
            elif current_state == possible_states[2] and re.search('C|culture', last_user_message) != None: # Eingabe korrekt: culture
                current_state = possible_states[3]
                index, suggestion = [(i, pref[0]) for i, pref in enumerate(cb_preferences) if pref[1] == "culture"].pop(0)
                _, _, _, action = cb_preferences.pop(index)
                plan["Mercredi"][1] = action
                plan["Mercredi"][2] = action
                return """C'est super! On peut {} le mercredi.
                J'aimerais bien aussi te montrer ma ville le lundi après ton arrivée. Qu'est-ce qu'on va faire le mardi ?""".format(suggestion)
            elif current_state == possible_states[2] and re.search('S|social', last_user_message) != None: # Eingabe korrekt: social
                current_state = possible_states[3]
                index, suggestion = [(i, pref[0]) for i, pref in enumerate(cb_preferences) if pref[1] == "social"].pop(0)
                _, _, _, action = cb_preferences.pop(index)
                plan["Mercredi"][1] = action
                plan["Mercredi"][2] = action
                return """C'est super! On peut {} le mercredi.
                J'aimerais bien aussi te montrer ma ville le lundi après ton arrivée. Qu'est-ce qu'on va faire le mardi ?""".format(suggestion)
            elif current_state == possible_states[2]: # && Eingabe ungültig
                return """Est-ce que tu préfères des activités sportives, culturelles ou sociales ?""" # TO DO (optional): Liste anlegen und random Frage generieren

            ######## 3 ########
            # state_3 - TO DO: Hierbei beachten, dass nicht versehentlich Eingabe als no Dislike durchgeht, sondern auch ungültige eingaben gefunden werden
            if current_state == possible_states[3] and not(any(word for word in cb_dislikes_short if word in re.sub(r'[^\w\s]', '', last_user_message.lower()).split())): # Eingabe korrekt: no Dislike
                # strip last_user_message of words like "Je, aimerais"
                action = process_name_action([last_user_message])
                action = " ".join(action).capitalize()
                plan["Mardi"][1] = action
                plan["Mardi"][2] = action
                current_state = possible_states[4]
                suggestion, _, _, action= cb_preferences.pop(0)
                plan["Jeudi"][1] = action
                plan["Jeudi"][2] = action
                # control for verbs with 'aller' where "de" has to be adjusted --> "d'"
                if re.search("^a", suggestion):
                    """Oui, ça c’est super cool ! Est-ce que tu as envie d'{} le jeudi ?""".format(suggestion)
                else:
                    return """Oui, ça c’est super cool ! Est-ce que tu as envie de {} le jeudi ?""".format(suggestion)
            elif current_state == possible_states[3] and any(word for word in cb_dislikes_short if word in re.sub(r'[^\w\s]', '', last_user_message.lower()).split()): # Eingabe korrekt: Dislike
                current_state = possible_states[4]
                new_activity, _, _, action = cb_preferences.pop(0)
                plan["Mardi"][1] = action
                plan["Mardi"][2] = action
                suggestion, _, _, action = cb_preferences.pop(0)
                plan["Jeudi"][1] = action
                plan["Jeudi"][2] = action
                # control for verbs with 'aller' where "de" has to be adjusted --> "d'"
                if re.search("^a", suggestion):
                    return """Moi, je n‘aime pas ça. Mais on peut {}.
                    Est-ce que tu as envie d'{} le jeudi ?""".format(new_activity, suggestion)
                else:
                    return """Moi, je n‘aime pas ça. Mais on peut {}.
                    Est-ce que tu as envie de {} le jeudi ?""".format(new_activity, suggestion)
            elif current_state == possible_states[3]: # && Eingabe ungültig
                return """Qu'est-ce qu'on va faire le mardi ?""" # TO DO (optional): Liste anlegen und random Frage generieren

            ######## 4 ########
            # use regex to detect yes and no
            # state_4
            elif current_state == possible_states[4] and re.search('O|oui', last_user_message) != None: # && Eingabe korrekt: Oui
                current_state = possible_states[5]
                return """Ah, parfait ! Enfin, il faut choisir une activité pour le vendredi midi. Il y a la possibilité
                d’aller au complexe sportif Bell. Là on pourra jouer ou regarder au hockey."""
            elif current_state == possible_states[4] and re.search('N|non', last_user_message) != None: # && Eingabe korrekt: Non
                new_activity, _, _, action = cb_preferences.pop(0)
                suggestion = new_activity # update suggestion
                plan["Jeudi"][1] = action
                plan["Jeudi"][2] = action
                # if new_activity starts with a vocal
                if re.search("^a", new_activity):
                    return """Est-ce que tu as envie d'{} le jeudi?""".format(new_activity) # TO DO (optional): Liste anlegen und random Frage generieren
                else:
                    return """Est-ce que tu as envie de {} le jeudi?""".format(new_activity)
            elif current_state == possible_states[4]: # && Eingabe ungültig
                if re.search("^a", suggestion):
                    return """Est-ce que tu as envie d'{} le jeudi? Dis-moi si c'est oui ou non, s'il te plaît.""".format(suggestion) # TO DO (optional): Liste anlegen und random Frage generieren
                else:
                    return """Est-ce que tu as envie de {} le jeudi? Dis-moi si c'est oui ou non, s'il te plaît.""".format(suggestion) # TO DO (optional): Liste anlegen und random Frage generieren


            ######## 5 ########
            # state_5
            elif current_state == possible_states[5] and (re.search('regarde', last_user_message) != None): # Eingabe korrekt: regarder
                current_state = possible_states[6]
                plan["Vendredi"][1] = "Regarder un jeu de hockey"# TO DO: use Spacy to get activity from user_message
                return """Très bon choix, moi je préfère aussi regarder les professionnels. \n Le vendredi soir j'ai organiser un fête d'adieu pour toi.
                Si tu veux tu peux chanter au karaoké là."""
            elif current_state == possible_states[5] and (re.search('joue', last_user_message) != None): # Eingabe korrekt: jouer
                current_state = possible_states[6]
                plan["Vendredi"][1] = "Jouer au hockey" # TO DO: use Spacy to get activity from user_message
                if cb_gender == "male":
                    return """Donc, je suis très curieux de voir dont tu es capable ;) \n Le vendredi soir j'ai organiser un fête d'adieu pour toi.
                    Si tu veux tu peux chanter au karaoké là."""
                elif cb_gender == "female":
                    return """Donc, je suis très curieuse de voir dont tu es capable ;) \n Le vendredi soir j'ai organiser un fête d'adieu pour toi.
                    Si tu veux tu peux chanter au karaoké là."""
            elif current_state == possible_states[5]: # && Eingabe ungültig
                return """Le vendredi midi on peut jouer ou regarder au hockey au complexe sportif Bell.""" # TO DO (optional): Liste anlegen und random Frage generieren

            ######## 6 ########
            # state_6
            elif current_state == possible_states[6] and re.search('O|oui', last_user_message) != None: # && Eingabe korrekt: oui
                current_state = possible_states[7]
                plan["Vendredi"][2] = "Fête d'adieu + chanter au karaoké"
                if cb_gender == "male":
                    return """Super, alors j’ai trouvé mon/ma partenaire de karaoké !
                    Veux-tu que je t'envoie le plan pour la semaine d'échange?"""
                elif cb_gender == "female":
                    return """Super, alors j’ai trouvé mon/ma partenaire de karaoké !
                    Veux-tu que je t'envoie le plan pour la semaine d'échange?"""
            elif current_state == possible_states[6] and re.search('N|non', last_user_message) != None: # && Eingabe korrekt: non
                current_state = possible_states[7]
                if cb_gender == "male":
                    return """Dommage, alors je dois chanter tout seul.
                    Veux-tu que je t'envoie le plan pour la semaine d'échange?"""
                elif cb_gender == "female":
                    return """Dommage, alors je dois chanter tout seule.
                    Veux-tu que je t'envoie le plan pour la semaine d'échange?"""
            elif current_state == possible_states[6]: # && Eingabe ungültig
                return """Est-ce que tu veux chanter au karaoké ? Dis-moi si c'est oui ou non, s'il te plaît.""" # TO DO (optional): Liste anlegen und random Frage generieren

            ######## 7 ########
            # state_7
            elif current_state == possible_states[7] and re.search('O|oui', last_user_message) != None:
                session.bot.online = "offline"
                session.bot.save()
                # switch Bot from online to offline
                # and don't send a response from chatbot anymore
                if cb_gender == "male": # GENDERN: mon partenaire
                    return """Voici notre plan pour la semaine d’échange:
                    <pre>{}</pre>
                    \n Je suis heureux de te rencontrer en personne ! À bientôt !""".format(tabulate(plan, headers=plan.keys(), tablefmt= 'fancy_grid'))
                elif cb_gender == "female": # GENDERN: mon partenaire
                    return """Voici notre plan pour la semaine d’échange:
                    <pre>{}</pre>
                    \n Je suis heureuse de te rencontrer en personne ! À bientôt !""".format(tabulate(plan, headers=plan.keys(), tablefmt= 'fancy_grid'))
            elif current_state == possible_states[7] and re.search('N|non', last_user_message) != None:
                session.bot.online = "offline"
                session.bot.save()
                if cb_gender == "male": # GENDERN: mon partenaire
                    return "Je suis heureux de te rencontrer en personne ! À bientôt !"
                elif cb_gender == "female": # GENDERN: mon partenaire
                    return "Je suis heureuse de te rencontrer en personne ! À bientôt !"
            elif current_state == possible_states[7]:
                return "Veux-tu que je t'envoie le plan pour la semaine d'échange? Dis-moi si c'est oui ou non, s'il te plaît."
            else:
                return "Pour commencer une nouvelle conversation, clique sur « restart chat »"

        # error control: no idea why the error came up but in order to control for it ask student to reformulate the sentence
        except IntegrityError:
            if cb_gender == "male":
                return "Je suis désolé, mais je n'ai pas entendu ce que tu as dit. Peux-tu le formuler différemment, s'il te plaît ?"
            elif cb_gender == "female":
                return "Je suis désolée, mais je n'ai pas entendu ce que tu as dit. Peux-tu le formuler différemment, s'il te plaît ?"
