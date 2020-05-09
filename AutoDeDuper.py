#! /usr/bin/env/python3
from os import walk, path, remove
import Crypto.Hash.SHA as sha

def dedupe(bsize=131072):
	#assert (str(type(bsize)) == "<type 'int'>"), "not passed an integer"
	filelist=[]
	sizes={}
	redund=[]
	for root, dirs, files in walk("."):
		for name in files:
			filelist.append(path.join(root, name))
	usc=0
	dsc=0
	for upath in filelist:
		wrksize=str(path.getsize(upath))
		if not wrksize in sizes.keys():
			sizes[wrksize] = [upath,]
			usc+=1
			print('us '+str(usc))
		else:
			sizes[wrksize] += [upath]
			dsc+=1
			print('ds '+str(dsc))
	uhc=0
	dhc=0

	for pathlist in sizes.values():
		if len(pathlist) > 1:
			hashes = {}
			for upath in pathlist:
				blocks=(path.getsize(upath) / bsize) + 1
				with open(upath, 'rb') as f:
					readcount=0
					hasher=sha.new()
					while readcount < blocks:
						hasher.update(f.read(bsize))
						readcount+=1
					whash = hasher.hexdigest()
				if not whash in hashes.keys():
					hashes[whash] = [upath,]
					uhc+=1
					print('uh '+str(uhc))
				else:
					hashes[whash] += [upath]
					dhc+=1
					print('DUPE '+str(dhc))
			for matchlist in hashes.values():
				if len(matchlist) > 1:
					redund.append(matchlist)
	deletedlist=[]
	for item in redund:
		counter = 1
		count = len(item)
		while counter < count:
			remove(item[counter])
			deletedlist.append(item[counter])
			counter += 1
	return deletedlist

if __name__ == '__main__':
	a = dedupe()
