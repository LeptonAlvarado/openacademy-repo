from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError


class GlobalTestOpenAcademySession(TransactionCase):
    '''
    This creates a global test file for sessisons
    '''

    # Seudo-constructor method
    def setUp(self):
        super(GlobalTestOpenAcademySession, self).setUp()
        self.session = self.env['openacademy.session']
        self.course = self.env.ref('openacademy.course0').id
        self.partner_azure_interior = self.env.ref('base.res_partner_12')
        self.partner_attendee = self.env.ref('base.res_partner_2')
    # Generic methods

    # Test methods

    def test_10_instructor_is_attendee(self):
        '''
        Check that raise of "A session's instructor can't be an attendee"
        '''

        with self.assertRaisesRegexp(
            ValidationError,
            "A session's instructor can't be an attendee"
        ):
            self.session.create({
                'name': 'Sesion test 1',
                'seats': 1,
                'instructor_id': self.partner_azure_interior.id,
                'attendee_ids': [(6, 0, [self.partner_azure_interior.id])],
                'course_id': self.course
            })
