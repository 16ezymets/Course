

def sorted_merge(sp1, sp2):
    events = []
    i1 = 0
    i2 = 0
    for q in range(len(sp1) + len(sp2)):
        if i1 == len(sp1):
            events += sp2[i2:]
            break
        elif i2 == len(sp2):
            events += sp1[i1:]
            break
        elif sp1[i1].time < sp2[i2].time:
            events.append(sp1[i1])
            i1 += 1
        else:
            events.append(sp2[i2])
            i2 += 1
    return events
