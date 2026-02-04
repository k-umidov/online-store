from django import forms
from .models import Category,Delivery,Customer
from django_svg_image_form_field import SvgAndImageFormField
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.forms import User

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = []
        field_classes = {
            'icon': SvgAndImageFormField,
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(label=False,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder': 'Имя пользователя'
    }))
    password = forms.CharField(label=False,widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))

class RegisterForm(UserCreationForm):
    username = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    email = forms.EmailField(label=False,widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша почта'
    }))
    password1 = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))
    password2 = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Потдвердите пароль'
    }))
    first_name = forms.CharField(label=False,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваше имя'
    }))
    last_name = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша фамилия'
    }))
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'form-control',
        'placeholder': 'Фото для профиля'
    }))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2','avatar')

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ('region','first_name','last_name','email','city','street','comment','phone',)
        widgets = {
        'region':forms.TextInput(attrs={
                'class': 'form-control',
        '       placeholder': 'Регион'
    }),
        'first_name':forms.TextInput(attrs={
                'class': 'form-control',
        '       placeholder': 'Ваша имя...'
    }),
        'last_name':forms.TextInput(attrs={
                'class': 'form-control',
        '       placeholder': 'Ваша фамилия...'
    }),
        'email':forms.EmailInput(attrs={
                'class': 'form-control',
        '       placeholder': 'Ваша почта...'
    }),
        'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Город'
            }),
        'street':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Адрес'
    }),
        'phone':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер телефона'
    }),
        'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Комментарии к заказу'
            }),
        }

class EditAccountForm(forms.ModelForm):
    username = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    email = forms.EmailField(label=False,widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша почта'
    }))
    first_name = forms.CharField(label=False,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваше имя'
    }))
    last_name = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша фамилия'
    }))
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'form-control',
        'placeholder': 'Фото для профиля'
    }))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','avatar')

class EditCustomerForm(forms.ModelForm):
    phone = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Телефон'
    }))
    city = forms.CharField(required=False,label=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Город'
    }))
    region = forms.CharField(required=False,label=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Регион'
    }))
    street = forms.CharField(required=False,label=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Адрес'
    }))
    email = forms.CharField(required=False,label=False, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Почта'
    }))
    class Meta:
        model = Customer
        fields = ('phone','city','region','email','street')




class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Текущий пароль'
        })
    )

    new_password1 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Новый пароль'
        })
    )

    new_password2 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердить'
        })
    )

