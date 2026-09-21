import sys
import os

# Add the 'src' directory to the Python path so we can import app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app, cart, products

import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Reset cart and stock before each test
    cart.clear()
    for p in products:
        p['stock'] = 10 
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test that the home page loads successfully and shows products."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Wireless Mouse' in response.data

def test_add_to_cart(client):
    """Test adding an item to the shopping cart."""
    response = client.post('/add_to_cart/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'Wireless Mouse' in response.data
    # Verify the item made it into the cart list
    assert len(cart) == 1
    assert cart[0]['name'] == 'Wireless Mouse'

def test_checkout(client):
    """Test completing checkout clears the cart."""
    # First add an item
    client.post('/add_to_cart/1', follow_redirects=True)
    assert len(cart) == 1
    
    # Then checkout
    response = client.post('/checkout', follow_redirects=True)
    assert response.status_code == 200
    assert len(cart) == 0