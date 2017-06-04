#!/usr/bin/env python3

"""
- freq starter missing potions
- consumables missing stuff:
  - potion, ward, 3 elixirs, 3 potions
- merge order on consumables
"""

import sys
import os
import urllib
import re
from pyquery import PyQuery
import json

RIOT = {}

def initRiot():
  RIOT.update(json.load(open("riot/rune.json"))['data'])
  RIOT.update(json.load(open("riot/mastery.json"))['data'])
  RIOT.update(json.load(open("riot/item.json"))['data'])


def url(url):
  user_agent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 ' +
                '(KHTML, like Gecko) Ubuntu/12.04 Chromium/18.0.1025.168 ' +
                'Chrome/18.0.1025.168 Safari/535.19')
  u = urllib.request.urlopen(urllib.request.Request(url,
    headers={'User-Agent': user_agent}))
  return u.read()


def makeItems(*data):
  out = []
  for i in data:
    out.append({"count": 1, "id": str(i)})
  return out


def getItems(obj):
  out = []
  counts = {}
  for o in obj["items"]:
    id = o["id"] if o['id'] != 2010 else 2003
    if id not in counts:
      counts[id] = 0
    counts[id] += 1
  added = set()
  for o in obj["items"]:
    id = o["id"] if o['id'] != 2010 else 2003
    if id in added: continue
    added.add(id)
    out.append({"count": counts[id], "id": str(id)})
  return out


def getRunes(champ, role, obj):
  r = obj['mostGames']['runes']

  if os.path.isfile('runes.json'):
    js = json.load(open("runes.json", 'rt'))
  else:
    js = {}
  js['%s/%s' % (champ, role)] = [ RIOT[x['id']]['name'] for x in r ]
  json.dump(js, open(os.path.join('runes.json'), 'wt'),
    sort_keys=True, indent=2)


def getMasteries(champ, role, obj):
  points = {}
  if not 'mostGames' in obj or not 'masteries' in obj['mostGames']:
    return
  for row in obj['mostGames']['masteries']:
    for d in row['data'].values():
      for m in d:
        if m['mastery']:
          points[m['mastery']] = m['points']
  if os.path.isfile('masteries.json'):
    js = json.load(open("masteries.json", 'rt'))
  else:
    js = {}
  js['%s/%s' % (champ, role)] = [ int(points[x]) for x in sorted(points) ]
  json.dump(js, open(os.path.join('masteries.json'), 'wt'),
    sort_keys=True, indent=2)

def getSkills(obj):

  seq = "".join(" QWER"[int(x[0])] for x in obj["order"])

  initial = seq[:3]
  if 'Q' not in initial or 'W' not in initial or 'E' not in initial:
    initial = seq[:4]

  final = list('QWE')
  final.sort(key = lambda x: seq.rfind(x))
  final = ''.join(final)

  extra = ""
  if any('^' in x for x in obj['order']):
    extra = " (R:"
    for o in obj['order']:
      if '^' in o:
        extra += " QWER"[int(o[2])]
    extra += ")"

  return '%s -> %s%s' % (initial, final, extra)


def buildSet(champ, role, outdir):
  print("Building for %s/%s" % (champ, role))

  data = url("http://champion.gg/champion/%s/%s" % (champ, role))
  # data = open('AatroxTop').read()
  page = PyQuery(data)

  patch = page("div.analysis-holder strong")[0].text

  for s in page("script"):
    if not s.text or 'matchupData.champion' not in s.text: continue

    content = re.findall('matchupData.championData = (.*?)\n',
                         s.text, re.DOTALL)[0]
    obj = json.loads(content)
    # print(json.dumps(obj, indent=2))

    getRunes(champ, role, obj['runes'])
    getMasteries(champ, role, obj['masteries'])

    out = {
      "map" : "any",
      "isGlobalForChampions": False,
      "associatedChampions": [],
      "title": role + " " + patch,
      "priority": False,
      "mode": "any",
      "isGlobalForMaps": True,
      "associatedMaps": [],
      "type": "custom",
      "sortrank": 1,
      "champion": obj["key"],
      "blocks": [],
    }

    trinketItems = makeItems(3340, 3341, 3363, 3364, 3363)
    visionTrinket = makeItems(3340)
    consumeItems = makeItems(2003, 2055, 2031, 2032, 2033, 2138, 2139, 2140)

    if obj['firstItems']['mostGames']['items']:
      out['blocks'].append({
        "type": "Most Frequent Starters (%d%% win - %d games)" % (
          100*obj["firstItems"]["mostGames"]['winPercent'],
          obj["firstItems"]["mostGames"]['games']),
        "items": getItems(obj["firstItems"]["mostGames"]) + visionTrinket
        })

    if obj['firstItems']['highestWinPercent']['items']:
      out['blocks'].append({
        "type": "Highest Win Rate Starters (%d%% win - %d games)" % (
          100*obj["firstItems"]["highestWinPercent"]['winPercent'],
          obj["firstItems"]["highestWinPercent"]['games']),
        "items": getItems(obj["firstItems"]["highestWinPercent"]) + visionTrinket
        })

    if obj['items']['mostGames']['items']:
      out['blocks'].append({
        "type": "Most Frequent Build (%d%% win - %d games)" % (
          100*obj["items"]["mostGames"]['winPercent'],
          obj["items"]["mostGames"]['games']),
        "items": getItems(obj["items"]["mostGames"])
        })

    if obj['items']['highestWinPercent']['items']:
      out['blocks'].append({
        "type": "Highest Win Rate Build (%d%% win - %d games)" % (
          100*obj["items"]["highestWinPercent"]['winPercent'],
          obj["items"]["highestWinPercent"]['games']),
        "items": getItems(obj["items"]["highestWinPercent"])
        })

    mostSkill = "%s (%d%% win - %d games)" % (
      getSkills(obj["skills"]["mostGames"]),
      100*obj["skills"]["mostGames"].get('winPercent', 0),
      obj["skills"]["mostGames"].get('games', 0))
    highSkill = "%s (%d%% win - %d games)" % (
      getSkills(obj["skills"]["highestWinPercent"]),
      100*obj["skills"]["highestWinPercent"].get('winPercent', 0),
      obj["skills"]["highestWinPercent"].get('games', 0))

    out['blocks'].append({ "type": "Consumables %s" % mostSkill, "items": consumeItems})
    out['blocks'].append({ "type": highSkill, "items": trinketItems})

    path = os.path.join(outdir, obj['key'], 'Recommended')

    os.makedirs(path, exist_ok=True)

    filename = '%s.json' % (role)

    json.dump(out, open(os.path.join(path, filename), 'wt'),
      sort_keys=True, indent=2)


def main(args):
  initRiot()

  # buildSet("Aatrox", "Top", "tmp")
  # return 0

  if len(args) < 2:
    print("usage: %s <outputdir>" % args[0])
    return 1
  outdir = args[1]

  print("Generating item sets for all champions...")

  index = url("http://champion.gg")
  page = PyQuery(index)

  for el in page("div.champ-index-img a"):
    href = el.get('href')
    names = href.split('/')[1:]
    if len(names) == 2: continue
    buildSet(names[1], names[2], outdir)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
