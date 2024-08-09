
# Helper Functions 

def write_to_file(content):
    with open('latest.md', 'w') as f:
        f.write(content)