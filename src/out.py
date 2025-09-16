from datetime import datetime

def to_file(lines, file, head, time_format):
    if head:
        file.write("# Manx v0.2\n")
        file.write(f"# Published: {datetime.now().strftime(time_format)}\n")
        file.write(f"# Unique Entries: {len(lines)}\n")
    for line in lines:
        file.write(f"{line}\n")
