import json

# Đọc file todo.json
def read_todos():
    try:
        with open("todo.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Lưu công việc vaof todo.json
def save_todos(todos):
    with open("todo.json", "w") as file:
        json.dump(todos, file, indent=4)

#  menu
def show_menu():
    print("\nTo-Do List Manager")
    print("1. Thêm công việc")
    print("2. Xóa công việc")
    print("3. Hiển thị công việc")
    print("4. Thoát")

# add công việc 
def add_task(todos):
    task = input("Nhập công việc cần thêm: ")
    todos.append(task)
    print(f"Đã thêm: {task}")

# Xóa công việc
def remove_task(todos):
    show_tasks(todos)
    task_index = int(input("Nhập công việc cần xóa: ")) - 1
    if 0 <= task_index < len(todos):
        removed_task = todos.pop(task_index)
        print(f"Đã xóa: {removed_task}")
    else:
        print("Khôg tồn tai!")

# Hiển thị danh sách công việc
def show_tasks(todos):
    if todos:
        print("\nDanh sách công việc:")
        for i, task in enumerate(todos, 1):
            print(f"{i}. {task}")
    else:
        print("Danh sách công việc trống!")

# Main function
def main():
    todos = read_todos()
    
    while True:
        show_menu()
        choice = input("Chọn một tùy chọn (1-4): ")
        
        if choice == '1':
            add_task(todos)
        elif choice == '2':
            remove_task(todos)
        elif choice == '3':
            show_tasks(todos)
        elif choice == '4':
            save_todos(todos)
            print("Đã lưu và thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng thử lại.")

if __name__ == "__main__":
    main()
