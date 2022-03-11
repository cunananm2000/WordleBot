from pprint import PrettyPrinter
from math import log2
from tqdm.auto import tqdm
import json
# i can't believe you didn't use numpy/pandas

def H(x):
	if x == 0: return 0
	return -1.0*x*log2(x)

def ID3(labels,data,level=0,parent=''):
	# print(labels,data)

	# if parent!='':
	# 	print(level*'	',f"---LEVEL {level} from {parent}---")
	# else:
	# 	print(level*'	',f"---LEVEL {level}---")

	# assert(len(labels)==len(data[0]))
	# assert(all(len(data[i])==len(data[0])) for i in range(len(data)))

	if len(labels) == 0:
		return {}
	n = len(data)
	freqs = {}
	for row in data:
		freqs[row[-1]] = freqs.get(row[-1],0) + 1
	H_y = sum(map(H,[v/len(data) for v in freqs.values()]))
	# H_y = H([row[-1] for row in data].count('Yes')/len(data))
	# print(level*'	','Current entropy =',H_y,',',*[f'{a}=({b}/{n})' for a,b in sorted(freqs.items())][::-1])
	# print(level*'	','Data set size =',n)
	if H_y == 0:
		# print(level*'	','Leaf value:',data[0][-1])
		return {
			'leaf value': f'{data[0][-1]}=({n}/{n})'
		}
	if len(labels) == 1:
		s = [f'{k}=({v}/{n})' for k,v in freqs.items()]
		# print(level*'	','Leaf value:',*s)
		return {
			'leaf value': ' '.join(s)
		}
	bestLabelIndex = 0
	bestGain = -1
	bestTree = {}
	# # loop over labels, except target variable
	for i in tqdm(range(len(labels)-1)):
		# if len(labels)==2:
		# 	print(level*'	','Considering',labels[i],'(only option)')
		# else:
		# 	print(level*'	','Considering',labels[i])
		freqs = {}
		for row in data:
			v,t = row[i],row[-1]
			if v not in freqs: freqs[v] = {}
			# freqs[v]['total'] += 1
			freqs[v][t] = freqs[v].get(t,0) + 1
		# print(freqs)
		H_y_label = 0
		for k,v in freqs.items():
			total = sum(v.values())
			freqs[k]['entropy'] = sum(map(H,[x/total for x in v.values()]))
			# print(level*'	',f' ({total}/{n})',f'Entropy on {k} =',freqs[k]['entropy'],',',*[f'{a}=({b}/{total})' for a,b in sorted(v.items())[::-1] if a!='entropy'])
			H_y_label += (total/n) * freqs[k]['entropy']
		# print(level*'	',' Total entropy on this label = ',H_y_label)
		gain = H_y - H_y_label
		# print(level*'	',' Gain on this label = ',gain)
		if gain > bestGain:
			bestGain = gain
			bestLabelIndex = i
			bestTree = {
				'data set size': n,
				'entropy': H_y,
				'label to split on': labels[i],
				'entropy_on_split': H_y_label,
				'gain': gain,
				'splits': {}
			}
			for k in freqs.keys():
				bestTree['splits'][k] = {
					'entropy on this value': freqs[k]['entropy'],
					'subtree': {}
				}
	sets = {}
	i = bestLabelIndex
	# print("****",labels)
	# print(level*'	',"Splitting on",labels[i])
	# print('best:',bestTree,list(bestTree['splits'].keys()))
	labelsCopy = labels.copy()
	dataCopy = data.copy()
	for row in dataCopy:
		v = row.pop(i)
		if v not in sets:
			sets[v] = []
		sets[v].append(row)
	# print(sets)
	labelsCopy.pop(i)
	for k in bestTree['splits'].keys():
		# print("\n\n----GIVING ----",k,level)
		# print(labelsCopy,sets[k])
		# print("--------\n\n")
		bestTree['splits'][k] = ID3(labelsCopy,sets[k],level+1,k)
	return bestTree

def main():
	# print(H(1/2))
	# return
	# print('here')
  # ah shit im here as well
  # oh 3ba is trivial this was stupid
	f = open('commonDistMatrix.txt')
	labels,*data = [line.strip().split(',') for line in f]
	# print(labels,data)
	
	pp = PrettyPrinter(indent=4)
	tree = ID3(labels,data,0)
	# print("****** BEST TREE ******")
	# pp.pprint(tree)
	print(json.dumps(tree, indent = 4))
main()