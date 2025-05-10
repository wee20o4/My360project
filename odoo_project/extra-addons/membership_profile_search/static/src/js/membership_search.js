// extra-addons/membership_profile_search/static/src/js/membership_search.js

document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("memberSearchInput");
  const counterElement = document.getElementById("memberCounter");

  updateMemberCounter();

  if (searchInput) {
    searchInput.addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        searchMembers();
      }
    });
  }
});

// Hàm chuẩn hóa chuỗi không dấu
function removeDiacritics(str) {
  return str
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/đ/g, "d")
    .replace(/Đ/g, "D");
}

function resetFilters() {
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
  try {
    const searchInput = document.getElementById("memberSearchInput");
    const activeButton = document.querySelector(".industry-btn.active");

    const searchTerm = searchInput ? searchInput.value.toLowerCase() : "";
    const industry = activeButton
      ? activeButton.getAttribute("data-industry")
      : "";

    filterMembers(searchTerm, industry);
  } catch (error) {
    console.error("Error in searchMembers:", error);
  }
}

function filterByIndustry(industry) {
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
  const cards = document.querySelectorAll(".card");

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
  const visibleCards = document.querySelectorAll(
    '.card-container:not([style*="display: none"])'
  ).length;
  const counterElement = document.getElementById("memberCounter");

  if (counterElement) {
    counterElement.textContent = visibleCards;
  }
}
