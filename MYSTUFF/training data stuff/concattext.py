import glob
filenames = glob.glob("TEXTSNEW/*.txt")

with open('oregairu-full-mod.txt', 'w', encoding='utf8') as outfile:
    for fname in filenames:
        with open(fname, encoding='utf8') as infile:
            for line in infile:
                outfile.write(line)
