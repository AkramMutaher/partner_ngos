# -*- coding: utf-8 -*-
# Copyright (c) 2020, Akram Mutaher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class TargetedPrograms(Document):
	pass

@frappe.whitelist()
def get_approvers(doctype, txt, searchfield, start, page_len, filters):


	approvers = []
	department_details = {}
	department_list = []
	
	employee_department = filters.get("project_proposal")
	if employee_department:
		department_list = frappe.db.sql("""select name from `tabProject Proposal`""")

	department_details = frappe.db.sql("""select name from `tabPrograms`""")
	

	if filters.get("doctype") == "Logical Framework":
		parentfield = "targeted_programs"
		field_name = "Targeted Programs"
	
	if department_list:
		for d in department_list:
			approvers += frappe.db.sql("""select programs.name from
				tabPrograms programs, `tabTargeted Programs` approver where
				approver.parent = %s
				and approver.parentfield = %s
				and approver.program=programs.name""",(d, parentfield), as_list=True)

	if len(approvers) == 0:
		approvers = department_details
	return set(tuple(approver) for approver in approvers)