from rest_framework.permissions import BasePermission


class CustomerPermission(BasePermission):
    """
    Custom permission class to restrict access to most APIs for customers.
    """

    def has_permission(self, request, view):
        # Allow access to specific APIs for authenticated customers
        allowed_apis_for_customers = [
            "CreateCustomerView",
            "CustomerLoginView",
        ]  # Add the names of APIs you want to allow access to customers

        allowed_apis_for_users = [
            "UserListView",  # Add other API view names you want to allow for regular users
            # "CustomerLoginView",
        ]
        user=request.user
        if user.is_staff:
            return True
        elif not user.is_staff:
            return False
        # if request.user.is_authenticated:
        #     if request.user.is_staff == False and view.__class__.__name__ in allowed_apis_for_customers:
        #         return True
        #     if request.user.is_staff:
        #         return view.__class__.__name__ in allowed_apis_for_users


        # # Check if the user is authenticated
        # if request.user.is_authenticated:
        #     try:
        #         # Check if the user is a customer
        #         customer = request.user.customer
        #         # If the user is a customer, check if the view is in the allowed list
        #         if customer.is_customer:
        #             return view.__class__.__name__ in allowed_apis_for_customers
        #     except AttributeError:
        #         # If the user is not a customer, check if the view is in the allowed list for users
        #         return view.__class__.__name__ in allowed_apis_for_users

        # Deny access if the user is not authenticated
        return False
