#!/usr/bin/env python3

import sys
import os
import urllib
import re
from pyquery import PyQuery
import json

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

  # data = open("cache_championgg/BardSupport").read()
  data = url("http://champion.gg/champion/%s/%s" % (champ, role))
  page = PyQuery(data)

  patch = page("div.analysis-holder strong")[0].text

  for s in page("script"):
    if not s.text or 'matchupData.champion' not in s.text: continue

    content = re.findall('matchupData.championData = (.*?);\n',
                         s.text, re.DOTALL)[0]
    obj = json.loads(content)

    out = {
      "map" : "any",
      "isGlobalForChampions": False,
      "associatedChampions": [],
      "title": role + " " + patch,
      "priority": False,
      "mode": "any",
      "isGlobalForMpas": True,
      "associatedMaps": [],
      "type": "custom",
      "sortrank": 1,
      "champion": obj["key"],
      "blocks": [],
    }

    trinketItems = makeItems(3340, 3341, 3342)
    consumeItems = makeItems(2003, 2004, 2044, 2043, 2041, 2138, 2137, 2139, 2140)

    skillItems = makeItems(3361, 3362, 3364, 3363, 2003)

    out['blocks'].append({
      "type": "Most Frequent Starters (%.2f%% win - %d games)" % (
        obj["firstItems"]["mostGames"]['winPercent'],
        obj["firstItems"]["mostGames"]['games']),
      "items": getItems(obj["firstItems"]["mostGames"]) + trinketItems
      })

    out['blocks'].append({
      "type": "Highest Win Rate Starters (%.2f%% win - %d games)" % (
        obj["firstItems"]["highestWinPercent"]['winPercent'],
        obj["firstItems"]["highestWinPercent"]['games']),
      "items": getItems(obj["firstItems"]["highestWinPercent"]) + trinketItems
      })

    if obj['items']['mostGames']['items']:
      out['blocks'].append({
        "type": "Most Frequent Build (%.2f%% win - %d games)" % (
          obj["items"]["mostGames"]['winPercent'],
          obj["items"]["mostGames"]['games']),
        "items": getItems(obj["items"]["mostGames"])
        })

    if obj['items']['highestWinPercent']['items']:
      out['blocks'].append({
        "type": "Highest Win Rate Build (%.2f%% win - %d games)" % (
          obj["items"]["highestWinPercent"]['winPercent'],
          obj["items"]["highestWinPercent"]['games']),
        "items": getItems(obj["items"]["highestWinPercent"])
        })

    out['blocks'].append({ "type": "Consumables", "items": consumeItems})

    out['blocks'].append({
      "type": "%s (%.2f%% win - %d games)" % (
        getSkills(obj["skills"]["mostGames"]),
        obj["skills"]["mostGames"]['winPercent'],
        obj["skills"]["mostGames"]['games']),
      "items": skillItems
      })

    out['blocks'].append({
      "type": "%s (%.2f%% win - %d games)" % (
        getSkills(obj["skills"]["highestWinPercent"]),
        obj["skills"]["highestWinPercent"]['winPercent'],
        obj["skills"]["highestWinPercent"]['games']),
      "items": skillItems
      })


    path = os.path.join(outdir, obj['key'], 'Recommended')

    os.makedirs(path, exist_ok=True)

    filename = '%s-%s.json' % (patch, role)

    json.dump(out, open(os.path.join(path, filename), 'wt'), indent=2)


def main(args):
  # buildSet("Khazix", "Jungle", "tmp")
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
