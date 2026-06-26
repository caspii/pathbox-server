import requests
import datetime

key = 'key-4b87291653134a800f45522ab1679d39'
sandbox = 'mg.casparwre.de'
recipient = 'caspar.wrede@gmail.com'
request_url = 'https://api.mailgun.net/v3/{0}/messages'.format(sandbox)


def game_created(game):
    """Send a mail when a game is created"""
    text = "Click me: http://keepthescore.co/game/" + game.read_token
    request = requests.post(request_url, auth=('api', key), data={
        'from': 'KeepTheScore.co <hello@keepthescore.co>',
        'to': recipient,
        'subject': 'Game created: ' + game.game_name,
        'text': text
    })

def status_report(report_text):
    """Send a (daily) report mail"""
    today = datetime.date.today()
    request = requests.post(request_url, auth=('api', key), data={
        'from': 'KeepTheScore.co <hello@keepthescore.co>',
        'to': recipient,
        'subject': 'Daily Report: ' + today.strftime('%d, %b %Y'),
        'text': report_text
    })
