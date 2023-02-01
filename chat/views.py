from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Bot, ChatSession, ChatMessage
import os
import importlib

def find_active_bots(request):
    """Scan bots directory for bots and register them. Deregister bots that no longer exist."""

    deactivate = [b.name for b in Bot.objects.filter(active=True)]  # start with all currently active bots on deactivate list

    # bots have to be installed in the "bots" directory
    # check all subdirectories there whether they are valid bot codes and register them
    # and deactivate missing or corrupt ones
    botdirs = [f.name for f in os.scandir('bots') if f.is_dir()]
    for botdir in botdirs:
        try:
            botmodule = importlib.import_module(f"bots.{botdir}.bot")
            name = botmodule.Bot.name
            try:
                bot = Bot.objects.get(name=name)
                if not bot.active:  # former inactive bot activated
                    bot.name = name
                    bot.active = True
                    bot.save()
                try:
                    deactivate.remove(name)  # remove active bot from deactivation list
                    messages.info(request, f"Bot {name} wurde deaktiviert.")
                except ValueError:  # new bot
                    messages.info(request, f"Bot {name} wurde wieder aktiviert.")
            except Bot.DoesNotExist:
                # create a new bot
                bot = Bot.objects.create(name=name, classpath=f"bots.{botdir}.bot", active=True)
                messages.info(request, f"Bot {name} wurde registriert und aktiviert.")
                pass
            avatar = None
            try:
                avatar = botmodule.Bot.avatar
            except ValueError:
                pass
            if avatar and avatar!=bot.avatar:
                bot.avatar = avatar
                bot.save()
        except ModuleNotFoundError:  # no bot.py file in folder
            print(f"bot.py missing for {botdir}")
        except AttributeError:  # no name in Bot class
            print(f"bot.py has no class Bot or name attribute in Bot class for {botdir}")

    # deactivate all active bots that were not found
    for d in deactivate:
        bot = Bot.objects.get(name=d)
        bot.active = False
        bot.save()
        messages.info(request, f"Bot {name} wurde deaktiviert.")

class RestartChat(LoginRequiredMixin, View):

    def get(self, request, chatid):

        try:
            chatsession = ChatSession.objects.get(pk=chatid, user=request.user)
        except ChatSession.DoesNotExist:
            return HttpResponseBadRequest(f"Chat session #{chatid} doest not exist for user {request.user.username}")

        chatsession.delete()
        return redirect("index")


class Index(LoginRequiredMixin, View):
    """The main view. Simply shows chat for now."""

    def post(self, request, chatid):
        try:
            #chatsession = ChatSession.objects.get(pk=chatid, user=request.user)
            chatsession = ChatSession.objects.filter(pk=chatid, user=request.user)[0]
        except ChatSession.DoesNotExist:
            return HttpResponseBadRequest(f"Chat session #{chatid} doest not exist for user {request.user.username}")

        # create chat message from user input
        content = request.POST.get('msg', '42!')
        ChatMessage.objects.create(user_message=True, session=chatsession, content=content)

        # create response from bot
        botmodule = importlib.import_module(chatsession.bot.classpath)
        botobject = botmodule.Bot()
        ChatMessage.objects.create(user_message=False, session=chatsession, content=botobject.chat(content, chatsession))

        chatsession.save()  # force saving changed session

        # show chat
        return redirect('index_chatid', chatid=chatsession.pk)

    def get(self, request, chatid=None):
        find_active_bots(request)  # check if there are new bots TODO: move to somewhere else

        # get (and if necessary, initialize) all bots for current user
        bots = Bot.objects.filter(active=True).order_by('name')
        for bot in bots:
            chatsession, created = ChatSession.objects.get_or_create(user=request.user, bot=bot)
            if created:
                botmodule = importlib.import_module(bot.classpath)
                botobject = botmodule.Bot()
                ChatMessage.objects.create(user_message=False, session=chatsession, content=botobject.welcome(chatsession))
            bot.chatsession = chatsession  # monkey patching for template. Find better solution.

        if bots:  # there are active bots
            if not chatid:
                return redirect('index_chatid', chatid=bots[0].chatsession.pk)
            else:
                try:
                    chatsession = ChatSession.objects.get(pk=chatid, user=request.user)
                except ChatSession.DoesNotExist:
                    return HttpResponseBadRequest(f"Chat session #{chatid} doest not exist for user {request.user.username}")

        chatmessages = ChatMessage.objects.filter(session=chatsession)
        return render(request, 'bot/index.html', locals())
