from wtforms import Form, StringField, validators


class GetRequestForm(Form):
    ip_address = StringField('ip_address', validators = [
        validators.IPAddress(ipv4=True, ipv6=False, message='You must provide an IP address in correct format.')
    ])
    community = StringField('community', validators = [
        validators.Regexp('\w+', message='You must provide a non empty sequence.')
    ])

    oid = StringField('oid', validators = [
        validators.Regexp('^([0-9]+.)+([0-9])+$', message='You must provide a valid OID sequence.')
    ])


def get_errors_wtforms(form) -> list:
    validation_fields = []
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            validation_fields.append({'field': fieldName, 'message': err})
    return validation_fields