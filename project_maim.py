from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext, storage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from bs4 import BeautifulSoup
import requests



def get_programs(url='https://www.hse.ru/education/magister/'):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    total_info = dict()


    def find_programs(type):
        faculties = soup.find_all('div',  f'edu-programm__tab edu-programm__{type}')
        total_info = dict()
        for i in faculties:
            faculties_child = i.findChildren('div', 'edu-programm__group')
            for i in faculties_child:
                name_list = list()
                link_list = list()
                price_list = list()

                name_child = i.findChildren('h3', 'u-accent u normal with-indent4 edu-programm__caption')
                price_child = i.findChildren('div', 'b-row__item b-row__item--2 b-row__item--t4 b-row__item--cost')
                year_child = i.findChildren('div', 'b-row__item b-row__item--2 b-row__item--t4 b-row__item--period')
                
                for y in year_child:
                    y = y.findChildren('div', 'edu-programm__data u-accent')
                    for t in y:
                        period = ''.join(filter(lambda x: x.isdigit(), t.text))
                        if len(period) > 1:
                            period = float(period) / 10


                for p in price_child:
                    if p.text != '':
                        if 'за весь' in p.text:
                            price = ''.join(filter(lambda x: x.isdigit(), p.text))
                            price = float(price) / float(period)
                            price_list.append(price)
                        else:
                            price = ''.join(filter(lambda x: x.isdigit(), p.text))
                            price = int(price)
                            price_list.append(price)

                for e in name_child:
                    e.text

                programm_name = e.text
                link_name_child = i.findChildren('a', 'link')
            
                for i in link_name_child:
                    t = i['href']
                    link_list.append(t)

                for e in link_name_child:
                    name_list.append(e.text)

                dvalue = list(zip(name_list, link_list, price_list))
                total_info[programm_name] = dvalue
            return total_info


    total_info['bachelor'] = find_programs('bachelor')
    total_info['magister'] = find_programs('magister')
    return total_info


def create_program_list(type):
    t = get_programs()
    tdict = dict()
    tlist = str()
    bachelor_programms = t[type]
    for i, e in enumerate(bachelor_programms):
        tlist += str(i + 1) + ') ' + e + '\n'
        tdict[i + 1] = bachelor_programms[e]
    result = (tlist, tdict)
    return result


def get_modules(price = 400000, url = 'https://www.hse.ru/ba/up/'):
    url  = url + 'courses'
    names_list = list()
    modules_list = list()

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    items = soup.find_all('div', 'edu-events__item')
    pages = soup.find_all('a', 'pages__page')

    pages_list = list()
    general_items = list()
    general_items.extend(items)
    
    for i in pages:
        pages_list.append(i['href'])

    for i in pages_list:
        url = i
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        items = soup.find_all('div', 'edu-events__item')
        general_items.extend(items)
    

    
    for i in general_items:
        modules_chilren = i.findChildren('div' , 'edu-events_modules')
        for i in modules_chilren:
            data = i.findChildren('ul', 'edu-filter_modules__list ui-sortable')
            for i in data:
                modules_list.append(i['data-tooltip'])
                     
    for i in general_items:
        name_children = i.findChildren('a', 'link link_dark')   
        for i in name_children:
            names_list.append(i.text)  
    modules = list(map(lambda x: str(x).split(','), modules_list))
    year_list = list()
    modules_tlist = list()
    for i in modules:
        tlist = list()
        for e in i:
            i = ''.join(filter(lambda x: x.isdigit(), e))
            tlist.append(i)
        year = tlist.pop(0)
        if len(tlist[0]) > 1:
            for i in tlist:
                t = list(tlist[0])
                t = list(map(lambda x: int(x), t))
                s = t[0]
                e = t[1]
                tlist = [i for i in range(s, e + 1)]
        year_list.append(year)
        modules_tlist.append(tlist)
    modules_final = list(zip(year_list, modules_tlist, names_list))
    
    year_1 = list()
    year_2 = list()
    year_3 = list()
    year_4 = list()
    for i in modules_final:
        if i[0] == '1':
            year_1.append(i)
        elif i[0] == '2':
            year_2.append(i)
        elif i[0] == '3':
            year_3.append(i)
        elif i[0] == '4':
            year_4.append(i)
    

    def add_price(year):
        counter = int()
        for i in year:
            counter += len(i[1])
        if counter != 0 and counter != None:
            year_price = int(price / counter)
        else:
            year_price = 0
        return year_price
    
    year_1_price = add_price(year_1)
    year_2_price = add_price(year_2)
    year_3_price = add_price(year_3)
    year_4_price = add_price(year_4)

    result = str()
    result += 'First Course\n'
    def create_mod_signs(elements):
        mod_signs = str()
        elements = list(map(lambda x: str(x), elements))
        if '1' in elements:
            mod_signs += '🟦'
        else:
            mod_signs += '◽'
        if '2' in elements:
            mod_signs += '🟦'
        else:
            mod_signs += '◽'
        if '3' in elements:
            mod_signs += '🟦'
        else:
            mod_signs += '◽'
        if '4' in elements:
            mod_signs += '🟦'
        else:
            mod_signs += '◽'
        return mod_signs

    
    for i, e in enumerate(year_1):
        result += '\n' +  e[2] + '\n' + create_mod_signs(e[1]) + '\n' + str(year_1_price * len(e[1])) + ' ₽' + ' \n'

    result += '\n\nSecond Course\n'

    for i, e in enumerate(year_2):
        result += '\n' +  e[2] + '  ' + create_mod_signs(e[1]) + '\n' + str(year_2_price * len(e[1])) + ' ₽' + '\n'

    result += '\n\nThird Course\n'

    for i, e in enumerate(year_3):
        result += '\n' +  e[2] + '\n' + create_mod_signs(e[1]) + '\n' + str(year_3_price * len(e[1])) + ' ₽' + '\n'

    result += '\n\nFourth Course\n'

    for i, e in enumerate(year_4):
        result += '\n' +  e[2] + '\n' + create_mod_signs(e[1]) + '\n' + str(year_4_price * len(e[1])) + ' ₽' + '\n'
    return result


def returning_answer(tdict, inputed_number):
    inputed_number = int(inputed_number)
    t = str()
    

    for i, e in enumerate(tdict[inputed_number]):
        tlist = list()
        t += str(i + 1) + ') ' + e[0] + ' ' + e[1] + '\n'
        tlist.append(e[1])
        tlist.append(e[2])
        
    t = 'Enter a number of the programm:' + '\n' + t
    return t

        
def return_certain_object(sourse_list, num):
    num = int(num)
    comp_dict = dict()
    for i, e in enumerate(sourse_list):
        comp_dict[i + 1] = (e[1] , e[2])
    return comp_dict[num]


storage = MemoryStorage()
bot = Bot(token='5609466951:AAE_oqTffKWT9pQPuU1lEhGH8zcTUxooBag')
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    final_modules = State()

@dp.message_handler(commands='start')
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Bachelor', 'Magister']
    keyboard.add(*buttons)
    await message.answer('Choose a type you want:',reply_markup=keyboard)
    await Form.final_modules.set()
    await Form.next()
    
@dp.message_handler(lambda message: message.text == "Bachelor" or message.text == "Magister")
async def without_puree(message: types.Message):
    t = message.text
    t = t.lower()
    tlist, tdict = create_program_list(t)
    await message.answer(f"Enter a number of the course:\n{tlist}",reply_markup=types.ReplyKeyboardRemove())
    print(tdict)
    await Form.next()



    @dp.message_handler(state = Form.final_modules)
    async def programms(message: types.Message, state: FSMContext):
        text = message.text
        try: 
            int(text)
        except ValueError:
            await message.answer('This is not a number')
        else:
            if int(text) > len(tdict) or int(text) <= 0:
                await message.answer("The number is not in range")
            else:
                answer = returning_answer(tdict, text)
                picked_program = tdict[int(text)]
                async with state.proxy() as data:
                    data['picked_program'] = picked_program
                await message.answer(answer)
                await Form.next()
                
               

    @dp.message_handler()
    async def finalll(message: types.Message, state: FSMContext):
        text = message.text
        async with state.proxy() as data:
            picked_program = data['picked_program']
        try: 
            int(text)
        except ValueError:
            await message.answer('This is not a number')
        else:
            if int(text) > len(picked_program) or int(text) <= 0:
                await message.answer("The number is not in range")
            else:

                link, price = return_certain_object(picked_program, text)
                response = get_modules(price, link)
                await message.answer(response)

if __name__ == '__main__':
    executor.start_polling(dp)