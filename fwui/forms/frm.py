from flask_wtf.form import FlaskForm


class frm(FlaskForm):
    def clean(self):
        pass

    def populate(self):
        self.cleaned_data = self.data.copy()
        self.cleaned_data.pop("csrf_token", None)
        self.cleaned_data.pop("submit", None)
        # self.cleaned_data = {k: str(v) for k, v in self.cleaned_data.items()}

    def validate_on_submit(self):
        self.populate()
        self.clean()
        return super().validate_on_submit()
