<template>
    <div class="container mt-5 ai-recommendation">
      <!-- 제목 -->
      <h2 class="mb-4 text-center">
        <span class="highlight">{{ username }}</span>님 맞춤 상품 추천
      </h2>
  
      <!-- 상품 유형 선택 -->
      <div class="row align-items-center mb-4">
        <label class="col-md-2 col-form-label">상품 유형</label>
        <div class="col-md-10 d-flex">
          <button
            v-for="type in productTypes"
            :key="type.value"
            class="btn me-2"
            :class="{ active: selectedType === type.value }"
            @click="selectProductType(type.value)"
          >
            {{ type.label }}
          </button>
        </div>
      </div>
  
      <!-- 가입 기간 선택 -->
      <div class="row align-items-center mb-4">
        <label class="col-md-2 col-form-label">가입 기간</label>
        <div class="col-md-10">
          <input
            type="range"
            class="form-range"
            min="6"
            max="36"
            step="6"
            v-model="selectedDuration"
          />
          <p class="text-center mt-2">가입 기간: {{ selectedDuration }}개월</p>
        </div>
      </div>
  
      <!-- 가입 금액 입력 -->
      <div class="row align-items-center mb-4">
        <label class="col-md-2 col-form-label">가입 금액</label>
        <div class="col-md-10 d-flex align-items-center">
          <button class="btn btn-input me-3" @click="openAmountModal">
            금액 입력하기
          </button>
          <p v-if="selectedAmount" class="mt-2">
            입력 금액: <span class="highlight">{{ selectedAmount }}만원</span>
          </p>
        </div>
      </div>
  
      <!-- 은행 선택 -->
      <div class="row align-items-center mb-4">
        <label class="col-md-2 col-form-label">은행</label>
        <div class="col-md-10">
          <button class="btn btn-input" @click="openBankModal">
            은행 선택하기
          </button>
          <p v-if="selectedBanks.length" class="mt-2">
            선택된 은행: 
            <span v-for="(bank, index) in selectedBanks" :key="bank.code">
              {{ bank.name }}
              <span v-if="index < selectedBanks.length - 1">, </span>
            </span>
          </p>
        </div>
      </div>
  
      <!-- 우대 조건 -->
      <div class="row align-items-center mb-4">
        <label class="col-md-2 col-form-label">우대 조건</label>
        <div class="col-md-10">
          <div class="d-flex flex-wrap">
            <button
              v-for="condition in specialConditions"
              :key="condition"
              class="btn me-2"
              :class="{ active: selectedConditions.includes(condition) }"
              @click="toggleCondition(condition)"
            >
              {{ condition }}
            </button>
          </div>
        </div>
      </div>
  
      <!-- AI 추천 버튼 -->
      <div class="text-center mt-5">
        <button class="btn-common" @click="goRecommendations">
          + AI 추천 받기
        </button>
      </div>
  
      <!-- 더미 결과 -->
      <!-- <div v-if="recommendations.length" class="recommendation-results mt-5">
        <h3>추천 결과</h3>
        <ul>
          <li v-for="(recommendation, index) in recommendations" :key="index">
            {{ recommendation }}
          </li>
        </ul>
      </div> -->
  
      <!-- 금액 입력 모달 -->
      <div
        class="modal fade"
        id="amountModal"
        tabindex="-1"
        aria-labelledby="amountModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="amountModalLabel">가입 금액 입력 (만원)</h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <input
                type="number"
                v-model="selectedAmount"
                class="form-control"
                placeholder="금액을 입력하세요"
              />
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-mint" data-bs-dismiss="modal">
                확인
              </button>
            </div>
          </div>
        </div>
      </div>
  
      <!-- 은행 선택 모달 -->
      <div
        class="modal fade"
        id="bankModal"
        tabindex="-1"
        aria-labelledby="bankModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="bankModalLabel">은행 선택</h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <div class="row">
                <div
                  v-for="bank in banks"
                  :key="bank.code"
                  class="col-4 text-center"
                  @click="toggleBank(bank)"
                >
                  <div :class="{ selected: selectedBanks.includes(bank) }">
                    {{ bank.name }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import { useRouter, useRoute } from "vue-router";

  const router = useRouter()
   
  const username = "김사피"; // 유저 이름 더미 데이터
  const productTypes = [
    { label: "예금", value: "deposit" },
    { label: "적금", value: "savings" },
  ];
  const selectedType = ref("deposit");
  
  const terms = [6, 12, 24, 36];
  const selectedDuration = ref(12);
  
  const selectedAmount = ref(null);
  
  const banks = [
    { name: "우리은행", code: "001" },
    { name: "국민은행", code: "002" },
    { name: "신한은행", code: "003" },
  ];
  const selectedBanks = ref([]);
  
  const specialConditions = [
    "신규 가입",
    "거래 연동",
    "사용 실적",
    "비대면/모바일",
    "마케팅 동의",
    "기타",
  ];
  const selectedConditions = ref([]);
  
  const recommendations = ref([]);
  
  const selectProductType = (type) => {
    selectedType.value = type;
  };
  
  const toggleCondition = (condition) => {
    const index = selectedConditions.value.indexOf(condition);
    if (index > -1) {
      selectedConditions.value.splice(index, 1);
    } else {
      selectedConditions.value.push(condition);
    }
  };
  
  const toggleBank = (bank) => {
    const index = selectedBanks.value.findIndex((b) => b.code === bank.code);
    if (index > -1) {
      selectedBanks.value.splice(index, 1);
    } else {
      selectedBanks.value.push(bank);
    }
  };
  
  const goRecommendations = () => {
    router.push({ name : 'ai-recommendations'})
  };
  </script>
  


  <style scoped>
  .highlight {
    color: var(--mint-color);
    font-weight: bold;
  }
  
  .nav-tabs {
    margin-bottom: 1rem;
  }
  
  .nav-link {
    color: black;
    font-weight: normal;
  }
  
  .nav-link.active {
    font-weight: bold;
    color: var(--orange-color);
  }
  
  .btn {
    padding: 10px 20px;
    border: 1px solid var(--mint-color);
    background-color: white;
    color: var(--mint-color);
    transition: background-color 0.3s ease;
  }
  
  .btn.active,
  .btn:hover {
    background-color: var(--mint-color);
    color: white;
  }
  
  .btn-recommend {
    background-color: var(--green-color);
    color: white;
    padding: 15px 30px;
    font-size: 18px;
  }
  
  .selected {
    font-weight: bold;
    background-color: var(--mint-color);
    color: white;
    border-radius: 8px;
  }
  </style>