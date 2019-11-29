files = ['VolumeT_part']

for file in files:
    with open('TEXTS/' + file + '.txt', encoding='utf8') as f:
        data = f.readlines()
    output = ''
    i = 0
    while i < len(data):
        element = data[i]
        if element == '\n':
            num_chars = 0
            for element_sub in data[i:]:
                if element_sub == '\n':
                    num_chars += 1
                else:
                    break
            i += num_chars-1

            for j in range(num_chars//2):
                output += element
        else:
            output += element
        i += 1
    with open('TEXTSNEW/' + file + 'MOD.txt', 'w', encoding='utf8') as f:
        f.write(output)









    '''start_i = 0
    end_i = 0
    print(data)
    # iterate over whole file and find line breaks
    for i in range(1000): #len(data)-1):
        if data[i:i+2] == '\n':
            print("true")
            end_i = i
            output += data[start_i:end_i]
            # when a line break is found, look for when there is no longer
            # a line break and make that index the start_i
            for j in range(i, len(data)-1):
                if data[j:j+2] == '\n' or data[j:j+2] == 'n\\':
                    pass
                else:
                    start_i = j
                    break
            i = start_i
    print(output)'''
