import re

def merge_tuples(input_file='output.txt', output_file='final_output.txt'):
    all_tuples = []
    inside_list = False

    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            if line.startswith('['):
                inside_list = True
                line = line[1:]  # Remove opening bracket
            if ']' in line:
                inside_list = False
                line = line.split(']')[0]  # Remove closing bracket
            if inside_list or line:
                tuples = re.findall(r'\(([^#)]+)\)', line)
                for t in tuples:
                    t = t.strip()
                    t = f'({t})' if not t.startswith('(') else t
                    all_tuples.append(t)

    with open(output_file, 'w') as file:
        file.write(f'[{" , ".join(all_tuples)}]')

if __name__ == '__main__':
    merge_tuples()
