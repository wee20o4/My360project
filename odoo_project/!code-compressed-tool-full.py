import os

EXCLUDED_FOLDERS = {
    "bin", "obj", "wwwroot", ".git", "Properties", "lib", "keys",
    "node_modules", ".vscode", ".document", "odoo-data", "images"
}

EXCLUDED_FILES = {
    "package-lock.json", "jsconfig.json", "vite.config.js",
    ".editorconfig", ".gitattributes", ".gitignore",
    ".prettierrc.json", ".prettierignore", "README.md",
    "!code-compressed-tool-full.py", "!code-compressed-tool.py",
    ".env", "!run-script-macos.txt", "!run-website.cmd"
}

def is_binary_file(file_path):
    """Kiểm tra xem file có phải là file nhị phân hay không."""
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(1024)  # Đọc một phần nhỏ của file
            return b"\x00" in chunk  # Nếu có byte null, có thể là nhị phân
    except Exception:
        return True  # Nếu không đọc được, coi như là nhị phân

def read_file_content(file_path):
    """Đọc nội dung file với các encoding khác nhau nếu cần."""
    encodings = ["utf-8", "latin-1", "ascii"]
    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                return "\n".join(line.strip() for line in f.readlines())
        except UnicodeDecodeError:
            continue
        except Exception as e:
            return f"[ERROR READING FILE: {e}]"
    return "[ERROR: Unable to decode file with available encodings]"

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

    # Duyệt qua tất cả các file trong thư mục
    for folder, _, files in os.walk(root_folder):
        if any(excluded in folder for excluded in EXCLUDED_FOLDERS):
            continue
        for file in files:
            if file in EXCLUDED_FILES:
                continue
            file_path = os.path.join(folder, file)
            if is_binary_file(file_path):
                print(f"Bỏ qua file nhị phân: {file_path}")
                continue
            files_to_process.append(file_path)

    total_files = len(files_to_process)
    compressed_content = (
        "The entire source code of my project has been compressed into a single .txt file, which I will provide. "
        "I need you to thoroughly read and analyze the code to identify any potential issues, errors, or inefficiencies. "
        "Please do not ask me to verify or check anything related to the code, as what I’m providing is the complete and final version of my codebase\n\n"
    )

    # Xử lý từng file
    for index, file_path in enumerate(files_to_process, start=1):
        relative_path = os.path.relpath(file_path, root_folder)
        content = read_file_content(file_path)
        
        total_characters += len(content)
        print(f"Processing ({index}/{total_files}) {relative_path} - {(index / total_files) * 100:.2f}% done")
        compressed_content += f"---{relative_path}\n{content}\n"

    # Ghi nội dung vào file đầu ra
    try:
        with open(output_file, "w", encoding="utf-8") as out_file:
            out_file.write(compressed_content)
        print(f"✅ Tổng số ký tự đã nén: {total_characters}")
        print(f"Source code đã được compressed thành file: {output_file}")
    except Exception as e:
        print(f"Lỗi khi ghi file {output_file}: {e}")

if __name__ == "__main__":
    root_directory = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(root_directory, "!code-compressed-tool.txt")
    compress_source_code(root_directory, output_file)