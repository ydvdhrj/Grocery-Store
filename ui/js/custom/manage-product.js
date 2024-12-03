document.addEventListener('DOMContentLoaded', async function() {
    // Check authentication
    if (!await checkAuth()) return;

    // Load UOM and products data
    try {
        const [uomList, products] = await Promise.all([
            callApi(API_ENDPOINTS.GET_UOM),
            callApi(API_ENDPOINTS.GET_PRODUCTS)
        ]);

        // Populate UOM dropdown
        const uomSelect = document.getElementById('uoms');
        uomList.forEach(uom => {
            const option = document.createElement('option');
            option.value = uom.uom_id;
            option.textContent = uom.uom_name;
            uomSelect.appendChild(option);
        });

        // Populate products table
        const tbody = document.querySelector('#productsTable tbody');
        tbody.innerHTML = '';
        products.forEach(product => {
            const row = tbody.insertRow();
            row.dataset.id = product.product_id;
            row.dataset.name = product.name;
            row.dataset.unit = product.uom_id;
            row.dataset.price = product.price_per_unit;
            row.innerHTML = `
                <td>${product.name}</td>
                <td>${uomList.find(u => u.uom_id === product.uom_id)?.uom_name || ''}</td>
                <td>${formatCurrency(product.price_per_unit)}</td>
                <td>
                    <button onclick="deleteProduct(${product.product_id})" class="btn btn-danger delete-product">Delete</button>
                </td>
            `;
        });
    } catch (error) {
        showError('Failed to load data: ' + error.message);
    }

    // Handle product form submission
    document.getElementById('productForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const productData = {
            name: document.getElementById('name').value,
            uom_id: parseInt(document.getElementById('uoms').value),
            price_per_unit: parseFloat(document.getElementById('price').value)
        };

        try {
            await callApi(API_ENDPOINTS.INSERT_PRODUCT, 'POST', productData);
            showSuccess('Product added successfully');
            window.location.reload();
        } catch (error) {
            showError('Failed to add product: ' + error.message);
        }
    });

    // Handle product modal
    const productModal = document.getElementById('productModal');
    productModal.addEventListener('hide.bs.modal', function(){
        document.getElementById('id').value = '0';
        document.getElementById('name').value = '';
        document.getElementById('uoms').value = '';
        document.getElementById('price').value = '';
        productModal.querySelector('.modal-title').textContent = 'Add New Product';
    });

    productModal.addEventListener('show.bs.modal', function(){
        // No need to load UOM list again
    });
});

async function deleteProduct(productId) {
    if (!confirm('Are you sure you want to delete this product?')) return;

    try {
        await callApi(API_ENDPOINTS.DELETE_PRODUCT, 'POST', { product_id: productId });
        showSuccess('Product deleted successfully');
        window.location.reload();
    } catch (error) {
        showError('Failed to delete product: ' + error.message);
    }
}