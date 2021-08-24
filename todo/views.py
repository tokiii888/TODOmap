from django import forms
from django.urls import reverse_lazy
from .models import Todo
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import requests, geocoder
from django.db.models.expressions import RawSQL
import math
from django.db.backends.signals import connection_created
from django.dispatch import receiver
from django.urls import reverse_lazy

#googleapikey = '取得したGoogleのAPIキー'

# Create your views here.

class Form(forms.ModelForm):
  #todo = forms.CharField(widget=forms.Textarea, label='')
  class Meta:
    model = Todo
    exclude = ('created_at','updated_at','lat','lng')  #入力項目から作成日時、更新日時を除外
    widgets = {
      #'todo': forms.TextInput(attrs={'autocomplete': 'off'}),
      'todo': forms.Textarea(attrs={'autocomplete': 'off', 'cols': 80, 'rows': 10}, ),
      'adress': forms.Textarea(attrs={'autocomplete': 'off', 'cols': 60, 'rows': 1},),
    }

@receiver(connection_created)
def extend_sqlite(connection=None, **kwargs):
    if connection.vendor == "sqlite":
        # sqlite doesn't natively support math functions, so add them
        cf = connection.connection.create_function
        cf('acos', 1, math.acos)
        cf('cos', 1, math.cos)
        cf('radians', 1, math.radians)
        cf('sin', 1, math.sin)

# 一覧表示
class Index(ListView):
  template_name = "todo/index.html"
  model = Todo
  paginate_by = 10 # ページネーションが5ページまで
  def get_queryset(self):
    def get_locations_nearby_coords(latitude, longitude):
      """
      Return objects sorted by distance to specified coordinates
      which distance is less than max_distance given in kilometers
      """
      # Great circle distance formula
      gcd_formula = "6371 * acos(\
      cos(radians(%s)) * cos(radians(lat)) \
      * cos(radians(lng) - radians(%s)) + \
      sin(radians(%s)) * sin(radians(lat)) \
      )"
      distance_raw_sql = RawSQL(
          gcd_formula,
          (latitude, longitude, latitude)
      )
      qs = Todo.objects.all() \
      .annotate(distance=distance_raw_sql)\
      .order_by('distance')
      return qs
    geo_request_url = 'https://get.geojs.io/v1/ip/geo.json'
    geo_data = requests.get(geo_request_url).json()
    return get_locations_nearby_coords(float(geo_data['latitude']), float(geo_data['longitude']))

# 詳細表示
class Detail(DetailView):
  template_name = "todo/detail.html"
  model = Todo


# 新規作成
class Create(CreateView):
  template_name = "todo/form.html"
  model = Todo
  form_class = Form
  success_url = reverse_lazy('todo:index')

    # 送られた値が正しかった時の処理(緯度経度の保存)
  def form_valid(self, form):
    adress = self.request.POST.get('adress')
    ret = geocoder.osm(adress, timeout=5.0)
    form.instance.lat = ret.lat
    form.instance.lng = ret.lng
    form.save()
    return super().form_valid(form)


# 更新
class Update(UpdateView):
  template_name = "todo/form.html"
  model = Todo
  form_class = Form
  success_url = reverse_lazy('todo:index')

    # 送られた値が正しかった時の処理(緯度経度の保存)
  def form_valid(self, form):
    pk = self.kwargs.get(self.pk_url_kwarg)
    adress = self.request.POST.get('adress')
    ret = geocoder.osm(adress, timeout=5.0)
    form.instance.lat = ret.lat
    form.instance.lng = ret.lng
    form.save()
    return super().form_valid(form)

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