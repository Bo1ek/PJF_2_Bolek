from django.forms import ModelForm, DateInput
from .models import Room, CalendarEvent
from django.contrib.auth.models import User
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude  =['host','participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

class CalendarEventForm(ModelForm):
    class Meta:
        model = CalendarEvent
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CalendarEventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)