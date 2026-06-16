# -*- coding: utf-8 -*-
"""Generate branding_data.xml with the embedded Sa Systems company logo."""

b64 = open("addons/ecoflow_dashboard/static/src/img/logo_b64.txt").read().strip()

xml = (
    '<?xml version="1.0" encoding="utf-8"?>\n'
    "<odoo>\n"
    "    <!-- Default ECOFLOW operational thresholds (overridable in Settings) -->\n"
    '    <record id="param_mass_balance_tolerance" model="ir.config_parameter">\n'
    "        <field name=\"key\">ecoflow.mass_balance_tolerance</field>\n"
    "        <field name=\"value\">0.02</field>\n"
    "    </record>\n"
    '    <record id="param_permit_expiry_days" model="ir.config_parameter">\n'
    "        <field name=\"key\">ecoflow.permit_expiry_days</field>\n"
    "        <field name=\"value\">30</field>\n"
    "    </record>\n"
    '    <record id="param_target_diversion_rate" model="ir.config_parameter">\n'
    "        <field name=\"key\">ecoflow.target_diversion_rate</field>\n"
    "        <field name=\"value\">75.0</field>\n"
    "    </record>\n\n"
    "    <!-- Apply Sa Systems branding to the main company -->\n"
    '    <function model="res.company" name="write">\n'
    "        <value eval=\"[ref('base.main_company')]\"/>\n"
    '        <value eval="{\'logo\': \'' + b64 + "'}\"/>\n"
    "    </function>\n"
    "</odoo>\n"
)

with open("addons/ecoflow_dashboard/data/branding_data.xml", "w") as f:
    f.write(xml)
print("wrote branding_data.xml", len(xml), "bytes")
