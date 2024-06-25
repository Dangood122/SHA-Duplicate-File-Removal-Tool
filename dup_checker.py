import hashlib
import os
import json

CONFIG_FILE = 'common_file_types.json'

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            'Documents': ['.txt', '.pdf', '.doc', '.docx'],
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'Videos': ['.mp4', '.avi', '.mov', '.mkv'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac']
        }

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)

# Load the initial configuration
common_file_types = load_config()

# Menu to update the config data
def display_menu():
    print("\nMenu:")
    print("1. Display file types")
    print("2. Add a new file type")
    print("3. Remove a file type")
    print("4. Add a new category")
    print("5. Remove a category")
    print("6. Exit")

def display_file_types():
    for category, extensions in common_file_types.items():
        print(f"{category}: {', '.join(extensions)}")

def add_file_type():
    display_file_types()
    category = input("Enter the category to add a file type to: ")
    if category in common_file_types:
        new_file_type = input("Enter the new file type (e.g., .xyz): ")
        if new_file_type not in common_file_types[category]:
            common_file_types[category].append(new_file_type)
            save_config(common_file_types)
            print(f"Added {new_file_type} to {category}.")
        else:
            print(f"{new_file_type} already exists in {category}.")
    else:
        print(f"Category {category} does not exist.")

def remove_file_type():
    display_file_types()
    category = input("Enter the category to remove a file type from: ")
    if category in common_file_types:
        file_type = input("Enter the file type to remove (e.g., .xyz): ")
        if file_type in common_file_types[category]:
            common_file_types[category].remove(file_type)
            save_config(common_file_types)
            print(f"Removed {file_type} from {category}.")
        else:
            print(f"{file_type} does not exist in {category}.")
    else:
        print(f"Category {category} does not exist.")

def add_category():
    display_file_types()
    category = input("Enter the new category name: ")
    if category not in common_file_types:
        common_file_types[category] = []
        save_config(common_file_types)
        print(f"Added new category {category}.")
    else:
        print(f"Category {category} already exists.")

def remove_category():
    display_file_types()
    category = input("Enter the category name to remove: ")
    if category in common_file_types:
        del common_file_types[category]
        save_config(common_file_types)
        print(f"Removed category {category}.")
    else:
        print(f"Category {category} does not exist.")

def main():
    while True:
        display_menu()
        choice = input("Choose an option: ")
        
        if choice == '1':
            display_file_types()
        elif choice == '2':
            add_file_type()
        elif choice == '3':
            remove_file_type()
        elif choice == '4':
            add_category()
        elif choice == '5':
            remove_category()
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()

### Hash calculation and comparison
def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Error calculating hash for {file_path}: {e}")
        return None

def scan_directory(directory, file_types):
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext_list in file_types.values() for ext in ext_list):
                file_path = os.path.join(root, file)
                file_hash = calculate_sha256(file_path)
                if file_hash:
                    if file_hash in file_hashes:
                        file_hashes[file_hash].append(file_path)
                    else:
                        file_hashes[file_hash] = [file_path]
    return file_hashes

def find_duplicates(file_hashes):
    return {hash: paths for hash, paths in file_hashes.items() if len(paths) > 1}

def print_duplicates(duplicates):
    for hash, paths in duplicates.items():
        print(f"Duplicate files (SHA256: {hash}):")
        for path in paths:
            print(f"  - {path}")

def delete_duplicates(duplicates):
    for hash, paths in duplicates.items():
        for path in paths[1:]:  # Keep one file, delete the rest
            try:
                os.remove(path)
                print(f"Deleted: {path}")
            except Exception as e:
                print(f"Error deleting {path}: {e}")

if __name__ == "__main__":
    directory = input("Enter the directory to scan: ")
    file_hashes = scan_directory(directory, common_file_types)
    duplicates = find_duplicates(file_hashes)
    
    if not duplicates:
        print("No duplicate files found.")
    else:
        print("\nDuplicate files found:")
        print_duplicates(duplicates)
        
        action = input("\nWould you like to delete all but one of each duplicate set? (yes/no): ").strip().lower()
        if action == 'yes':
            delete_duplicates(duplicates)
            print("Duplicate files deleted.")
        else:
            print("No files were deleted.")
