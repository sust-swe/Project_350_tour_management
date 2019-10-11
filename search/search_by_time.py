from homepage.base import *


class DateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        year_choice = [("", "------------")]
        for i in range(dt.today().year, dt.today().year+5):
            year_choice += [(str(i), str(i))]
        self.fields['year'] = forms.ChoiceField(choices=year_choice)
        self.fields['month'] = forms.ChoiceField(
            choices=[("", "------------")])
        self.fields['day'] = forms.ChoiceField(choices=[("", "------------")])
        self.fields['to_year'] = forms.ChoiceField(
            choices=[("", "------------")], label='Year')
        self.fields['to_month'] = forms.ChoiceField(
            choices=[("", "------------")], label='Month')
        self.fields['to_day'] = forms.ChoiceField(
            choices=[("", "------------")], label='Day')


class View1(views.View):
    template_name = 'search_by_time.html'

    def get(self, request):
        form = DateForm()
        print(form)
        return render(request, self.template_name, {'form': form})


urlpatterns = [
    path('', View1.as_view())
]
