<template>
  <div class="container mt-5 ai-recommendation">
    <!-- 제목 -->
    <h2 class="mb-4 text-center">
      <span class="highlight">{{ username }}</span
      >님 맞춤 상품 추천
    </h2>

    <!-- 사용자 입력 영역 -->
    <div style="margin-left: 120px;">
      <!-- 상품 유형 선택 -->
      <div class="row align-items-center mb-5 mt-6">
        <label class="col-md-2 col-form-label">상품 유형</label>
        <div class="col-md-10 d-flex search-btn">
          <button
            v-for="type in productTypesList"
            :key="type.value"
            class="btn me-5"
            :class="{
              'btn-primary': productType === type.value,
              'btn-outline-primary': productType !== type.value,
            }"
            @click="selectProductType(type.value)"
          >
            {{ type.label }}
          </button>
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
import { useUserStore } from "@/stores/user";

const aiStore = useAiStore();
const userStore = useUserStore()

const { productType } = storeToRefs(aiStore);
const router = useRouter();

const username = userStore.name

const productTypesList = [
  { label: "예금", value: "deposits" },
  { label: "적금", value: "savings" },
];


// 상품 유형 선택
const selectProductType = (type) => {
  productType.value = type;
};

// 가입 기간 선택
// const selectDuration = (term) => {
//   filters.value.joinTerm = term;
// };

// 가입 금액 입력
// const setAmount = (amount) => {
//   filters.value.amount = amount;
// };

// const selectBank = (bankCode) => {
//   // 이미 선택된 은행인지 확인
//   const index = filters.value.bank.indexOf(bankCode);

//   if (index > -1) {
//     // 선택된 은행이 이미 포함된 경우: 제거
//     filters.value.bank.splice(index, 1);
//   } else {
//     // 포함되지 않은 경우: 추가
//     filters.value.bank.push(bankCode);
//   }

//   console.log("현재 선택된 은행:", filters.value.bank);
// };

// const toggleBankSelection = (bankCode) => {
//   selectBank(bankCode);
// };

// // 우대 조건 추가/제거 함수
// const selectCondition = (condition) => {
//   const index = filters.value.conditions.indexOf(condition);

//   // 조건이 이미 포함된 경우: 제거
//   if (index > -1) {
//     filters.value.conditions.splice(index, 1);
//     console.log(filters.value);
//   }
//   // 조건이 포함되지 않은 경우: 추가
//   else {
//     filters.value.conditions.push(condition);
//     console.log(filters.value);
//   }
// };

// AI 추천 요청
const goRecommendations = () => {
  // console.log("Filters:", filters.value); // 확인용 출력
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
