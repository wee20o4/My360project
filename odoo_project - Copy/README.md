@ -1,122 +0,0 @@
Membership Profile Search Module
Mô tả
Mô-đun Membership Profile Search được phát triển cho Odoo 16.0, cung cấp chức năng quản lý và hiển thị danh sách hội viên công khai trên website Odoo. Các tính năng chính bao gồm:

Tìm kiếm hội viên: Tìm kiếm theo tên, công ty, ngành nghề hoặc địa chỉ, hỗ trợ tìm kiếm không dấu.
Lọc theo ngành nghề: Cho phép lọc hội viên dựa trên ngành nghề.
Hiển thị chi tiết hội viên: Hiển thị thông tin như ảnh đại diện, tên công ty, ngành nghề, địa chỉ.
Giao diện responsive: Thân thiện với người dùng trên cả desktop và mobile.
Bảo mật: Phân quyền truy cập công khai và nội bộ.

Mô-đun này được thiết kế để tích hợp với các mô-đun Odoo như website, membership, và website_partner.
Yêu cầu

Phiên bản Odoo: 16.0
Mô-đun phụ thuộc:
base
website
membership
website_partner
web_editor
website_sale
im_livechat

Docker: Cần cài đặt Docker và Docker Compose để triển khai môi trường.
Hệ điều hành: Linux/amd64 (khuyến nghị).

Cài đặt

Chuẩn bị môi trường Docker:

Cài đặt Docker và Docker Compose.
Tạo thư mục dự án và sao chép các file cấu hình (docker-compose.yml, Dockerfile, odoo.conf) vào thư mục.

Sao chép mã nguồn:

Đặt thư mục extra-addons/membership_profile_search vào thư mục dự án.

Cấu hình:

Chỉnh sửa file odoo.conf để đảm bảo các thông số như db_host, db_user, db_password, và admin_passwd phù hợp với môi trường của bạn.
Đảm bảo file Dockerfile tham chiếu đúng thư mục extra-addons.

Chạy ứng dụng:
docker-compose up -d

Truy cập Odoo tại http://localhost:8069.
Đăng nhập với tài khoản admin (mật khẩu mặc định: 12345) và cài đặt mô-đun Membership Profile Search.

Kích hoạt mô-đun:

Vào Ứng dụng trong Odoo, tìm Membership Profile Search và nhấn Cài đặt.

Hướng dẫn sử dụng

Truy cập danh sách hội viên:

Truy cập URL /membership trên website Odoo.
Sử dụng thanh tìm kiếm để tìm hội viên theo tên, công ty, ngành nghề hoặc địa chỉ.
Nhấn các nút lọc ngành nghề để thu hẹp kết quả.

Xem chi tiết hội viên:

Nhấp vào thẻ hội viên để xem thông tin chi tiết (URL: /partners/<partner_id>).
Trang chi tiết hiển thị ảnh đại diện, tên công ty, ngành nghề, và địa chỉ.

Quản lý dữ liệu:

Quản trị viên có thể thêm/sửa thông tin hội viên trong giao diện Odoo (menu Danh bạ).
Đảm bảo hội viên có website_published=True và membership_state != 'none' để hiển thị công khai.

Cấu trúc file

Cấu hình hệ thống:

docker-compose.yml: Cấu hình dịch vụ Odoo và PostgreSQL.
Dockerfile: Dockerfile để xây dựng image Odoo tùy chỉnh.
odoo.conf: Cấu hình Odoo, bao gồm đường dẫn addons và thông tin cơ sở dữ liệu.

Mã nguồn mô-đun:

extra-addons/membership_profile_search/**manifest**.py: Thông tin mô-đun.
extra-addons/membership_profile_search/**init**.py: Khởi tạo mô-đun.
extra-addons/membership_profile_search/controllers/**init**.py: Khởi tạo controllers.
extra-addons/membership_profile_search/controllers/main.py: Xử lý yêu cầu HTTP.
extra-addons/membership_profile_search/models/**init**.py: Khởi tạo models.
extra-addons/membership_profile_search/models/membership_profile_search.py: Mở rộng model res.partner.
extra-addons/membership_profile_search/security/ir.model.access.csv: Quyền truy cập.
extra-addons/membership_profile_search/views/membership_profile_search_templates.xml: Template giao diện website.
extra-addons/membership_profile_search/static/src/css/membership_search.css: CSS cho giao diện.
extra-addons/membership_profile_search/static/src/js/membership_search.js: JavaScript cho tìm kiếm và lọc.

Tài liệu IDE:

.idea/projectSettingsUpdater.xml: Cấu hình IDE Rider.
.idea/workspace.xml: Cấu hình không gian làm việc IDE.

Lưu ý

Bảo mật: Đảm bảo thay đổi admin_passwd trong odoo.conf trước khi triển khai sản phẩm.
Hiệu suất: Đối với dữ liệu hội viên lớn, cân nhắc tối ưu hóa truy vấn trong main.py.
Tùy chỉnh: Có thể mở rộng CSS/JavaScript trong static/src để tùy chỉnh giao diện.

Giấy phép

LGPL-3

Tác giả

Nhóm 1 - VINA

-- Cách test:
docker exec -it 2e0c29c7f6d7 bash

Truy cập E:\My360project\odoo_project\extra-addons\membership_profile_search\tests\

docker exec 2e0c29c7f6d7 odoo -c /etc/odoo/odoo.conf --test-enable --no-http --stop-after-init -d odoo -u membership_profile_search --test-tags membership_profile_search

docker exec 2e0c29c7f6d7 bash -c "python3 -m py_compile /mnt/extra-addons/membership_profile_search/tests/test_membership_profile_search.py"

docker exec 2e0c29c7f6d7 odoo -c /etc/odoo/odoo.conf --init base,website,membership,website_partner,web_editor,website_sale,im_livechat -d odoo --stop-after-init

docker exec 2e0c29c7f6d7 odoo -c /etc/odoo/odoo.conf --test-enable --no-http --stop-after-init -d odoo -u membership_profile_search --test-tags membership_profile_search --log-level=test
