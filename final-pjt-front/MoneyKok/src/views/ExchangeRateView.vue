<template>
    <div>
      <div class="container mt-5">
        <h2 class="mb-4">환율 계산기</h2>
  
        <!-- 변환 방향 선택 -->
        <div class="direction-card p-4 mb-4 shadow-sm">
          <div class="row mb-3 align-items-center">
            <label class="col-md-2 col-form-label">변환 방향</label>
            <div class="col-md-10">
              <div class="search-btn">
                <button
                  class="btn"
                  :class="{ 'btn-primary': direction === 'krwToForeign', 'btn-outline-primary': direction !== 'krwToForeign' }"
                  @click="setDirection('krwToForeign')"
                >
                  원화 → 타국 통화
                </button>
                <button
                  class="btn"
                  :class="{ 'btn-primary': direction === 'foreignToKrw', 'btn-outline-primary': direction !== 'krwToForeign' }"
                  @click="setDirection('foreignToKrw')"
                >
                  타국 통화 → 원화
                </button>
              </div>
            </div>
          </div>
        </div>
  
        <!-- 검색 조건 -->
        <div class="search-card p-4 mb-4 shadow-sm">
          <!-- 상태 선택 -->
          <div class="row mb-3 align-items-center">
            <label class="col-md-2 col-form-label">상태 선택</label>
            <div class="col-md-10">
              <div class="search-btn">
                <button
                  v-for="item in states"
                  :key="item"
                  class="btn"
                  :class="{ 'btn-primary': state === item, 'btn-outline-primary': state !== item }"
                  @click="setState(item)"
                >
                  {{ item }}
                </button>
              </div>
            </div>
          </div>
  
          <!-- 통화 선택 -->
          <div class="row mb-3 align-items-center">
            <label class="col-md-2 col-form-label">타국 통화 선택</label>
            <div class="col-md-10">
              <select v-model="country" class="form-select">
                <option
                  v-for="currency in store.curName.filter(c => c !== '한국 원')" 
                  :key="currency"
                  :value="currency"
                >
                  {{ currency }}
                </option>
              </select>
            </div>
          </div>
        </div>
  
        <!-- 환전 결과 -->
        <div class="result-card p-4 mb-5 shadow-sm">
          <h5 class="mb-3">환전 결과</h5>
  
          <!-- 금액 입력 -->
          <div class="row mb-3 align-items-center">
            <label class="col-md-2 col-form-label">{{ inputLabel }}</label>
            <div class="col-md-10 input-group">
              <input
                type="number"
                v-model="exchangeBefore"
                class="form-control"
                placeholder="금액 입력"
              />
              <span class="input-group-text">{{ inputUnit }}</span>
            </div>
          </div>
  
          <!-- 계산 결과 -->
          <div class="row mb-3 align-items-center">
            <label class="col-md-2 col-form-label">{{ outputLabel }}</label>
            <div class="col-md-10 input-group">
              <input
                type="text"
                :value="formattedExchangeAfter"
                class="form-control result"
                readonly
              />
              <span class="input-group-text">{{ outputUnit }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, onMounted, computed } from "vue";
  import { useExchangeStore } from "@/stores/exchangerate";
  
  // Store 및 데이터 정의
  const store = useExchangeStore();
  const states = ["송금 받을 때", "송금 보낼 때", "매매 기준율"];
  const state = ref("");
  const country = ref("");
  const direction = ref("krwToForeign"); // 변환 방향 (기본: 원화 → 타국 통화)
  const exchangeDetail = ref({});
  const exchangeBefore = ref("");
  const exchangeAfter = ref("조건을 입력해주세요.");
  
  // 변환 방향 설정
  const setDirection = (newDirection) => {
    direction.value = newDirection;
    resetInputs();
  };
  
  // 상태 설정
  const setState = (item) => {
    state.value = state.value === item ? "" : item;
  };
  
  // 통화 선택에 따른 환율 정보 업데이트
  const updateExchangeDetail = () => {
    exchangeDetail.value =
      store.exchangeInfo.find((item) => item.cur_nm === country.value) || {};
    calculateExchange();
  };
  
  // 환율 계산 로직
  const calculateExchange = () => {
    if (!state.value || !country.value || !exchangeBefore.value) {
      exchangeAfter.value = "조건을 입력해주세요.";
      return;
    }
  
    const rateKey =
      state.value === "송금 받을 때"
        ? "ttb"
        : state.value === "송금 보낼 때"
        ? "tts"
        : "deal_bas_r";
  
    const rate = exchangeDetail.value[rateKey]?.replace(",", "");
  
    if (rate) {
      exchangeAfter.value =
        direction.value === "krwToForeign"
          ? Number(exchangeBefore.value) / Number(rate)
          : Number(exchangeBefore.value) * Number(rate);
    } else {
      exchangeAfter.value = "환율 정보를 찾을 수 없습니다.";
    }
  };
  
  // 포맷된 환전 결과
  const formattedExchangeAfter = computed(() =>
    typeof exchangeAfter.value === "number"
      ? new Intl.NumberFormat("ko-KR", {
          style: "currency",
          currency: direction.value === "krwToForeign" ? exchangeDetail.value.cur_unit : "KRW",
        }).format(exchangeAfter.value)
      : exchangeAfter.value
  );
  
  // 데이터 변경 감지
  watch([state, country], updateExchangeDetail);
  watch(exchangeBefore, calculateExchange);
  
  // 라벨 및 단위 설정
  const inputLabel = computed(() =>
    direction.value === "krwToForeign" ? "원화 입력" : "타국 통화 입력"
  );
  const outputLabel = computed(() =>
    direction.value === "krwToForeign" ? "타국 통화 결과" : "원화 결과"
  );
  const inputUnit = computed(() =>
    direction.value === "krwToForeign" ? "KRW" : exchangeDetail.value.cur_unit
  );
  const outputUnit = computed(() =>
    direction.value === "krwToForeign" ? exchangeDetail.value.cur_unit : "KRW"
  );
  
  // 입력 초기화
  const resetInputs = () => {
    exchangeBefore.value = "";
    exchangeAfter.value = "조건을 입력해주세요.";
  };
  
  // Store 데이터 로드
  onMounted(() => {
    store.getExchangeInfo();
  });
  </script>
  
  <style scoped>
  .search-card,
  .result-card,
  .direction-card {
    background-color: #fff;
    border: 1px solid #cacaca;
    border-radius: 8px;
    padding: 20px;
  }
  
  .search-btn .btn {
    border-color: var(--mint-color) !important;
    margin-right: 15px;
    color: var(--mint-color);
  }
  
  .search-btn .btn:hover {
    background-color: var(--mint-color);
    color: white;
    border-color: var(--mint-color) !important;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .search-btn .btn-primary {
    background-color: var(--mint-color);
    color: white;
    border-color: var(--mint-color) !important;
  }
  
  .search-btn .btn-outline-primary {
    border-color: var(--mint-color) !important;
  }

  .input-group-text {
    color: var(--orange-color);
  }

  /* .result {
    font-weight: bolder;
  } */
  </style>
  