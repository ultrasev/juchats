
class APIS(object):
    MODES = 'https://www.hermchats.com/gw/chatweb/gpt/modes'
    WSS='wss://www.hermchats.com/gw/chatgpt/ws/{}'
    DIALOGS='https://www.hermchats.com/gw/chatweb/gpt/dialogs'
    CREATE_DIALOG='https://www.hermchats.com/gw/chatweb/gpt/createDialog'


HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'dnt': '1',
    'noninductive': 'true',
    'origin': 'https://www.hermchats.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.hermchats.com/chat/MTE0NTEK',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}
