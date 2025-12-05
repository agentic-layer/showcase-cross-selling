from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from . import mock_database

# Create an MCP server for customer CRM data
mcp: FastMCP = FastMCP(name="Customer CRM")


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

    # For skeleton purposes, using mock data based on customer_id
    if int(customer_id.lower()[-3:]) <= mock_database.get_database_size():
        mock_customer_data = mock_database.get_customer(customer_id)
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


@mcp.tool()
def get_all_customer_data() -> dict:
    return _create_success_response(
        "All Customer CRM data retrieved",
        customer_data=mock_database.get_all_customers(),
    )


@mcp.tool()
def search_customer_by_name(name: str) -> dict:
    """
    Searches for customers by name (case-insensitive, partial match).

    Use this tool when you have a customer's name but not their ID.
    For example, if a broker asks about "Anna Müller", use this tool to find her.

    Args:
        name (str): The customer's name or part of it (e.g., "Anna", "Müller", or "Anna Müller").

    Returns:
        dict: A dictionary containing the search results.
              On success with matches:
              {
                  "status": "success",
                  "message": "Found X customer(s) matching 'name'",
                  "customers": [
                      {
                          "customer_id": "cust001",
                          "name": "Anna Müller",
                          "email": "anna.mueller@email.com",
                          ... (full customer data)
                      }
                  ],
                  "count": 1
              }
              On success with no matches:
              {
                  "status": "success",
                  "message": "No customers found matching 'name'",
                  "customers": [],
                  "count": 0
              }

    Usage Guidance:
        This is the preferred tool when brokers refer to customers by name instead of ID.
        It performs a case-insensitive partial match, so searching for "anna" will find "Anna Müller".
    """
    if not name or not name.strip():
        return _create_error_response("Customer name is required.", "MISSING_NAME")

    search_term = name.strip().lower()
    all_customers = mock_database.get_all_customers()
    matches = []

    for customer_id, customer_data in all_customers.items():
        customer_name = customer_data.get("personal_info", {}).get("name", "").lower()
        if search_term in customer_name:
            # Include customer_id in the result
            customer_with_id = {"customer_id": customer_id, **customer_data}
            matches.append(customer_with_id)

    if matches:
        return _create_success_response(
            f"Found {len(matches)} customer(s) matching '{name}'",
            customers=matches,
            count=len(matches),
        )
    else:
        return _create_success_response(
            f"No customers found matching '{name}'",
            customers=[],
            count=0,
        )


@mcp.tool()
def send_message(customer_id: str, subject: str, body: str) -> dict:
    """
    Sends a message to the specified customer.

    :param customer_id:
    :param subject:
    :param body:
    :return:
    """

    print("--- Mock Sending Message ---")
    print(f"To: Customer {customer_id}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    print("--------------------------")

    return _create_success_response(f"Message sent to customer {customer_id}")


@mcp.custom_route("/health", methods=["GET"])
async def health_check(_: Request) -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse({"status": "healthy"})


def main():
    mcp.run(transport="streamable-http", host="0.0.0.0")


if __name__ == "__main__":
    main()
