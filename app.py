import os
import math

def create_dummy_file(filename, size_in_mb):
    """Create a file with repeated message to reach specified size in MB"""
    message = "This file is generated through python by Mujeeb and Hayyan for Research Report\n"
    message_bytes = len(message.encode('utf-8'))
    size_in_bytes = size_in_mb * 1024 * 1024  
    
    repetitions = math.ceil(size_in_bytes / message_bytes)
    
    with open(filename, 'w') as f:
        content = message * repetitions
        f.write(content[:size_in_bytes])
    
    print(f"Created file '{filename}' of size {size_in_mb}MB with repeated message")

def main():
    output_dir = "dummy_files"
    os.makedirs(output_dir, exist_ok=True)
    
    for size in range(1, 16):
        filename = os.path.join(output_dir, f"dummy_{size}MB.txt")
        create_dummy_file(filename, size)

if __name__ == "__main__":
    main()
