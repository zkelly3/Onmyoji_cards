import hashlib
import pickle
import time
import random
import os.path

cards = {'N': [], 'SSN': [], 'R': [], 'SR': [], 'SSR': []}
allcards = {'N': [], 'SSN': [], 'R': [], 'SR': [], 'SSR': []}

class UserManager:
    def __init__(self, users):
        self.all_users = users
    
    def register(self, id, name):
        if id in self.all_users:
            return False
        else:
            self.all_users[id] = User(id, name)
            return True
    
    def login(self, id):
        if id in self.all_users:
            return self.all_users[id]
        else:
            return None

class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.allSSR = 0
        self.allSSN = 0
        self.allcards = 0
        self.poor1 = 0
        self.poor2 = 0
        self.poor3 = 0
        self.poor4 = 0
        self.poor5 = 0
        self.oneblue100 = 0
        self.oneblue = 0
        self.noSSR = 0
        self.cards = {'N': {}, 'SSN': {}, 'R': {}, 'SR': {}, 'SSR': {}}
    
    def drawCardR(self, number):
        if number == 1 and self.oneblue100 <= 0:
            self.oneblue += 1
        if self.oneblue >= 100 and self.oneblue100 <= 0:
            self.oneblue100 = 1
        
        seed = str(time.time())
        h = hashlib.sha1()
        h.update(seed.encode())
        h.update(self.id.encode())
        hashed = h.digest()
        random_seed = int.from_bytes(hashed, 'big')
        random.seed(random_seed)
        
        result = []
        for i in range(number):
            randnum = random.uniform(0, 100)
            if randnum <= 78.8:
                if self.poor5 <= 0:
                    self.noSSR += 1
                if self.noSSR >= 100 and self.poor1 <= 0:
                    self.poor1 = 1
                if self.noSSR >= 200 and self.poor2 <= 0:
                    self.poor2 = 1
                if self.noSSR >= 300 and self.poor3 <= 0:
                    self.poor3 = 1
                if self.noSSR >= 400 and self.poor4 <= 0:
                    self.poor4 = 1
                if self.noSSR >= 500 and self.poor5 <= 0:
                    self.poor5 = 1
                drawn_type = 'R'
            elif randnum <= 98.8:
                if self.poor5 <= 0:
                    self.noSSR += 1
                if self.noSSR >= 100 and self.poor1 <= 0:
                    self.poor1 = 1
                if self.noSSR >= 200 and self.poor2 <= 0:
                    self.poor2 = 1
                if self.noSSR >= 300 and self.poor3 <= 0:
                    self.poor3 = 1
                if self.noSSR >= 400 and self.poor4 <= 0:
                    self.poor4 = 1
                if self.noSSR >= 500 and self.poor5 <= 0:
                    self.poor5 = 1
                drawn_type = 'SR'
            else:
                self.noSSR = 0
                drawn_type = 'SSR'
            
            index = random.randint(0, len(cards[drawn_type])-1)
            drawn_card = cards[drawn_type][index]
            if drawn_card not in self.cards[drawn_type]:
                self.cards[drawn_type][drawn_card] = 1
            else:
                self.cards[drawn_type][drawn_card] += 1
            result.append((drawn_type, drawn_card))
        
        self.maintain()
        
        for drawn in result:
            if drawn[0] == 'R':
                print("你很普通的抽到了R式神 " + drawn[1] + "！")
            elif drawn[0] == 'SR':
                print("你的符咒閃出亮光，抽到了SR式神 " + drawn[1] + "！")
            elif drawn[0] == 'SSR':
                print("你的符咒毀天滅地，抽到了SSR式神 " + drawn[1] + "！")
        print('')
        
    def drawCardN(self):
        seed = str(time.time())
        h = hashlib.sha1()
        h.update(seed.encode())
        h.update(self.id.encode())
        hashed = h.digest()
        random_seed = int.from_bytes(hashed, 'big')
        random.seed(random_seed)
        
        result = []
        for i in range(5):
            randnum = random.uniform(0, 100)
            if randnum <= 87:
                randfrog = random.uniform(0, 100)
                if randfrog <= 97: #3%呱呱
                    drawn_type = 'N'
                else:
                    drawn_type = 'SSN'
            else:
                drawn_type = 'R'
            
            index = random.randint(0, len(cards[drawn_type])-1)
            drawn_card = cards[drawn_type][index]
            if drawn_card not in self.cards[drawn_type]:
                self.cards[drawn_type][drawn_card] = 1
            else:
                self.cards[drawn_type][drawn_card] += 1
            result.append((drawn_type, drawn_card))
        
        self.maintain()
        
        for drawn in result:
            if drawn[0] == 'N':
                print("大人午安，我是N式神 " + drawn[1] + "！")
            elif drawn[0] == 'R':
                print("嗨，我是R式神 " + drawn[1] + "！")
            elif drawn[0] == 'SSN':
                print("呱呱，我是SSN式神 " + drawn[1] + "！")
        print('')
    
    def maintain(self):
        ownTypeCnt = 0
        for type in self.cards:
            ownTypeCnt += len(self.cards[type])
        allTypeCnt = 0
        for type in allcards:
            allTypeCnt += len(allcards[type])
        if ownTypeCnt >= allTypeCnt and self.allcards <= 0:
            self.allcards = 1
        
        if len(self.cards['SSR']) >= len(allcards['SSR']) and self.allSSR <= 0:
            self.allSSR = 1
        
        if len(self.cards['SSN']) >= len(allcards['SSN']) and self.allSSN <= 0:
            self.allSSN = 1
    
def printWords(strs):
    if type(strs) == 'str':
        strs = [strs]
    
    for str in strs:
        print(str)

def loop(description, options):
    option_map = dict(options)
    
    while True:
        printWords(description)
        cmd = input('> ')
        if cmd in option_map:
            returnValue = option_map[cmd]()
            if returnValue:
                break
        else:
            print("指令錯誤，請再試一次\n")

def register(manager):
    new_id = input("您的ID是：")
    new_name = input("您的暱稱是：")
    if not manager.register(new_id, new_name):
        print("這個ID已被使用\n")
    else:
        print("註冊成功！")
        print("記得登進去玩，不然我沒在這裡寫存檔ouo\n")
    return False

def login(manager):
    id = input("請輸入要登入的ID：")
    current_user = manager.login(id)
    if current_user is None:
        print("查無此ID或發生了其他問題\n")
        print('')
    else:
        print("登入成功。嗨，" + current_user.name + "\n")
        run(manager, current_user)
    return False

def leave():
    return True

def run(manager, user):
    print("這是一個模擬陰陽師抽抽的小玩具，跟真實情況會有諸多不同")
    print("蛤你問我不能抽的東西怎麼辦？啾咪")
    print('')
    
    loop(["如果有問題可以輸入help來看有哪些指令可以玩", "離開前請記得登出(exit)，不然不會幫你存檔哦"], [
        ('achieve', lambda: achieve(user)),
        ('draw', lambda: draw(user)),
        ('exit', lambda: logout(manager, user)),
        ('handbook', lambda: handbook(user)),
        ('help', helpmain)
    ])
    return False

def achieve(user):
    print("這裡可以看目前拿了什麼成就，歡迎光臨ouo\n")
    loop(["如果有問題可以輸入help來看有哪些指令可以玩"], [
        ('collect', lambda: collect(user)),
        ('exit', leaveachieve),
        ('help', helpachieve),
        ('progress', lambda: progress(user))
    ])

def collect(user):
    if user.oneblue100 == 1:
        if '小袖之手' not in user.cards['R']:
            user.cards['R']['小袖之手'] = 1
        else:
            user.cards['R']['小袖之手'] += 1
        user.oneblue100 = 2
        user.maintain()
        print("領取「單抽一百次」的獎勵：小袖之手")
    if user.poor1 == 1:
        if '數珠' not in user.cards['R']:
            user.cards['R']['數珠'] = 1
        else:
            user.cards['R']['數珠'] += 1
        user.poor1 = 2
        user.maintain()
        print("領取「非酋初級」的獎勵：數珠")
    if user.poor2 == 1:
        if '兔丸' not in user.cards['R']:
            user.cards['R']['兔丸'] = 1
        else:
            user.cards['R']['兔丸'] += 1
        user.poor2 = 2
        user.maintain()
        print("領取「非酋中級」的獎勵：兔丸")
    if user.poor3 == 1:
        if '小松丸' not in user.cards['SR']:
            user.cards['SR']['小松丸'] = 1
        else:
            user.cards['SR']['小松丸'] += 1
        user.poor3 = 2
        user.maintain()
        print("領取「非酋高級」的獎勵：小松丸")
    if user.poor4 == 1:
        if '日和坊' not in user.cards['SR']:
            user.cards['SR']['日和坊'] = 1
        else:
            user.cards['SR']['日和坊'] += 1
        user.poor4 = 2
        user.maintain()
        print("領取「非洲陰陽師」的獎勵：日和坊")
    if user.poor5 == 1:
        if '兩面佛' not in user.cards['SSR']:
            user.cards['SSR']['兩面佛'] = 1
        else:
            user.cards['SSR']['兩面佛'] += 1
        user.poor5 = 2
        user.maintain()
        print("領取「非洲大陰陽師」的獎勵：兩面佛")
    if user.allSSN == 1:
        index = random.randint(0, len(allcards['SSR'])-1)
        randSSR = allcards['SSR'][index]
        if randSSR not in user.cards['SSR']:
            user.cards['SSR'][randSSR] = 1
        else:
            user.cards['SSR'][randSSR] += 1
        user.allSSN = 2
        user.maintain()
        print("領取「呱皇」的獎勵：隨機SSR")
        print("獲得SSR式神 " + randSSR)
    if user.allSSR == 1:
        if '萬年竹' not in user.cards['SR']:
            user.cards['SR']['萬年竹'] = 1
        else:
            user.cards['SR']['萬年竹'] += 1
        user.allSSR = 2
        user.maintain()
        print("領取「SSR全收集」的獎勵：萬年竹")
    if user.allcards == 1:
        if '鬼燈' not in user.cards['SSR']:
            user.cards['SSR']['鬼燈'] = 1
        else:
            user.cards['SR']['鬼燈'] += 1
        user.allcards = 2
        user.maintain()
        print("領取「歐皇」的獎勵：鬼燈")
    print('')
    return False

def leaveachieve():
    print("加油繼續拚成就哦ouo")
    return True

def helpachieve():
    print("collect: 領取已完成成就的獎勵")
    print("exit: 離開成就區")
    print("help: 你現在正在看著它，會告訴你現在可以用哪些指令")
    print("progress: 可以查看已完成和未完成的成就")
    print('')
    return False

def progress(user):
    yes = []
    no = []
    
    ownTypeCnt = 0
    for type in user.cards:
        ownTypeCnt += len(user.cards[type])
    allTypeCnt = 0
    for type in allcards:
        allTypeCnt += len(allcards[type])
    if user.allcards >= 1:
        yes.append('歐皇')
    else:
        no.append('歐皇 ' + str(ownTypeCnt) + '/' + str(allTypeCnt))
    
    ownSSRTypeCnt = len(user.cards['SSR'])
    allSSRTypeCnt = len(allcards['SSR'])
    if user.allSSR >= 1:
        yes.append('SSR全收集')
    else:
        no.append('SSR全收集 ' + str(ownSSRTypeCnt) + '/' + str(allSSRTypeCnt))
    
    if user.poor1 >= 1:
        yes.append('非酋初級')
    if user.poor2 >= 1:
        yes.append('非酋中級')
    if user.poor3 >= 1:
        yes.append('非酋高級')
    if user.poor4 >= 1:
        yes.append('非洲陰陽師')
    if user.poor5 >= 1:
        yes.append('非洲大陰陽師')
    
    if user.poor1 <= 0:
        pass
    elif user.poor2 <= 0:
        no.append('非酋中級 ' + str(user.noSSR) + '/200')
    elif user.poor3 <= 0:
        no.append('非酋高級 ' + str(user.noSSR) + '/300')
    elif user.poor4 <= 0:
        no.append('非洲陰陽師 ' + str(user.noSSR) + '/400')
    elif user.poor5 <= 0:
        no.append('非洲大陰陽師 ' + str(user.noSSR) + '/500')
    
    ownSSNTypeCnt = len(user.cards['SSN'])
    allSSNTypeCnt = len(allcards['SSN'])
    if user.allSSN >= 1:
        yes.append('呱皇')
    else:
        no.append('呱皇 ' + str(ownSSNTypeCnt) + '/' + str(allSSNTypeCnt))
    
    if user.oneblue100 >= 1:
        yes.append('單抽一百次')
    
    print('已完成：')
    printWords(yes)
    print('')
    print('未完成：')
    printWords(no)
    print('')
    return False

def draw(user):
    print("這裡是抽卡區，歡迎光臨ouo\n")
    loop(["如果有問題可以輸入help來看有哪些指令可以玩"], [
        ('exit', leavedraw),
        ('5gray', user.drawCardN),
        ('1blue', lambda: user.drawCardR(1)),
        ('10blue', lambda: user.drawCardR(10)),
        ('help', helpdraw)
    ])
    return False

def leavedraw():
    print("不抽抽了嗎，掰掰ouo\n")
    return True

def helpdraw():
    print("exit: 離開抽卡區")
    print("5gray: 抽五張灰票，內含N式神和SSN呱")
    print("1blue: 抽一張藍票，內含R、SR式神...可能有SSR式神(?)")
    print("10blue: 抽十張藍票，內含R、SR式神...可能有SSR式神(?)")
    print("help: 你現在正在看著它，會告訴你現在可以用哪些指令")
    print('')
    return False

def handbook(user):
    print("這裡是式神圖鑑，歡迎光臨ouo\n")
    loop(["如果有問題可以輸入help來看有哪些指令可以玩"], [
        ('exit', leavehandbook),
        ('help', helphandbook),
        ('showall', showall),
        ('showown', lambda: showown(user))
    ])
    return False

def leavehandbook():
    print("圖鑑會想念你的，掰掰ouo\n")
    return True

def helphandbook():
    print("exit: 離開圖鑑")
    print("help: 你現在正在看著它，會告訴你現在可以用哪些指令")
    print("showall: 查看這個小玩具裡面全部有哪些式神")
    print("showown: 查看你目前拿到了哪幾種式神")
    print('')
    return False

def showall():
    for type, names in allcards.items():
        print(type + ':')
        cnt = 0
        for name in names:
            print(name + ' ', end='')
            cnt += 1
            if cnt % 5 == 0 or cnt == len(names):
                print('')
        print('')
    return False

def showown(user):
    cardcnt = 0
    for type, names in user.cards.items():
        print(type + ':')
        cnt = 0
        for name in names:
            cardcnt += 1
            print(name + ' ', end='')
            cnt += 1
            if cnt % 5 == 0 or cnt == len(names):
                print('')
        print('')
    if cardcnt == 0:
        print("尼的圖鑑很可憐，請快點去抽卡>:(\n")
    
    return False

def helpmain():
    print("achieve: 進入成就區")
    print("draw: 進入抽卡區")
    print("exit: 登出目前這個帳號")
    print("handbook: 看看可愛的式神圖鑑")
    print("help: 你現在正在看著它，會告訴你現在可以用哪些指令")
    print('')
    return False

def logout(manager, user):
    print("存檔中...可能會花很多時間...\n")
    user_file = open("user.pkl", "wb")
    pickle.dump(manager.all_users, user_file)
    user_file.close()
    print(user.name + "掰掰ouo\n")
    return True

def main():
    cards_file = open("cards.txt", "r", encoding = 'utf8')
    for line in cards_file.readlines():
        card_type, card_name = line.rstrip().split(' ')
        cards[card_type].append(card_name)
    cards_file.close()
    handbook_file = open("handbook.txt", "r", encoding = 'utf8')
    for line in handbook_file.readlines():
        card_type, card_name = line.rstrip().split(' ')
        allcards[card_type].append(card_name)
    handbook_file.close()
    
    if os.path.isfile("user.pkl"):
        user_file = open("user.pkl", "rb")
        users = pickle.load(user_file)
        user_file.close()
    else:
        users = {}
    manager = UserManager(users)
    
    print("歡迎光臨抽抽小玩具\n")
    loop(["新增帳號請輸入register", "登入請輸入login", "離開請輸入exit"], [
        ('register', lambda: register(manager)),
        ('login', lambda: login(manager)),
        ('exit', leave)
    ])
    

if __name__ == '__main__':
    main()
