/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class CateringEprocurementKiosk extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");

        this.state = useState({
            step: 'supplier', // supplier -> products -> success
            suppliers: [],
            products: [],
            cart: [], // Array of { product: Object, qty: Number }
            selectedSupplierId: null,
            searchQuery: '',
            showCart: false,
            createdPOName: ''
        });

        onWillStart(async () => {
            await this.loadSuppliers();
        });
    }

    get cartItemsCount() {
        return this.state.cart.reduce((acc, item) => acc + item.qty, 0);
    }

    get filteredProducts() {
        if (!this.state.searchQuery) return this.state.products;
        const q = this.state.searchQuery.toLowerCase();
        return this.state.products.filter(p => p.name.toLowerCase().includes(q));
    }

    getCartQty(productId) {
        const item = this.state.cart.find(i => i.product.id === productId);
        return item ? item.qty : 0;
    }

    async loadSuppliers() {
        // Find partners that are suppliers
        this.state.suppliers = await this.orm.searchRead(
            'res.partner',
            [['supplier_rank', '>', 0]],
            ['id', 'name', 'image_128']
        );
    }

    async selectSupplier(supplierId) {
        this.state.selectedSupplierId = supplierId;
        // Fetch products associated with this supplier through product.supplierinfo
        // In Odoo, we search product.product where seller_ids.partner_id contains this supplier
        this.state.products = await this.orm.searchRead(
            'product.product',
            [['seller_ids.partner_id', '=', supplierId], ['purchase_ok', '=', true]],
            ['id', 'name', 'uom_id'],
            { limit: 100 }
        );
        this.state.step = 'products';
        this.state.cart = [];
        this.state.showCart = false;
        this.state.searchQuery = '';
    }

    updateCart(product, delta) {
        const existingIndex = this.state.cart.findIndex(i => i.product.id === product.id);
        if (existingIndex >= 0) {
            this.state.cart[existingIndex].qty += delta;
            if (this.state.cart[existingIndex].qty <= 0) {
                this.state.cart.splice(existingIndex, 1);
            }
        } else if (delta > 0) {
            this.state.cart.push({ product: product, qty: delta });
        }
    }

    removeFromCart(productId) {
        const index = this.state.cart.findIndex(i => i.product.id === productId);
        if (index >= 0) {
            this.state.cart.splice(index, 1);
        }
    }

    toggleCart() {
        this.state.showCart = !this.state.showCart;
    }

    onSearch(ev) {
        this.state.searchQuery = ev.target.value;
    }

    async submitOrder() {
        if (this.state.cart.length === 0) return;

        try {
            const orderLines = this.state.cart.map(item => ({
                product_id: item.product.id,
                product_qty: item.qty
            }));

            // Call the custom model method to generate the PO
            const poId = await this.orm.call(
                'purchase.order',
                'create_kiosk_order',
                [this.state.selectedSupplierId, orderLines]
            );

            // Fetch the generated name to display
            const po = await this.orm.read('purchase.order', [poId], ['name']);
            this.state.createdPOName = po[0].name;
            
            this.state.step = 'success';
            
            setTimeout(() => {
                if (this.state.step === 'success') {
                    this.resetKiosk();
                }
            }, 5000);
            
        } catch (error) {
            this.notification.add("Error creating Purchase Order.", { type: "danger" });
            console.error(error);
        }
    }

    resetKiosk() {
        this.state.step = 'supplier';
        this.state.selectedSupplierId = null;
        this.state.cart = [];
        this.state.showCart = false;
        this.state.searchQuery = '';
    }

    closeKiosk() {
        this.action.doAction('base.action_ui_view');
    }
}

CateringEprocurementKiosk.template = "catering_eprocurement.Kiosk";

registry.category("actions").add("catering_eprocurement.kiosk_action", CateringEprocurementKiosk);
