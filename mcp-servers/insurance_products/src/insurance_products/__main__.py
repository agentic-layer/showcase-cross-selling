from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from . import mock_database

# Create an MCP server for insurance products
mcp: FastMCP = FastMCP("SecureLife Insurance Products")

# Company name
insurance_company_name = "SecureLife Insurance"


def _create_error_response(message: str, error_code: str, **additional_data) -> dict:
    """Create a standardized error response."""
    response = {"status": "error", "message": message, "error_code": error_code}
    response.update(additional_data)
    return response


def _create_success_response(message: str, **additional_data) -> dict:
    """Create a standardized success response."""
    response = {"status": "success", "message": message}
    response.update(additional_data)
    return response


@mcp.tool()
def get_insurance_products() -> dict:
    """
    Retrieves all available insurance products from the product database.

    This tool fetches a comprehensive list of all insurance products offered,
    including details about their features, pricing, and eligibility criteria.
    It is the primary method for discovering what insurance options are available
    to customers.

    Returns:
        A dictionary containing the status of the operation and the retrieved products.
        On success, the dictionary will have the following structure:
        {
            "status": "success",
            "message": "Insurance products retrieved successfully",
            "products": {
                "life_insurance": {
                    "product_id": "LIFE001",
                    "name": "SecureLife Premium",
                    "description": "Comprehensive life insurance with flexible coverage options",
                    ...
                },
                "health_insurance": { ... },
                ...
            },
            "product_count": 7
        }
        On failure, the dictionary might look like this:
        {
            "status": "error",
            "error_message": "Failed to connect to the product database."
        }

    Usage Guidance:
    This tool should be used when a user (an insurance broker) asks a general question about the types
    of insurance available, such as "What insurance products do we offer?", "Can you tell
    me about our products?", or "I'm looking for a specific insurance for a customer." It provides the
    foundational information needed to answer broad queries and can be the first
    step before using more specific tools to get quotes or filter products.


    Error Handling:
    If the tool returns a status of "error", inform the user that you are
    currently unable to retrieve the product information and suggest they try
    again later.
    """
    # For skeleton purposes, using comprehensive mock product data
    mock_products = mock_database.get_all_products()

    return _create_success_response(
        "Insurance products retrieved successfully",
        products=mock_products,
        product_count=len(mock_products),
    )


@mcp.tool()
def get_product_details(product_id: str) -> dict:
    """
    Retrieves detailed information about a specific insurance product.

    Args:
        product_id: The ID of the insurance product to retrieve details for

    Returns:
        Dictionary with detailed product information or error if not found.
    """
    # Get all products first
    all_products_response = mock_database.get_all_products()

    if all_products_response["status"] != "success":
        return all_products_response

    products = all_products_response["products"]

    # Find the specific product
    for product_key, product_data in products.items():
        if product_data["product_id"] == product_id:
            return _create_success_response(
                f"Product details for {product_data['name']}",
                product=product_data,
                product_key=product_key,
            )

    return _create_error_response(
        f"Product with ID '{product_id}' not found",
        "PRODUCT_NOT_FOUND",
        requested_product_id=product_id,
    )


@mcp.tool()
def get_products_by_segment(segment: str) -> dict:
    """
    Retrieves insurance products that target a specific customer segment.

    Args:
        segment: The customer segment to filter by (e.g., "families", "high_income", "business_owners")

    Returns:
        Dictionary with products matching the specified segment.
    """
    # Get all products first
    all_products_response = mock_database.get_all_products()

    if all_products_response["status"] != "success":
        return all_products_response

    products = all_products_response["products"]
    matching_products = {}

    # Filter products by segment
    for product_key, product_data in products.items():
        if "target_segments" in product_data and segment in product_data["target_segments"]:
            matching_products[product_key] = product_data

    if not matching_products:
        return _create_error_response(
            f"No products found for segment '{segment}'",
            "NO_PRODUCTS_FOR_SEGMENT",
            requested_segment=segment,
        )

    return _create_success_response(
        f"Found {len(matching_products)} products for segment '{segment}'",
        products=matching_products,
        segment=segment,
        product_count=len(matching_products),
    )


@mcp.custom_route("/health", methods=["GET"])
async def health_check(_: Request) -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse({"status": "healthy"})


def main():
    mcp.run(transport="streamable-http", host="0.0.0.0")


if __name__ == "__main__":
    main()
