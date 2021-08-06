from django import forms
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Todo
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.

def index(request):
  latest_todo_list = Todo.objects.order_by('-updated_at')[:5]
  context={
    'latest_todo_list' : latest_todo_list
  }
  return render(request, 'todo/index.html', context)

class Form(forms.ModelForm):
  class Meta:
    model = Todo
    exclude = ('created_at','updated_at',)  #入力項目から作成日時、更新日時を除外

# 一覧表示
class Index(ListView):
  template_name = "index.html"
  model = Todo
  paginate_by = 10 # ページネーションが5ページまで

# 詳細表示
class Detail(DetailView):
  template_name = "detail.html"
  model = Todo

# 新規作成
class Create(CreateView):
  template_name = "form.html"
  model = Todo
  form_class = Form
  success_url = reverse_lazy('todo:index')

# 更新
class Update(UpdateView):
  template_name = "form.html"
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
  template_name = "delete.html"
  model = Todo
  success_url = reverse_lazy('todo:index')