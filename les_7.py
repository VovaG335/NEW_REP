from telebot import TeleBot
import db
from time import sleep
from random import choice
night = True
players = []
TOKEN = '6038029656:AAFm7Umm_0KKVyfWeLQisj4ZJSeef1QxJsA'
game = False
bot = TeleBot(TOKEN)

@bot.message_handler(commands = ['start'])
def game_on(message):
    if not game: 
        bot.send_message(message.chat_id, 'Напиши в лс')

def get_killed(night):
    if not night:
        username_killed = db.citizens_kill()
        return f'Горожане выгнали: {username_killed}'
    username_killed = db.mafia_kill()
    return f'Мафия убила: {username_killed}'

def game_loop(message):
    global night, game
    bot.send_message(
        message.chat.id, "Добро пожаловать в игру! Вам дается 1 минута, чтобы познакомиться")
    sleep(60)
    while True:
        msg = get_killed(night)
        bot.send_message(message.chat.id, msg)
        if not night:
            bot.send_message(
                message.chat.id, "Город засыпает, просыпается мафия. Наступила ночь")
        else:
            bot.send_message(
                message.chat.id, "Город просыпается. Наступил день")
        winner = db.check_winner()
        if winner == 'Мафия' or winner == 'Горожане':
            game = False
            bot.send_message(
                message.chat.id, text=f'Игра окончена победили: {winner}')
            return
        db.clear(dead=False)
        night = not night
        alive = db.get_all_alive()
        alive = '\n'.join(alive)
        bot.send_message(message.chat.id, text=f'В игре:\n{alive}')
        sleep(60)

@bot.message_handler(func = lambda m: m.text.lower() == 'играть' and m.chat.type == 'private')
def send_text(message):
    bot.send_message(message.chat_id, f'{message.from_user.firs_name}')
    db.insert_player(player_id = message.from_user.id, username = from_user.firs_name)

@bot.message_handler(commands = ['game'])
def game_start(message):
    global game
    players = db.player_amount()
    if players >= 4 and not game:
        plaer_roles = db.player_role()
        mafia_usernames = db.get_mafia_usernames()
        for player_id, role in player_roles:
            bot.send_message(player_id, role)
            if role == 'mafia':
                bot.send_message(player_id, 'Ты мафия')
        game = True
        bot.send_message(message.chat_id, 'Начинаем')
        return 
    else:
        bot.send_message(message.chat.id, 'Людей недостаточно')

@bot.message_handler(commands = ["kick"])
def kick(message):
    global night
    username = ' '.join(message.text.split(' ')[1:])
    usernames = db.get_all_allive()
    if not night:
        if not username in usernames:
            bot.send_message(message.chat.id, 'Такого имени нет')
            return
        voted = db.vote("citizen_vote", username, message.from_user.id)
        if voted:
            bot.send_message(message.chat.id, "Ваш голос учитан")
            return
        bot.send_message(message.chat.id, "Вы уже голосовали")
        return
    bot.send_message(message.chat.id, "Сейчас ночь вы не можете никого выгнать")       

@bot.message_handler(commands = ["kill"])
def kill(message):
    global night
    username = ' '.join(message.text.split(' ')[1:])
    usernames = db.get_all_alive()
    mafias = db.get_mafia_usernames()
    if night and message.from_user.first_name in mafias:
        if not username in usernames:
            bot.send_message(message.chat.id, 'Такого имени нет')
            return
        voted = db.vote("mafia_vote", username, message.from_user.id)
        if voted:
            bot.send_message(message.chat.id, "Ваш голос учитан")
            return
        bot.send_message(message.chat.id, "Вы уже голосовали")
        return
    bot.send_message(message.chat.id, "Сейчас день вы не можете никого выгнать")       



if __name__ == '__main__':
    bot.polling(none_stop=True)

