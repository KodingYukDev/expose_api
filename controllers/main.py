from odoo import http
from odoo.http import request


class ExposeApiController(http.Controller):
    @http.route('/api/public/blog/posts', type='json', auth='public', csrf=False, methods=['POST'])
    def public_blog_posts(self, limit=30, offset=0, **kwargs):
        posts = request.env['blog.post'].sudo().search([
            ('website_published', '=', True),
        ], limit=int(limit), offset=int(offset), order='write_date desc, create_date desc')

        result = []
        for p in posts:
            result.append({
                'id': p.id,
                'name': p.name,
                'subtitle': p.subtitle or '',
                'website_url': p.website_url or '',
                'create_date': p.create_date,
                'write_date': p.write_date,
                'cover': f"/web/image/blog.post/{p.id}/image_1920" if p.image_1920 else None,
            })

        return {'result': result}

    @http.route('/api/public/blog/post', type='json', auth='public', csrf=False, methods=['POST'])
    def public_blog_post(self, slug=None, **kwargs):
        if not slug:
            return {'result': None}

        # Match by website_url suffix
        post = request.env['blog.post'].sudo().search([
            ('website_published', '=', True),
            ('website_url', 'ilike', f"/{slug}"),
        ], limit=1)

        if not post:
            return {'result': None}

        return {
            'result': {
                'id': post.id,
                'name': post.name,
                'subtitle': post.subtitle or '',
                'website_url': post.website_url or '',
                'create_date': post.create_date,
                'write_date': post.write_date,
                'content': post.content or '',
                'cover': f"/web/image/blog.post/{post.id}/image_1920" if post.image_1920 else None,
            }
        }

    @http.route('/api/public/jobs', type='json', auth='public', csrf=False, methods=['POST'])
    def public_jobs(self, limit=50, offset=0, **kwargs):
        jobs = request.env['hr.job'].sudo().search([
            ('website_published', '=', True),
        ], limit=int(limit), offset=int(offset), order='write_date desc, create_date desc')

        result = []
        for j in jobs:
            result.append({
                'id': j.id,
                'name': j.name,
                'website_url': j.website_url or '',
                'description': j.description or '',
                'requirements': j.requirements or '',
                'create_date': j.create_date,
                'write_date': j.write_date,
                'location': j.address_id.city if j.address_id and j.address_id.city else '',
                'type': j.contract_type_id.name if j.contract_type_id else '',
            })

        return {'result': result}

    @http.route('/api/public/contact', type='json', auth='public', csrf=False, methods=['POST'])
    def public_contact(self, name=None, email=None, phone=None, message=None, **kwargs):
        if not name or not email or not message:
            return {'result': None, 'error': 'name, email, message are required'}

        lead = request.env['crm.lead'].sudo().create({
            'name': f"Website Contact - {name}",
            'partner_name': name,
            'email_from': email,
            'phone': phone or '',
            'description': message,
        })

        return {'result': {'id': lead.id}}

    @http.route('/api/public/courses', type='json', auth='public', csrf=False, methods=['POST'])
    def public_courses(self, limit=100, offset=0, **kwargs):
        channels = request.env['slide.channel'].sudo().search([
            ('website_published', '=', True),
        ], limit=int(limit), offset=int(offset), order='create_date desc')

        result = []
        for c in channels:
            result.append({
                'id': c.id,
                'name': c.name,
                'description': c.description or '',
                'description_short': c.description_short or '',
                'total_slides': c.total_slides,
                'total_time': c.total_time,
                'rating_avg_stars': c.rating_avg_stars,
                'members_count': c.members_count,
                'enroll': c.enroll,
                'channel_type': c.channel_type,
                'image': f"/web/image/slide.channel/{c.id}/image_1920" if c.image_1920 else None,
            })

        return {'result': result}

    @http.route('/api/public/course', type='json', auth='public', csrf=False, methods=['POST'])
    def public_course(self, id=None, **kwargs):
        if not id:
            return {'result': None}

        channel = request.env['slide.channel'].sudo().browse(int(id))
        if not channel.exists() or not channel.website_published:
            return {'result': None}

        # Preview curriculum: only titles + meta, no URLs/content
        slides = request.env['slide.slide'].sudo().search([
            ('channel_id', '=', channel.id),
            ('is_published', '=', True),
        ], order='sequence asc, id asc')

        preview_slides = []
        for s in slides:
            preview_slides.append({
                'id': s.id,
                'name': s.name,
                'sequence': s.sequence,
                'slide_type': s.slide_type,
                'completion_time': s.completion_time,
                'is_preview': s.is_preview,
            })

        return {
            'result': {
                'id': channel.id,
                'name': channel.name,
                'description': channel.description or '',
                'description_short': channel.description_short or '',
                'total_slides': channel.total_slides,
                'total_time': channel.total_time,
                'rating_avg_stars': channel.rating_avg_stars,
                'members_count': channel.members_count,
                'enroll': channel.enroll,
                'channel_type': channel.channel_type,
                'image': f"/web/image/slide.channel/{channel.id}/image_1920" if channel.image_1920 else None,
                'slides_preview': preview_slides,
            }
        }
