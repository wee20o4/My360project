/** @odoo-module **/

const { Component } = owl;

class MembershipDirectory extends Component {
  static template = "membership_search_profile.MembershipDirectory";

  setup() {
    this.state = { members: [], error: null };
    this.loadMembers();
  }

  async loadMembers() {
    try {
      const members = await this.rpc({
        model: "res.partner",
        method: "search_read",
        args: [
          [
            ["is_company", "=", false],
            ["membership", "=", true],
          ],
          ["name"],
          0,
          50,
        ],
      });
      this.state.members = members;
    } catch (error) {
      console.error("Error loading members:", error);
      this.state.error = "Không thể tải danh sách hội viên. Vui lòng thử lại.";
      this.state.members = [];
    }
  }
}

odoo.define(
  "membership_search_profile.MembershipDirectory",
  function (require) {
    const publicWidget = require("web.public.widget");
    publicWidget.registry.MembershipDirectory = publicWidget.Widget.extend({
      selector: ".membership_directory",
      start: function () {
        if (this.el) {
          const component = new MembershipDirectory(this);
          component.mount(this.el);
        }
        return this._super.apply(this, arguments);
      },
    });
  }
);
