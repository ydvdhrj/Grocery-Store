document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    fetch('/api/check-auth')
        .then(response => {
            if (!response.ok) {
                window.location.href = 'login.html';
            }
        });

    // Load dashboard data
    Promise.all([
        fetch('/api/getProducts'),
        fetch('/api/getAllOrders')
    ])
    .then(responses => Promise.all(responses.map(r => r.json())))
    .then(([products, orders]) => {
        // Update product count
        document.getElementById('productCount').textContent = products.length;
        
        // Update order count
        document.getElementById('orderCount').textContent = orders.length;
        
        // Display recent orders
        const recentOrders = orders.slice(-5); // Get last 5 orders
        const tbody = document.getElementById('recentOrdersTable').getElementsByTagName('tbody')[0];
        
        recentOrders.forEach(order => {
            const row = tbody.insertRow();
            row.insertCell(0).textContent = order.order_id;
            row.insertCell(1).textContent = order.customer_name;
            row.insertCell(2).textContent = `$${order.total_amount.toFixed(2)}`;
            row.insertCell(3).textContent = new Date(order.order_date).toLocaleDateString();
        });
    })
    .catch(error => {
        console.error('Error loading dashboard data:', error);
    });

    // Handle logout
    document.getElementById('logoutBtn').addEventListener('click', function(e) {
        e.preventDefault();
        fetch('/api/logout')
            .then(response => response.json())
            .then(data => {
                window.location.href = 'login.html';
            })
            .catch(error => {
                console.error('Error during logout:', error);
            });
    });
});
