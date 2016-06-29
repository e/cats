#!/usr/bin/python
import json
import random


# 10000 turns
MAX_TURNS = 10000


class CatFinder:
    def __init__(self, n=10):
        self.n = n
        self.closed_stations = []
        self.stations = []
        self.connections = {}
        self.visited_stations = {}
        self.found_cats = []
        self.locked_cats = []
        self.average = 0
        self.max_turns = MAX_TURNS

    def read_map(self):
        with open('tfl_stations.json') as f:
            stations = json.loads(f.read())
        with open('tfl_connections.json') as f:
            raw_connections = json.loads(f.read())
        connections = {}
        for item in raw_connections:
            if connections.get(int(item[0])):
                connections[int(item[0])].append(int(item[1]))
            else:
                connections[int(item[0])] = [int(item[1])]
            if connections.get(int(item[1])):
                connections[int(item[1])].append(int(item[0]))
            else:
                connections[int(item[1])] = [int(item[0])]
        self.stations = stations
        self.connections = connections
        return stations, connections

    def spread_creatures(self, stations=[]):
        monkey_locations = {}
        for i in range(1, self.n + 1):
            monkey = i
            location = random.choice(self.connections.keys())
            monkey_locations[monkey] = location
        cat_locations = {}
        for i in range(1, self.n + 1):
            cat = i
            location = random.choice(self.connections.keys())
            cat_locations[cat] = location
        self.monkey_locations = monkey_locations
        self.cat_locations = cat_locations
        return monkey_locations, cat_locations

    def move_cat(self, cat):
#        print 'cat:'
#        print cat
#        print 'cat location:'
#        print self.cat_locations[cat]
#        print 'connections:'
#        print self.connections
#        print 'connections for cat:'
#        print self.connections.get(self.cat_locations[cat])
        if not self.connections.get(self.cat_locations[cat]):
            self.locked_monkeys.append(owner)
            return
        possible_destinations = [
            dest for dest in self.connections[self.cat_locations[cat]] 
            if dest not in self.closed_stations
        ]
        if len(possible_destinations) == 0:
            self.locked_cats.append(cat)
            # print 'cat locked'
            return
        dest = random.choice(possible_destinations)
        self.cat_locations[cat] = dest
        return cat, dest

    # We will use "owner" as stated in the problem although monkeys do not 
    # actually "own" cats, or viceversa, in our humble opinion
    def move_monkey(self, owner):
        if not self.connections.get(self.monkey_locations[owner]):
            # print 'monkey locked'
            return
        possible_destinations = [
            dest for dest in self.connections[self.monkey_locations[owner]] 
            if dest not in self.closed_stations
        ]
        if self.visited_stations.get(owner):
            if (len(self.visited_stations[owner]) <
                     len(possible_destinations) - 1:
                possible_destinations = [
                    dest for dest in possible_destinations
                    if dest not in self.visited_stations[owner]
                ]
        if len(possible_destinations) == 0:
            # print 'monkey locked'
            return
        dest = random.choice(possible_destinations)
        self.monkey_locations[owner] = dest
        if self.visited_stations.get(owner):
            if len(self.visited_stations[owner]) < len(possible_destinations):
                self.visited_stations[owner].append(dest)
        else:
            self.visited_stations[owner] = [dest]
        if len(self.visited_stations[owner]) == len(possible_destinations):
            self.visited_stations [owner] = []
        return owner, dest

    def search_cats(self):
        for cat in self.cat_locations:
            self.move_cat(cat)
        for monkey in self.monkey_locations:
            self.move_monkey(monkey)
            if self.monkey_locations[monkey] == self.cat_locations[monkey]:
                self.closed_stations.append(self.monkey_locations[monkey])
                self.found_cat_callback(
                        monkey, self.stations[self.monkey_locations[monkey]])
        for cat in self.found_cats + self.locked_cats:
            monkey = cat
            try:
                del self.cat_locations[cat]
                del self.monkey_locations[monkey]
            except KeyError:
                pass

    def found_cat_callback(self, monkey, station):
        cat = monkey
        self.found_cats.append(cat)
        print ('Monkey %d found cat %d - %s is now closed' %
                (monkey, monkey, station))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("n", help="Number of cats", type=int)
    args = parser.parse_args()
    cat_finder = CatFinder(args.n)
    cat_finder.read_map()
    cat_finder.spread_creatures(cat_finder.stations)
    # 10000 turns
    for i in range(cat_finder.max_turns):
        if not cat_finder.cat_locations:
            break
        # print 'cat_locations:'
        # print cat_finder.cat_locations
        cat_finder.search_cats()
        # print cat_finder.cat_locations
    print('Total number of cats: %d' % cat_finder.n)
    print('Number of cats found: %d' % len(cat_finder.found_cats))
    average = float(i) / len(cat_finder.found_cats)
    print('Average number of movements required to find a cat: %d' % average)
