import os

folder = "src/images/Brandy"

files = sorted(os.listdir(folder))

for i, filename in enumerate(files, start=1):
    old_path = os.path.join(folder, filename)

    # skip folders
    if not os.path.isfile(old_path):
        continue

    # keep original extension
    extension = os.path.splitext(filename)[1]

    new_name = f"Brandy_{i}{extension}"
    new_path = os.path.join(folder, new_name)

    os.rename(old_path, new_path)

    print(f"{filename} -> {new_name}")