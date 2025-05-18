/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { SearchBar } from "./SearchBar";
import { IndustryFilter } from "./IndustryFilter";
import { MemberCard } from "./MemberCard";

export class MemberList extends Component {
    static template = "membership_profile_search.MemberList";
    static components = { SearchBar, IndustryFilter, MemberCard };

    setup() {
        this.state = useState({
            searchTerm: "",
            industry: "",
            members: this.props.members || [],
        });
    }

    updateSearch(searchTerm) {
        this.state.searchTerm = searchTerm;
    }

    updateIndustry(industry) {
        this.state.industry = industry;
    }

    get filteredMembers() {
        const normalizedSearch = this.removeDiacritics(this.state.searchTerm).toLowerCase();
        const normalizedIndustry = this.removeDiacritics(this.state.industry).toLowerCase();

        return this.state.members.filter(member => {
            const name = this.removeDiacritics(member.name || "").toLowerCase();
            const company = this.removeDiacritics(member.company_name || "").toLowerCase();
            const industry = this.removeDiacritics(member.industry_id?.name || "").toLowerCase();
            const address = this.removeDiacritics(
                [member.street, member.city, member.state_id?.name, member.country_id?.name]
                    .filter(Boolean).join(", ") || ""
            ).toLowerCase();

            const matchesSearch = !normalizedSearch ||
                name.includes(normalizedSearch) ||
                company.includes(normalizedSearch) ||
                industry.includes(normalizedSearch) ||
                address.includes(normalizedSearch);

            const matchesIndustry = !normalizedIndustry || industry === normalizedIndustry;

            return matchesSearch && matchesIndustry;
        });
    }

    removeDiacritics(str) {
        return str
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .replace(/đ/g, "d")
            .replace(/Đ/g, "D");
    }
}