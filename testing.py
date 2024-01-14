file_path_1 = "files/qrels.txt"
file_path_2 = "files/qrels_rel.txt"

def find_duplicate_lines(file1, file2):
    lines_file1 = set()
    duplicate_lines = []

    with open(file1, 'r') as file:
        for line in file:
            lines_file1.add(line.strip())

    with open(file2, 'r') as file:
        for line in file:
            if line.strip() in lines_file1:
                duplicate_lines.append(line.strip())

    return duplicate_lines

# Find duplicate lines between the two files
duplicates = find_duplicate_lines(file_path_1, file_path_2)

# Print the duplicate lines
for line in duplicates:
    print(line)

print(len(duplicates))