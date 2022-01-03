from flask_wtf.form import FlaskForm


class frm(FlaskForm):
    def clean(self):
        pass

    def populate(self):
        self.cleaned_data = self.data.copy()
        self.cleaned_data.pop("csrf_token", None)
        self.cleaned_data.pop("submit", None)

    def validate_on_submit(self):
        self.populate()
        self.clean()
        return super().validate_on_submit()
