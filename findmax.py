#!/usr/bin/env pypy3

import os
import sys
import json
import itertools


def printMasteries(m):
  counts = "%d/%d/%d" % (sum(x for x in m[:20]), sum(x for x in m[20:39]), sum(x for x in m[39:]))
  print(counts)

  c = lambda x: '.' if x == 0 else x

  print('%s%s%s%s %s%s%s%s %s%s%s%s' % (c(m[0]), c(m[1]), c(m[2]), c(m[3]),
                                        c(m[20]), c(m[21]), c(m[22]), c(m[23]),
                                        c(m[39]), c(m[40]), c(m[41]), c(m[42])))
  print('%s%s%s%s %s%s %s  %s%s%s' % (c(m[4]), c(m[5]), c(m[6]), c(m[7]),
                                      c(m[24]), c(m[25]), c(m[26]),
                                      c(m[43]), c(m[44]), c(m[45])))
  print('%s%s%s%s %s%s%s%s %s%s%s%s' % (c(m[8]), c(m[9]), c(m[10]), c(m[11]),
                                        c(m[27]), c(m[28]), c(m[29]), c(m[30]),
                                        c(m[46]), c(m[47]), c(m[48]), c(m[49])))
  print('%s%s%s%s %s%s%s%s %s%s%s%s' % (c(m[12]), c(m[13]), c(m[14]), c(m[15]),
                                        c(m[31]), c(m[32]), c(m[33]), c(m[34]),
                                        c(m[50]), c(m[51]), c(m[52]), c(m[53])))
  print('%s%s %s %s%s%s   %s%s ' % (c(m[16]), c(m[17]), c(m[18]),
                                   c(m[35]), c(m[36]), c(m[37]),
                                   c(m[54]), c(m[55])))
  print(' %s    %s    %s  ' % (c(m[19]), 
                               c(m[38]),
                               c(m[56])))


def findMasteries(data, champs=None, number=1):
  validchamps = [ c for c in champs if data[c] ]  
  combs = set(tuple(data[c]) for c in validchamps)
  minscore = 1e99
  bestmast = None
  print(len(combs))

  for mset in itertools.combinations(combs, min(number, len(combs))):
    score = 0.0
    for c in validchamps:
      score += min(
        sum([abs(r[i] - data[c][i]) for i in range(57)]) for r in mset)/30.0
    score /= len(validchamps)
    if score < minscore:
      minscore = score
      bestmast = mset

  print("match: %.0f%%" % (100*(1-minscore)))
  for r in bestmast:
    printMasteries(r)


def findRunes(data, champs, number=1):
  validchamps = [ c for c in champs if data[c] ]
  combs = set(tuple(data[c]) for c in validchamps)
  minscore = 1e99
  bestrunes = None

  for runeset in itertools.combinations(combs, min(number, len(combs))):
    score = 0.0
    for c in validchamps:
      score += min(4 - sum([1 if r[i] == data[c][i] else 0 for i in range(4)])
        for r in runeset)/4.0
    score /= len(validchamps)
    if score < minscore:
      minscore = score
      bestrunes = runeset

  print("match: %.0f%%" % (100*(1-minscore)))
  for r in bestrunes:
    print(' - '.join(r))


def main(args):
  print("Finding optimal runes/masteries:\n")

  GROUPS = {}
  NUMS = {}

  GROUPS['ADC'] = ['Jinx/ADC', 'Kalista/ADC', 'Corki/ADC', 'Vayne/ADC', 'Graves/ADC', 'Tristana/ADC', 'Sivir/ADC', 'Caitlyn/ADC', 'Varus/ADC', 'Quinn/ADC', 'Lucian/ADC']
  GROUPS['APMid'] = ['Annie/Middle', 'Heimerdinger/Middle', 'Leblanc/Middle', 'Malzahar/Middle', 'Orianna/Middle', 'Brand/Middle', 'Cassiopeia/Middle', 'Lissandra/Middle', 'Zyra/Middle', 'Ahri/Middle', 'Katarina/Middle', 'Karma/Middle', 'Fizz/Middle', 'Ziggs/Middle', 'Lux/Middle', 'Swain/Middle', 'Diana/Middle', 'Velkoz/Middle', 'Xerath/Middle', 'Veigar/Middle', 'Chogath/Middle', 'Karthus/Middle', 'TwistedFate/Middle', 'Morgana/Middle', 'Azir/Middle', 'Ekko/Middle', 'Nidalee/Middle']
  NUMS['APMid'] = (1, 2)
  GROUPS['ADMid'] = ['Varus/Middle', 'Talon/Middle','Jayce/Middle', 'Zed/Middle' ]
  GROUPS['TankSupport'] = ['Leona/Support', 'Thresh/Support' ]
  NUMS['TankSupport'] = (1, 2)
  GROUPS['APSupport'] = ['Morgana/Support', 'Annie/Support', 'Karma/Support', 'Sona/Support']

  GROUPS['ADJungle'] = [ 'MasterYi/Jungle', 'Tryndamere/Jungle', 'Udyr/Jungle', 'Jax/Jungle', 'RekSai/Jungle', 'Warwick/Jungle', 'Pantheon/Jungle', 'Vi/Jungle', 'Nocturne/Jungle' ]
  GROUPS['TankJungle'] =  [ 'Volibear/Jungle', 'Udyr/Jungle', 'Shyvana/Jungle', 'Sejuani/Jungle', 'Trundle/Jungle']
  GROUPS['APJungle'] =  [ 'Nidalee/Jungle', 'Diana/Jungle', 'Gragas/Jungle', 'Amumu/Jungle' ]

  GROUPS['ADTop'] = [ 'Irelia/Top', 'Quinn/Top', 'Nasus/Top', 'Poppy/Top', 'Darius/Top', 'Jayce/Top', 'Tryndamere/Top', 'Fizz/Top', 'Hecarim/Top', 'Jax/Top', 'Pantheon/Top', 'Fiora/Top' ]
  GROUPS['TankTop'] = [ 'Volibear/Top', 'Poppy/Top', 'DrMundo/Top', 'Renekton/Top', 'Trundle/Top', 'Garen/Top', 'Hecarim/Top']
  NUMS['TankTop'] = (1, 2)
  GROUPS['APTop'] = [ 'Ekko/Top', 'Swain/Top', 'Heimerdinger/Top', 'Rumble/Top', 'Lissandra/Top', 'Chogath/Top', 'Malphite/Top' ]

  runes = json.load(open("runes.json"))
  masteries = json.load(open("masteries.json"))

  for role in [ 'ADC', 'Middle', 'Top', 'Jungle', 'Support' ]:
    GROUPS['base/' + role] = [ x for x in runes.keys() if x.endswith(role) ]

  for g in sorted(GROUPS):
    print("==========", g, "=========")
    num = NUMS.get(g, (1,1))
    findRunes(runes, GROUPS[g], num[0])
    findMasteries(masteries, GROUPS[g], num[1])
    print()


if __name__ == '__main__':
  sys.exit(main(sys.argv))

