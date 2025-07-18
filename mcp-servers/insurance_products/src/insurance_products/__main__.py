from fastmcp import FastMCP

# Create an MCP server for insurance products
mcp = FastMCP("SecureLife Insurance Products")

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
                "Cash value accumulation (whole life)",
            ],
            "target_segments": ["families", "high_income", "business_owners"],
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
                "Dental and vision add-ons available",
            ],
            "target_segments": ["families", "self_employed", "premium"],
        },
        "car_insurance": {
            "product_id": "AUTO001",
            "name": "DriveSecure Comprehensive",
            "description": "Full coverage auto insurance with competitive rates",
            "coverage_types": [
                "Liability",
                "Collision",
                "Comprehensive",
                "Uninsured motorist",
            ],
            "discount_factors": [
                "Safe driver discount (up to 25%)",
                "Multi-policy discount (15%)",
                "Anti-theft device discount (5%)",
                "Good student discount (10%)",
            ],
            "average_premium_range": {"min": 60, "max": 200},
            "target_segments": ["all_drivers", "families", "young_professionals"],
        },
        "home_insurance": {
            "product_id": "HOME001",
            "name": "HomeShield Complete",
            "description": "Comprehensive home insurance protecting property and belongings",
            "coverage_types": [
                "Dwelling",
                "Personal property",
                "Liability",
                "Additional living expenses",
            ],
            "premium_factors": [
                "Property value",
                "Location",
                "Construction type",
                "Security features",
            ],
            "average_premium_range": {"min": 80, "max": 300},
            "target_segments": ["homeowners", "premium", "families"],
        },
        "travel_insurance": {
            "product_id": "TRAVEL001",
            "name": "TravelSafe International",
            "description": "Travel insurance for domestic and international trips",
            "coverage_options": [
                "Trip cancellation/interruption",
                "Medical emergencies abroad",
                "Lost/delayed baggage",
                "Emergency evacuation",
            ],
            "premium_range": {"per_day": {"min": 2, "max": 15}},
            "trip_duration_max": 365,
            "target_segments": ["frequent_travelers", "families", "business_travelers"],
        },
        "disability_insurance": {
            "product_id": "DISABILITY001",
            "name": "IncomeProtect",
            "description": "Disability insurance to protect income in case of inability to work",
            "coverage_percentage": {"min": 60, "max": 80},
            "benefit_period_options": ["2 years", "5 years", "until retirement"],
            "waiting_period_options": [30, 90, 180, 365],
            "target_segments": ["high_income", "professionals", "skilled_workers"],
        },
        "business_insurance": {
            "product_id": "BUSINESS001",
            "name": "BusinessGuard Pro",
            "description": "Comprehensive business insurance for small to medium enterprises",
            "coverage_types": [
                "General liability",
                "Property",
                "Business interruption",
                "Cyber liability",
            ],
            "target_segments": ["business_owners", "self_employed", "professionals"],
        },
        # New Products
        "personal_liability_insurance": {
            "product_id": "LIABILITY001",
            "name": "PrivatSchutz Sorglos",
            "description": "Essential personal liability insurance covering damages to third parties.",
            "min_coverage": 5000000,
            "max_coverage": 50000000,
            "average_premium_range": {"min": 5, "max": 15},  # monthly
            "features": ["Coverage for personal injury and property damage", "Loss of keys coverage",
                         "Worldwide coverage"],
            "target_segments": ["all_drivers", "families", "young_professionals", "homeowners", "students"],
        },
        "legal_protection_insurance": {
            "product_id": "LEGAL001",
            "name": "RechtSicher Privat",
            "description": "Comprehensive legal protection for private, professional, and traffic-related disputes.",
            "coverage_areas": ["Private life", "Work", "Traffic", "Housing"],
            "average_premium_range": {"min": 15, "max": 40},  # monthly
            "features": ["Free initial legal consultation", "Mediation services", "Choice of own lawyer"],
            "target_segments": ["families", "professionals", "all_drivers", "homeowners"],
        },
        "pet_insurance": {
            "product_id": "PET001",
            "name": "TierGesundheit Premium",
            "description": "Health insurance for your pets, covering vet bills for surgeries and treatments.",
            "pet_types_covered": ["dog", "cat"],
            "coverage_options": ["Surgery only", "Full coverage including outpatient care"],
            "average_premium_range": {"min": 20, "max": 80},  # monthly
            "features": ["Direct billing with vets", "Preventive care allowance", "Coverage for hereditary conditions"],
            "target_segments": ["families", "pet_owners"],
        },
        "motorcycle_insurance": {
            "product_id": "MOTO001",
            "name": "ZweiradSicher",
            "description": "Specialized insurance for motorcycles, scooters, and mopeds.",
            "coverage_types": ["Liability", "Partial cover", "Fully comprehensive"],
            "discount_factors": ["Garage parking", "Seasonal license plate", "Experienced rider discount"],
            "average_premium_range": {"min": 20, "max": 150},
            "target_segments": ["all_drivers", "young_professionals"],
        },
        "electronics_insurance": {
            "product_id": "ELEC001",
            "name": "GadgetGarant",
            "description": "Protection for your valuable electronics like smartphones, laptops, and cameras.",
            "covered_perils": ["Accidental damage", "Liquid damage", "Theft", "Short circuit"],
            "device_age_max": 24,  # in months
            "premium_factors": ["Device value", "Coverage scope"],
            "target_segments": ["students", "young_professionals", "families", "frequent_travelers"],
        },
        "valuables_insurance": {
            "product_id": "VALUABLES001",
            "name": "WertgegenstandTresor",
            "description": "Specialized insurance for high-value items like jewelry, art, and musical instruments.",
            "covered_items": ["Jewelry & Watches", "Art & Antiques", "Musical Instruments", "Designer Handbags"],
            "coverage_basis": "Agreed value",
            "features": ["Worldwide all-risk coverage", "No deductible option", "Coverage during transit"],
            "target_segments": ["high_income", "premium", "professionals"],
        },
        "rental_deposit_insurance": {
            "product_id": "RENTAL001",
            "name": "Kautionsfrei Wohnen",
            "description": "An alternative to a cash rental deposit (Mietkaution), providing a guarantee to your landlord.",
            "annual_premium_rate": {"percentage_of_deposit": {"min": 3.5, "max": 5.0}},
            "max_deposit_amount": 15000,
            "features": ["Frees up cash", "Quick and easy online application", "Accepted by most landlords"],
            "target_segments": ["students", "young_professionals", "families"],
        },
        "personal_cyber_insurance": {
            "product_id": "CYBER001",
            "name": "CyberSafe Home",
            "description": "Protection against online risks such as identity theft, cyberbullying, and online shopping fraud.",
            "coverage_types": ["Data recovery costs", "Online account fraud", "Identity theft recovery",
                               "Legal costs for reputation damage"],
            "average_premium_range": {"min": 8, "max": 25},  # monthly
            "features": ["24/7 support hotline", "Psychological support after cyberbullying",
                         "Proactive security advice"],
            "target_segments": ["families", "high_income", "professionals", "students"],
        }
    }

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
            requested_segment=segment,
        )

    return _create_success_response(
        f"Found {len(matching_products)} products for segment '{segment}'",
        products=matching_products,
        segment=segment,
        product_count=len(matching_products),
    )


def main():
    mcp.run(transport="streamable-http", host="0.0.0.0")


if __name__ == "__main__":
    main()
