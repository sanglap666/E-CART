from django import forms


PAYMENT_CHOICES = (
    ('s','STRIPE'),
    ('u','UPI'),
    ('cod','CASH ON DELIVERY'),
)

class  AddressForm(forms.Form):
    
    


    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Billing Name'}))
    phoneno = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Contact No.'}))
    street = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Street address'}))
    houseno = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'House address'}))
    pincode = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Pincode'}))
    
    #options = forms.ChoiceField(choices=PAYMENT_CHOICES,label='Payment Options') 

    