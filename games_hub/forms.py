from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from .models import GameRating, Comment
from django import forms


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text="Required. Provide a valid email address.")

    recaptcha = ReCaptchaField(
        error_messages={
            "required": "Будь ласка, заповніть поле reCAPTCHA.",
        }
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Ім'я користувача"
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["placeholder"] = "Електронна пошта"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Пароль"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Підтвердіть пароль"
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs.pop("help_text", None)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Аккаунт з такою поштою вже зареєстрований.")
        return email


class GameRatingForm(forms.ModelForm):
    class Meta:
        model = GameRating
        fields = ("rating",)
        labels = {"rating": "Ваша оцінка"}


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))

    class Meta:
        model = Comment
        fields = ["content"]
