odoo.define('membership_profile.vcard', function (require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    const {Markup} = require('web.utils');

    var _t = core._t;

    publicWidget.registry.ImportVCard = publicWidget.Widget.extend({
        selector: '.o_onclick_create_vcard',
        events: {'click': '_onClick'},
        /**
         * 
         */
        _onClick: function () {
            const vcard = this.$target.closest('[data-vcard]').data('vcard');
            // this._downloadVCard(vcard, 'contact.vcf');
            this._openVCard(vcard);
        },
        /**
         * 
         * @param {*} vcard 
         */
        _openVCard: function (vcard) {
            const blob = new Blob([vcard], { type: 'text/vcard' });
            const vcardURL = URL.createObjectURL(blob);
            window.open(vcardURL);
        },
        /**
         * Unused
         */
        _downloadVCard: function(vcard, filename) {
            const vcardData = 'data:text/plain;charset=utf-8,' + encodeURIComponent(vcard);
            const element = document.createElement('a');
            element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(vcard));
            element.setAttribute('download', filename);
            element.style.display = 'none';
            document.body.appendChild(element);

            element.click();
            document.body.removeChild(element);
        }

    });
    return publicWidget.registry.ImportVCard;
});
