/** @odoo-module **/

import { Component, useState, useEffect } from "@odoo/owl";

export class SearchBar extends Component {
    static template = "membership_profile_search.SearchBar";

    setup() {
        this.state = useState({ value: "" });
        this.debounceTimeout = null;
    }

    onInput(ev) {
        clearTimeout(this.debounceTimeout);
        this.debounceTimeout = setTimeout(() => {
            this.state.value = ev.target.value;
            this.props.onSearch(this.state.value);
        }, 300);
    }
}