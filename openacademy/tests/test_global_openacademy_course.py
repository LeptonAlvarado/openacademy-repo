#-*- coding: utf-8 -*-

from psycopg2 import IntegrityError

from openerp.tests.common import TransactionCase
from openerp.tools import mute_logger

class GlobalTesteOpenAcademyCourse(TransactionCase):
    '''
    Global test to openacademy course model.
    Test create course and trigger contraints.
    '''

    # Method seudo-contructor of test setUp
    def setUp(self):
        # Define global variables to test methods
        super(GlobalTesteOpenAcademyCourse, self).setUp()
        self.course = self.env['openacademy.course']

    # Method of class that don't is test
    def create_course(self, course_name, course_description,
                     course_responsible_id):
        # Create a course with parameters received
        course_id = self.course.create({
            'name':course_name,
            'description':course_description,
            'responsible_id': course_responsible_id,
        })
        return course_id

    # Method of test startswith 'def test_*(self)'
    # Mute the error odoo.sql_db to avoid showing it on log
    @mute_logger('odoo.sql_db')
    def test_01_same_name_description(self):
        '''
        Test create a course with same name and description.
        To test contraint of name different to description.
        '''
        # Error raised exepected with message expected
        with self.assertRaisesRegex(
            IntegrityError,
            'new row for relation "openacademy_course" violates check constraint "openacademy_course_name_description_check"'
        ):
            # Create a course with same name and description to raise error
            self.create_course('test', 'test', None)