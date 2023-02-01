from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Bot(models.Model):
    name = models.CharField(max_length=64, null=False, unique=True)
    classpath = models.CharField(max_length=512, null=False)
    avatar = models.CharField(max_length=1024, null=True)
    active = models.BooleanField(default=True)
    online = models.CharField(max_length=1024, default="online")


class ChatSession(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    data = models.JSONField(default=dict)


class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    user_message = models.BooleanField()
    content = models.CharField(max_length=8192)
    mkdate = models.DateTimeField(auto_now_add=True)


class FrenchLex(models.Model):
    form = models.CharField(max_length=128)  # the word form
    lemma = models.CharField(max_length=128)  # the lemma identifier
    morph = models.CharField(max_length=16)  # coded morphological information

    @classmethod
    def read_lex(cls, fn='data/french.lex'):

        if cls.objects.all().count() > 0:  # only read the lex if it's empty
            return

        with open(fn, "r", encoding='iso8859-1') as f:
            entries = f.readlines()

        for entry in entries:
            fields = entry[:-1].split("\t")
            cls.objects.create(form=fields[0], lemma=fields[1], morph=fields[2])

    @classmethod
    def changePersonne(cls, verbe, anciennePersonne, nouvellePersonne, pluriel=True, indicative=True):
        """ prend un verbe comme entrée,
            et rend la meme forme Ã  la nouvelle personne.
            On préfère le pluriel.
            Si on a le choix entre indicative et subjonctive,
            on prÃ©fÃ¨re l'indicative, sauf si la variable 'indicative' est mise
            Ã  'False'
        """
        codeMode = ""
        personne = ""
        lemme = ""
        infos = cls.objects.filter(form=verbe)

        # s'il ne connait pas le verbe, alors on le laisse tel quel.
        if not infos:
            return verbe

        # essayons de trouver les bons codes pour la personne recherchÃ©e
        for info in infos:
            if str(anciennePersonne) in info.morph:
                for c in info.morph:
                    if c.isdigit():
                        break
                    codeMode += c
                personne = info.morph[-1]
                lemme = info.lemma

        # si je ne trouve pas la bonne personne, je prend les codes
        # de la 1Ã¨re info dans la liste.
        if codeMode == "":
            for c in infos[0].morph:
                    if c.isdigit():
                        break
                    codeMode += c
            personne = infos[0].morph[-1]
            lemme = infos[0].lemma

        # cas spÃ©cial de forme identique indicative et subjonctive
        if codeMode == "PS":
            if indicative:
                codeMode = "P"
            else:
                codeMode = "S"

        # cas spÃ©cial de passage au pluriel de politesse
        if pluriel:
            personne = "p"
        else:
            personne = "s"

        marecherche = cls.objects.filter(lemma=lemme, morph__contains=codeMode).filter(morph__contains=str(nouvellePersonne)).filter(morph__contains=personne)
        if not marecherche:
            return verbe
        else:
            return marecherche[1].form
