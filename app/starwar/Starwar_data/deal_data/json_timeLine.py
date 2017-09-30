#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

films = []
characters = []
planets = []
starships = []
vehicles = []
species = []

with open('../csv/films.txt', 'r') as fr:
    for line in fr:
        tmp = json.loads(line.strip('\n'))
        films.append(tmp)
with open('../csv/characters.txt', 'r') as fr:
    for line in fr:
        tmp = json.loads(line.strip('\n'))
        characters.append(tmp)
with open('../csv/planets.txt', 'r') as fr:
    for line in fr:
        tmp = json.loads(line.strip('\n'))
        planets.append(tmp)
with open('../csv/starships.txt', 'r') as fr:
    for line in fr:
        tmp = json.loads(line.strip('\n'))
        starships.append(tmp)
with open('../csv/vehicles.txt', 'r') as fr:
    for line in fr:
        tmp = json.loads(line.strip('\n'))
        vehicles.append(tmp)
with open('../csv/species.txt', 'r') as fr:
    for line in fr:
        tmp = json.loads(line.strip('\n'))
        species.append(tmp)

data = []
for item in characters:
    tmp = []
    for film in films:
        flag = False
        for f in film['characters']:
            if item['url'] == f:
                flag = True
                break
        if flag:
            tmp.append(1)
        else:
            tmp.append(0)

    data.append({
        'name': item['name'],
        'type': 'character',
        'group': 0,
        'vector': tmp
    })
for item in planets:
    tmp = []
    for film in films:
        flag = False
        for f in film['planets']:
            if item['url'] == f:
                flag = True
                break
        if flag:
            tmp.append(1)
        else:
            tmp.append(0)

    data.append({
        'name': item['name'],
        'type': 'planet',
        'group': 1,
        'vector': tmp
    })
for item in starships:
    tmp = []
    for film in films:
        flag = False
        for f in film['starships']:
            if item['url'] == f:
                flag = True
                break
        if flag:
            tmp.append(1)
        else:
            tmp.append(0)

    data.append({
        'name': item['name'],
        'type': 'starship',
        'group': 2,
        'vector': tmp
    })
for item in vehicles:
    tmp = []
    for film in films:
        flag = False
        for f in film['vehicles']:
            if item['url'] == f:
                flag = True
                break
        if flag:
            tmp.append(1)
        else:
            tmp.append(0)

    data.append({
        'name': item['name'],
        'type': 'vehicle',
        'group': 3,
        'vector': tmp
    })
for item in species:
    tmp = []
    for film in films:
        flag = False
        for f in film['species']:
            if item['url'] == f:
                flag = True
                break
        if flag:
            tmp.append(1)
        else:
            tmp.append(0)

    data.append({
        'name': item['name'],
        'type': 'specie',
        'group': 4,
        'vector': tmp
    })

films = [[films[x]['title'], films[x]['release_date']] for x in xrange(0, len(films))]

result = {
    'films': films,
    'data': data
}

with open('../templates/timeline.json', 'w') as fw:
    fw.write(json.dumps(result))
