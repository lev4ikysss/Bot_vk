import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from vkbottle import Keyboard, KeyboardButtonColor, Text


token = "vk1.a.JOoYiO3KTipqXkIz0qr62mUiG5zrXRtHqexehP_d0Z7-jbevq6kY1kWbESNBGl3GYgXJxBkkClz_LBiAiHL4ifoaUId809Ld_FAOCD3En2bTG_e2dCAoU8QXL5Szlm323H0939m7UGbG4NODg3S16teQOGYMrir_VmRAlpJZpvHTW4BxNKPI6wW4h6FHJzSJ4nmxIYeYIT83yS8t0rFGSw"

vk = vk_api.VkApi(token=token)
def write_msg(user_id, message) :
    Random = int(random.uniform(0, 1000000000000))
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': Random})

def write_msg_Keyboard(user_id, message, keyboard) :
    Random = int(random.uniform(0, 1000000000000))
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': Random, 'keyboard': keyboard})

longpoll = VkLongPoll(vk)

def Menu(user_id) :
    Random = int(random.uniform(0, 1000000000000))
    keyboard = (
        Keyboard(one_time=True, inline=False)
        .add(Text("Предложить идею для факультета"), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text("Роль"), color=KeyboardButtonColor.POSITIVE)
        .add(Text("Вызвать администратора"), color=KeyboardButtonColor.NEGATIVE)
        .row()
        .add(Text("Рассылка"), color=KeyboardButtonColor.SECONDARY)
        .add(Text("Cтать рассыльником"), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text("Помощь"), color=KeyboardButtonColor.SECONDARY)
    ).get_json()
    vk.method('messages.send', {'user_id': user_id, 'random_id': Random, 'keyboard': keyboard, 'message': 'Открываю меню'})

def NewMessage(a, b) :
    if a.lower() == "начать" :
        write_msg(b, "Привет, ты находишься в боте факультета, главная цель бота это рассылка")
        f0 = open("Учащиеся.txt", "r")
        f1 = open("Наставники.txt", "r")
        if b in f0 or f1 :
            f0.close
            f1.close
            Menu(b)
        else:
            f0.close
            f1.close
            keyboard = (
                Keyboard(one_time=False, inline=True)
                .add(Text("Ученик"), color=KeyboardButtonColor.POSITIVE)
                .add(Text("Наставник"), color=KeyboardButtonColor.NEGATIVE)
                ).get_json()
            write_msg_Keyboard(b, "Кто ты?", keyboard)
            for event in longpoll.listen() :
                if event.to_me :
                    if event.type == VkEventType.MESSAGE_NEW :
                        message = event.text
                        user_id = event.user_id
                        if message == "Ученик" :
                            f = open("Учащиеся.txt", 'a')
                            f.write(f"{user_id}\n")
                            write_msg(user_id, "Успешно!")
                            print('Новый учащийся!', user_id)
                            f.close
                            Menu(user_id)
                            break
                        elif message == "Наставник" :
                            f = open("Наставники.txt", 'a')
                            f.write(f"{user_id}\n")
                            write_msg(user_id, "Успешно!")
                            print('Новый наставник!', user_id)
                            f.close
                            Menu(user_id)
                            break
    elif a.lower() == "меню" :
        Menu(b)
    elif a.lower() == "предложить идею для факультета" :
        write_msg(b, "Напишите своё предложение в виде сообщения, если оно будет дельным мы вас наградим")
        for event in longpoll.listen() :
            if event.to_me :
                if event.type == VkEventType.MESSAGE_NEW :
                    text = event.text
                    user_id = event.user_id
                    write_msg(729760987, f"новая идея: {text}, vk.com/gim223275032?sel={user_id}")
                    write_msg(user_id, "Успешно, предложение было отправленно на рассмотрение")
                    Menu(b)
    elif a.lower() == "вызвать администратора" :
        write_msg(729760987, f"Участник вызвал администратора, vk.com/gim223275032?sel={b}")
        write_msg(b, "Вы вызвали администратора, ожидайте")
    elif a.lower() == "роль" :
        f0 = open('Учащиеся.txt', 'r')
        f1 = open('Наставники.txt', 'r')
        if str(b) in f0 :
            write_msg(b, "Ваша роль: Ученик")
        elif str(b) in f1 :
            write_msg(b, "Ваша роль: Наставник")
        else :
            write_msg(b, "У вас нету роли")
        f0.close
        f1.close
        Menu(b)
    elif a.lower() == "помощь" :
        write_msg(b, "Вот доступные команды:\nНачать - команда позволяет записать роль, если вы уже записывали свою роль и хотите перезаписать её напишите @teapot_from_china, т.к. команда будет открывать меню\nМеню - открывает меню")
        Menu(b)
    elif a.lower() == "get my id" :
        print(b)
        write_msg(b, b)
        Menu(b)
    elif a.lower() == "стать рассыльником" :
        f = open("Рассыльники.txt", "r")
        if b in f :
            f.close
            write_msg(b, "Вы уже являетесь рассыльником")
            Menu(b)
        else :
            f.close
            keyboard = (
                Keyboard(one_time=False, inline=True)
                .add(Text("Стать рассыльником"), color=KeyboardButtonColor.POSITIVE)
                .add(Text("В меню"), color=KeyboardButtonColor.NEGATIVE)
                ).get_json()
            write_msg_Keyboard(b, "Хотите стать рассыльником?\nУчтите что рассыльники должны соблюдать следующие правила:\n1.Рассыльник должен уведомлять факультет рассылкой хотябы раз в месяц\n2.Повторяющиеся рассылки запрещены\n3.Маты и ненармотивная лексика в рассылках строго запрещены\nРассыльники как и наставники могут обменивать баллы на таланты в нашем магазине", keyboard)
            for event in longpoll.listen() :
                if event.to_me :
                    if event.type == VkEventType.MESSAGE_NEW :
                        message = event.message
                        user_id = event.user_id
                        if message == "В меню" :
                            Menu(user_id)
                            break
                        elif message == "Стать рассыльником" :
                            f = open("Рассыльники", "a")
                            f.write(f"{user_id}\n")
                            f.close
                            print(f"Новый рассыльник! {user_id}")
                            write_msg(user_id, 'Успешно, теперь вам доступна команда "Рассылка"')
                            Menu(user_id)
                            break
    elif a.lower() == "рассылка" :
        f0 = open("Рассыльники.txt", "r")
        f1 = open("Наставники.txt", "r")
        if b in f0 or f1 :
            f0.close
            f1.close
            keyboard = (
                Keyboard(one_time=True, inline=False)
                .add(Text("Быстрая рассылка"), color=KeyboardButtonColor.NEGATIVE)
                .add(Text("Обычная рассылка"), color=KeyboardButtonColor.POSITIVE)
                .row()
                .add(Text("В меню"), color=KeyboardButtonColor.PRIMARY)
            ).get_json()
            write_msg_Keyboard(b, "Вы можете начать рассылку\nПосторайтесь не злоупотреблять быстрыми рассылками, ведь за них дают меньше баллов", keyboard)
            for event in longpoll.listen() :
                if event.to_me :
                    if event.type == VkEventType.MESSAGE_NEW :
                        if event.message == "В меню" :
                            Menu(event.user_id)
                            break
                        elif event.message == "Быстрая рассылка" :
                            with open("Учащиеся.txt") as file:
                                for line in file:
                                    write_msg(line.rstrip(), "Новое задание!\nhttps://vk.com/app8038390")
                            print("Успешная рассылка!")
                            write_msg(b, "Успешно!")
                            Menu(b)
                            break
                        elif event.message == "Обычная рассылка" :
                            keyboard = (
                                Keyboard(one_time=True, inline=False)
                                .add(Text("В факультете"), color=KeyboardButtonColor.NEGATIVE)
                                .add(Text("На бирже"), color=KeyboardButtonColor.POSITIVE)
                                .row()
                                .add(Text("В меню"), color=KeyboardButtonColor.PRIMARY)
                            ).get_json()
                            write_msg_Keyboard(b, "Где выложено задание?", keyboard)
                            for event in longpoll.listen() :
                                if event.to_me :
                                    if event.type == VkEventType.MESSAGE_NEW :
                                        Who = event.message.lower()
                                        write_msg(b, "Введите название задания:")
                                        for event in longpoll.listen() :
                                            if event.to_me :
                                                if event.type == VkEventType.MESSAGE_NEW :
                                                    Name = event.message
                                                    write_msg(b, "Введите награду за задание:")
                                                    for event in longpoll.listen() :
                                                        if event.to_me :
                                                            if event.type == VkEventType.MESSAGE_NEW :
                                                                Umnicoin = event.message
                                                                write_msg(b, "Введите описание задания:")
                                                                for event in longpoll.listen() :
                                                                    if event.to_me :
                                                                        if event.type == VkEventType.MESSAGE_NEW :
                                                                            Opisanie = event.message
                                                                            keyboard = (
                                                                                Keyboard(one_time=True, inline=False)
                                                                                .add(Text("Подтвердить"), color=KeyboardButtonColor.POSITIVE)
                                                                                .add(Text("Отклонить"), color=KeyboardButtonColor.NEGATIVE)
                                                                            ).get_json()
                                                                            write_msg_Keyboard(b, f'Ученикам будет отправленно следующие сообщение:\n\n\nНовое задание {Who}!\n\nПод названием"{Name}"\n\nНаграда составляет: {Umnicoin} умникоинов\n\nОписание задания: {Opisanie}\n\nhttps://vk.com/app8038390", keyboard')
                                                                            for event in longpoll.listen() :
                                                                                if event.to_me :
                                                                                    if event.type == VkEventType.MESSAGE_NEW :
                                                                                        if event.message == "Подтвердить" :
                                                                                            with open("Учащиеся.txt") as file:
                                                                                                for line in file:
                                                                                                    write_msg(line.rstrip(), f'Новое задание {Who}!\n\nПод названием"{Name}"\n\nНаграда составляет: {Umnicoin} умникоинов\n\nОписание задания: {Opisanie}\n\nhttps://vk.com/app8038390')
                                                                                                print("Новая рассылка!")
                                                                                                write_msg(b, "Успешно!")
                                                                                                Menu(b)
                                                                                        elif event.message == "Отклонить" :
                                                                                            Menu(b)
                                                                                        break
                                                                            break
                                                                break
                                                    break
                                        break
                            break
        else:
            f0.close
            f1.close
            write_msg(b, "Недостаточно прав")
            Menu(b) 

for event in longpoll.listen() :
    if event.to_me :
        if event.type == VkEventType.MESSAGE_NEW :
            NewMessage(event.text, event.user_id)
