from objects import Atom


def sorted_merge(sp1, sp2):
    events = []
    i = 0
    j = 0
    for q in range(len(sp1) + len(sp2)):
        if i == len(sp1):
            events += sp2[j:]
            break
        elif j == len(sp2):
            events += sp1[i:]
            break
        elif sp1[i].time < sp2[j].time:
            events.append(sp1[i])
            i += 1
        else:
            events.append(sp2[j])
            j += 1
    return events
