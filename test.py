from spacy.lang.fr import French
import spacy
import re

activities_list = [("faire une randonnée dans le parc national de la Jacques-Cartier", "sport", "jacques-cartier"), ("faire une randonnée guidée dans le parc de la Gatineau", "sport", "gatineau"),
    ("faire du ski", "sport", "ski"), ("faire du snowboard", "sport", "snowboard"), ("faire de la luge", "sport", "luge"), ("faire une excursion en motoneige", "sport", "motoneige"),
    ("faire une excursion en traîneau à chiens à Mont-Tremblant", "sport", "traîneau"), ("faire du rafting en eaux vives sur la rivière Rouge", "sport", "rafting"),
    ("faire de la natation au Centre aquatique Desjardins", "sport", "natation"), ("faire du canoë sur glace sur le fleuve Saint-Laurent", "sport", "canoë"),
    ("faire du benji", "sport", "benji"), ("faire un tour de tyrolienne sur Mont Tremblant", "sport", "tyrolienne"), ("faire de l'escalade sur Mont Catherine", "sport", "escalade"),
    ("aller au club de Trampoline Acrosport Barani", "sport", "trampoline"), ("jouer au tennis", "sport", "tennis"), ("faire un tour du vélo", "sport", "vélo"), ("faire du yoga", "sport", "yoga"),
    ("jouer au paintball à Barkmere", "sport", "paintball"), ("aller à l’académie de karting", "sport", "kart"), ("faire une promenade", "sport", "promenade"), ("faire une balade", "sport", "balade"),

    ("aller au Musée de la nature et des sciences de Sherbrooke", "culture", "Sherbrooke"), ("aller au Musée du squelette", "culture", "squelette"), ("aller au Musée du Fjord", "culture", "fjord"),
    ("visiter le Zoo sauvage de Saint-Félicien", "culture", "zoo"), ("aller au Musée maritime de Charlevoix", "culture", "charlevoix"), ("aller au Musée de la civilisation", "culture", "civilisation"),
    ("visiter le lieu historique Fort-Lennox", "culture", "fort-lennox"), ("visiter le lieu historique Forts-de-Lévis", "culture", "forts-de-lévis"), ("regarder un film au cinéma", "culture", "cinéma"),
    ("aller au Festival d’été de Québec", "culture", "festival d'été"), ("aller au Festival international de jazz de Montréal", "culture", "festival international de jazz"),
    ("visiter le Musée national des beaux-arts du Québec", "culture", "beaux-arts"), ("visiter le Centre d’art Diane-Dufresne", "culture", "diane-dufresne"),
    ("visiter le Centre des arts contemporains du Québec à Sorel-Tracy", "culture", "sorel-tracy"), ("visiter la Cinémathèque québécoise", "culture", "cinémathèque"),

    ("aller à la fête au centre de jeunes", "social", "fête"), ("aller dans une Escape Room", "social", "escape room"), ("jouer Mario Kart", "social", "mario kart"),
    ("jouer aux cartes", "social", "cartes"), ("jouer au billard", "social", "billard"), ("jouer au lasertag", "social", "lasertag"), ("aller au parc de loisirs", "social", "parc"),
    ("aller à un marché aux puces", "social", "marché"), ("réaliser un court-métrage", "social", "court-métrage"), ("faire un dîner de différentes cultures", "social", "dîner"),
    ("faire du shopping", "social", "shopping"), ("faire des biscuits", "social", "biscuit")]

last_user_message = "J'aimerais bien aller au parc de-la-Villete."
print(last_user_message.lower().split())

# initializing string
test_str = "Gfg, is m'appelle best : for ! Geeks ;"

# printing original string
print("The original string is : " + test_str)

# Removing punctuations in string
# Using regex
res = re.sub(r'[^\w\s]', '', last_user_message.lower()).split()
print(res)
