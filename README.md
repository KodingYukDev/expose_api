# Expose API (Odoo 17)

Public JSON API endpoints for Odoo 17 LMS preview and website content.

## Features
- Exposes read-only public JSON endpoints for website, courses (\website_slides\), blog posts, events, recruitment, and CRM integrations.
- Built for headless frontends (such as Next.js) consuming Odoo 17 content.

## Requirements
- Odoo 17.0
- Odoo modules: \website\, \website_slides\, \website_blog\, \website_event\, \hr_recruitment\, \crm\, \kodingyuk_website_cms\

## Installation
1. Copy this module into your Odoo \ddons_path\.
2. Update the Apps list in Odoo (Developer Mode).
3. Install **Expose API**.

## License
Licensed under the **LGPL-3.0** license. See [LICENSE](LICENSE) for details.