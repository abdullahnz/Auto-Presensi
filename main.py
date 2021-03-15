#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests, json

s = requests.Session()

class ELearning:
    # base url
    BASE = 'https://siswa.smkn2solo.sch.id/'

    # usefull path
    URL  = {
        'login'   : BASE + 'pages/auth/checkLogin.php',
        'absen'   : BASE + 'pages/classroom/enroll.php?id=',
        'front'   : BASE + 'pages/frontpage/index.php',
        'check'   : BASE + 'pages/classroom/_hari_ini.php',
        'discuss' : BASE + 'pages/classroom/ajax/getDiscussion.php?id=',
    }

    IS_STARTED = 'sedang berlangsung'
    
    # Constructor
    def __init__(self, username, password, message):
        self.username = username
        self.password = password
        self.message  = message

    def getFrontpage(self):
        return s.get(self.URL['front']).text
    
    def doLogin(self):
        print(f'INFO: Trying to login with user \'{self.username}\' ... ')
        
        data = {
            'userName' : self.username,
            'password' : self.password
        }
        
        s.post(self.URL['login'], data=data)
        
        # Check with goto front page.
        if self.username in self.getFrontpage():
            return True

        return False

    def getDiscussion(self, enroll_id):
        # Get source data of discussion page by enroll_id.
        content = s.get(self.URL['discuss'] + str(enroll_id)).text
        content = BeautifulSoup(content, 'html.parser')
        
        result = {}

        for i, td in enumerate(content.find_all('td')):
            # Remove empty first index
            cols = td.text.splitlines()[1:]

            # This contains username, date, and time
            info = cols[-1].split()

            # Separate message with another information data (info)
            message = ' '.join(cols[:-1])

            # Parsing and convert to dictionary data
            result[i] = {
                'from' : info[3],
                'message' : message.strip(),
                'day' : ' '.join(info[0:2]),
                'time' : info[2],
            }

        return result

    def printInfoSubject(self, data):
        result  = f"\nINFO: {data['mapel']} (ID: {data['enroll_id']})\n"
        result += f"      Guru   : {data['guru']}\n"
        result += f"      Time   : {data['time_start']} - {data['time_end']}\n"
        result += f"      Status : {data['status']}\n"
        result += f"      Materi : {data['materi']}"
        print(result)

    def parseTable(self, content):
        content = BeautifulSoup(content, 'html.parser')
        tables  = content.findAll('div', attrs={
            'class' : 'table-responsive'
        })

        result = {}

        for table in tables:
            # Loop all rows
            for rows in table.findAll('tr')[1:]:
                # Get all cols from row
                cols = rows.findAll('td')
                temp = []
                for col in cols:
                    # Add all subject's data from col's field.
                    temp.append(col.text.strip())
                    
                    # Get subject's enroll_id
                    __a = col.find('a')
                    if __a:
                        temp.append(__a['href'].split("=")[1])
                
                # Parse and convert to dictionary.
                result[temp[0]] = {
                    'day'      : temp[1],    'date'   : temp[2],     'time_start' : temp[4],
                    'time_end' : temp[5],    'mapel'  : temp[6],     'guru'       : temp[7],
                    'status'   : temp[9],    'enroll_id' : temp[10], 'materi'     : temp[8].replace('\n', " | "),
                }

        return result

    def doAbsent(self, enroll_id):
        # Prepare target url
        path = self.URL['absen'] + str(enroll_id)

        # Init post data
        data = {
            'isiPesan' : self.message,
            'submit' : 'pesan'
        }
        
        # Post absen requests data.
        s.post(path, data=data)
        
        # Get all discussions on a subjects by enroll_id.
        discuss = self.getDiscussion(enroll_id)

        # Printing all of discuss info to user.
        for i in range(len(discuss)):
            print(f"   - [{discuss[i]['time']}] \"{discuss[i]['message']}\" (from: {discuss[i]['from'].split('@')[0]})")

    def run(self):
        # Do login and check if the user isLoggedIn successfully.
        # It will return / exit if the user can't login.
        if self.doLogin():
            print(f'INFO: Successfully login with username \'{self.username}\'.')
        else:
            print(f'WARN: Login failed, check your login credentials or your connection, then try again.')
            return False
        
        # Just info message like debug :)
        print('INFO: Checking \'mapel\' for today ...')
        
        # Check, get and parse subject data for today.
        subData = s.get(self.URL['check']).text
        subData = self.parseTable(subData)

        # Just info message like debug again :)
        print(f'INFO: Found {len(subData)} mapel for today.')
        
        # Checking and do absen if the subject is started.
        for i in range(len(subData)):
            # Calculate keys dictionary data.
            keys = f"{i+1}"
            
            # Get dictionary data by keys
            data = subData[keys]

            # Print out info of the data.
            self.printInfoSubject(data)
            
            if data['status'] == self.IS_STARTED:
                # Just info message like debug again and again :)
                print(f'\nINFO: Do absen and get all discussion (ID: {data["enroll_id"]})')
                
                # Do absen
                self.doAbsent(data['enroll_id'])
        return True

if __name__ == "__main__":
    siswa = ELearning('username@smkn2-solo.net', 'password', 'pesan_hadir - Hadir')
    siswa.run()
    
