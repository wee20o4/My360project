/** @odoo-module **/

import { mount } from "@odoo/owl";
import { MemberList } from "../components/MemberList";

document.addEventListener("DOMContentLoaded", () => {
    const root = document.querySelector(".member-list-container");
    if (root) {
        mount(MemberList, root, { props: { members: window.members || [] } });
    } else {
        console.error("Không tìm thấy phần tử .member-list-container. Đảm bảo template đã được render.");
    }
});