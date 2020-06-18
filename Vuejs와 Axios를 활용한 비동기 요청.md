# Vuejs와 Axios를 활용한 비동기 요청

- Js를 활용한 비동기 요청으로 불필요한 새로고침과 렌더링 코스트 낭비를 방지
- JS는 Vanilla JS가 대신 Vuejs를 활용
- Vuejs와 axios모두 CDN을 활용

## Ⅰ. 준비과정

### 1. CDN 작성

- 모든 html이 공유하는 `base.html`의 헤더에 CDN 작성

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Title</title>
  <style>
  <!-- Vue, Axios -->
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
</head>
<body>
</body>
</html>
```

### 2. Vuejs

#### (1) Vue 인스턴스 생성

- el : 마운트할 element
- delimiters : DTL과 겹치는 구분 문자 해결
- data : 반응형 데이터 정의
- methods : data를 변경할 함수 작성
- mounted : 초기값 부여가 필요할때 사용

```vue
<script>
    const vm = new Vue({
        el: '#app',
        delimiters: ['$[[', ']]'],
        data: {
            stringData: '',
            arrayData: [],
        },
        methods: {
            setData: function () {
                vm.$data.stringData = "값"
                vm.$data.arrayData = ["값1", "값2"]
        },
        mounted: function() {
            //this.setData()
            vm.$data.stringData = "초기값"
            vm.$data.arrayData = ["초기값1", "초기값2"]
        }
    })
</script>
```

#### (2) Vue 문법 활용

##### 조건문과 반복문

- `v-for="data in arrayData"`
- `v-if="조건"`
- 첫번째만 특정 클래스 주기

```vue
<template v-for="data in arrayData">
    <template v-if="data === arrayData[0]">
        <div class="common_class uniq_class"></div>
    </template>
    <template v-else>
        <div class="common_class"></div>
    </template>
</template>
```

##### 바인딩

- `:key = value`
- 반복요소를 활용한 바인딩

```vue
<template v-for="data in arrayData">
    <a :href=`articles/${data.id}/`>
        <img :src="data.img_url">
    </a>
</template>
```

### 3. Axios

`axios.get(url, params:{키:밸류})`

- 해당 url로 get 요청

- parameter는 키:밸류 객체형태로 전달
- 응답 성공시 .then() 콜백함수 실행
- 응답 실패시 .catch() 콜백함수 실행

```js
// GET 방식, url = API요청 url
axios.get(url, {
    params: {
        키: 밸류,
    }
})
    .then(res => {
    // 응답 성공시
})
    .catch(err => {
    // 응답 실패시
})
```

### 4. serializer

- like, follow 등의 구현시에는 불필요
- QuerySet을 다룰경우 직렬화가 요구됨

#### (1) REST Framework 설치

- 패키지 공식문서 : https://www.django-rest-framework.org/tutorial/quickstart/

```bash
$ pip install djangorestframework
```

#### (2) `settings.py` 설정 변경

- `INSTALLED_APPS` 설정 변수 아래의 내용 추가

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

#### (3) `serializers.py` 생성

- `serializers`와 `직렬화하고자 하는 모델` import
- 출력하고자 하는 `fields` 설정

```python
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('column1', 'column2', ....) # 모든column 출력 "__all__"
```

#### (4) `views.py` 함수 등록

- 직렬화 불필요
  - `django.http`의 `JsonResponse` 를 import 하여 data를 리턴
- 직렬화 필요시
  - 위에서 작성한 `.serializers.py` 에서 `ArticleSerializer` import하여 QuerySet 직렬화
    - 직렬화 데이터가 여러개면 `many = True` 옵션 설정
  - `rest_framework.response` 의 `Response` 를 import하여 data를 리턴
  - REST 위한 `@api_view['GET'])` 데코레이터 작성

```python
# 직렬화 불필요
from django.http import JsonResponse
def returnData1(request):
    ...
    data = {
        '키': 밸류
    }
    return JsonResponse(data)
```

```python
# 직렬화 필요
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ArticleSerializer

@api_view(['GET'])
def get_recommend(request):
    ...
    serializer = ArticleSerializer(QuertSet, many=True)
    data = {
		...
        'serializer_data': serializer.data
    }
    return Response(data)
```

## Ⅱ. 최종코드

### 1. settings.py

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

### 2. serializers.py

```python
from rest_framework import serializers
from .models import Movie

class MovieCarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'poster_path')
```

### 3. views.py

```python
# 직렬화 불필요
from django.http import JsonResponse
def returnData1(request):
    ...
    data = {
        '키': 밸류
    }
    return JsonResponse(data)

# 직렬화 필요
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ArticleSerializer

@api_view(['GET'])
def returnData2(request):
    ...
    serializer = ArticleSerializer(QuertSet, many=True)
    data = {
		...
        'serializer_data': serializer.data
    }
    return Response(data)
```

### 4. base.html

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Title</title>
  <style>
  <!-- Vue, Axios -->
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
</head>
<body>
    {% block app %}
    {% endblock %}
</body>
</html>
```

### 5. main.html

```vue
<!--base.html을 상속-->
{% extends 'base.html' %}
{% block app %}
	<h1> $[[ stringData ]] </h1>
    <template v-for="data in arrayData">
        <template v-if="data === arrayData[0]">
            <div class="common_class unique_class">
                <a :href=`articles/${data.id}/`>
                    <img :src="data.img_url">
                </a>
            </div>
        </template>
        <template v-else>
            <div class="common_class">
                <a :href=`articles/${rec.id}/`>
                    <img :src="data.img_url">
                </a>
            </div>
        </template>
    </template>
{% endblock %}

{% block script %}
    <script>
        const vm = new Vue({
            el: '#app',
            delimiters: ['$[[', ']]'],
            data: {
                stringData: '',
                arrayData: [],
            },
            methods: {
                setData: function () {
                    vm.$data.stringData = "값"
                    vm.$data.arrayData = ["값1", "값2"]
            },
            mounted: function() {
                // this.setData()도 가능
                vm.$data.stringData = "초기값"
                vm.$data.arrayData = ["초기값1", "초기값2"]
            }
        })
    </script>
{% endblock %}
```
