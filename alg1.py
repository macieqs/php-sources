import http.client
import json
import random
import sys
import time
import logging
import pprint

log = logging.getLogger('grot-client')

SERVER = 'grot-lukaszjagodzinski.c9.io'

if __name__ == '__main__':
    token = sys.argv[1]  # your Access Token
    game = sys.argv[2]  # 0 (development mode), 1 (duel), 2 (contest)

    time.sleep(random.random())

    # connect to the game server
    client = http.client.HTTPConnection(SERVER, 80)
    client.connect()

    # block until the game starts
    client.request('GET', '/games/{}/board?token={}'.format(game, token))

    response = client.getresponse()
    '''
    {
        "score": 0,  # obtained points
        "moves": 5,  # available moves
        "moved": [None, None],  # your last choice [x, y]
        "board": [
            [
                {
                    "points": 1,
                    "direction": "up",
                    "x": 0,
                    "y": 0,
                },
                {
                    "points": 0,
                    "direction": "down",
                    "x": 1,
                    "y": 0,
                }
            ],
            [
                {
                    "points": 5,
                    "direction": "right",
                    "x": 0,
                    "y": 1,
                },
                {
                    "points": 0,
                    "direction": "left",
                    "x": 1,
                    "y": 1,
                }
            ]
        ]
    }
    '''

    while response.status == 200:
        data = json.loads(response.read().decode())
        
        def alg():
            
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(data['board'])
            
            fours = []
            
            for y, row in enumerate(data['board']):
                for x, item in enumerate(row):
                    if item['points'] == 4:
                        print(x,y)
                        fours.append([x,y])
                        
            print(fours)
            
            for element in fours[:]:
                x = element[0]
                y = element[1]
                if x == 0 and data['board'][y][x]['direction'] == 'left':
                    fours.remove(element)
                if x == 4 and data['board'][y][x]['direction'] == 'right':
                    fours.remove(element)
                if y == 0 and data['board'][y][x]['direction'] == 'up':
                    fours.remove(element)
                if y == 4 and data['board'][y][x]['direction'] == 'down':
                    fours.remove(element)
            
            print('test')
            print(fours)
            
            if len(fours) == 1:
                return fours[0]
                
            if len(fours) == 0:
                return [random.randint(0, 4),random.randint(0, 4)]
            
            if len(fours) > 1:
                return fours[1]
            
        point = alg()
        print(point)
        
        time.sleep(random.random() * 3 + 1)
        
        #import pdb; pdb.set_trace()
        time.sleep(random.random() * 3 + 1)

        # make your move and wait for a new round
        client.request(
            'POST', '/games/{}/board?token={}'.format(game, token),
            json.dumps({
                'x': point[0],
                'y': point[1],
            })
        )

        response = client.getresponse()