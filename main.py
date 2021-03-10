#!/usr/bin/python3

from bs4 import BeautifulSoup
from datetime import datetime
import requests

s = requests.Session()

class ELearning:
    # base url
    base_url = 'https://siswa.smkn2solo.sch.id/'

    # usefull path
    path = {
        'login' : 'pages/auth/checkLogin.php',
        'absen' : 'pages/classroom/enroll.php?id=',
        'front' : 'pages/frontpage/index.php',
        'check' : 'pages/classroom/_hari_ini.php',
    }
    
    # init login credential
    def __init__(self, username, password, message):
        self.username = username
        self.password = password
        self.message  = message

    def view_frontpage(self):
        url = self.base_url + self.path['front']
        return s.get(url).text
    
    def login(self):
        url = self.base_url + self.path['login']
        _data = {
            'userName' : self.username,
            'password' : self.password
        }
        r = s.post(url, data=_data)
        
        # isLoggedIn
        if self.username in self.view_frontpage():
            return True

        return False

    def parse_table(self, response):
        data = BeautifulSoup(response, 'html.parser')
        tables = data.findAll('div', attrs={
            'class' : 'table-responsive'
        })

        result = []
        for table in tables:
            for rows in table.findAll('tr')[1:]:
                cols = rows.findAll('td')
                temp = []
                for col in cols:
                    temp.append(col.text.strip())
                    __a = col.find('a')
                    if __a:
                        temp.append(__a['href'].split("=")[1])
                result.append(temp)

        return result

    def do_absen(self, enroll_id):
        print(f"[!] Enroll ID : {enroll_id}")
        
        __url = self.base_url + self.path['absen'] + str(enroll_id)
        _data = {
            'isiPesan' : self.message,
            'submit' : 'pesan'
        }
        s.post(__url, data=_data)

    def start(self):
        if self.login():
            print('[!] Login: Success!')
        else:
            print('[!] Login: Failed!')
            return False
            
        __url = self.base_url + self.path['check']
        _data = s.get(__url).text
        _data = self.parse_table(_data)
        
        st  = lambda s: s.split(":")[0]
        now = datetime.now()

        for _d in _data:
            print(f" {_d[0]}- {_d[6]}\t | {st(_d[4])}-{st(_d[5])} | {_d[7]}")
            # kosek
            if _d[9] != 'berakhir' and (_d[4] == now.strftime("%H") and (_d[5] < now.strftime("%M") or _d[5] == now.strftime("%M"))):
                self.do_absen(_d[-1])        
        return True

if __name__ == "__main__":
    siswa = ELearning('username', 'password', 'pesan_absen')
    siswa.start()
    
