from flask_wtf import Form
from wtforms import StringField, BooleanField, IntegerField, SubmitField, ValidationError
from wtforms.validators import DataRequired


def clp_validate(form, field):
    if field.data > 5:
        raise ValidationError("Too many stars")
    elif field.data < 0:
        raise ValidationError("Not enough stars")


def rank_validate(form, field):
    if field.data > 25:
        raise ValidationError("Rank is too low")
    elif field.data < 1:
        raise ValidationError("Rank is too high")

def wr_validate(form, field):
    if field.data:
        if not isinstance(field.data, int):
            raise ValidationError("Winrate must be an integer")
        elif field.data < 0:
            raise ValidationError("Winrate must be greater than or equal to 0")
        elif field.data > 100:
            raise ValidationError("Winrate must be less than or equal to 100")



class FullForm(Form):
    rank = IntegerField('rank', [rank_validate])
    current_stars = IntegerField('current_stars', [clp_validate])
    win_streak = BooleanField('win_streak')
    goal = IntegerField('goal', [rank_validate])
    winrate = IntegerField('winrate', [wr_validate])
