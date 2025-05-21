odoo.define('membership_profile.public_member_snippet', function (require) {
'use strict';

const publicWidget = require('web.public.widget');
const DynamicSnippet = require('website.s_dynamic_snippet');
const core = require('web.core');

const _lt = core._lt;

const PublicMemberSnippet = DynamicSnippet.extend({
    selector: '.s_public_member_snippet',
    events: {
        'input #member-search-query': '_onInput',
        'click .member-search-query': '_onSearch',
        'click .o_member_search_close': '_resetSearch'
    },
    disabledInEditableMode: false,
    /**
     * 
     * @override 
     */
    init: function() {
        this._super.apply(this, arguments);
        this.currentPathname = window.location.pathname;
        this.template_key = "membership_profile.dynamic_filter_template_public_member_card";
        this.committee_template_key = false;
        this.committee_id = false;
        this.committee_data = {level_1: [], level_2: [], level_3: []};
        this.committee_data_end = null;
        this.committee_data_start = null;
        this.committee_name = null;
        this.searchTerm = null;
        this.not_found = false;
        this._onInput = _.debounce(this._onInput, 400);
    },
    /**
     * @private
     */
    _onInput: function () {
        var searchBar = document.getElementById("member-search-query");
        var self = this;
        // console.log('Input SearchBar', searchBar);
        searchBar.addEventListener("keypress", function(event) {
            // If the user presses the "Enter" key on the keyboard
            if (event.key === "Enter") {
                // console.log('Search bar enter')
                // event.preventDefault();
                self._onSearch(event);
            }
        });
    },

    /**
     * @private
     */
    _onSearch: function (ev) {
        // console.log('Searching .....')
        ev.preventDefault();
        this.$input_member = this.$el.find("input#member-search-query");
        var wasEmpty = !this.$input_member.val();
        if (!wasEmpty) {
            this.searchTerm = this.$input_member.val().trim();
            // console.log('Value search', this.searchTerm);
            this._renderSearchMember()
        };
    },

    _resetSearch: function () {
        this.searchTerm = null;
        this._renderSearchMember();
    },

    _renderSearchMember: async function () {
        await this._fetchData();
        // console.log('Fetching data and render')
        return this._render();
    },

    /**
     * Method to be overridden in child components if additional configuration elements
     * are required in order to fetch data.
     * @private
     */
    _isConfigComplete: function () {
        return this._super.apply(this, arguments);
    },
    /**
     * Method to be overridden in child components in order to prepare QWeb
     * options.
     * @private
    */
    _getQWebRenderOptions: function () {
        const options = this._super(...arguments);
        options.back_url = this.currentPathname;
        // options.registered_text = _lt('Registered');
        // options.go_to_website_text = _lt('Go to website');
        // options.save_contact_text = _lt('Save Contact');
        options.registered_text = _lt('Ngành nghề');
        options.go_to_website_text = _lt('Đến website');
        options.save_contact_text = _lt('Lưu liên hệ');
        options.is_committee_template = this.committee_template_key;
        options.committee_name = this.committee_name;
        options.committee_data_end = this.committee_data_end;
        options.committee_data_start = this.committee_data_start;
        options.not_found = this.not_found;
        options.search = false;
        if (this.searchTerm !== null) {
            if (this.searchTerm.length > 0){
                options.search = true;
                if (this.not_found) {
                    options.search_count = 0;
                } else {
                    options.search_count = this.data.length;
                }
            }
        }
        // console.log('OPTIONS', options);
        return options;
    },
    /**
     * @override
     */
    async _fetchData() {
        const searchDomain = this._getSearchDomain();
        if (!this.committee_template_key){
            const members = await this._rpc({
                'route': '/snippets/partners/members',
                'params': {
                    'search': this.searchTerm,
                    'category_id': searchDomain,
                },
            });
            this.data = members['partners'];
            if (this.data.length < 1 && this.searchTerm && this.searchTerm.length > 1) {
                this.data = [{messages: _lt("Không thể tìm thấy kết quả tìm kiếm cho ") + "'" + this.searchTerm + "'"}];
                this.not_found = true;
            }
            else {
                this.not_found = false;
            }
            // if (this.data.length > 0 && this.not_found === true) this.not_found = false;
        }
        else {
            const members = await this._rpc({
                'route': '/snippet/member_committee/' + this.committee_id,
                'params': {
                    'category_id': searchDomain,
                },
            });
            this.data = members['data']
            this.committee_data_end = members['committee_data_end']
            this.committee_data_start = members['committee_data_start']
            this.committee_name = members['committee_name']
        }
    },
    /**
     * @override
     * @private
     */
    _getSearchDomain: function () {
        const searchDomain = this._super.apply(this, arguments);
        const filterByTagIds = JSON.parse(this.$el.get(0).dataset.filterByTagIds || '[]');
        const filterByCommitteeIds = JSON.parse(this.$el.get(0).dataset.filterByCommitteeId || -1);

        if (filterByTagIds.length > 0) {
            searchDomain.push(['category_id', 'in', filterByTagIds]);
        }
        // var searchTerm = null
        // if (window.location.search.length > 0){
        //     searchTerm = window.location.search;
        // }
        // if (searchTerm) {
        //     const urlParams = new URLSearchParams(window.location.search);
        //     const obj = {};

        //     for (const key of urlParams.keys()) {
        //         obj[key] = urlParams.get(key);
        //     }
        //     if (obj.search.length > 0){
        //         this.searchTerm = obj.search.trim();
        //     }
        // }
        if (filterByCommitteeIds != -1) {
            this.committee_template_key = true;
            this.committee_id = filterByCommitteeIds;
        }
        return searchDomain;
    },
});

publicWidget.registry.dynamic_snippet = PublicMemberSnippet;

return PublicMemberSnippet;

});
