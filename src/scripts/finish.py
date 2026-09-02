from pathlib import Path

data_dir = Path("src/data")

files = sorted(data_dir.glob("*.js"))

imports = []
entries = []

for i, file in enumerate(files):
    var_name = f"artist{i}"
    imports.append(
        f'import {var_name} from "./src/data/{file.name}";'
    )
    entries.append(f"  {var_name},")

output = "\n".join(imports)
output += "\n\nexport const artists = [\n"
output += "\n".join(entries)
output += "\n];\n"

Path("artists.js").write_text(output, encoding="utf-8")