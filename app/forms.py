from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DateField, DecimalField, PasswordField,FieldList,FormField, HiddenField,FloatField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class RSQRForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    requirements = TextAreaField('Requirements', validators=[DataRequired()])
    justification = TextAreaField('Justification', validators=[DataRequired()])
    deliverables = TextAreaField('Deliverables', validators=[DataRequired()])

class ManagementCouncilForm(FlaskForm):
    council_date = DateField('Meeting Date', validators=[DataRequired()])
    chairperson = StringField('Chairperson', validators=[Optional()])
    title = StringField('Project Title', validators=[Optional()])
    pdc = StringField('PDC', validators=[Optional()])
    cost = DecimalField('Project Cost (INR)', validators=[Optional()])
    council_pdf = FileField('Upload PDF', validators=[FileAllowed(['pdf'], 'PDF files only!')])


class OfferEvaluationForm(FlaskForm):
    eoffer_eval_date = DateField('Offer Evaluation Committee Date', validators=[DataRequired()])
    eval_chairperson = StringField('Chairperson Name', validators=[DataRequired()])
    eval_member = StringField('Member Name', validators=[DataRequired()])
    eval_user = StringField('User Name', validators=[DataRequired()])
    evaluation_pdf = FileField('Upload PDF', validators=[FileAllowed(['pdf'], 'PDF only!')])
  
    evaluation_pdf = FileField('Upload PDF', validators=[FileAllowed(['pdf'], 'PDF files only!')])

class SummaryOfferForm(FlaskForm):
    personnel_cost = DecimalField('Personnel Cost', validators=[DataRequired()])
    equipment_cost = DecimalField('Equipment Cost', validators=[DataRequired()])
    other_cost = DecimalField('Other Cost', validators=[DataRequired()])
    summary_pdf = FileField('Upload PDF', validators=[FileAllowed(['pdf'], 'PDF files only!')])

class NDASOCForm(FlaskForm):
    nda_pdf = FileField('Upload NDA PDF', validators=[FileAllowed(['pdf'], 'PDF files only!')])
    soc_pdf = FileField('Upload SOC PDF', validators=[FileAllowed(['pdf'], 'PDF files only!')])

# forms/uo_number_form.py
# A subform for dynamic cost entries
class DynamicCostEntryForm(FlaskForm):
    category = StringField('Category')
    amount = DecimalField('Amount', validators=[Optional(), NumberRange(min=0)], places=2)

class UONumberForm(FlaskForm):
    # Fixed cost fields
    personnel = DecimalField('Personnel', validators=[Optional(), NumberRange(min=0)], places=2)
    equipment = DecimalField('Equipment', validators=[Optional(), NumberRange(min=0)], places=2)
    travel = DecimalField('Travel', validators=[Optional(), NumberRange(min=0)], places=2)
    contingencies = DecimalField('Contingencies', validators=[Optional(), NumberRange(min=0)], places=2)
    visiting_faculty = DecimalField('Visiting Faculty', validators=[Optional(), NumberRange(min=0)], places=2)
    technical_support = DecimalField('Technical Support', validators=[Optional(), NumberRange(min=0)], places=2)
    ipr_fees = DecimalField('IPR Fees', validators=[Optional(), NumberRange(min=0)], places=2)
    overheads = DecimalField('Overheads', validators=[Optional(), NumberRange(min=0)], places=2)

    # Dynamic entries
    dynamic_entries = FieldList(FormField(DynamicCostEntryForm), min_entries=0)
   
    # Hidden field to know the action type
    mode = HiddenField('Mode')

  

class UniqueSectionForm(FlaskForm):
    section_code = StringField('Section Code', validators=[DataRequired()])



#contract

class CostEntryForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])


class MilestoneForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])


class ContractForm(FlaskForm):
    contact_number = StringField('Contact Number', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    contract_pdf = FileField('Upload Contract (PDF)', validators=[Optional(), FileAllowed(['pdf'])])
    
    # Fixed cost categories (auto-injected on first load)
    cost_entries = FieldList(FormField(CostEntryForm), min_entries=0)
    
    # Fixed milestone descriptions will be inserted in route
    milestones = FieldList(FormField(MilestoneForm), min_entries=0)
    
    

    
#sanctionletterform



class SanctionCostEntryForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])

class SanctionPaymentMilestoneForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])

class SanctionCARSMilestoneForm(FlaskForm):
    milestone_category = StringField('Milestone Category', validators=[DataRequired()])
    deliverable = StringField('Deliverable', validators=[DataRequired()])
    duration_months = IntegerField('Duration (in months)', validators=[DataRequired()])

class SanctionLetterForm(FlaskForm):
    contact_number = StringField('Contact Number', validators=[DataRequired()])
    sanction_date = DateField('Sanction Date', validators=[DataRequired()])
    uo_code = StringField('UO Code', validators=[Optional()])
    usc_code = StringField('USC Code', validators=[Optional()])
    sanction_pdf = FileField('Upload Sanction Letter PDF', validators=[Optional()])

    costs = FieldList(FormField(SanctionCostEntryForm), min_entries=1)
    payment_milestones = FieldList(FormField(SanctionPaymentMilestoneForm), min_entries=1)
    cars_milestones = FieldList(FormField(SanctionCARSMilestoneForm), min_entries=1)

    


  