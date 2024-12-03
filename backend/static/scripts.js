document.addEventListener('DOMContentLoaded', function() {
    fetch('/getUOM')
        .then(response => response.json())
        .then(data => {
            const uomList = document.getElementById('uom-list');
            data.forEach(uom => {
                const listItem = document.createElement('li');
                listItem.textContent = uom.uom_name;
                uomList.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error fetching UOMs:', error));
});
