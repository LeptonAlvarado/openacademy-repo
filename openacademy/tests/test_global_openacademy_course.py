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
    def test_10_same_name_description(self):
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


    @mute_logger('odoo.sql_db')
    def test_20_two_courses_same_name(self):
        '''
        Test to create two courses with the same name.
        To raise constraint of unique name
        '''

        new_id = self.create_course('test1', 'test_description', None)
        print('new_id %s', new_id)
        with self.assertRaisesRegexp(
            IntegrityError,
            'duplicate key value violates unique constraint "openacademy_course_name_unique"'
        ):
            new_id2 = self.create_course('test1','test_description',None)
            print('new_id %s',new_id2)
            
    
    def test_15_duplicate_course(self):
        '''
        Test to duplicate a course and check if it works fine
        '''
        course = self.env.ref('openacademy.course0')
        course_id = course.copy()
        print('course id: %s',course_id)