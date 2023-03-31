from shopping_cart import ShoppingCart
import pytest
from item_database import ItemDatabase
from unittest.mock import Mock


# So we don't have to set up cart with 5 apples every time. Each test function still makes new shopping cart.
@pytest.fixture
def cart():
    return ShoppingCart(5)


def test_can_add_item_to_cart(cart):
    cart.add("apple")
    assert cart.size() == 1


def test_when_item_added_then_cart_contains_item(cart):
    cart.add("apple")
    assert "apple" in cart.get_items()


def test_when_add_more_than_max_items_should_fail(cart):
    for _ in range(5):
        cart.add("apple")
    # Test passes if error is thrown (which we want)
    with pytest.raises(OverflowError):
        cart.add("apple")


def test_can_get_total_price(cart):
    cart.add("apple")
    cart.add("orange")
    item_database = ItemDatabase()

    # Create mock run since database could change under your feet
    # item_database.get = Mock(return_value=1.0)

    def mock_get_item(item: str):
        if item == "apple":
            return 1.0
        if item == "orange":
            return 2.0

    item_database.get = Mock(side_effect=mock_get_item)
    assert cart.get_total_price(item_database) == 3.0
