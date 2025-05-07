import os

EXCLUDED_FOLDERS = {
    "bin", "obj", "wwwroot", ".git", "Properties", "lib", "keys",
    "node_modules",
    ".vscode",
    ".document",
    "odoo-data",
    "images"
}

EXCLUDED_FILES = {
    "package-lock.json",
    "jsconfig.json",
    "vite.config.js",
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    ".prettierrc.json",
    ".prettierignore",
    "README.md",
    "!code-compressed-tool-full.py",
    "!code-compressed-tool.py",
    ".env",
    "!run-script-macos.txt",
    "!run-website.cmd"
}

def compress_source_code(root_folder, output_file):
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
            print(f"Đã xóa file cũ: {output_file}")
        except Exception as e:
            print(f"Lỗi khi xóa file cũ {output_file}: {e}")
            return 

    files_to_process = []
    total_characters = 0

    for folder, _, files in os.walk(root_folder):
        if any(excluded in folder for excluded in EXCLUDED_FOLDERS):
            continue
        for file in files:
            if file in EXCLUDED_FILES:
                continue
            files_to_process.append(os.path.join(folder, file))

    total_files = len(files_to_process)
    compressed_content = ""

    for index, file_path in enumerate(files_to_process, start=1):
        relative_path = os.path.relpath(file_path, root_folder)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = "\n".join(line.strip() for line in f.readlines())  # Giữ nguyên dòng, chỉ xóa khoảng trắng thừa
        except Exception as e:
            content = f"[ERROR READING FILE: {e}]"
        
        total_characters += len(content)
        print(f"Processing ({index}/{total_files}) {relative_path} - {(index / total_files) * 100:.2f}% done")
        compressed_content += f"---{relative_path}\n{content}\n"  # Giữ nguyên dòng, chỉ loại bỏ khoảng trắng đầu cuối

    with open(output_file, "w", encoding="utf-8") as out_file:
        out_file.write(compressed_content)

    print(f"✅ Tổng số ký tự đã nén: {total_characters}")

if __name__ == "__main__":
    root_directory = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(root_directory, "!code-compressed-tool.txt")
    compress_source_code(root_directory, output_file)
    print(f"Source code đã được compressed thành file: {output_file}")
