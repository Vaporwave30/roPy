import requests
import json
import re

name = "example_pkg"
roPyHeaders = {'user-agent': 'Mozilla/5.0'}

def getId(username):
    IdResponse = requests.get(f'http://api.roblox.com/users/get-by-username?username={username}')
    return IdResponse.json()['Id']

def getUsername(userId):
    UserResponse = requests.get(f'http://api.roblox.com/users/{userId}')
    if UserResponse.status_code == 200:
        return UserResponse.json()['Username']
    else: 
        return f'Got a {UserResponse.status_code}'


def getRobux(SecurityCookie):
    cookie = requests.cookies.RequestsCookieJar()
    cookie.set('.ROBLOSECURITY', value=SecurityCookie, domain='.roblox.com', path='/')
    RobuxResponse = requests.get('https://api.roblox.com/currency/balance', cookies=cookie)
    if RobuxResponse.status_code == 200:
        return str(RobuxResponse.json()['robux'])
    if RobuxResponse.status_code != 200:
        return '0'

def getUsernameFromCookie(SecurityCookie):
    cookie = requests.cookies.RequestsCookieJar()
    cookie.set('.ROBLOSECURITY', value=SecurityCookie, domain='.roblox.com', path='/')
    UserResponse = requests.get('https://www.roblox.com/mobileapi/userinfo', cookies=cookie, allow_redirects=False)
    sex = UserResponse.text
    outputFile.write(sex + '\n' + '\n')
    if UserResponse.status_code == 200:
        return str(UserResponse.json()['UserName'])
    else:
        return 'No user'

def getCookie(username, password, devicehandle, browserid):
    req = requests.post(
        url='https://api.roblox.com/v2/login',
        json={'username':username, 'password': password},
        headers={'RBX-Device-Handle': devicehandle},
        cookies={"RBXEventTrackerV2": 'browserid='+str(browserid)}
    )
    if req.status_code == 200:
        return req.cookies['.ROBLOSECURITY']
    else:
        return None

def getJoin(userId):
    #this code is really ugly but it works
    joinResponse = requests.get(f'https://www.roblox.com/users/{userId}/profile', headers=roPyHeaders)
    if joinResponse.status_code == 200:
        joinResponseText = joinResponse.text
        joinDateRaw = str(re.search(r'Join Date<p class=text-lead>(.*?)<li class=profile-stat>', joinResponseText).group(0))
        joinDateRa = re.sub('Join Date<p class=text-lead>', '', joinDateRaw)
        joinDate = re.sub('<li class=profile-stat>', '', joinDateRa)
        return joinDate
    if joinResponse.status_code != 200:
        return f'Got a {joinResponse.status_code}'


def verifiedCheck(userId):
    verifiedResponse = requests.get(f'https://api.roblox.com/ownership/hasasset?userId={userId}&assetId=102611803')
    if verifiedResponse.text == 'true':
        return True
    else:
        return False
		
def getRap(userId):
    types = ['Hat', 'HairAccessory', 'FaceAccessory', 'NeckAccessory', 'ShoulderAccessory', 'FrontAccessory', 'BackAccessory', 'WaistAccessory', 'Gear', 'Face']
    rap = 0
    for i in types:
        cursor = ""
        h = rapFunc1(userId, i, cursor)
        if "data" in h:
            for i in h["data"]:
                if 'recentAveragePrice' in i:
                    rap = rap + i['recentAveragePrice']
                if 'nextPageCursor' in h and h['nextPageCursor'] != 'None':
                    cursor = h['nextPageCursor']
                else:
                    break
    return rap

def rapFunc1(userId, i, cursor):
    res = requests.get(f'https://inventory.roblox.com/v1/users/{userId}/assets/collectibles?assetType={i}&limit=100&cursor={cursor}')
    res = res.json()
    return res

