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

  cards.forEach(function (card) {
    const name = card.querySelector(".card-title strong")
      ? card.querySelector(".card-title strong").textContent.toLowerCase()
      : "";
    const company = card.querySelector(".card-text:nth-child(2)")
      ? card.querySelector(".card-text:nth-child(2)").textContent.toLowerCase()
      : "";
    const cardIndustry = card.querySelector(".card-text:nth-child(3)")
      ? card.querySelector(".card-text:nth-child(3)").textContent.toLowerCase()
      : "";
    const address = card.querySelector(".card-text:nth-child(4)")
      ? card.querySelector(".card-text:nth-child(4)").textContent.toLowerCase()
      : "";

    const matchesSearch =
      !searchTerm ||
      name.includes(searchTerm) ||
      company.includes(searchTerm) ||
      cardIndustry.includes(searchTerm) ||
      address.includes(searchTerm);

    const matchesIndustry =
      !industry || cardIndustry.includes(industry.toLowerCase());

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
