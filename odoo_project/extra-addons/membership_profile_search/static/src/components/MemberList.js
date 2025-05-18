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
      members: Array.isArray(this.props.members) ? this.props.members : [],
      page: 1,
      total: 0,
      limit: 12,
      error: null, // Thêm trạng thái lỗi
    });
  }

  async updateSearch(searchTerm) {
    this.state.searchTerm = searchTerm;
    this.state.page = 1;
    await this.fetchMembers();
  }

  async updateIndustry(industry) {
    this.state.industry = industry;
    this.state.page = 1;
    await this.fetchMembers();
  }

  async changePage(page) {
    this.state.page = page;
    await this.fetchMembers();
  }

  async fetchMembers() {
    try {
      const response = await fetch(
        `/membership/data?search=${encodeURIComponent(
          this.state.searchTerm
        )}&industry=${encodeURIComponent(this.state.industry)}&page=${
          this.state.page
        }`
      );
      if (!response.ok) {
        throw new Error("Không thể tải dữ liệu hội viên");
      }
      const data = await response.json();
      if (!Array.isArray(data)) {
        throw new Error("Dữ liệu trả về không hợp lệ");
      }
      this.state.members = data;
      this.state.total = data.length || 0;
      this.state.limit = 12;
      this.state.error = null;
    } catch (error) {
      console.error("Lỗi khi tải dữ liệu hội viên:", error);
      this.state.members = [];
      this.state.total = 0;
      this.state.error =
        "Không thể tải dữ liệu hội viên. Vui lòng thử lại sau.";
    }
  }
}
