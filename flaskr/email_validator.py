import re

# was going to go with the monstrocity located at https://stackoverflow.com/questions/201323/how-to-validate-an-email-address-using-a-regular-expression
# more specically, this one http://www.ex-parrot.com/~pdw/Mail-RFC822-Address.html
# but I decided I wanted my regex to finish running this decade
# so we'll go with the simpiler one found here https://stackoverflow.com/questions/8022530/how-to-check-for-valid-email-address
email_regex_from_stack_overflow = re.compile(r'[^@]+@[^@]+\.[^@]+')


def validate_email(email):
    errors = []
    if not email:
        errors.append('Email is required.')
    elif not email_regex_from_stack_overflow.match(email):
        errors.append('Email format is invalid.')
    return errors
