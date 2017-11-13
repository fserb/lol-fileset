#!/usr/bin/env pypy3

import os
import sys
import json
import itertools

TYPES = list("PDSRI")
ALLPERKS = []

for t in TYPES:
  for s in itertools.product('0123', repeat=4):
    for t2 in TYPES:
      for s2 in itertools.product('0123', repeat=3):
        ALLPERKS.append(t+''.join(s)+' '+t2+''.join(s2))

def findRunes(data, champs):
  validchamps = [ c for c in champs if c in data ]
  combs = set(data[c] for c in validchamps)
  votes = {}

  print(combs)

  for p in ALLPERKS:
    score = 0.0
    for c in combs:
      s = 0.0
      if c[0] == p[0]:
        if c[1] == p[1]: s += 5
        if c[2] == p[2]: s += 1
        if c[3] == p[3]: s += 1
        if c[4] == p[4]: s += 1
      if c[6] == p[6]:
        if c[7] == p[7]: s += 1
        if c[8] == p[8]: s += 1
        if c[9] == p[9]: s += 1
      score += 100*s/11.0
    votes[p] = score/len(combs)

  vk = sorted(votes.keys(), key=lambda a: votes[a], reverse=True)
  for k in vk[:10]:
    print (k, votes[k])



def main(args):
  print("Finding optimal runes/masteries:\n")

  GROUPS = {}

  GROUPS['ADC'] = ['Jinx/ADC', 'Kalista/ADC', 'Corki/ADC', 'Vayne/ADC', 'Tristana/ADC', 'Sivir/ADC', 'Caitlyn/ADC', 'Varus/ADC', 'Quinn/ADC', 'Lucian/ADC']
  GROUPS['APMid'] = ['Annie/Middle', 'Heimerdinger/Middle', 'Leblanc/Middle', 'Malzahar/Middle', 'Orianna/Middle', 'Brand/Middle', 'Cassiopeia/Middle', 'Lissandra/Middle', 'Zyra/Middle', 'Ahri/Middle', 'Katarina/Middle', 'Karma/Middle', 'Fizz/Middle', 'Ziggs/Middle', 'Lux/Middle', 'Swain/Middle', 'Diana/Middle', 'Velkoz/Middle', 'Xerath/Middle', 'Veigar/Middle', 'Chogath/Middle', 'Karthus/Middle', 'TwistedFate/Middle', 'Morgana/Middle', 'Azir/Middle', 'Ekko/Middle', 'Nidalee/Middle']
  GROUPS['ADMid'] = ['Varus/Middle', 'Talon/Middle','Jayce/Middle', 'Zed/Middle' ]
  GROUPS['TankSupport'] = ['Leona/Support', 'Thresh/Support' ]
  GROUPS['APSupport'] = ['Morgana/Support', 'Annie/Support', 'Karma/Support', 'Sona/Support', 'Teemo/Support']

  GROUPS['ADJungle'] = [ 'MasterYi/Jungle', 'Tryndamere/Jungle', 'Udyr/Jungle', 'Jax/Jungle', 'RekSai/Jungle', 'Warwick/Jungle', 'Pantheon/Jungle', 'Vi/Jungle', 'Nocturne/Jungle' ]
  GROUPS['TankJungle'] =  [ 'Volibear/Jungle', 'Udyr/Jungle', 'Shyvana/Jungle', 'Sejuani/Jungle', 'Trundle/Jungle']
  GROUPS['APJungle'] =  [ 'Nidalee/Jungle', 'Diana/Jungle', 'Gragas/Jungle', 'Amumu/Jungle' ]

  GROUPS['ADTop'] = [ 'Irelia/Top', 'Quinn/Top', 'Nasus/Top', 'Poppy/Top', 'Darius/Top', 'Jayce/Top', 'Tryndamere/Top', 'Fizz/Top', 'Hecarim/Top', 'Jax/Top', 'Pantheon/Top', 'Fiora/Top' ]
  GROUPS['TankTop'] = [ 'Volibear/Top', 'Poppy/Top', 'DrMundo/Top', 'Renekton/Top', 'Trundle/Top', 'Garen/Top', 'Hecarim/Top']
  GROUPS['APTop'] = [ 'Ekko/Top', 'Swain/Top', 'Heimerdinger/Top', 'Rumble/Top', 'Lissandra/Top', 'Chogath/Top', 'Malphite/Top', 'Teemo/Top']

  runes = json.load(open("runes.json"))

  for role in [ 'ADC', 'Middle', 'Top', 'Jungle', 'Support' ]:
    GROUPS['base/' + role] = [ x for x in runes.keys() if x.endswith(role) ]

  for g in sorted(GROUPS):
    print("==========", g, "=========")
    findRunes(runes, GROUPS[g])
    print()


if __name__ == '__main__':
  sys.exit(main(sys.argv))
