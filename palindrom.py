def pal(word):
    d = (len(word))
    for a in range(0, d/2):
        if word[a] != word[-(a+1)]:
            return False
    return True
    
"""word == word[::1]"""