from fastmcp import FastMCP

# Create an MCP server for customer CRM data
mcp = FastMCP(name="Customer CRM")


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


# used to be "crm://customer/{customer_id}"
@mcp.tool()
def get_customer_crm_data(customer_id: str) -> dict:
    """
    Retrieves a comprehensive 360-degree view of a customer from the CRM system.

    This tool fetches a complete profile for a given customer, including their
    personal information such as email address, any existing insurance policies, their complete communication
    history with the company, and internal metrics like risk profile and lifetime value.
    It serves as a foundational step for most customer-related inquiries.

    Args:
        customer_id (str): The unique identifier for the customer (e.g., "cust001").
                           This ID is required to locate the customer's record.

    Returns:
        dict: A dictionary containing the execution status and the customer's data.
              On success, the dictionary will have the following structure:
              {
                  "status": "success",
                  "message": "A confirmation message.",
                  "customer_data": {
                      "customer_id": "The customer's ID.",
                      "personal_info": {
                          "name": "Full name.",
                          "age": "Age in years.",
                          "address": "Full mailing address.",
                          ...
                      },
                      "existing_policies": [
                          {
                              "policy_id": "The policy identifier.",
                              "product_type": "Type of insurance product.",
                              ...
                          }
                      ],
                      "communication_history": [
                          {
                              "date": "Date of communication (YYYY-MM-DD).",
                              "type": "Method of communication (e.g., 'phone_call').",
                              "subject": "Subject of the communication.",
                              "notes": "A summary of the interaction."
                          }
                      ],
                      ...
                  }
              }
              On failure, the dictionary will contain:
              {
                  "status": "error",
                  "error_message": "A description of what went wrong.",
                  "error_code": "A unique code for the error type (e.g., 'MISSING_CUSTOMER_ID')."
              }

    Usage Guidance:
        This tool should be the first one you call when a user (an insurance broker) asks for help
        information on a customer's account or policies. Use it to gather essential context
        before attempting to answer questions, provide advice, or recommend new products.
        Understanding the customer's history is crucial for a relevant and personalized
        conversation. For instance, before suggesting home insurance, check the
        communication history and existing policies to see if it has been discussed
        or if they already have it.

    Error Handling:
        - If the status is "error" with the error_code "MISSING_CUSTOMER_ID",
          you must ask the user to provide the customer ID.
        - If the tool returns any other error (e.g., a customer ID that is not found
          in the system), inform the user that you were unable to retrieve their
          information and ask them to verify the ID they provided. Do not retry
          with the same ID.
    """
    if not customer_id or not customer_id.strip():
        return _create_error_response("Customer ID is required.", "MISSING_CUSTOMER_ID")

    customer_id = customer_id.strip()

    # TODO: Implement actual CRM database connection
    # For skeleton purposes, using mock data based on customer_id
    if customer_id.lower() == "cust001":
        mock_customer_data = {
            "customer_id": customer_id,
            "personal_info": {
                "name": "Anna Müller",
                "birth_date": "1985-03-15",
                "age": 39,
                "address": "Hauptstraße 123, 10115 Berlin",
                "phone": "+49 30 12345678",
                "email": "anna.mueller@email.com",
                "occupation": "Software Engineer",
                "annual_income": 75000,
                "marital_status": "married",
                "children": 2,
                "home_ownership": "owner",
            },
            "existing_policies": [
                {
                    "policy_id": "POL001",
                    "product_type": "Car Insurance",
                    "premium_amount": 85.30,
                    "coverage_amount": 50000,
                    "start_date": "2021-06-01",
                    "status": "active",
                    "vehicle": "BMW 3 Series, 2020",
                }
            ],
            "communication_history": [
                {
                    "date": "2024-01-15",
                    "type": "phone_call",
                    "subject": "Policy renewal inquiry",
                    "notes": "Customer asked about car insurance policy renewal and mentioned recently buying a house",
                },
                {
                    "date": "2023-12-20",
                    "type": "email",
                    "subject": "Claim status inquiry",
                    "notes": "Follow-up on minor car accident claim - settled successfully",
                },
                {
                    "date": "2023-11-28",
                    "type": "phone_call",
                    "subject": "Home insurance inquiry",
                    "notes": "Customer mentioned she already has home insurance with another provider when asked about our home insurance products",
                },
                {
                    "date": "2023-10-05",
                    "type": "phone_call",
                    "subject": "Life insurance inquiry",
                    "notes": "Customer expressed interest in life insurance after birth of second child but did not proceed",
                },
            ],
            "risk_profile": "low",
            "customer_segment": "premium",
            "lifetime_value": 15000,
        }
    elif customer_id.lower() == "cust002":
        mock_customer_data = {
            "customer_id": customer_id,
            "personal_info": {
                "name": "Thomas Schmidt",
                "birth_date": "1975-08-22",
                "age": 49,
                "address": "Lindenallee 45, 20099 Hamburg",
                "phone": "+49 40 98765432",
                "email": "thomas.schmidt@email.com",
                "occupation": "Business Manager",
                "annual_income": 95000,
                "marital_status": "married",
                "children": 1,
                "home_ownership": "owner",
            },
            "existing_policies": [
                {
                    "policy_id": "POL003",
                    "product_type": "Life Insurance",
                    "premium_amount": 150.00,
                    "coverage_amount": 300000,
                    "start_date": "2019-03-10",
                    "status": "active",
                    "type": "term_life",
                },
                {
                    "policy_id": "POL004",
                    "product_type": "Home Insurance",
                    "premium_amount": 180.00,
                    "coverage_amount": 400000,
                    "start_date": "2020-07-15",
                    "status": "active",
                },
            ],
            "communication_history": [
                {
                    "date": "2024-02-10",
                    "type": "email",
                    "subject": "Policy review request",
                    "notes": "Customer requested annual policy review and asked about investment products",
                },
                {
                    "date": "2023-11-18",
                    "type": "phone_call",
                    "subject": "Claim notification",
                    "notes": "Minor home damage claim due to storm - processed quickly",
                },
            ],
            "risk_profile": "low",
            "customer_segment": "premium",
            "lifetime_value": 25000,
        }
    else:
        # Default customer data for other IDs
        mock_customer_data = {
            "customer_id": customer_id,
            "personal_info": {
                "name": "Max Mustermann",
                "birth_date": "1990-01-01",
                "age": 34,
                "address": "Musterstraße 1, 12345 München",
                "phone": "+49 89 12345678",
                "email": "max.mustermann@email.com",
                "occupation": "Office Worker",
                "annual_income": 45000,
                "marital_status": "single",
                "children": 0,
                "home_ownership": "renter",
            },
            "existing_policies": [],
            "communication_history": [
                {
                    "date": "2024-01-05",
                    "type": "web_inquiry",
                    "subject": "Insurance information request",
                    "notes": "Customer submitted online form asking for insurance quotes",
                }
            ],
            "risk_profile": "medium",
            "customer_segment": "standard",
            "lifetime_value": 5000,
        }

    return _create_success_response(
        f"Customer CRM data retrieved for {customer_id}",
        customer_data=mock_customer_data,
    )


def main():
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
