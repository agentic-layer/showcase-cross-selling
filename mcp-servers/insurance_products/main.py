from fastmcp import FastMCP

# Create an MCP server for insurance products
mcp = FastMCP("SecureLife Insurance Products")

# Company name
insurance_company_name = "SecureLife Insurance"


def _create_error_response(message: str, error_code: str, **additional_data) -> dict:
    """Create a standardized error response."""
    response = {
        "status": "error",
        "message": message,
        "error_code": error_code
    }
    response.update(additional_data)
    return response


def _create_success_response(message: str, **additional_data) -> dict:
    """Create a standardized success response."""
    response = {
        "status": "success",
        "message": message
    }
    response.update(additional_data)
    return response


@mcp.tool()
def get_insurance_products() -> dict:
    """
    Retrieves all available insurance products from the product database
    with their features, pricing, and eligibility criteria.

    Returns:
        Dictionary with all available insurance products and their details.
    """
    # TODO: Implement actual product database connection
    # For skeleton purposes, using comprehensive mock product data
    mock_products = {
        "life_insurance": {
            "product_id": "LIFE001",
            "name": "SecureLife Premium",
            "description": "Comprehensive life insurance with flexible coverage options",
            "min_coverage": 50000,
            "max_coverage": 1000000,
            "age_range": {"min": 18, "max": 70},
            "base_premium_rate": 0.8,  # per 1000 coverage per month
            "features": [
                "Term and whole life options",
                "Accidental death benefit",
                "Disability waiver of premium",
                "Cash value accumulation (whole life)"
            ],
            "target_segments": ["families", "high_income", "business_owners"]
        },
        "health_insurance": {
            "product_id": "HEALTH001",
            "name": "HealthGuard Plus",
            "description": "Comprehensive health insurance with extensive coverage",
            "monthly_premium_range": {"min": 180, "max": 600},
            "age_range": {"min": 18, "max": 75},
            "features": [
                "Hospitalization coverage",
                "Outpatient treatment",
                "Prescription drugs",
                "Preventive care",
                "Dental and vision add-ons available"
            ],
            "target_segments": ["families", "self_employed", "premium"]
        },
        "car_insurance": {
            "product_id": "AUTO001",
            "name": "DriveSecure Comprehensive",
            "description": "Full coverage auto insurance with competitive rates",
            "coverage_types": ["Liability", "Collision", "Comprehensive", "Uninsured motorist"],
            "discount_factors": [
                "Safe driver discount (up to 25%)",
                "Multi-policy discount (15%)",
                "Anti-theft device discount (5%)",
                "Good student discount (10%)"
            ],
            "average_premium_range": {"min": 60, "max": 200},
            "target_segments": ["all_drivers", "families", "young_professionals"]
        },
        "home_insurance": {
            "product_id": "HOME001",
            "name": "HomeShield Complete",
            "description": "Comprehensive home insurance protecting property and belongings",
            "coverage_types": ["Dwelling", "Personal property", "Liability", "Additional living expenses"],
            "premium_factors": ["Property value", "Location", "Construction type", "Security features"],
            "average_premium_range": {"min": 80, "max": 300},
            "target_segments": ["homeowners", "premium", "families"]
        },
        "travel_insurance": {
            "product_id": "TRAVEL001",
            "name": "TravelSafe International",
            "description": "Travel insurance for domestic and international trips",
            "coverage_options": [
                "Trip cancellation/interruption",
                "Medical emergencies abroad",
                "Lost/delayed baggage",
                "Emergency evacuation"
            ],
            "premium_range": {"per_day": {"min": 2, "max": 15}},
            "trip_duration_max": 365,
            "target_segments": ["frequent_travelers", "families", "business_travelers"]
        },
        "disability_insurance": {
            "product_id": "DISABILITY001",
            "name": "IncomeProtect",
            "description": "Disability insurance to protect income in case of inability to work",
            "coverage_percentage": {"min": 60, "max": 80},
            "benefit_period_options": ["2 years", "5 years", "until retirement"],
            "waiting_period_options": [30, 90, 180, 365],
            "target_segments": ["high_income", "professionals", "skilled_workers"]
        },
        "business_insurance": {
            "product_id": "BUSINESS001",
            "name": "BusinessGuard Pro",
            "description": "Comprehensive business insurance for small to medium enterprises",
            "coverage_types": ["General liability", "Property", "Business interruption", "Cyber liability"],
            "target_segments": ["business_owners", "self_employed", "professionals"]
        }
    }

    return _create_success_response(
        "Insurance products retrieved successfully",
        products=mock_products,
        product_count=len(mock_products)
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
    all_products_response = get_insurance_products()

    if all_products_response["status"] != "success":
        return all_products_response

    products = all_products_response["products"]

    # Find the specific product
    for product_key, product_data in products.items():
        if product_data["product_id"] == product_id:
            return _create_success_response(
                f"Product details for {product_data['name']}",
                product=product_data,
                product_key=product_key
            )

    return _create_error_response(
        f"Product with ID '{product_id}' not found",
        "PRODUCT_NOT_FOUND",
        requested_product_id=product_id
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
    all_products_response = get_insurance_products()

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
            requested_segment=segment
        )

    return _create_success_response(
        f"Found {len(matching_products)} products for segment '{segment}'",
        products=matching_products,
        segment=segment,
        product_count=len(matching_products)
    )