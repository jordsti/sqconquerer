__author__ = 'JordSti'
import sys

if __name__ == '__main__':
    print "SqConquerer Test Script"

    gen_map = False
    net_player = False

    for a in sys.argv:
        if a == '-map_generate':
            print "Map Generation testing"
            gen_map = True
        elif a == '-net_player':
            print "Net Player testing"
            net_player = True

    if gen_map:
        from generator import map_generator
        from map import game_map

        gen = map_generator()
        gen.generate(10)

        map = gen.map

        mt = map.to_string()
        print mt

    if net_player:
        #creating 4 players to test

        from player import net_player

        players = []
        players.append(net_player("jordsti", None))
        players.append(net_player("joshua", None))
        players.append(net_player("john", None))
        players.append(net_player("marcel", None))

        for p in players:
            print p.name, p.player_id, p.get_key()
