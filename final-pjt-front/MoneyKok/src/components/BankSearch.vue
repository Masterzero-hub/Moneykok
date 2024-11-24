<template>
    <div class="container mt-5">
      <!-- 헤더 -->
      <div class="row justify-content-center">
        <div class="col-md-8 text-center">
          <h2 class="section-title mb-4">은행 검색</h2>
          <p class="text-muted mb-4">
            위치와 은행명을 입력하거나 주변 은행을 검색하세요.
          </p>
  
          <!-- 광역시/도 선택 -->
          <div class="input-group mb-3">
            <select class="form-select" v-model="selectedProvince" @change="updateCities">
              <option value="" disabled selected>광역시/도 선택</option>
              <option v-for="province in provinces" :key="province" :value="province">
                {{ province }}
              </option>
            </select>
          </div>
  
          <!-- 시/군/구 선택 -->
          <div class="input-group mb-3" v-if="selectedProvince">
            <select class="form-select" v-model="selectedCity">
              <option value="" disabled selected>시/군/구 선택</option>
              <option v-for="city in cities[selectedProvince]" :key="city" :value="city">
                {{ city }}
              </option>
            </select>
          </div>
  
          <!-- 은행 선택 -->
          <div class="input-group mb-3">
            <select class="form-select" v-model="selectedBank">
              <option value="" disabled selected>은행 선택</option>
              <option v-for="bank in banks" :key="bank.code" :value="bank.name">
                {{ bank.name }}
              </option>
            </select>
          </div>
  
          <button class="btn-common btn-mint" @click="searchLocation">
            검색
          </button>
          <button class="btn-common btn-outline-primary mt-2" @click="searchNearbyBanks">
            현재 위치 주변 검색
          </button>
        </div>
      </div>
  
      <!-- 지도 및 결과 -->
      <div class="row justify-content-center mt-5">
        <div class="col-md-10">
          <div id="map" class="map-container"></div>
        </div>
      </div>
  
      <div class="row justify-content-center mt-5" v-if="bankList.length">
        <div class="col-md-10">
          <h4 class="section-subtitle mb-3">
            검색 결과: 총 {{ bankList.length }} 개의 은행이 있습니다.
          </h4>
          <div
            v-for="(bank, index) in bankList"
            :key="bank.id"
            class="bank-card shadow-sm p-3 mb-4"
          >
            <h5>{{ index + 1 }}. {{ bank.place_name }}</h5>
            <p>{{ bank.road_address_name }}</p>
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
      // Kakao Maps API
      apiKey: import.meta.env.VITE_KAKAO_API_KEY,
      map: null,
      ps: null,
      infowindow: null,
      bankList: [],
      searchRadius: 1000, // 검색 반경

      // 선택 데이터
      selectedProvince: "",
      selectedCity: "",
      selectedBank: "",

      // 지역 데이터
      provinces: [
        "서울특별시", "세종특별자치시", "광주광역시", "대구광역시", "대전광역시", "부산광역시", "울산광역시",
        "인천광역시", "강원도", "경기도", "경상남도", "경상북도", "전라남도", "전라북도",
        "충청남도", "충청북도", "제주특별자치도",
      ],
      cities: {
        "서울특별시": ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구"],
        "세종특별자치시": ["세종시"],
        "광주광역시": ["동구", "서구", "남구", "북구", "광산구"],
        "대구광역시": ["중구", "동구", "서구", "남구", "북구", "수성구", "달서구"],
        "대전광역시": ["동구", "중구", "서구", "유성구", "대덕구"],
        "부산광역시": ["중구", "서구", "동구", "영도구", "부산진구", "동래구", "남구"],
        "울산광역시": ["중구", "남구", "동구", "북구", "울주군"],
        "인천광역시": ["중구", "동구", "미추홀구", "연수구", "남동구", "부평구", "계양구"],
        "강원도": ["춘천시", "원주시", "강릉시", "동해시", "태백시", "속초시", "삼척시"],
        "경기도": ["수원시", "고양시", "용인시", "성남시", "부천시", "안산시", "안양시"],
        "경상남도": ["창원시", "진주시", "통영시", "사천시", "김해시", "밀양시", "거제시"],
        "경상북도": ["포항시", "경주시", "김천시", "안동시", "구미시", "영주시", "영천시"],
        "전라남도": ["목포시", "여수시", "순천시", "나주시", "광양시"],
        "전라북도": ["전주시", "군산시", "익산시", "정읍시", "남원시"],
        "충청남도": ["천안시", "공주시", "보령시", "아산시", "서산시"],
        "충청북도": ["청주시", "충주시", "제천시"],
        "제주특별자치도": ["제주시", "서귀포시"],
      },

      // 은행 데이터
      banks: [
        { name: "우리은행", code: "0010001" },
        { name: "한국스탠다드차드은행", code: "0010002" },
        { name: "아이엠뱅크", code: "0010016" },
        { name: "부산은행", code: "0010017" },
        { name: "광주은행", code: "0010019" },
        { name: "제주은행", code: "0010020" },
        { name: "전북은행", code: "0010022" },
        { name: "경남은행", code: "0010024" },
        { name: "중소기업은행", code: "0010026" },
        { name: "국민은행", code: "0010927" },
        { name: "신한은행", code: "0011625" },
        { name: "농협은행주식회사", code: "0013175" },
        { name: "하나은행", code: "0013909" },
        { name: "케이뱅크", code: "0014674" },
        { name: "수협은행", code: "0014807" },
        { name: "카카오뱅크", code: "0015130" },
        { name: "토스뱅크", code: "0017801" },
      ],
    };
  },
  mounted() {
    const apiKey = this.apiKey;
    const script = document.createElement("script");
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${apiKey}&libraries=services,clusterer,drawing&autoload=false`;

    script.onload = () => {
      kakao.maps.load(() => {
        this.initializeMap();
      });
    };

    document.body.appendChild(script);
  },
  methods: {
    updateCities() {
      this.selectedCity = ""; // 시/군/구 초기화
    },
    initializeMap() {
      const container = document.getElementById("map");
      const options = {
        center: new kakao.maps.LatLng(37.5665, 126.9780), // 서울 중심
        level: 5,
      };

      this.map = new kakao.maps.Map(container, options);
      this.ps = new kakao.maps.services.Places(this.map);
      this.infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
    },
    searchLocation() {
      if (!this.selectedProvince || !this.selectedCity || !this.selectedBank) {
        alert("모든 필드를 선택해주세요.");
        return;
      }

      const keyword = `${this.selectedProvince} ${this.selectedCity} ${this.selectedBank}`;
      this.ps.keywordSearch(keyword, (data, status) => {
        if (status === kakao.maps.services.Status.OK) {
          this.bankList = data;
          const bounds = new kakao.maps.LatLngBounds();

          data.forEach((place) => {
            if (place.category_group_code === "BK9") {
              this.displayMarker(place);
              bounds.extend(new kakao.maps.LatLng(place.y, place.x));
            }
          });

          this.map.setBounds(bounds);
        } else {
          alert("검색 결과가 없습니다.");
          this.bankList = [];
        }
      });
    },
    searchNearbyBanks() {
      if (!navigator.geolocation) {
        alert("이 브라우저에서는 Geolocation이 지원되지 않습니다.");
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const lat = pos.coords.latitude;
          const lon = pos.coords.longitude;

          const center = new kakao.maps.LatLng(lat, lon);
          this.map.setCenter(center);

          this.searchPlacesByCoordinates(lat, lon, "은행");
        },
        (err) => {
          console.error(`ERROR(${err.code}): ${err.message}`);
          alert("현재 위치를 가져올 수 없습니다.");
        }
      );
    },
    searchPlacesByCoordinates(lat, lon, keyword) {
      this.bankList = []; // 기존 결과 초기화

      this.ps.keywordSearch(
        keyword,
        (data, status) => {
          if (status === kakao.maps.services.Status.OK) {
            const bounds = new kakao.maps.LatLngBounds();

            data.forEach((place) => {
              if (place.category_group_code === "BK9") {
                this.bankList.push(place);
                this.displayMarker(place);
                bounds.extend(new kakao.maps.LatLng(place.y, place.x));
              }
            });

            this.map.setBounds(bounds);
          } else {
            alert("현재 위치 주변에 해당 은행이 없습니다.");
          }
        },
        {
          location: new kakao.maps.LatLng(lat, lon),
          radius: this.searchRadius,
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
  
  .btn-common {
    padding: 10px 20px;
    font-size: 1rem;
    font-weight: bold;
  }
  
  .btn-mint {
    background-color: #51e3d4;
    color: white;
    border: none;
  }
  
  .btn-outline-primary {
    border: 1px solid #51e3d4;
    color: #51e3d4;
    padding: 5px 10px;
    font-size: 0.9rem;
  }
  </style>
  