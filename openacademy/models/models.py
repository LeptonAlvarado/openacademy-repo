# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Model to store course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one(
            'res.users', string="Responsible",
            index=True, ondelete='set null', default=lambda self, *a: self.env.uid)
    session_ids = fields.One2many('openacademy.session','course_id')

class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'Model to store course'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one('res.partner', string='Instructor',
            domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', 'Teacher')])
    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    taken_seats = fields.Float(compute='_taken_seats')
    active = fields.Boolean(default=True)

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for record in self.filtered('seats'):
            record.taken_seats = 100.0 * len(record.attendee_ids) / record.seats
