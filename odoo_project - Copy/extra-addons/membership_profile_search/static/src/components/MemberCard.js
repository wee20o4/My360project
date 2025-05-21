/** @odoo-module **/

import { Component } from "@odoo/owl";

export class MemberCard extends Component {
    static template = "membership_profile_search.MemberCard";

    get imageSrc() {
        return this.props.member.image_1920 && this.props.member.image_1920 !== ""
            ? `/web/image/res.partner/${this.props.member.id}/image_1920`
            : "/membership_profile_search/static/img/placeholder.png";
    }
}