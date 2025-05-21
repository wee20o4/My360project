odoo.define('membership_profile.zoom', function (require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var _lt = core._lt; 

    publicWidget.registry.ZoomQRCode = publicWidget.Widget.extend({
        selector: '.pm_zoom',
        events: {'click': '_onClick'},
        /**
         * 
         */
        _onClick: function () {
            // const modalTitle =  _lt("Scan the QR code to save contact !")
            const src = this.$target[0].currentSrc;
            const name = this.$target[0].dataset.name;
            const modalTitle = _lt(`${name}  Profile`)
            const $createModal = $(`
                <div class="modal fade" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">${modalTitle}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <img width="100%" src="${src}" alt="QR Code"/>
                            </div>
                        </div>
                    </div>
                </div>`);
            $createModal.appendTo('body').modal('show');
        },
    });
    return publicWidget.registry.ZoomQRCode;
});
