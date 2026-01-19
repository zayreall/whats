from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

class FAQForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    answer = TextAreaField('Answer', validators=[DataRequired()])

    # 🔽 Update this field from StringField to SelectField
    category = SelectField(
        'Category',
        choices=[
            ('General Information', 'General Information'),
            ('Shipping & Delivery', 'Shipping & Delivery'),
            ('Returns & Refunds', 'Returns & Refunds'),
            ('Payment', 'Payment'),
            ('Technical Support', 'Technical Support')
        ],
        validators=[DataRequired()]
    )

    tags = StringField('Tags')
    status = SelectField('Status', choices=[('draft', 'Draft'), ('published', 'Published')], validators=[DataRequired()])
    submit = SubmitField('Save')




