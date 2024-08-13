// API URL
const API_URL = 'http://localhost:8000';

// Function to fetch all products
async function getProducts() {
    try {
        const response = await fetch(`${API_URL}/products/`);
        const products = await response.json();
        displayProducts(products);
    } catch (error) {
        console.error('Error fetching products:', error);
    }
}

// Function to display products
function displayProducts(products) {
    const productList = document.getElementById('product-list');
    productList.innerHTML = '<h2>Product List</h2>';
    products.forEach(product => {
        const productDiv = document.createElement('div');
        productDiv.classList.add('product-item');
        productDiv.innerHTML = `
            <h3>${product.name}</h3>
            <p>Description: ${product.description || 'N/A'}</p>
            <p>Price: $${product.price.toFixed(2)}</p>
            <p>Quantity: ${product.quantity}</p>
        `;
        productList.appendChild(productDiv);
    });
}

// Function to add a new product
async function addProduct(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const product = Object.fromEntries(formData.entries());

    console.log('Sending product data:', product); // Debugging

    try {
        const response = await fetch(`${API_URL}/products/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(product),
        });
        const newProduct = await response.json();

        if (!response.ok) {
            throw new Error(JSON.stringify(responseData));
        }
        console.log('Product added:', responseData);
        showNotification('Product added successfully!');

        getProducts(); // Refresh the product list
        event.target.reset(); // Clear the form
    } catch (error) {
        console.error('Error adding product:', error);
        showNotification(`Failed to add product: ${error.message}`, true);
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    getProducts();
    document.getElementById('add-product-form').addEventListener('submit', addProduct);
});