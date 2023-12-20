




def find(needle, haystack):
    index = -1
    length_needle = len(needle)
    for i in range(len(haystack)):
        if (haystack[i] == needle[0]):
            matching = 1
            for j in range(length_needle):
                if (haystack[i + (j)] != needle[0 + (j)]):
                    matching = 0
                    
            if (matching == 1):
                index = i
                break;

    return index


one = "llo"
two = "he  llo world"

print(find(one, two))