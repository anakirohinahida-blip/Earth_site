from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class ApplicationForm(forms.Form):
    plot_size = forms.IntegerField(
        label='Размер участка (м²)',
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Например: 600'
            }
        )
    )

    passport_data = forms.CharField(
        label='Серия и номер паспорта',
        validators=[
            RegexValidator(
                regex=r'^\d{4}\s?\d{6}$',
                message='Формат: XXXX XXXXXX'
            )
        ],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '1234 567890'
            }
        )
    )

    cadastral_number = forms.CharField(
        label='Кадастровый номер',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '25:10:000000:123'
            }
        )
    )

    address = forms.CharField(
        label='Адрес участка',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите адрес участка'
            }
        )
    )

    payment_acquisitions = forms.ChoiceField(
        label='Вид приобретения',
        choices=[
            ('rent', 'Аренда'),
            ('purchase', 'Покупка')
        ],
        widget=forms.Select(
            attrs={'class': 'form-select'}
        )
    )

    building = forms.ChoiceField(
        label='Тип строения',
        choices=[
            ('home', 'Дом'),
            ('shop', 'Магазин'),
            ('factory', 'Завод'),
            ('other', 'Другое')
        ],
        widget=forms.Select(
            attrs={'class': 'form-select'}
        )
    )

    document = forms.FileField(
        label='Документы',
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control'
            }
        )
    )



class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Логин',
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'client123'
        })
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.ru'
        })
    )

    password = forms.CharField(
        label='Пароль',
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    password_confirm = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    full_name = forms.CharField(
        label='ФИО',
        validators=[
            RegexValidator(
                regex=r'^[А-Яа-яЁё\s]+$',
                message='Только кириллица'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Иванов Иван Иванович'
        })
    )

    phone = forms.CharField(
        label='Телефон',
        validators=[
            RegexValidator(
                regex=r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$',
                message='Формат: 8(900)123-45-67'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '8(900)123-45-67'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            raise forms.ValidationError('Пароли не совпадают')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user



class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    def clean(self):
        cleaned_data = super().clean()

        user = authenticate(
            username=cleaned_data.get('username'),
            password=cleaned_data.get('password')
        )

        if not user:
            raise forms.ValidationError('Неверный логин или пароль')

        self.user = user
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)