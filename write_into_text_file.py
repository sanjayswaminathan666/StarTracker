def write_to_file(file_path, content):
    with open(file_path, 'a') as output_file:  # 'a' mode to append
        output_file.write(content + '\n')  # Append content followed by a newline