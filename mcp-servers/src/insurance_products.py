"""Insurance Products MCP server."""

from fastmcp import FastMCP
from opentelemetry.trace import get_tracer

import middleware
import otel
import products_db
import response

otel.setup_otel()
tracer = get_tracer(__name__)

# Create an MCP server for insurance products
mcp: FastMCP = FastMCP("SecureLife Insurance Products", middleware=[middleware.OtelMetricsMiddleware()])


def _summarize_product(product_id: str, product_data: dict) -> dict:
    """Extract a slim product summary with only the essential fields."""
    return {
        "product_id": product_id,
        "name": product_data.get("name"),
        "type": product_data.get("type"),
        "description": product_data.get("description"),
        "target_segments": product_data.get("target_segments"),
    }


@mcp.tool()
def get_insurance_products() -> dict:
    """
    Retrieves slim summaries of all available insurance products.

    Returns product_id, name, type, description, and target_segments for each product.
    Use get_product_details to get complete information about a specific product.

    Returns:
        Dictionary with product summaries and product_count on success, or error details on failure.
    """
    with tracer.start_as_current_span("products_db.get_all_products"):
        mock_products = products_db.get_all_products()

    summaries = {key: _summarize_product(key, data) for key, data in mock_products.items()}

    return response.create_success_response(
        "Insurance products retrieved successfully",
        products=summaries,
        product_count=len(summaries),
    )


@mcp.tool()
def get_product_details(product_id: str) -> dict:
    """
    Retrieves complete information about a specific insurance product.

    Use this tool to get full product details (pricing, features, eligibility, etc.)
    after identifying a product via one of the list tools.

    Args:
        product_id: The ID of the insurance product to retrieve details for

    Returns:
        Dictionary with complete product information or error if not found.
    """
    # Find the specific product
    with tracer.start_as_current_span("products_db.get_all_products", attributes={"product_id": product_id}):
        product_data = products_db.get_all_products().get(product_id)
    if product_data is not None:
        return response.create_success_response(
            f"Product details for {product_data['name']}",
            product=product_data,
            product_id=product_id,
        )

    return response.create_error_response(
        f"Product with ID '{product_id}' not found",
        "PRODUCT_NOT_FOUND",
        requested_product_id=product_id,
    )


@mcp.tool()
def get_products_by_segment(segment: str) -> dict:
    """
    Retrieves slim summaries of insurance products targeting a specific customer segment.

    Returns product_id, name, type, description, and target_segments for each match.
    Use get_product_details for complete information about a specific product.

    Args:
        segment: The customer segment to filter by (e.g., "families", "high_income", "business_owners")

    Returns:
        Dictionary with product summaries matching the segment, or error if none found.
    """
    # Get all products
    with tracer.start_as_current_span("products_db.get_all_products", attributes={"segment": segment}):
        products = products_db.get_all_products()
    matching_products = {}

    # Filter products by segment
    for product_id, product_data in products.items():
        if "target_segments" in product_data and segment in product_data["target_segments"]:
            matching_products[product_id] = _summarize_product(product_id, product_data)

    if not matching_products:
        return response.create_error_response(
            f"No products found for segment '{segment}'",
            "NO_PRODUCTS_FOR_SEGMENT",
            requested_segment=segment,
        )

    return response.create_success_response(
        f"Found {len(matching_products)} products for segment '{segment}'",
        products=matching_products,
        segment=segment,
        product_count=len(matching_products),
    )


@mcp.tool()
def get_products_by_type(product_type: str) -> dict:
    """
    Retrieves slim summaries of insurance products of a specific type.

    Returns product_id, name, type, description, and target_segments for each match.
    Use get_product_details for complete information about a specific product.

    Args:
        product_type: The product type to filter by (e.g., "life insurance", "health insurance",
                     "auto insurance", "home insurance", "travel insurance", etc.)

    Returns:
        Dictionary with product summaries matching the type, or error if none found.
    """
    # Get all products
    with tracer.start_as_current_span("products_db.get_all_products", attributes={"product_type": product_type}):
        products = products_db.get_all_products()
    matching_products = {}

    # Filter products by type
    for product_id, product_data in products.items():
        if product_data.get("type") == product_type:
            matching_products[product_id] = _summarize_product(product_id, product_data)

    if not matching_products:
        return response.create_error_response(
            f"No products found for type '{product_type}'",
            "NO_PRODUCTS_FOR_TYPE",
            requested_type=product_type,
        )

    return response.create_success_response(
        f"Found {len(matching_products)} products for type '{product_type}'",
        products=matching_products,
        product_type=product_type,
        product_count=len(matching_products),
    )
