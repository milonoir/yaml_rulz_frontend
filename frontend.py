from flask import Flask
from flask import request
from flask import render_template
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from yaml_rulz.validator import YAMLValidator

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = b'\xab\x92T\xaf&\x91q\x8cT\tQ|\xc6\xbc\xdb\x0c\tW\xd2|t\x92\x9b\x1c'


class Form(FlaskForm):
    schema = TextAreaField('Template', [DataRequired()])
    resource = TextAreaField('Resource', [DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    issues = []
    if request.method == 'POST' and form.validate():
        try:
            validator = YAMLValidator(
                schema_content=form.schema.data,
                resource_content=form.resource.data,
                exclusions_content=None
            )
        except Exception as exc:
            issues.append({'severity': 'Fatal', 'message': 'Error: {}'.format(exc)})
        else:
            _, issues = validator.get_validation_issues()
    return render_template('frontend.html', form=form, issues=issues)
