def fix_log_file(input_path, output_path):
    with open(input_path, 'r') as f:
        lines = f.readlines()

    fixed_lines = []
    i = 0
    while i < len(lines):
        current_line = lines[i].strip()
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if next_line:  # If the next line is not empty
                current_line += f"\t{next_line}"
        fixed_lines.append(current_line + '\n')
        i += 2  # Skip to the next even line pair

    with open(output_path, 'w') as f:
        f.writelines(fixed_lines)



fix_log_file("LOG.TXT", "fixed_log.txt")
