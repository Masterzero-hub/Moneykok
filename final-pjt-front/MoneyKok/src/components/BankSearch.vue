<template>
    <div class="container mt-5">
      <!-- 헤더 -->
      <div class="row justify-content-center">
        <div class="col-md-8 text-center">
          <h2 class="section-title mb-4">현재 위치 주변의 은행을 찾아보세요</h2>
          <p class="text-muted mb-4">
            주변에 있는 은행을 쉽게 검색하고 필요한 정보를 확인하세요.
          </p>
          <button class="btn-common btn-mint" @click="searchNearbyBanks">
            주변 은행 조회
          </button>
        </div>
      </div>
  
      <!-- 지도 -->
      <div class="row justify-content-center mt-5">
        <div class="col-md-10">
          <div id="map" class="map-container"></div>
        </div>
      </div>
  
      <!-- 결과 목록 -->
      <div class="row justify-content-center mt-5" v-if="bankList.length">
        <div class="col-md-10">
          <h4 class="section-subtitle mb-3">
            근처에 총 {{ bankList.length }} 개의 은행이 있습니다.
          </h4>
          <div
            v-for="(bank, index) in bankList"
            :key="bank.id"
            class="bank-card shadow-sm p-3 mb-4"
          >
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h5 class="bank-title mb-1">{{ index + 1 }}. {{ bank.place_name }}</h5>
                <p class="text-muted mb-1">{{ bank.category_name }}</p>
                <p class="bank-address mb-1" v-if="bank.road_address_name">
                  <strong>주소:</strong> {{ bank.road_address_name }}
                </p>
                <p class="bank-phone mb-1" v-if="bank.phone">
                  <strong>전화:</strong> {{ bank.phone }}
                </p>
              </div>
              <div>
                <a
                  :href="bank.place_url"
                  class="btn-small-common btn-mint"
                  target="_blank"
                >
                  상세 보기
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- 검색 결과가 없을 경우 -->
      <div class="row justify-content-center mt-5" v-else>
        <div class="col-md-8 text-center">
          <p class="text-muted">검색 결과가 없습니다. 버튼을 눌러 다시 시도하세요.</p>
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
        searchRadius: 1000, // 고정 검색 반경 (미터)
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
  .section-title {
    font-size: 1.8rem;
    font-weight: bold;
    color: #333;
  }
  
  .section-subtitle {
    font-size: 1.2rem;
    font-weight: bold;
    color: #555;
  }
  
  .map-container {
    width: 100%;
    height: 500px;
    border-radius: 10px;
    overflow: hidden;
  }
  
  .bank-card {
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 15px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  
  .bank-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }
  
  .bank-title {
    font-size: 1.1rem;
    font-weight: bold;
  }
  
  .bank-address,
  .bank-phone {
    font-size: 0.9rem;
    color: #555;
  }

  
  </style>
  