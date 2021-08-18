from django import forms
from django.db import models
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Todo
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import geocoder

#googleapikey = '取得したGoogleのAPIキー'

# Create your views here.

class Form(forms.ModelForm):
  #todo = forms.CharField(widget=forms.Textarea, label='')
  class Meta:
    model = Todo
    exclude = ('created_at','updated_at',)  #入力項目から作成日時、更新日時を除外
    widgets = {
      #'todo': forms.TextInput(attrs={'autocomplete': 'off'}),
      'todo': forms.Textarea(attrs={'autocomplete': 'off', 'cols': 80, 'rows': 10}, ),
      'adress': forms.Textarea(attrs={'autocomplete': 'off', 'cols': 60, 'rows': 1},),
    }
# 一覧表示
class Index(ListView):
  template_name = "todo/index.html"
  model = Todo
  paginate_by = 10 # ページネーションが5ページまで
  # フィルタ
  #def get_queryset(self):
  # return MyModel.objects.filter(some_column=foo)

# 詳細表示
class Detail(DetailView):
  template_name = "todo/detail.html"
  model = Todo
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    pk = self.kwargs.get(self.pk_url_kwarg)
    object = self.model.objects.get(pk=pk)
    ret = geocoder.osm(object.adress, timeout=5.0)
    context['lat'] = ret.lat
    context['lng'] = ret.lng
    return context

# 新規作成
class Create(CreateView):
  template_name = "todo/form.html"
  model = Todo
  form_class = Form
  success_url = reverse_lazy('todo:index')

# 更新
class Update(UpdateView):
  template_name = "todo/form.html"
  model = Todo
  form_class = Form
  success_url = reverse_lazy('todo:index')

# 削除
class Delete(DeleteView):
  """
  Todoの削除
  【デフォルトの動作】
  getリクエスト・・・確認ページへ遷移
  postリクエスト・・・削除を実行
  【補足】
  レコードを削除せず、有効フラグを消す(論理削除)場合は
  deleteをオーバーライドしてその中に処理を書く
  """
  template_name = "todo/delete.html"
  model = Todo
  success_url = reverse_lazy('todo:index')