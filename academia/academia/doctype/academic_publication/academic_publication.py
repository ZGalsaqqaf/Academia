

from frappe.model.document import Document
import frappe
from frappe import _

class AcademicPublication(Document):
    def validate(self):
        if self.date_of_publish:
            if self.date_of_publish > frappe.utils.today():
                frappe.throw(_("Date of publish must be less than or equal to today's date"))






class AcademicPublication(Document):
    def validate(self):
        # Calling functions
        self.validate_page_numbers()
        self.validate_url()


    # FN: Verifying 'from_page', 'to_page' and 'page_numbers' fields
    def validate_page_numbers(self):
        # Verifying that both fields are filled, not just one
        if (not self.from_page and self.to_page) or (self.from_page and not self.to_page):
            frappe.throw("Please fill both 'From Page' and 'To Page' fields.")
        # Verifying that both fields have non-null values
        elif self.from_page and self.to_page:
            # Verifying that both fields contain only numbers and this - character
            if not self.from_page.replace('-', '').isdigit() or not self.to_page.replace('-', '').isdigit():
                frappe.throw("Page numbers must be integer.")
            # Verifying that both fields do not contain negative values 
            elif int(self.from_page) < 0 or int(self.to_page) < 0:
                frappe.throw("Page numbers must be positive.")
            # Verifying that the first page is not greater than the last page
            elif int(self.from_page) > int(self.to_page):
                frappe.throw("First page must be less than last page.")
            # Writing the correct values in a specific format
            else:
                if int(self.from_page) == int(self.to_page):
                    self.page_numbers = self.from_page
                else:
                    self.page_numbers = f"{self.from_page} - {self.to_page}"
        # Verifying that both fields have null values
        else:
            self.page_numbers = '0'
            self.from_page = '0'
            self.to_page = '0'
    # End of the function


    # FN: Verifying 'publication_link' field
    def validate_url(self):
        # Define a regular expression pattern for validating URLs
        url_pattern = re.compile(r'^(http|https|ftp)://\S+$')
        # Verifying that publication_link matches the URL pattern
        if self.publication_link:
            if not url_pattern.match(self.publication_link):
                frappe.throw("Publication Link in not valid. Please enter a valid URL starting with http, https, or ftp")
    # End of the function

