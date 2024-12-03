document.addEventListener('DOMContentLoaded', function() {
    fetch('/getAllOrders')
        .then(response => response.json())
        .then(data => {
            const orderList = document.getElementById('order-list');
            data.forEach(order => {
                const listItem = document.createElement('li');
                listItem.textContent = `Order #${order.order_id} - ${order.customer_name} - $${order.total}`;
                orderList.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error fetching orders:', error));
});
