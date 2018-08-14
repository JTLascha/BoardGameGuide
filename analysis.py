lines = []
for i in open("games.txt","r"):
	lines.append(i)

gamesPlayed = set()
games = []
pairs = set()
knownMechanics = set()
class Game:
	def __init__(self,name,rank,complexity,rating,language,cat,partCat,played):
		self.name = name
		self.rank = int(rank)
		self.complexity = float(complexity)
		self.rating = float(rating)
		self.language = float(language)
		self.cat = set(cat)
		self.partCat = set(partCat)
		if played == "1":
			gamesPlayed.add(self)

class Pair:
	def __init__(self,g1,g2):
		self.games = set([g1,g2])
		self.shared = set()
		for cat1 in g1.cat:
			for cat2 in g2.cat:
				if cat1 == cat2:
					self.shared.add(str(cat1))
		self.dist = len(self.shared)

# lines consist of [Game Name],[Rank],[Complexity],[Rating],[Language]-[Comma delimited categories]-[Comma delimited partial categories]-[0/1 for unplayed/played]
for line in lines:
	line = line.split("-")
	for i in range(0,len(line)):
		line[i] = line[i].split(",")
	line[3][0] = line[3][0].strip()
	games.append(Game(line[0][0],line[0][1],line[0][2],line[0][3],line[0][4],line[1],line[2],line[3][0]))

def printAll():
	for g in games:
		print(g.name)
	print()

def findPairs():
	for i in range(0,len(games)):
		for x in range(i + 1, len(games)):
			pairs.add(Pair(games[i],games[x]))

def suggest(learn=False):
	min = None
	minLang = None
	mygames = []
	fam = None
	for g in games:
		if not(learn and g in gamesPlayed):
			if minLang == None:
				minLang = g.language
			elif g.language < minLang:
				minLang = g.language
	for g in games:
		if not(learn and g in gamesPlayed):
			if minLang == g.language:
				mygames.append(g)
	for g in mygames:
		if not (learn and g in gamesPlayed):
			newFam = 0
			for mech in g.cat:
				thisisnew = True
				for known in knownMechanics:
					if mech == known:
						thisisnew = False
				if not thisisnew:
					newFam += 1
			if fam == None:
				fam = newFam
			elif fam < newFam:
				fam = newFam
	strangers = []
	for g in mygames:
		if not (learn and g in gamesPlayed):
			newFam = 0
			for mech in g.cat:
				thisisnew = True
				for known in knownMechanics:
					if mech == known:
						thisisnew = False
				if not thisisnew:
					newFam += 1
			if newFam != fam:
				strangers.append(g)
	for g in strangers:
		mygames.remove(g)

	for g in mygames:
		if not (learn and g in gamesPlayed):
			newMech = 0
			for mech in g.cat:
				thisisnew = True
				for known in knownMechanics:
					if mech == known:
						thisisnew = False
				if thisisnew:
					newMech += 1
			if min == None:
				min = newMech
			elif min > newMech:
				min = newMech

	sug = None
	for g in mygames:
		if not (learn and g in gamesPlayed):
			newMech = 0
			for mech in g.cat:
				thisisnew = True
				for known in knownMechanics:
					if mech == known:
						thisisnew = False
				if thisisnew:
					newMech += 1

			if newMech == min:
				if sug == None:
					sug = g
				else:
					if g.language < sug.language:
						sug = g
					elif g.language == sug.language and g.complexity < sug.complexity:
						sug = g
	if sug != None:
		print(sug.name)
		print(str(min) + " new mechanics: ",end="")
		for mech in sug.cat:
			if not mech in knownMechanics:
				print(mech,end=", ")
		print()
		k = 0
		for mech in sug.cat:
			if mech in knownMechanics:
				k += 1
		print(str(k) + " Known mechanics: ",end="")
		for mech in sug.cat:
			if mech in knownMechanics:
				print(mech,end=", ")
		print()
		print()
	return sug

def learn(gname):
	for g in games:
		if g.name == gname:
			gamesPlayed.add(g)
			for mech in g.cat:
				knownMechanics.add(mech)
			return None

def Plan():
	plan = []
	sug = suggest(learn=True)
	while sug != None:
		plan.append(sug.name)
		learn(sug.name)
		sug = suggest(learn=True)
	print()

def showPairs(g):
	mypairs = set()
	orderedPairs = []
	orderedDist = []
	orderedShare = []
	for p in pairs:
		for ga in p.games:
			if ga.name == g:
				mypairs.add(p)

#sort the pairs by number of shared mechanics
	while len(mypairs) > 0:
		maxSet = set()
		max = 0
		for p in mypairs:
			if p.dist > max:
				max = p.dist

		toRemove = []
		for p in mypairs:
			if p.dist == max:
				maxSet.add(p)
				toRemove.append(p)
		for p in toRemove:
			mypairs.remove(p)

		#sort maxSet further based on complexity and language
		toRemove = []
		for p in maxSet:
			for ga in p.games:
				if ga.name != g:
					orderedPairs.append(ga.name)
					orderedDist.append(p.dist)
					orderedShare.append(p.shared)
					toRemove.append(p)
		for p in toRemove:
			maxSet.remove(p)

	for i in range(0,len(orderedPairs)):
		print(orderedPairs[i] + " has " + str(orderedDist[i]) + " shared mechanics.")
		print("They are:",end=" ")
		for s in orderedShare[i]:
			print(s,end=", ")
		print()
		print()

findPairs()
RUNNING = True
while RUNNING:
	inp = input("Enter a command: ").split(",")
	print()
	if inp[0] == "print":
		printAll()
	elif inp[0] == "quit":
		RUNNING = False
	elif inp[0] == "findpairs":
		findPairs()
	elif inp[0] == "compare":
		if len(inp) > 1:
			showPairs(inp[1])
	elif inp[0] == "plan":
		Plan()
	elif inp[0] == "suggest":
		suggest(learn=True)
	elif inp[0] == "learn":
		if len(inp) > 1:
			learn(inp[1])
	elif inp[0] == "help":
		print("print - print names of all games")
		print("compare,[GAME NAME] - compare all games to the selected game")
		print("plan - create a plan to learn your unplayed games")
		print("suggest - Suggest the next game to play based on which mechanics your group is familiar with.")
		print("learn,[GAME NAME] - mark the chosen game as learned (for this session only)")
		print("quit -  exit the program")
		print()
	else:
		print("Invalid Command.(type 'help' to see a list of commands)")
