odoo.define('membership_profile.s_public_member_options', function (require) {
'use strict';

const options = require('web_editor.snippets.options');
const dynamicSnippetOptions = require('website.s_dynamic_snippet_options');


const DynamicPublicMemberSnippet = dynamicSnippetOptions.extend({
    /**
     *
     * @override
     */
    init: function () {
        this._super.apply(this, arguments);
        this.modelNameFilter = 'res.partner';
        this.public_members = {};
        this.default_filter_committee = '/'
        this.committeeIds = {}
    },

    /**
     * @override
     */
    start: function () {
        return this._super.apply(this, arguments);
    },

    async willStart() {
        const _super = this._super.bind(this);
        this.tagIDs = JSON.parse(this.$target[0].dataset.filterByTagIds || '[]');
        const tags = await this._rpc({
            model: 'res.partner.category',
            method: 'search_read',
            domain: [],
            fields: ['id', 'display_name'],
        });
        this.allTagsByID = {};
        for (const tag of tags) {
            this.allTagsByID[tag.id] = tag;
        }

        return _super(...arguments);
    },

    _fetchCommittees: function() {
        return this._rpc({
            model: 'membership.committee',
            method: 'search_read',
            domain: [],
            fields: ['id', 'name'],
        });

    },
    /**
     *
     * @override
     * @private
     */
    _renderCustomXML: async function (uiFragment) {
        await this._super.apply(this, arguments);
        await this._setDefaultFilterCommittee(uiFragment);
    },

    _setDefaultFilterCommittee: async function (uiFragment) {
        if (!Object.keys(this.committeeIds).length) {
            const committeeList = await this._fetchCommittees();
            this.committeeIds = {}
            for (const committee of committeeList) {
                this.committeeIds[committee.id] = committee;
            }
        }
        const committeeSelectorEl = uiFragment.querySelector('[data-name="committee_id_opt"]');
        // Set text filter member for toggle
        return this._renderSelectUserValueWidgetButtons(committeeSelectorEl, this.committeeIds);
    },

    /**
     * @override
     * @param {*} previewMode 
     * @param {*} widgetValue 
     * @param {*} params 
     */
    selectDataAttribute: function (previewMode, widgetValue, params) {
        this._super.apply(this, arguments);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------
    /**
     * Fetches public members.
     * @private
     * @returns {Promise}
     */
    _fetchPublicMembers: async function () {
        const members = await this._rpc({
            'route': '/snippets/partners/members',
            'params': {},
        });
        return members;
    },
    /**
     * @override
     */
    _fetchDynamicFilters: async function() {
        this._defaultFilterId = 8;
    },
    /**
     * @override
     */
    _fetchDynamicFilterTemplates: async function() {
        this._defaultTemplateKey = 'membership_profile.dynamic_filter_template_public_member_card';
    },

    _renderPublicMemberSelector: async function (uiFragment) {
        if (!Object.keys(this.public_members).length) {
            const membersList = await this._fetchPublicMembers();
            this.public_members = membersList['partners'];
        }
        const memberSelectorEl = uiFragment.querySelector('[data-name="member_tag_opt"]');
        const _render = await this._renderSelectUserValueWidgetButtons(memberSelectorEl, this.public_members);
        return _render;
    },

    setTags(previewMode, widgetValue, params) {
        this.tagIDs = JSON.parse(widgetValue).map(tag => tag.id);
        this.selectDataAttribute(previewMode, JSON.stringify(this.tagIDs), params);
    },
    /**
     * @override
     */
    async _computeWidgetState(methodName, params) {
        if (methodName === 'setTags') {
            return JSON.stringify(this.tagIDs.map(id => this.allTagsByID[id]));
        }
        return this._super(...arguments);
    },
});

options.registry.public_member_snippet = DynamicPublicMemberSnippet;

return DynamicPublicMemberSnippet;
});