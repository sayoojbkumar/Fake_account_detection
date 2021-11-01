input_files = ['users_f.csv', 'users_data_f.csv']
output_file = 'output.csv'

output = None
for infile in input_files:
    with open(infile, 'r',encoding="UTF-16") as fh:
        if output:
            for i, l in enumerate(fh.readlines()):
                output[i] = "{},{}".format(output[i].rstrip('\n'), l)
        else:
            output = fh.readlines()

with open(output_file, 'w') as fh:
    for line in output:
        fh.write(line) 
