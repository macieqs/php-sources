from datetime import now, timedelta


def dni():
    x = 0
    while True:
        yield now()+timedelta(x)
        x = x + 1

sq = dni()
for x in range(6):
    print "dzien %s" % sq.next()
