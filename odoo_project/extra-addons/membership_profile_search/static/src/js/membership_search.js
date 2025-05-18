document.addEventListener("DOMContentLoaded", function () {
    /**
     * Hàm khởi tạo khi DOM được tải hoàn toàn.
     * Thiết lập các sự kiện và kiểm tra sự tồn tại của các phần tử cần thiết.
     */
    console.log("DOM loaded, initializing membership search script");

    const searchInput = document.getElementById("memberSearchInput");
    const counterElement = document.getElementById("memberCounter");

    if (!searchInput) {
        console.error(
            "Không tìm thấy phần tử 'memberSearchInput'. Vui lòng kiểm tra template."
        );
        return;
    }
    if (!counterElement) {
        console.error(
            "Không tìm thấy phần tử 'memberCounter'. Vui lòng kiểm tra template."
        );
        return;
    }

    console.log(
        "Found searchInput and counterElement, setting up event listeners"
    );

    updateMemberCounter();

    // Thêm sự kiện input để tìm kiếm tức thời
    searchInput.addEventListener("input", function (e) {
        console.log("Input event triggered, search term:", e.target.value);
        searchMembers();
    });
});

// Hàm chuẩn hóa chuỗi không dấu
function removeDiacritics(str) {
    /**
     * Hàm chuẩn hóa chuỗi, loại bỏ dấu tiếng Việt để hỗ trợ tìm kiếm không dấu.
     * 
     * @param {string} str - Chuỗi văn bản cần chuẩn hóa.
     * @returns {string} - Chuỗi đã được loại bỏ dấu và thay thế ký tự 'đ', 'Đ'.
     */
    return str
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/đ/g, "d")
        .replace(/Đ/g, "D");
}

function resetFilters() {
    /**
     * Hàm đặt lại các bộ lọc tìm kiếm, bao gồm xóa từ khóa tìm kiếm và đặt lại nút lọc ngành nghề.
     */
    const searchInput = document.getElementById("memberSearchInput");
    const industryButtons = document.querySelectorAll(".industry-btn");

    if (searchInput) searchInput.value = "";
    if (industryButtons) {
        industryButtons.forEach((btn) => {
            btn.classList.remove("active");
            if (btn.getAttribute("data-industry") === "") {
                btn.classList.add("active");
            }
        });
    }

    filterMembers("", "");
}

function searchMembers() {
    /**
     * Hàm thực hiện tìm kiếm hội viên dựa trên từ khóa và ngành nghề được chọn.
     * Gọi hàm filterMembers để lọc danh sách hội viên hiển thị.
     */
    try {
        const searchInput = document.getElementById("memberSearchInput");
        const activeButton = document.querySelector(".industry-btn.active");

        const searchTerm = searchInput ? searchInput.value.toLowerCase() : "";
        const industry = activeButton
            ? activeButton.getAttribute("data-industry")
            : "";

        console.log("Searching with term:", searchTerm, "and industry:", industry);
        filterMembers(searchTerm, industry);
    } catch (error) {
        console.error("Error in searchMembers:", error);
    }
}

function filterByIndustry(industry) {
    /**
     * Hàm lọc hội viên theo ngành nghề được chọn, đồng thời xóa từ khóa tìm kiếm.
     * 
     * @param {string} industry - Tên ngành nghề để lọc.
     */
    try {
        const searchInput = document.getElementById("memberSearchInput");
        const industryButtons = document.querySelectorAll(".industry-btn");

        searchInput.value = ""; // Clear search input
        industryButtons.forEach((btn) => {
            btn.classList.remove("active");
            if (btn.getAttribute("data-industry") === industry) {
                btn.classList.add("active");
            }
        });

        filterMembers("", industry);
    } catch (error) {
        console.error("Error in filterByIndustry:", error);
    }
}

function filterMembers(searchTerm, industry) {
    /**
     * Hàm lọc danh sách hội viên dựa trên từ khóa tìm kiếm và ngành nghề.
     * Hiển thị hoặc ẩn các card hội viên dựa trên tiêu chí lọc.
     * 
     * @param {string} searchTerm - Từ khóa tìm kiếm.
     * @param {string} industry - Ngành nghề để lọc.
     */
    const cards = document.querySelectorAll(".card");
    if (!cards.length) {
        console.warn("Không tìm thấy hội viên nào.");
        return;
    }
    // Chuẩn hóa từ khóa tìm kiếm
    const normalizedSearchTerm = removeDiacritics(searchTerm).toLowerCase();

    cards.forEach(function (card) {
        // Lấy dữ liệu từ card và chuẩn hóa
        const name = card.querySelector(".card-title strong")
            ? removeDiacritics(
                  card.querySelector(".card-title strong").textContent
              ).toLowerCase()
            : "";
        const company = card.querySelector(".card-text:nth-child(2)")
            ? removeDiacritics(
                  card.querySelector(".card-text:nth-child(2)").textContent
              ).toLowerCase()
            : "";
        const industryElement = card.querySelector(".card-text:nth-child(3)");
        const cardIndustry = industryElement
            ? removeDiacritics(
                  industryElement.getAttribute("data-industry") || ""
              ).toLowerCase()
            : "";
        const address = card.querySelector(".card-text:nth-child(4)")
            ? removeDiacritics(
                  card.querySelector(".card-text:nth-child(4)").textContent
              ).toLowerCase()
            : "";

        // Kiểm tra khớp với từ khóa tìm kiếm
        const matchesSearch =
            !normalizedSearchTerm ||
            name.includes(normalizedSearchTerm) ||
            company.includes(normalizedSearchTerm) ||
            cardIndustry.includes(normalizedSearchTerm) ||
            address.includes(normalizedSearchTerm);

        // Kiểm tra khớp với ngành nghề
        const matchesIndustry =
            !industry || cardIndustry === removeDiacritics(industry).toLowerCase();

        // Hiển thị hoặc ẩn card
        if (matchesSearch && matchesIndustry) {
            card.parentElement.style.display = "block";
        } else {
            card.parentElement.style.display = "none";
        }
    });

    updateMemberCounter();
}

function updateMemberCounter() {
    /**
     * Hàm cập nhật số lượng hội viên hiển thị trên giao diện.
     */
    const visibleCards = document.querySelectorAll(
        '.card-container:not([style*="display: none"])'
    ).length;
    const counterElement = document.getElementById("memberCounter");

    if (counterElement) {
        counterElement.textContent = visibleCards;
    }
}