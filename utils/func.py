
# Helper Functions 

def write_to_file(content):
    with open('latest.md', 'w') as f:
        f.write(content)

def append_to_file(content):
    with open('latest.md', 'a') as file:
        file.write(content)