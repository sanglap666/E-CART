from django.contrib.auth import get_user_model
from django.db.models import Q
from django import forms


user = get_user_model()

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='password confirmation',widget=forms.PasswordInput)

    class Meta:
        model = user
        fields = ['email','username']

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')  
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("passwords do not match")

        return password2

    def save(self,commit=True):
        user = super(UserCreationForm,self).save(commit=False)  
        print(user)
        user.set_password(self.cleaned_data['password1'])
        if commit :
            user.save()
        return user    


class UserLoginForm(forms.Form):

    query = forms.CharField(label='Username/Email',widget=forms.TextInput)
    password = forms.CharField(label='Passowrd',widget=forms.PasswordInput)    

    def clean(self,*args,**kargs):

        query = self.cleaned_data.get('query')
        password = self.cleaned_data.get('password')

        user_qs_final = user.objects.filter(
            Q(username__iexact = query) | Q(email__iexact = query) ).distinct()

        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError("Invalid Credentials - user does not exist ")
        
        user_obj  = user_qs_final.first() 

        if not user_obj.check_password(password):
            raise forms.ValidationError("USER credentials not correct")

        self.cleaned_data['object'] = user_obj

        return super(UserLoginForm,self).clean(*args,**kargs)   

