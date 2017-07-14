from flask_wtf import Form
from wtforms import StringField, BooleanField, IntegerField, SubmitField, ValidationError
from wtforms.validators import DataRequired


def cg_validate(form, field):
    if not isinstance(field.data, int):
        raise ValidationError("LP gain must be an integer")
    elif field.data <= 0:
        raise ValidationError("LP gain must be greater than 0")
    elif field.data > 100:
        raise ValidationError("LP gain must be less than 101")

def cl_validate(form, field):
    if not isinstance(field.data, int):
        raise ValidationError("LP loss must be an integer")
    elif field.data <= 0:
        raise ValidationError("LP loss must be greater than 0")
    elif field.data > 100:
        raise ValidationError("LP loss must be less than 101")

def clp_validate(form, field):
    if not isinstance(field.data, int):
        raise ValidationError("LP must be an integer")
    elif field.data < 0:
        raise ValidationError("LP must be greater or equal to 0")
    elif field.data > 100:
        raise ValidationError("LP must be less than 101")

def sw_validate(form, field):
    if not isinstance(field.data, int):
        raise ValidationError("Series wins must be an integer")
    elif field.data < 0:
        raise ValidationError("Series wins must be greater than or equal to 0")
    elif field.data > 2:
        raise ValidationError("Series wins must be less than or equal to 2")

def sl_validate(form, field):
    if not isinstance(field.data, int):
        raise ValidationError("Series losses must be an integer")
    elif field.data < 0:
        raise ValidationError("Series losses must be greater than or equal to 0")
    elif field.data > 2:
        raise ValidationError("Series losses must be less than or equal to 2")

def rank_validate(form, field):
    ranks = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "bronze", "silver", "gold", "platinum", "diamond"]
    too_high = ["Master", "Challenger"]
    divisions = ["V", "IV", "III", "II", "I", '5', '4', '3', '2', '1', "v", "iv", "iii", "ii", "i"]
    if len(field.data.split()) != 2:
        raise ValidationError("Not a valid rank")
    rank = field.data.split()[0]
    division = field.data.split()[1]
    if rank not in ranks and rank not in too_high:
        raise ValidationError("Not a valid tier")
    elif rank not in ranks:
        raise ValidationError("Your rank is too high to need this tool")
    elif division not in divisions:
        raise ValidationError("Not a valid divison")
    return rank_validate

def wr_validate(form, field):
    if field.data:
        if not isinstance(field.data, int):
            raise ValidationError("Winrate must be an integer")
        elif field.data < 0:
            raise ValidationError("Winrate must be greater than or equal to 0")
        elif field.data > 100:
            raise ValidationError("Winrate must be less than or equal to 100")

def user_validate(form, field):
    if len(field.data) < 0:
        raise ValidationError("Summoner Name too short")
    elif len(field.data) > 16:
        raise ValidationError("Summoner Name too long")


class FullForm(Form):
    rank = StringField('rank', [rank_validate])
    current_gain = IntegerField('current_gain', [cg_validate])
    current_loss = IntegerField('current_loss', [cl_validate])
    current_LP = IntegerField('current_LP', [clp_validate])
    in_series = BooleanField('in_series')
    series_wins = IntegerField('series_wins', [sw_validate])
    series_losses = IntegerField('series_losses', [sl_validate])
    goal = StringField('goal', validators=[DataRequired(), rank_validate])
    winrate = IntegerField('winrate', validators=[DataRequired(), wr_validate])

class AbridgedForm(Form):
    username = StringField('username', validators=[DataRequired(), user_validate])
    goal = StringField('goal', validators=[DataRequired(), rank_validate])
    winrate = IntegerField('winrate', [wr_validate])
