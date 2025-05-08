document.addEventListener("DOMContentLoaded", function() {
    // Get elements safely with null checks
    const searchInput = document.getElementById("memberSearchInput");
    const industryFilter = document.getElementById("industryFilter");
    const counterElement = document.getElementById("memberCounter");
    
    // Initialize counter
    updateMemberCounter();
    
    // Add event listeners only if elements exist
    if (searchInput) {
        searchInput.addEventListener("keypress", function(e) {
            if (e.key === "Enter") {
                searchMembers();
            }
        });
    }
    
    if (industryFilter) {
        industryFilter.addEventListener("change", function() {
            filterByIndustry();
        });
    }
});

function resetFilters() {
    const searchInput = document.getElementById("memberSearchInput");
    const industryFilter = document.getElementById("industryFilter");
    
    if (searchInput) searchInput.value = "";
    if (industryFilter) industryFilter.value = "";
    
    filterMembers("", "");
}

function searchMembers() {
    try {
        const searchInput = document.getElementById("memberSearchInput");
        const industryFilter = document.getElementById("industryFilter");
        
        const searchTerm = searchInput ? searchInput.value.toLowerCase() : "";
        const industry = industryFilter ? industryFilter.value : "";
        
        filterMembers(searchTerm, industry);
    } catch (error) {
        console.error("Error in searchMembers:", error);
    }
}

function filterByIndustry() {
    try {
        const searchInput = document.getElementById("memberSearchInput");
        const industryFilter = document.getElementById("industryFilter");
        
        const searchTerm = searchInput ? searchInput.value.toLowerCase() : "";
        const industry = industryFilter ? industryFilter.value : "";
        
        filterMembers(searchTerm, industry);
    } catch (error) {
        console.error("Error in filterByIndustry:", error);
    }
}

function filterMembers(searchTerm, industry) {
    const cards = document.querySelectorAll(".card");

    cards.forEach(function(card) {
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
    const visibleCards = document.querySelectorAll('.card-container:not([style*="display: none"])').length;
    const counterElement = document.getElementById("memberCounter");
    
    if (counterElement) {
        counterElement.textContent = visibleCards;
    }
}