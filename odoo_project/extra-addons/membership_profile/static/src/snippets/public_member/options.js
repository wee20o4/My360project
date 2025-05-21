odoo.define('public_member.options', function (require) {
    'use strict';

    require('web.dom_ready');
    const { _t } = require('web.core');
    const options = require('web_editor.snippets.options');
    require('website.editor.snippets.options');

    options.registry.PublicMemberTitleFilter = options.Class.extend({
        events: {
            'click we-button.o_we_select_filter_member': '_onSelectFilterMember',
        },
        /**
         * @override 
        */
        init: function () {
            this._super.apply(this, arguments);
            this.dynamicFilters = {};
        },
        /**
         * @override
         */
        start: function () {
            this.default_filter = this.$target.closest('[data-filter-member]').data('filter-member');
            this.default_filter_key = this.$target.closest('[data-filter-member-key]').data('filter-member-key');
            this._setDefaultFilter();
            this._setFilterKeyActive();
            return this._super.apply(this, arguments);
        },
        /**
         *
         * @override
         */
        async onBuilt() {
            console.log('onBuilt');
        },

        /**
         * 
         */
        async _setOptionsDefaultValues() {
            if (this.dynamicFilters[selectedFilterId] &&
                    !this.dynamicFilterTemplates[this.$target.get(0).dataset['templateKey']]) {
                this._setDefaultTemplate();
            }
            this.options.wysiwyg.odooEditor.observerActive();
        },
        /**
         * 
         * @param {*} uiFragment 
         */
        _setDefaultFilter: function (vals) {
            if (!vals) vals = this.default_filter;
            const weSelect = this.$el.find("we-select[data-name='filter_public_member'] div we-toggler");
            // Set text filter member for toggle
            return weSelect.text(vals);
        },
        /**
         * 
         * @param {*} uiFragment 
         */
        _setFilterKeyActive: function () {
            // Add class active for button have value equal filter
            this.$el.find("we-select[data-name='filter_public_member'] we-selection-items we-button[data-select-filter-member='" + this.default_filter_key + "']").addClass('active');
        },
        /**
         *
         * @override
         * @private
         */
        _renderCustomXML: async function (uiFragment) {
            await this._super.apply(this, arguments);
        },
        /**
         * 
         */
        _onSelectFilterMember: function (event) {
            const filterMember = event.target.closest('[data-select-filter-member]');
            const value_filter = filterMember.dataset.selectFilterMember;
            return this.setDefaultFilter(value_filter)
        },
        /**
         * @override
         */
        async setDefaultFilter(vals) {
            this.$target.get(0).dataset['filterMember'] = "Alls";
            this.$target.get(0).dataset['filterMemberKey'] = "alls";
            this.trigger_up('request_save', { reload: true, optionSelector: this.data.selector });
            // var self = this
            // await this._rpc({
            //     route: '/website/set-value-filter-member',
            //     params: {
            //         'value_field_filter_member': vals,
            //     },
            // }).then(function () {
            //     self.trigger_up('request_save', { reload: true, optionSelector: self.data.selector });
            // });
        },
    });
});