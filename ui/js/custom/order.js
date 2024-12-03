var productPrices = {};

document.addEventListener('DOMContentLoaded', async function() {
    // Check authentication
    if (!await checkAuth()) return;

    let products = [];
    let orderItems = [];

    try {
        // Load products
        products = await callApi(API_ENDPOINTS.GET_PRODUCTS);
        
        // Populate product dropdown
        const productSelect = document.getElementById('product');
        products.forEach(product => {
            const option = document.createElement('option');
            option.value = product.product_id;
            option.textContent = product.name;
            productSelect.appendChild(option);
            productPrices[product.product_id] = product.price_per_unit;
        });

        // Load existing orders
        const orders = await callApi(API_ENDPOINTS.GET_ORDERS);
        const tbody = document.querySelector('#ordersTable tbody');
        tbody.innerHTML = '';
        orders.forEach(order => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${order.order_id}</td>
                <td>${order.customer_name}</td>
                <td>${formatCurrency(order.total)}</td>
                <td>${formatDate(order.order_date)}</td>
            `;
        });
    } catch (error) {
        showError('Failed to load data: ' + error.message);
    }

    // Handle adding items to order
    document.getElementById('addToOrder').addEventListener('click', function() {
        const productId = parseInt(document.getElementById('product').value);
        const quantity = parseFloat(document.getElementById('quantity').value);
        
        if (!productId || !quantity) {
            showError('Please select a product and enter quantity');
            return;
        }

        const product = products.find(p => p.product_id === productId);
        if (!product) {
            showError('Product not found');
            return;
        }

        const total = quantity * product.price_per_unit;
        orderItems.push({
            product_id: productId,
            quantity: quantity,
            total_price: total
        });

        // Update order items table
        const itemsBody = document.querySelector('#orderItemsTable tbody');
        const row = itemsBody.insertRow();
        row.innerHTML = `
            <td>${product.name}</td>
            <td>${quantity}</td>
            <td>${formatCurrency(product.price_per_unit)}</td>
            <td>${formatCurrency(total)}</td>
            <td><button onclick="this.closest('tr').remove(); updateTotal();" class="btn btn-danger">Remove</button></td>
        `;

        // Reset form
        document.getElementById('quantity').value = '';
        updateTotal();
    });

    // Handle order submission
    document.getElementById('orderForm').addEventListener('submit', async function(e) {
        e.preventDefault();

        if (orderItems.length === 0) {
            showError('Please add items to the order');
            return;
        }

        const orderData = {
            customer_name: document.getElementById('customerName').value,
            total: calculateTotal(),
            order_details: orderItems
        };

        try {
            await callApi(API_ENDPOINTS.INSERT_ORDER, 'POST', orderData);
            showSuccess('Order placed successfully');
            window.location.reload();
        } catch (error) {
            showError('Failed to place order: ' + error.message);
        }
    });
});

function updateTotal() {
    const total = calculateTotal();
    document.getElementById('totalAmount').textContent = formatCurrency(total);
}

function calculateTotal() {
    let total = 0;
    document.querySelectorAll('#orderItemsTable tbody tr').forEach(row => {
        const cells = row.cells;
        total += parseFloat(cells[3].textContent.replace(/[^0-9.-]+/g, ''));
    });
    return total;
}

// Add more button click event
document.getElementById('addMoreButton').addEventListener('click', function() {
    var row = $(".product-box").html();
    $(".product-box-extra").append(row);
    $(".product-box-extra .remove-row").last().removeClass('hideit');
    $(".product-box-extra .product-price").last().text('0.0');
    $(".product-box-extra .product-qty").last().val('1');
    $(".product-box-extra .product-total").last().text('0.0');
});

// Remove row click event
$(document).on("click", ".remove-row", function (){
    $(this).closest('.row').remove();
    calculateValue();
});

// Cart product change event
$(document).on("change", ".cart-product", function (){
    var product_id = $(this).val();
    var price = productPrices[product_id];

    $(this).closest('.row').find('#product_price').val(price);
    calculateValue();
});

// Product quantity change event
$(document).on("change", ".product-qty", function (e){
    calculateValue();
});

// Save order click event
document.getElementById('saveOrder').addEventListener('click', function(){
    var formData = $("form").serializeArray();
    var requestPayload = {
        customer_name: null,
        total: null,
        order_details: []
    };
    var orderDetails = [];
    for(var i=0;i<formData.length;++i) {
        var element = formData[i];
        var lastElement = null;

        switch(element.name) {
            case 'customerName':
                requestPayload.customer_name = element.value;
                break;
            case 'product_grand_total':
                requestPayload.grand_total = element.value;
                break;
            case 'product':
                requestPayload.order_details.push({
                    product_id: element.value,
                    quantity: null,
                    total_price: null
                });                
                break;
            case 'qty':
                lastElement = requestPayload.order_details[requestPayload.order_details.length-1];
                lastElement.quantity = element.value
                break;
            case 'item_total':
                lastElement = requestPayload.order_details[requestPayload.order_details.length-1];
                lastElement.total_price = element.value
                break;
        }

    }
    callApi("POST", orderSaveApiUrl, {
        'data': JSON.stringify(requestPayload)
    });
});