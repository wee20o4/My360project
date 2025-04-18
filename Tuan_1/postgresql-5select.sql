CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    address TEXT,
    role VARCHAR(20) NOT NULL CHECK (role IN ('Reader', 'Staff', 'Manager')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE Books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100),
    publisher VARCHAR(100),
    publish_year INT CHECK (publish_year > 0),
    category VARCHAR(50),
    isbn VARCHAR(20) UNIQUE,
    total_copies INT NOT NULL CHECK (total_copies >= 0),
    available_copies INT NOT NULL CHECK (available_copies >= 0)
);
CREATE TABLE BookCopies (
    id SERIAL PRIMARY KEY,
    book_id INT NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Available', 'Borrowed', 'Lost', 'Damaged')),
    FOREIGN KEY (book_id) REFERENCES Books(id) ON DELETE CASCADE
);
CREATE TABLE BorrowRecords (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    copy_id INT NOT NULL,
    borrow_date DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    return_date DATE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Borrowed', 'Returned', 'Overdue')),
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (copy_id) REFERENCES BookCopies(id),
    CONSTRAINT chk_due_date CHECK (due_date >= borrow_date)
);
CREATE TABLE Fines (
    id SERIAL PRIMARY KEY,
    borrow_id INT UNIQUE NOT NULL,
    amount NUMERIC(10,2) NOT NULL CHECK (amount >= 0),
    paid BOOLEAN DEFAULT FALSE,
    paid_date DATE,
    FOREIGN KEY (borrow_id) REFERENCES BorrowRecords(id)
);
CREATE TABLE Feedbacks (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);
-- Insert
INSERT INTO Users (full_name, email, phone, address, role) VALUES
('Nguyen Van A', 'a@example.com', '0909123456', '123 Le Loi, HCMC', 'Reader'),
('Tran Thi B', 'b@example.com', '0911123456', '456 Tran Hung Dao, HCMC', 'Staff'),
('Le Van C', 'c@example.com', '0922123456', '789 Nguyen Hue, HCMC', 'Manager'),
('Pham Thi D', 'd@example.com', '0933123456', '12 Bach Dang, Da Nang', 'Reader'),
('Hoang Van E', 'e@example.com', '0944123456', '34 Ly Thuong Kiet, Hanoi', 'Reader'),
('Vo Thi F', 'f@example.com', '0955123456', '56 Tran Phu, HCMC', 'Staff');

INSERT INTO Books (title, author, publisher, publish_year, category, isbn, total_copies, available_copies) VALUES
('Introduction to Algorithms', 'Thomas H. Cormen', 'MIT Press', 2009, 'Computer Science', '9780262033848', 5, 4),
('Clean Code', 'Robert C. Martin', 'Prentice Hall', 2008, 'Software Engineering', '9780132350884', 3, 2),
('1984', 'George Orwell', 'Secker & Warburg', 1949, 'Fiction', '9780451524935', 4, 3),
('To Kill a Mockingbird', 'Harper Lee', 'J.B. Lippincott & Co.', 1960, 'Fiction', '9780061120084', 6, 6),
('Design Patterns', 'Erich Gamma', 'Addison-Wesley', 1994, 'Software Engineering', '9780201633610', 2, 1);

INSERT INTO BookCopies (book_id, status) VALUES
(1, 'Available'), (1, 'Available'), (1, 'Borrowed'), (1, 'Available'), (1, 'Lost'),
(2, 'Available'), (2, 'Borrowed'), (2, 'Damaged'),
(3, 'Available'), (3, 'Available'), (3, 'Borrowed'), (3, 'Available'),
(4, 'Available'), (4, 'Available'), (4, 'Available'), (4, 'Available'), (4, 'Available'), (4, 'Available'),
(5, 'Borrowed'), (5, 'Available');

INSERT INTO BorrowRecords (user_id, copy_id, borrow_date, due_date, return_date, status) VALUES
(1, 3, '2025-04-10', '2025-04-20', NULL, 'Borrowed'),
(1, 7, '2025-03-01', '2025-03-10', '2025-03-15', 'Returned'),
(4, 11, '2025-04-01', '2025-04-10', NULL, 'Overdue'),
(5, 19, '2025-04-05', '2025-04-15', NULL, 'Borrowed');

INSERT INTO Fines (borrow_id, amount, paid, paid_date) VALUES
(2, 10000.00, TRUE, '2025-04-01'),
(3, 20000.00, FALSE, NULL);

INSERT INTO Feedbacks (user_id, content) VALUES
(1, 'Thư viện rất tuyệt vời, nhiều sách hay.'),
(2, 'Cần thêm sách về Machine Learning.'),
(3, 'Dịch vụ mượn trả sách rất nhanh chóng.'),
(4, 'Có thể bổ sung thêm khu đọc nhóm không?'),
(5, 'Tôi thích không gian yên tĩnh ở đây.');

-----------------------------------------------------------------------------------------------------

-- 1. Liệt kê tất cả người dùng đang mượn sách (chưa trả)
SELECT u.full_name, u.email, br.borrow_date, br.due_date
FROM Users u
JOIN BorrowRecords br ON u.id = br.user_id
WHERE br.status = 'Borrowed';

-- 2. Thống kê số lượng sách theo từng thể loại
SELECT category, COUNT(*) AS total_books
FROM Books
GROUP BY category;

-- 3. Tìm các cuốn sách còn ít hơn 2 bản có sẵn
SELECT title, available_copies
FROM Books
WHERE available_copies < 2;

-- 4. Hiển thị các khoản phạt chưa thanh toán
SELECT u.full_name, f.amount, f.paid, br.due_date
FROM Fines f
JOIN BorrowRecords br ON f.borrow_id = br.id
JOIN Users u ON br.user_id = u.id
WHERE f.paid = FALSE;

-- 5. Liệt kê các phản hồi của người dùng có vai trò là 'Reader'
SELECT u.full_name, f.content, f.created_at
FROM Feedbacks f
JOIN Users u ON f.user_id = u.id
WHERE u.role = 'Reader';

