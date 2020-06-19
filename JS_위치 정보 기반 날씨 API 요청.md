# JS_위치 정보 기반 날씨 API 요청

## Ⅰ. 호출 과정

- 브라우저에서 위치 정보를 획득한다.
- 획득한 경도, 위도값으로 날씨 API에 요청한다

### 1. 브라우저 위치 정보 획득

- 위치 정보는 `window.navigator.geolocation` 객체 안에 있다.
- 해당 기기가 기능을 제공하여야 하고, 유저가 위치 정보 제공에 동의해야 한다.

```js
if (navigator.geolocation) {
    // 해당 기기가 기능을 제공한다.
} else {
    // 해당 기기가 기능을 제공하지 않는다
}
```

#### (1) geolocation

> `window.navigator.geolocation`

- getCurrentPosition : 현재 Position 정보를 읽는다
- watchPostion : Position 정보를 일정 주기로 읽는다(watch) => `속도 = 거리/시간` 으로 속도 계산 가능
- clearWatch : Position 정보를 일정 주기로 읽는 watch 행위를 끝낸다.

#### (2) getCurrentPosition

> `window.navigator.geolocation.getCurrentPosition`

- 인자1 : 성공시 호출될 함수
- 인자2 : 실패시 호출될 함수
- 인자3 : 옵션

```js
navigator.geolocation.getCurrentPosition(function(position) {
    // 성공시
    // position.coords.키
    // position.titmestamp
}, function(error) {
    // 실패시
    // 유저 제공 거부시 error.code == 1 & error.message == "User denied Geolocation"
}, {
    // 옵션
})
```

#### (3) 위치정보 리턴값

> 성공시

- coords
  - accuracy : 정확도
  - altitude : 고도
  - altitudeAccuracy
  - heading
  - latitude : 위도
  - longitude : 경도
  - speed
- timestamp

#### (4) 오류코드

> 실패시

- 유저가  위치 정보 제공 거부시
  - code : 1
  - message :  "User denied Geolocation"

#### (5) 옵션

- enableHighAccuracy : 배터리 소모하여 정확도 향상 (t/f)
- maximumAge : position 정보 캐싱 (sec)
- timeout : 주어진 시간안에 못찾으면 에러 (sec)

### 2. openweather 날씨 API 요청

#### (1) 특정 도시이름으로 날씨 요청

> 위치 정보를 못 얻을시, 디폴트 도시값을 정해 요청한다.

```
GET : https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}
```

#### (2) 특정 경도 위도로 날씨 요청 => 가장 근거리 데이터 획득

```
GET : https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}
```

#### (3) 날씨 정보 리턴값

- coords
  - lon :경도
  - lat : 위도
- weather[0]
  - id : 날씨 id
  - main : 날씨
  - description : 자세한 날씨
  - icon : 날씨 아이콘
- name : 도시정보

## Ⅱ. 최종 코드

```js
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        const url = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
        // url를 이용해 날씨를 요청 후, 활용한다.
    }, function(err) {
        	if (err.code === 1) {
                const url = "https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"
                // url를 이용해 날씨를 요청 후, 활용한다.
              } else {
                console.log('기타 에러입니다', err)
              }
    }, {
            //옵션
    })
} else {
    const url = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    // url를 이용해 날씨를 요청 후, 활용한다.
}
```

