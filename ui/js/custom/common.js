// API endpoints
const API_ENDPOINTS = {
    LOGIN: '/api/login',
    REGISTER: '/api/register',
    LOGOUT: '/api/logout',
    CHECK_AUTH: '/api/check-auth',
    GET_PRODUCTS: '/api/getProducts',
    INSERT_PRODUCT: '/api/insertProduct',
    DELETE_PRODUCT: '/api/deleteProduct',
    GET_ORDERS: '/api/getAllOrders',
    INSERT_ORDER: '/api/insertOrder',
    GET_UOM: '/api/getUOM'
};

// Helper function for making API calls
async function callApi(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(endpoint, options);
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'API call failed');
    }
    return response.json();
}

// Check authentication status
async function checkAuth() {
    try {
        const response = await fetch(API_ENDPOINTS.CHECK_AUTH);
        if (!response.ok) {
            window.location.href = '/login.html';
            return false;
        }
        return true;
    } catch (error) {
        console.error('Auth check failed:', error);
        window.location.href = '/login.html';
        return false;
    }
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Show error message
function showError(message) {
    alert(message);
}

// Show success message
function showSuccess(message) {
    alert(message);
}

// Export common functions
window.callApi = callApi;
window.checkAuth = checkAuth;
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;
window.showError = showError;
window.showSuccess = showSuccess;
window.API_ENDPOINTS = API_ENDPOINTS;

// For product drop in order
var productsApiUrl = 'https://fakestoreapi.com/products';

function calculateValue() {
    var total = 0;
    $(".product-item").each(function( index ) {
        var qty = parseFloat($(this).find('.product-qty').val());
        var price = parseFloat($(this).find('#product_price').val());
        price = price*qty;
        $(this).find('#item_total').val(price.toFixed(2));
        total += price;
    });
    $("#product_grand_total").val(total.toFixed(2));
}

function orderParser(order) {
    return {
        id : order.id,
        date : order.employee_name,
        orderNo : order.employee_name,
        customerName : order.employee_name,
        cost : parseInt(order.employee_salary)
    }
}

function productParser(product) {
    return {
        id : product.id,
        name : product.employee_name,
        unit : product.employee_name,
        price : product.employee_name
    }
}

function productDropParser(product) {
    return {
        id : product.id,
        name : product.title
    }
}

//To enable bootstrap tooltip globally
// $(function () {
//     $('[data-toggle="tooltip"]').tooltip()
// });