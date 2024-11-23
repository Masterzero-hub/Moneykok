<template>
  <div class="container mt-5 ai-recommendation">
    <!-- 제목 -->
    <h2 class="mb-5 text-center">
      <span class="highlight">{{ username }}</span
      >님 맞춤 상품 추천
    </h2>

    <!-- 사용자 입력 영역 -->
    <div style="margin-left: 120px;">
      <!-- 상품 유형 선택 -->
      <div class="row align-items-center mb-5">
        <label class="col-md-2 col-form-label">상품 유형</label>
        <div class="col-md-10 d-flex search-btn">
          <button
            v-for="type in productTypes"
            :key="type.value"
            class="btn me-5"
            :class="{
              'btn-primary': filters.productType === type.value,
              'btn-outline-primary': filters.productType !== type.value,
            }"
            @click="selectProductType(type.value)"
          >
            {{ type.label }}
          </button>
        </div>
      </div>

      <!-- 가입 기간 선택 -->
      <div class="row mb-3 align-items-center mb-5">
        <label class="col-md-2 col-form-label">가입 기간</label>
        <div class="col-md-10">
          <div class="search-btn">
            <button
              v-for="term in terms"
              :key="term"
              class="btn"
              :class="{
                'btn-primary': filters.joinTerm === term,
                'btn-outline-primary': filters.joinTerm !== term,
              }"
              @click="selectDuration(term)"
            >
              {{ term }}개월
            </button>
          </div>
        </div>
      </div>

      <!-- 가입 금액 입력 -->
      <div class="row align-items-center mb-5">
        <label class="col-md-2 col-form-label">가입 금액</label>
        <div class="col-md-10 d-flex align-items-center" style="font-size: 20px;">
          <button
            class="btn-common btn-mint mt-1 mb-1"
            data-bs-toggle="modal"
            data-bs-target="#amountModal"
          >
            금액 입력하기
          </button>
          <p v-if="filters.amount" class="mt-3 ms-3">
            입력 금액: <span class="highlight">{{ filters.amount }}만원</span>
          </p>
        </div>
      </div>

      <!-- 은행 선택 -->
      <div class="row mb-3 align-items-center mb-5">
        <label class="col-md-2 col-form-label">은행 선택</label>
        <div class="col-md-10 d-flex align-items-center" style="font-size: 20px;">
          <button
            class="btn-common btn-mint mt-2 mb-2"
            data-bs-toggle="modal"
            data-bs-target="#bankModal"
          >
            은행 선택하기
          </button>
          <p
            v-if="filters.bank.length > 0"
            class="mt-2 ms-3"
            style="margin-left: 10px; margin-bottom: 10px"
          >
            선택된 은행:
            <span class="highlight" v-for="(bankCode, index) in filters.bank" :key="index">
              {{
                banks.find((bank) => bank.code === bankCode)?.name ||
                "알 수 없는 은행"
              }}<span v-if="index < filters.bank.length - 1">, </span>
            </span>
          </p>
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
        <div class="modal-dialog modal-lg">
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
              <div class="row gy-3">
                <div
                  v-for="bank in banks"
                  :key="bank.name"
                  class="col-6 col-md-4 col-lg-3"
                >
                  <div
                    class="bank-item text-center p-3 shadow-sm rounded"
                    :class="{
                      'selected-bank':
                        filters.bank && filters.bank.includes(bank.code),
                    }"
                    @click="toggleBankSelection(bank.code)"
                  >
                    <img
                      :src="`/bank_image/${bank.code}.jpg`"
                      width="100px"
                      height="100px"
                      :alt="bank.name"
                      class="bank-logo mb-2"
                    />
                    <p class="mb-0">{{ bank.name }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

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
              <h5 class="modal-title" id="amountModalLabel">
                가입 금액 입력 (만원)
              </h5>
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
                v-model="filters.amount"
                class="form-control"
                placeholder="금액을 입력하세요"
              />
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-mint"
                data-bs-dismiss="modal"
              >
                확인
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 우대 조건 -->
      <div class="mb-5">
        <div class="row mb-3 align-items-start">
          <label class="col-md-2 col-form-label mt-2">우대 조건</label>
          <div class="col-md-10">
            <div class="search-btn">
              <button
                v-for="condition in conditions"
                :key="condition"
                class="btn mb-2"
                :class="
                  filters.conditions.includes(condition)
                    ? 'btn-primary'
                    : 'btn-outline-primary'
                "
                @click="selectCondition(condition)"
              >
                {{ condition }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- AI 추천 버튼 -->
    <div class="text-center mt-5">
      <button class="btn-common" @click="goRecommendations">
        AI 추천 받기
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import { useAiStore } from "@/stores/ai";

const store = useAiStore();
const { filters } = storeToRefs(store);
const router = useRouter();

const username = "김사피";

const productTypes = [
  { label: "예금", value: "deposit" },
  { label: "적금", value: "savings" },
];
const terms = [6, 12, 24, 36];
const banks = [
  { name: "우리은행", code: "0010001" },
  { name: "한국스탠다드차드은행", code: "0010002" },
  { name: "아이엠뱅크", code: "0010016" },
  { name: "부산은행", code: "0010017" },
  { name: "광주은행", code: "0010019" },
  { name: "제주은행", code: "0010020" },
  { name: "전북은행", code: "0010022" },
  { name: "경남은행", code: "0010024" },
  { name: "중소기업은행", code: "0010026" },
  { name: "한국산업은행", code: "0010030" },
  { name: "국민은행", code: "0010927" },
  { name: "신한은행", code: "0011625" },
  { name: "농협은행주식회사", code: "0013175" },
  { name: "하나은행", code: "0013909" },
  { name: "주식회사 케이뱅크", code: "0014674" },
  { name: "수협은행", code: "0014807" },
  { name: "카카오뱅크", code: "0015130" },
  { name: "토스뱅크 주식회사", code: "0017801" },
];
const conditions = [
  "신규 가입",
  "거래 연동",
  "사용 실적",
  "비대면/모바일 뱅킹",
  "마케팅 및 기타 동의",
  "기타",
];

// 상품 유형 선택
const selectProductType = (type) => {
  filters.value.productType = type;
};

// 가입 기간 선택
const selectDuration = (term) => {
  filters.value.joinTerm = term;
};

// 가입 금액 입력
const setAmount = (amount) => {
  filters.value.amount = amount;
};

const selectBank = (bankCode) => {
  // 이미 선택된 은행인지 확인
  const index = filters.value.bank.indexOf(bankCode);

  if (index > -1) {
    // 선택된 은행이 이미 포함된 경우: 제거
    filters.value.bank.splice(index, 1);
  } else {
    // 포함되지 않은 경우: 추가
    filters.value.bank.push(bankCode);
  }

  console.log("현재 선택된 은행:", filters.value.bank);
};

const toggleBankSelection = (bankCode) => {
  selectBank(bankCode);
};

// 우대 조건 추가/제거 함수
const selectCondition = (condition) => {
  const index = filters.value.conditions.indexOf(condition);

  // 조건이 이미 포함된 경우: 제거
  if (index > -1) {
    filters.value.conditions.splice(index, 1);
    console.log(filters.value);
  }
  // 조건이 포함되지 않은 경우: 추가
  else {
    filters.value.conditions.push(condition);
    console.log(filters.value);
  }
};

// AI 추천 요청
const goRecommendations = () => {
  console.log("Filters:", filters.value); // 확인용 출력
  router.push({ name: "ai-recommendations" });
};
</script>

<style scoped>
/* 제목 스타일 */
.highlight {
  color: var(--orange-color);
  font-weight: bold;
}

/* 버튼 기본 스타일 */
.btn {
  padding: 10px 20px;
  border: 1px solid var(--mint-color);
  background-color: white;
  color: var(--mint-color);
  border-radius: 8px;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn:hover {
  background-color: var(--mint-color);
  color: white;
}

.bank-item.selected-bank {
  background-color: var(--mint-color); /* 선택된 은행의 배경색 */
  color: white; /* 선택된 텍스트 색상 */
}


/* 우대 조건 버튼 스타일 수정 */
.search-btn {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start; /* 왼쪽 정렬 */
  margin-left: 0; /* 은행 선택 버튼과 일치 */
}

.search-btn .btn {
  margin: 5px; /* 버튼 간격 조정 */
}

/* 호버 시 버튼 스타일 */
.search-btn .btn:hover {
  background-color: var(--mint-color); /* 호버 시 배경색 변경 */
  color: white; /* 호버 시 글자색 변경 */
  border-color: var(--mint-color); /* 호버 시 테두리 색상 변경 */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
}

/* 활성화된 버튼 테두리 색상 */
.search-btn .btn-primary {
  background-color: var(--mint-color);
  color: white;
  border-color: var(--mint-color) !important; /* 활성화 상태 테두리 색상 */
}

/* 비활성화된 버튼 테두리 색상 */
.search-btn .btn-outline-primary {
  border-color: var(--mint-color) !important; /* 비활성화 상태 테두리 색상 */
}
</style>
