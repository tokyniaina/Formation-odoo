from odoo import models, fields, api
from odoo import exceptions


class Registration(models.Model):
    _name = 'registration.registration'
    _description = 'registration.registration'

    @api.model
    def create(self, values):
        if values.get('name'):
            values['name'] = 'Value by creation method'
        return super(Registration, self).create(values)

    @api.multi
    def write(self, values):
        values['name'] = 'value by'
        return super(Registration, self).write(values)

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        default.update({'name': 'copy(name)', 'code': 'copy -001'})
        return super(Registration, self).copy(default)

    @api.multi
    def unlink(self):
        for record in self:
            if record.state == 'done':
                raise exceptions.UserError('You cannot delete record in done state')
        return super(Registration, self).unlink()

    name = fields.Char(string='Nom', required=False)
    code = fields.Char(string='code')
    start_date = fields.Date(string='Date de debut', help='Date')
    end_date = fields.Date(string='Date de fin', help='Date')
    description = fields.Text(string='Description', required=False, readonly=False)
    cycle_id = fields.Many2one('cycle.cycle', string='Cycle')
    year_id = fields.Many2one('year.year', string='Année univ')
    claim_ids = fields.One2many('claim.claim', 'reg_id', string='Reclamation')
    student_id = fields.Many2one('res.partner', string='Etudiant', domain="[('student_ok','=', True)]")
    state = fields.Selection(
        [('new', 'Nouveau'), ('done', 'Validé'),
         ('cancel', 'Annuler')], string="Status")

    nbr = fields.Integer(compute='_compute_claims')

    @api.multi
    @api.depends('claim_ids')
    def _compute_claims(self):
        self.nbr= len(self.claim_ids)



class Claim(models.Model):
    _name = 'claim.claim'
    _description = 'Réclamation'

    name = fields.Char(string='Nom', required=True)
    code = fields.Char(string='code')
    start_date = fields.Date(string='Date de debut', help='Date')
    end_date = fields.Date(string='Date de fin', help='Date')
    description = fields.Text(string='Description', required=False, readonly=False)
    reg_id = fields.Many2one('registration.registration', string='Inscription')
    user_id = fields.Many2one('res.users', string="Responsable")
    state = fields.Selection(
        [('new', 'nouvelle'), ('done', 'Validé'),
         ('cancel', 'Annuler')], string="Status")

    amount = fields.Float(string='Montant')
    hours_nbr = fields.Integer(string='#Heurs')
    total = fields.Float(compute='_total_compute', string='Total')

    @api.multi
    @api.depends('amount', 'hours_nbr')
    def _total_compute(self):
        self.total = self.amount * self.hours_nbr


class Year(models.Model):
    _name = 'year.year'
    _description = 'year.year'

    name = fields.Char(string='Nom', required=True)
    code = fields.Char(string='code')
    start_date = fields.Date(string='Date de debut', help='Date')
    end_date = fields.Date(string='Date de fin', help='Date')
    description = fields.Text(string='Description', required=False, readonly=False)
    session_ids = fields.One2many('session.session', 'year_id', string='session')


class Session(models.Model):
    _name = 'session.session'
    _description = 'session.session'

    name = fields.Char(string='Nom', required=True)
    code = fields.Char(string='code')
    start_date = fields.Date(string='Date de debut', help='Date')
    end_date = fields.Date(string='Date de fin', help='Date')
    description = fields.Text(string='Description', required=False, readonly=False)
    year_id = fields.Many2one('year.year', string='Année univ')


class Cycle(models.Model):
    _name = 'cycle.cycle'
    _description = 'cycle.cycle'

    name = fields.Char(string='Nom', required=True)
    code = fields.Char(string='code')
    description = fields.Text(string='Description', required=False, readonly=False)
    level_ids = fields.One2many('level.level', 'cycle_id', string='Niveau')

    # Registration_ids = fields.One2many('registration.registration', 'cycle_id', string='Inscription')

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.name and record.code:
                result.append((record.id, record.name + ' / ' + record.code))
            if record.name and not record.code:
                result.append((record.id, record.name))
        return result


class Level(models.Model):
    _name = 'level.level'
    _description = 'level.level'

    name = fields.Char(string='Nom', required=True)
    code = fields.Char(string='code')
    description = fields.Text(string='Description', required=False, readonly=False)
    section_ids = fields.One2many('section.section', 'level_id', string='Section')
    cycle_id = fields.Many2one('cycle.cycle', string='Cycle')


class Section(models.Model):
    _name = 'section.section'
    _description = 'section.section'

    name = fields.Char(string='Nom', required=True)
    code = fields.Char(string='code')
    description = fields.Text(string='Description', required=False, readonly=False)
    module_ids = fields.One2many('module.module', 'section_id', string='Module')
    level_id = fields.Many2one('level.level', string='Niveau')


class Module(models.Model):
    _name = 'module.module'
    _description = 'models'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='code')
    description = fields.Text(string='Description')
    section_id = fields.Many2one('section.section', string='Section')


class Partner(models.Model):
    _inherit = 'res.partner'

    student_ok = fields.Boolean(string='Est un étudient')
    birthday = fields.Date(string='Date de maissance')
    age = fields.Integer(string='Age')
    reg_ids = fields.One2many('registration.registration', 'student_id', string="Inscription")


class Prof(models.Model):
    _inherit = 'hr.employee'
    _name = 'teacher.teacher'

    age = fields.Integer(string='Age')
    cin = fields.Char(string='CIN')
