<template>
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <br />
          <h4 class="text-center">현재 위치 주변의 은행을 검색해보세요</h4>
          <div class="d-flex justify-content-center mt-3">
            <button type="button" class="btn btn-outline-success" @click="searchNearbyBanks">
              주변 은행 조회
            </button>
          </div>
        </div>
      </div>
  
      <div class="row justify-content-center mt-4">
        <div>
          <div id="map" class="map-container"></div>
        </div>
      </div>
  
      <div class="row justify-content-center mt-4" v-if="bankList.length">
        <div>
          <p>근처에 총 {{ bankList.length }} 개의 은행이 있습니다.</p>
          <hr />
          <div v-for="(bank, index) in bankList" :key="bank.id">
            <ul class="list-unstyled">
              <li>
                <strong>{{ index + 1 }}번째 은행</strong>
              </li>
              <li>{{ bank.place_name }}</li>
              <li>{{ bank.category_name }}</li>
              <li v-if="bank.phone">{{ bank.phone }}</li>
              <li v-if="bank.road_address_name">{{ bank.road_address_name }}</li>
              <li>
                <a :href="bank.place_url" target="_blank">{{ bank.place_url }}</a>
              </li>
            </ul>
            <hr />
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "BankSearch",
    data() {
      return {
        apiKey: import.meta.env.VITE_KAKAO_API_KEY,
        map: null,
        latitude: null,
        longitude: null,
        infowindow: null,
        ps: null,
        bankList: [],
        searchRadius: 1000, // 고정 검색 반경 (1000미터)
      };
    },
    mounted() {
      const apiKey = this.apiKey;
  
      if (!apiKey) {
        console.error("Kakao API 키가 설정되지 않았습니다.");
        return;
      }
  
      const script = document.createElement("script");
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${apiKey}&libraries=services,clusterer,drawing&autoload=false`;
  
      script.onload = () => {
        console.log("Kakao Maps SDK 로드 완료");
        kakao.maps.load(() => {
          console.log("Kakao Maps 객체 준비 완료");
          this.initializeMap(); // 지도 초기화
        });
      };
  
      document.body.appendChild(script);
    },
    methods: {
      initializeMap() {
        // 지도 초기화 (중앙 좌표: 서울)
        const container = document.getElementById("map");
        const options = {
          center: new kakao.maps.LatLng(37.5665, 126.9780),
          level: 5,
        };
  
        this.map = new kakao.maps.Map(container, options);
        this.ps = new kakao.maps.services.Places(this.map);
        this.infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
      },
      searchNearbyBanks() {
        // 사용자 위치 가져오기
        if (!navigator.geolocation) {
          alert("이 브라우저에서는 Geolocation이 지원되지 않습니다.");
          return;
        }
  
        navigator.geolocation.getCurrentPosition(
          (pos) => {
            this.latitude = pos.coords.latitude;
            this.longitude = pos.coords.longitude;
  
            // 지도 중심 이동
            const center = new kakao.maps.LatLng(this.latitude, this.longitude);
            this.map.setCenter(center);
  
            // 주변 은행 검색
            this.searchPlacesByCoordinates(this.latitude, this.longitude);
          },
          (err) => {
            console.error(`ERROR(${err.code}): ${err.message}`);
            alert("현재 위치를 가져올 수 없습니다.");
          }
        );
      },
      searchPlacesByCoordinates(lat, lon) {
        if (!this.ps) {
          console.error("Kakao Maps 객체가 아직 준비되지 않았습니다.");
          return;
        }
  
        this.bankList = []; // 기존 결과 초기화
  
        this.ps.keywordSearch(
          "은행",
          (data, status, pagination) => {
            if (status === kakao.maps.services.Status.OK) {
              const bounds = new kakao.maps.LatLngBounds();
  
              data.forEach((place) => {
                if (place.category_group_code === "BK9") {
                  this.bankList.push(place);
                }
                this.displayMarker(place);
                bounds.extend(new kakao.maps.LatLng(place.y, place.x));
              });
  
              this.map.setBounds(bounds);
            } else {
              alert("현재 위치 주변에 해당 은행이 없습니다.");
            }
          },
          {
            location: new kakao.maps.LatLng(lat, lon),
            radius: this.searchRadius, // 고정된 반경 사용
          }
        );
      },
      displayMarker(place) {
        const marker = new kakao.maps.Marker({
          map: this.map,
          position: new kakao.maps.LatLng(place.y, place.x),
        });
  
        kakao.maps.event.addListener(marker, "click", () => {
          this.infowindow.setContent(
            `<div style="padding:5px;font-size:12px;">${place.place_name}</div>`
          );
          this.infowindow.open(this.map, marker);
        });
      },
    },
  };
  </script>
  
  <style scoped>
  #map {
    width: 100%;
    height: 500px;
  }
  
  .map-container {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .input-group {
    display: flex;
    align-items: center;
  }
  
  .input-group .form-control {
    flex: 1;
  }
  </style>
  