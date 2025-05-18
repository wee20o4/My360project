from odoo.tests import tagged
from odoo.tests.common import HttpCase
from odoo.exceptions import ValidationError
import unicodedata
import re

@tagged('membership_profile_search')
class TestMembershipProfileSearch(HttpCase):
    """
    Kiểm thử các chức năng tìm kiếm và lọc hội viên trong mô-đun Membership Profile Search.
    """

    def setUp(self):
        super(TestMembershipProfileSearch, self).setUp()
        # Tạo dữ liệu mẫu để kiểm thử
        self.industry = self.env['res.partner.industry'].create({
            'name': 'Công nghệ thông tin',
        })

        self.partner1 = self.env['res.partner'].create({
            'name': 'Công ty TNHH Công nghệ Vina',
            'company_name': 'Vina Tech',
            'industry_id': self.industry.id,
            'street': '123 Đường Lê Lợi',
            'city': 'Vũng Tàu',
            'country_id': self.env.ref('base.vn').id,
            'website_published': True,
            'membership_state': 'paid',
        })

        self.partner2 = self.env['res.partner'].create({
            'name': 'Nguyễn Văn A',
            'company_name': 'Doanh nghiệp Minh Anh',
            'industry_id': self.industry.id,
            'street': '456 Đường Nguyễn Huệ',
            'city': 'Hà Nội',
            'country_id': self.env.ref('base.vn').id,
            'website_published': True,
            'membership_state': 'paid',
        })

        # Tạo hội viên không công khai để kiểm thử phân quyền
        self.partner3 = self.env['res.partner'].create({
            'name': 'Công ty Không Công Khai',
            'company_name': 'Hidden Corp',
            'industry_id': self.industry.id,
            'street': '789 Đường Trần Phú',
            'city': 'Đà Nẵng',
            'country_id': self.env.ref('base.vn').id,
            'website_published': False,
            'membership_state': 'none',
        })

    def remove_diacritics(self, text):
        """
        Hàm chuẩn hóa chuỗi, loại bỏ dấu tiếng Việt để hỗ trợ tìm kiếm không dấu.
        """
        text = unicodedata.normalize('NFD', text)
        text = re.sub(r'[\u0300-\u036f]', '', text)
        text = text.replace('đ', 'd').replace('Đ', 'D')
        return text

    def test_remove_diacritics(self):
        """
        Kiểm thử hàm chuẩn hóa chuỗi không dấu.
        """
        test_cases = [
            ('Công nghệ Thông tin', 'Cong nghe Thong tin'),
            ('Đường Nguyễn Huệ', 'Duong Nguyen Hue'),
            ('Việt Nam', 'Viet Nam'),
        ]

        for input_text, expected in test_cases:
            result = self.remove_diacritics(input_text)
            self.assertEqual(result, expected, f"Chuẩn hóa không dấu thất bại: {input_text}")

    def test_search_members_by_name(self):
        """
        Kiểm thử tìm kiếm hội viên theo tên.
        """
        response = self.url_open('/membership?search=Công ty TNHH Công nghệ Vina')
        self.assertTrue(self.partner1.name in response.text, "Không tìm thấy hội viên theo tên")

        response = self.url_open('/membership?search=Nguyễn Văn A')
        self.assertTrue(self.partner2.name in response.text, "Không tìm thấy hội viên theo tên cá nhân")

    def test_search_members_by_company(self):
        """
        Kiểm thử tìm kiếm hội viên theo tên công ty.
        """
        response = self.url_open('/membership?search=Vina Tech')
        self.assertTrue(self.partner1.company_name in response.text, "Không tìm thấy hội viên theo tên công ty")

        response = self.url_open('/membership?search=Doanh nghiệp Minh Anh')
        self.assertTrue(self.partner2.company_name in response.text, "Không tìm thấy hội viên theo tên công ty")

    def test_search_members_by_industry(self):
        """
        Kiểm thử tìm kiếm hội viên theo ngành nghề.
        """
        response = self.url_open('/membership?search=Công nghệ thông tin')
        self.assertTrue(self.partner1.name in response.text, "Không tìm thấy hội viên theo ngành nghề")
        self.assertTrue(self.partner2.name in response.text, "Không tìm thấy hội viên theo ngành nghề")

    def test_search_members_by_address(self):
        """
        Kiểm thử tìm kiếm hội viên theo địa chỉ.
        """
        response = self.url_open('/membership?search=Đường Lê Lợi')
        self.assertTrue(self.partner1.street in response.text, "Không tìm thấy hội viên theo địa chỉ")

        response = self.url_open('/membership?search=Nguyễn Huệ')
        self.assertTrue(self.partner2.street in response.text, "Không tìm thấy hội viên theo địa chỉ")

    def test_search_no_diacritics(self):
        """
        Kiểm thử tìm kiếm không dấu.
        """
        response = self.url_open('/membership?search=Cong nghe Thong tin')
        self.assertTrue(self.partner1.name in response.text, "Không tìm thấy hội viên khi tìm kiếm không dấu")
        self.assertTrue(self.partner2.name in response.text, "Không tìm thấy hội viên khi tìm kiếm không dấu")

    def test_filter_by_industry(self):
        """
        Kiểm thử lọc hội viên theo ngành nghề qua server-side.
        """
        response = self.url_open('/membership')
        self.assertTrue('Công nghệ thông tin' in response.text, "Không hiển thị nút lọc ngành nghề")

        # Kiểm tra danh sách hội viên theo ngành nghề
        members = self.env['res.partner'].sudo().search([
            ('membership_state', '!=', 'none'),
            ('website_published', '=', True),
            ('industry_id.name', 'ilike', 'Công nghệ thông tin')
        ])
        self.assertIn(self.partner1, members, "Hội viên 1 không được lọc theo ngành nghề")
        self.assertIn(self.partner2, members, "Hội viên 2 không được lọc theo ngành nghề")

    def test_member_detail_page(self):
        """
        Kiểm thử hiển thị trang chi tiết hội viên.
        """
        response = self.url_open(f'/partners/{self.partner1.id}')
        self.assertTrue(self.partner1.name in response.text, "Không hiển thị tên hội viên trên trang chi tiết")
        self.assertTrue(self.partner1.company_name in response.text, "Không hiển thị tên công ty trên trang chi tiết")
        self.assertTrue(self.partner1.street in response.text, "Không hiển thị địa chỉ trên trang chi tiết")

    def test_unauthorized_access(self):
        """
        Kiểm thử truy cập trang chi tiết hội viên không công khai hoặc không phải hội viên.
        """
        response = self.url_open(f'/partners/{self.partner3.id}', allow_redirects=False)
        self.assertEqual(response.status_code, 404, "Không chặn truy cập hội viên không công khai")

    def test_empty_search(self):
        """
        Kiểm thử tìm kiếm với từ khóa không khớp.
        """
        response = self.url_open('/membership?search=NonExistentKeyword')
        self.assertTrue("Không tìm thấy hội viên nào phù hợp với tiêu chí tìm kiếm" in response.text,
                        "Không hiển thị thông báo khi không tìm thấy hội viên")

    def test_access_with_internal_user(self):
        """
        Kiểm thử truy cập trang chi tiết hội viên với người dùng nội bộ.
        """
        # Giả lập người dùng nội bộ
        self.authenticate('admin', 'admin')
        response = self.url_open(f'/partners/{self.partner3.id}')
        self.assertTrue(self.partner3.name in response.text, "Người dùng nội bộ không xem được hội viên không công khai")

    def test_search_empty_fields(self):
        """
        Kiểm thử tìm kiếm với hội viên có trường trống.
        """
        # Tạo hội viên với một số trường trống
        empty_partner = self.env['res.partner'].create({
            'name': 'Hội viên Không Đầy Đủ',
            'website_published': True,
            'membership_state': 'paid',
        })
        response = self.url_open('/membership?search=Hội viên Không Đầy Đủ')
        self.assertTrue(empty_partner.name in response.text, "Không tìm thấy hội viên với trường trống")
