import click
import frappe


def before_uninstall():
    delete_custom_fields()
    delete_property_setters()


def delete_custom_fields():
    custom_fields = get_custom_fields_to_remove()
    for doctype, fields in custom_fields.items():
        try:
            frappe.db.delete(
                "Custom Field",
                filters={"dt": doctype, "fieldname": ["in", fields]},
            )
        except Exception as e:
            print(f"Error occured when deleting custom fields", e)
            click.secho("Clicked Error occured when deleting custom fields", fg="red")

        frappe.clear_cache(doctype=doctype)

    print("Custom fields deleted successfully")
    click.secho("Clicked Custom fields deleted successfully", fg="green")


def delete_property_setters():
    unique_doctypes = []
    property_setters = get_property_setter_to_delete()
    for property_setter in property_setters:
        try:
            frappe.db.delete(
                "Property Setter",
                filters=property_setter,
            )
            if property_setter.get("doc_type") not in unique_doctypes:
                unique_doctypes.append(property_setter.get("doc_type"))
        except Exception as e:
            print(f"Error occured when deleting property setter", e)
            click.secho("Clicked Error occured when deleting property setter", fg="red")

    for doctype in unique_doctypes:
        frappe.clear_cache(doctype=doctype)

    print("Property setters deleted successfully")
    click.secho("Clicked Property setters deleted successfully", fg="green")


def get_custom_fields_to_remove():
    custom_fields = {
        "Employee": [
            "area",
            "biometric_code",
            "biometric_id",
            "enable_biometric",
            "column_break_49",
            "column_break_50",
            "other_allowance",
            "worker_subsistence",
            "column_break_54",
        ],
        "Loan": [
            "loan_repayments_not_from_salary",
            "not_from_salary_loan_repayments",
            "total_nsf_repayments",
        ],
        "Payroll Entry": [
            "bank_account_for_transfer",
            "bank_payment_details",
            "cheque_date",
            "cheque_number",
            "column_break_34",
            "section_break_35",
        ],
        "Salary Component": [
            "sdl_emolument_category",
            "column_break_16",
        ],
        "Repayment Schedule": [
            "change_amount",
            "changed_interest_amount",
            "changed_principal_amount",
        ],
    }
    return custom_fields


def get_property_setter_to_delete():
    property_setters = [
        {
            "doc_type": "Additional Salary",
            "field_name": "naming_series",
            "property": "options",
        },
        {"doc_type": "Employee", "field_name": "department", "property": "permlevel"},
        {"doc_type": "Employee", "field_name": "job_profile", "property": "permlevel"},
        {
            "doc_type": "Leave Application",
            "field_name": "naming_series",
            "property": "options",
        },
        {"doc_type": "Loan", "field_name": "loan_type", "property": "in_list_view"},
        {
            "doc_type": "Loan",
            "field_name": "loan_type",
            "property": "in_standard_filter",
        },
        {"doc_type": "Loan", "field_name": "posting_date", "property": "in_list_view"},
        {
            "doc_type": "Loan",
            "field_name": "repay_from_salary",
            "property": "allow_on_submit",
        },
        {"doc_type": "Loan", "field_name": "repayment_method", "property": "options"},
        {"doc_type": "Loan", "field_name": "status", "property": "in_standard_filter"},
        {
            "doc_type": "Payroll Entry",
            "field_name": "branch",
            "property": "in_list_view",
        },
        {
            "doc_type": "Payroll Entry",
            "field_name": "company",
            "property": "print_width",
        },
        {
            "doc_type": "Salary Structure Assignment",
            "field_name": "employee",
            "property": "in_list_view",
        },
    ]

    return property_setters
