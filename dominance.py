from matplotlib.style import use
from zmq import CONNECT_ROUTING_ID


def rec(string):
    if(string.count("-") == 0):
        s = "0b" + string
        s = int(s, 2)
        mintermls[origin].append(s)
        minterm.add(s)
        if(s in counting):
            counting[s] += 1
        else:
            counting[s] = 1
        return
    for i in range(len(string)):
        if (string[i] == "-"):
            string = string[:i] + "1" + string[i+1:]
            rec(string)
            string = string[:i] + "0" + string[i+1:]
            rec(string)
            break
        
def rowCheck(minterm):
    for i in range(len(minterm) - 1):
        for j in range(i+1, len(minterm)):
            a = set(useful[minterm[i]])
            b = set(useful[minterm[j]])
            if len(a) == len(b):
                continue
            elif len(a) > len(b):
                if b.issubset(a):
                    return(rowDominance(minterm))
            else:
                if a.issubset(b):
                    return(rowDominance(minterm))
    return minterm
    
def rowDominance(minterm):
    global useful
    useful = {}
    for s in mintermls.keys():
        useful[s] = []
        for k in mintermls[s]:
            if k in minterm:
                useful[s].append(k)
    ls = list(useful.keys())
    dom = set()
    for i in range(len(ls)-1):
        if len(useful[ls[i]]) == 0:
            dom.add(ls[i])
            continue
        for j in range(i+1, len(ls)):
            a = set(useful[ls[i]])
            b = set(useful[ls[j]])
            if len(useful[ls[j]]) == 0:
                dom.add(ls[j])
                continue
            if len(a) == len(b):
                continue
            elif len(a) > len(b):
                if b.issubset(a):
                    dom.add(ls[j])
            else:
                if a.issubset(b):
                    dom.add(ls[i])
    for d in dom:
        del useful[d]
    return rowCheck(list(useful.keys()))

def colCheck(minterm): # {1}, {1, 2}, {1, 2, 3}
    for i in range(len(minterm) - 1):
        for j in range(i+1, len(minterm)):
            a = set(coldic[minterm[i]])
            b = set(coldic[minterm[j]])
            if len(a) == len(b):
                continue
            elif len(a) > len(b):
                if b.issubset(a):
                    return(colDominance(minterm))
            else:
                if a.issubset(b):
                    return(colDominance(minterm))
    result = sorted(minterm)
    return result

def colDominance(minterm):
    global coldic
    coldic = {}
    for s in mintermls.keys():
        for k in mintermls[s]:
            if k not in minterm:
                continue
            if k in coldic:
                coldic[k].add(s)
            else:
                coldic[k] = set()
                coldic[k].add(s)
    ls = list(coldic.keys())
    dom = set()
    for i in range(len(ls)-1):
        if len(coldic[ls[i]]) == 0:
            dom.add(ls[i])
            continue
        for j in range(i+1, len(ls)):
            a = set(coldic[ls[i]])
            b = set(coldic[ls[j]])
            if len(coldic[ls[j]]) == 0:
                dom.add(ls[j])
                continue
            if len(a) == len(b):
                continue
            elif len(a) > len(b):
                if b.issubset(a):
                    dom.add(ls[j])
            else:
                if a.issubset(b):
                    dom.add(ls[i])
    for d in dom:
        del coldic[d]
    return colCheck(list(coldic.keys()))

def dominance(pi_list):
    global mintermls, origin, counting, minterm
    counting = {}
    mintermls = {}
    minterm = set()
    for s in pi_list:
        origin = s
        mintermls[origin] = []
        rec(s)
    epi = []
    for s in mintermls:
        for m in mintermls[s]:
            if(counting[m] == 1):
                pi_list.remove(s)
                epi.append(s)
                break
    for p in epi:
        for m in mintermls[p]:
            if m in minterm:
                minterm.remove(m)
        del mintermls[p]
    print(rowDominance(minterm))
    print(colDominance(minterm))
    
dominance(['00-', '0-0', '11-', '1-1', '-01', '-10'])
dominance(["10-0", "101-", "110-", "1-11", "11-1", "--00"])
dominance(['001-', '00-1', '010-', '01-0', '0-01', '0-10', '-110'])
