

flag = 0
with open("res/genome/GRCh38.primary_assembly.genome.fa", 'r') as file:
    with open("res/genome/GRCh38_chr20.fa", "w") as out_file:
        for line in file:
            if line.startswith(">chr20"):
                flag=1
            elif line.startswith(">"):
                flag=0

            if flag:
                out_file.write(line)
