from django import forms

class AddBook(forms.Form):

    bookname = forms.CharField(max_length=50,label="Kitap Adı")
    image = forms.FileField(label="Resim Ekle")

    def clean(self):
        bookname = self.cleaned_data.get("bookname")
        image = self.cleaned_data.get("image")       
       
        values = {
            "bookname" : bookname,
            "image"    : image,
        }

        return values
    
