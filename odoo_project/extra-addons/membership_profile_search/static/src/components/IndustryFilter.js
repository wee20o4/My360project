/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class IndustryFilter extends Component {
    static template = "membership_profile_search.IndustryFilter";

    setup() {
        this.state = useState({ activeIndustry: "" });
    }

    setIndustry(industry) {
        this.state.activeIndustry = industry;
        this.props.onIndustryChange(industry);
    }
}