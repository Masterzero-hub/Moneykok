<template>
  <div class="container mt-5">
    <div v-if="productDetail && productDetail.options">
      <div class="card">
        <div class="card-header">
          <!-- 로고와 상품명 -->
          <div class="card-header-left">
            <img :src="`/bank_image/${productDetail.bank.fin_co_no}.jpg`" alt="Bank Logo"
              class="logo-img rounded-circle" />
            <h2 class="mb-0">{{ productDetail.fin_prdt_nm }}</h2>
          </div>
        </div>

        <div class="card-body">
          <!-- 기본 정보 -->
          <h4 class="card-title mt-3">기본 정보</h4>
          <p><strong>상품 코드:</strong> {{ productDetail.fin_prdt_cd }}</p>
          <p><strong>가입 대상:</strong> {{ productDetail.join_member }}</p>
          <p><strong>가입 방법:</strong> {{ productDetail.join_way }}</p>
          <p>
            <strong>가입 한도:</strong>
            (최저)
            {{ productDetail.deposit_min_amount !== null ? productDetail.deposit_min_amount+'만원' : '제한 없음' }}
            (최고)
            {{ productDetail.deposit_max_amount !== null ? productDetail.deposit_max_amount+'만원' : '제한 없음' }}
          </p>
          <p>
            <strong>우대 조건: </strong>
            <button v-for="condition in [
              ...new Set(
                productDetail.special_conditions.map((cond) => cond.category)
              ),
            ]" :key="condition" class="conditons-btn me-3">
              {{ condition }}
            </button>
          </p>
          <p><strong>기타 안내: </strong>{{ productDetail.etc_note }}</p>
          <p><strong>우대 조건 안내: </strong>{{ productDetail.processed_spcl_cnd }}</p>

          <!-- 이자율 계산기 -->
          <div class="container mt-5">
            <hr />
            <h2 class="text-center mb-4 mt-5">이자 계산기</h2>

            <!-- 선택된 금리 정보 -->
            <div class="text-center mb-4">
              <h3 class="cal-rate">
                {{ calculatedRate.toFixed(2) }}%
              </h3>
              <p class="text-muted">
                <span>기본 {{ baseInterestRate }}%</span>
                <span v-if="joinConditions.length > 0">
                  + 우대 {{ additionalRate.toFixed(2) }}%
                </span>
              </p>
            </div>

            <!-- 저축 기간 선택 -->
            <div class="d-flex justify-content-center gap-3 flex-wrap mb-4">
              <button v-for="option in productDetail.options" :key="option.id" class="option-btn btn-outline-primary"
                :class="{ active: joinTerm === option.save_trm }" @click="selectJoinTerm(option.save_trm)">
                <p class="mb-1">{{ option.save_trm }}개월</p>
                <p class="mb-0">기본 {{ option.intr_rate }}%</p>
              </button>
            </div>

            <!-- 우대 조건 체크 -->
            <div class="mb-4">
              <h4>우대 조건</h4>
              <div v-for="condition in productDetail.special_conditions" :key="condition.condition_content"
                class="d-flex align-items-center justify-content-between mb-2">
                <p class="mb-0">{{ condition.condition_content }}</p>
                <div>
                  <span class="me-2">+{{ condition.prime_rate }}%</span>
                  <input type="checkbox" :value="condition" v-model="joinConditions" />
                </div>
              </div>
            </div>

            <!-- 가입 금액 입력 및 가입하기 버튼 -->
            <div class="d-flex justify-content-center align-items-center mt-4">
              <input v-model="joinAmount" type="number" class="form-control me-3" placeholder="가입 금액 (만원)"
                style="max-width: 200px;" />
              <button class="btn-small-common btn-mint" @click="handleJoin">
                가입하기
              </button>
            </div>
          </div>





        </div>
      </div>
    </div>

    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>



<script setup>
import { useDepositsStore } from "@/stores/deposits";
import { useUserStore } from "@/stores/user";
import { onMounted, ref, computed, watch } from "vue";
import { storeToRefs } from "pinia";
import { useRoute, useRouter } from "vue-router";
const router = useRouter();
const route = useRoute();
const depositCode = route.params.deposit_code;
const depositStore = useDepositsStore();
const userStore = useUserStore();
const {
  products,
  productDetail,
  filters,
  filteredProducts,
  getProducts,
  getProductDetail,
  getFilteredProducts,
  joinTerm,
  joinAmount,
  finalJoinRate,
  joinConditions,
  resetState,
  joinProduct
} = storeToRefs(depositStore);

const { isLogin } = storeToRefs(userStore)

// 가입 가능 기간 목록
const terms = [6, 12, 24, 36];
// 가입 상태 변수

onMounted(() => {
  depositStore.getProductDetail(depositCode);
  depositStore.resetState();
  console.log(productDetail.value);
});


// 가입 조건 상태 초기화
watch(
  () => route.params.deposit_code,
  (newDepositCode) => {
    depositStore.resetState(); // 상태 초기화
    depositStore.getProductDetail(newDepositCode); // 새로운 상품 상세 데이터 요청
  }
);


const joinDenyContent = function (num) {
  if (num == 1) {
    return "제한 사항 없음";
  }
};


// 기본 이율 계산
const baseInterestRate = computed(() => {
  const option = productDetail.value?.options?.find(
    (opt) => opt.save_trm === joinTerm.value
  );
  return option ? option.intr_rate : 0;
});

// 추가 우대 이율 계산
const additionalRate = computed(() =>
  joinConditions.value.reduce((total, cond) => total + cond.prime_rate, 0)
);

// 최종 이자율을 실시간 반영 (vue에서 처리)
const calculatedRate = computed({
  get() {
    return parseFloat(baseInterestRate.value) + parseFloat(additionalRate.value);
  },
  set(value) {
    finalJoinRate.value = parseFloat(value.toFixed(2)); // 문자열을 숫자로 변환
  },
});

// 실시간 finalJoinRate 업데이트
watch(
  [baseInterestRate, additionalRate],
  ([newBase, newAdditional]) => {
    finalJoinRate.value = parseFloat((newBase + newAdditional).toFixed(2)); // 소수점 둘째 자리로 변환
  },
  { immediate: true } // 초기 값도 반영
);


// 가입 기간 선택
const selectJoinTerm = (term) => {
  joinTerm.value = term;
};


// 가입 처리
const handleJoin = () => {
  if (isLogin.value == false) {
    // 로그인 여부 확인
    alert("로그인이 필요합니다.");
    router.push({ name: "login" }); // 로그인 페이지로 이동
    return;
  }


  if (!joinTerm.value || !joinAmount.value) {
    alert("가입 기간과 가입 금액을 입력해주세요.");
    return;
  }
  // 최종 이자율 저장
  finalJoinRate.value = calculatedRate.value; // 변경된 변수명 사용

  depositStore.joinProduct(depositCode);
  console.log(
    `가입 완료: 기간=${joinTerm.value}개월, 금액=${joinAmount.value}만원, 이자율=${finalJoinRate.value}%`
  );
  alert('상품 가입이 완료되었습니다.')

  // 페이지 이동
  router.push({ name: "myproduct" });
};
</script>



<style scoped>
/* 카드 스타일 */
.card {
  /* transition 속성 제거 */
  transform: none;
  /* 호버 시 크기 변화를 없앰 */
  box-shadow: none;
  /* 호버 시 그림자 효과를 없앰 */
}

/* 체크박스 스타일 */
.checkbox-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

input[type="checkbox"] {
  transform: scale(1.2);
}

.bonus-rate {
  color: var(--mint-color);
  font-weight: bold;
  margin-left: auto;
}

p {
  font-size: 20px !important;
  /* 글자 크기 설정 (단위: px, em, rem, %) */
  line-height: 2 !important;
  /* 줄 간격 */
}

/* 카드 스타일 */
.card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

/* 헤더 스타일 */

.card-header {
  display: flex;
  justify-content: space-between;
  /* 왼쪽과 오른쪽 공간 나누기 */
  align-items: center;
  /* 세로축 가운데 정렬 */
  padding: 15px 20px;
  /* 여백 설정 */
  border-bottom: 1px solid #ddd;
  /* 카드 헤더 하단 구분선 */
}

.card-header-left {
  display: flex;
  align-items: center;
  /* 로고와 상품명을 세로 정렬 */
  gap: 10px;
  /* 로고와 상품명 간격 */
}

/* 은행명 스타일 */
.bank {
  font-size: 25px;
  font-weight: 400;
  text-align: right;
  /* 오른쪽 정렬 */
}

/* 로고 스타일 */
.logo-img {
  margin-right: 10px;
  width: 42px;
  height: 42px;
}

/* 상품명 스타일 */
.card h5 {
  font-size: 1.1rem;
  margin: 0;
}

.card-body p {
  margin: 10px 0;
  /* 줄글 사이에 여백 추가 */
  line-height: 1.6;
  /* 줄 간격 증가로 가독성 향상 */
  font-size: 16px;
  /* 글자 크기 조정 */
}

.card p {
  margin: 0;
}

.condition-buttons {
  margin: 0px 10px;
  font-size: 15px;
}

.cal-rate {
  color: var(--orange-color);
  font-weight: bolder;
}

/* 버튼 스타일 */
.option-btn {
  border-color: var(--mint-color) !important;
  /* 새로운 테두리 색상 */
  margin-right: 15px;
  color: var(--mint-color) !important;
  background-color: inherit;
}

.option-btn.active {
  background-color: var(--mint-color) !important;
  /* 활성화된 상태에서 배경색 유지 */
  color: white !important;
  /* 활성화된 상태에서 텍스트 색상 */
}

/* 호버 시 버튼 스타일 */
.option-btn:hover {
  background-color: var(--mint-color) !important;
  /* 호버 시 배경색 변경 */
  color: white !important;
  /* 호버 시 글자색 변경 */
  border-color: var(--mint-color);
  /* 호버 시 테두리 색상 변경 */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  /* 그림자 효과 */
}

.btn-primary {
  background-color: var(--mint-color) !important;
  color: white;
  border-color: var(--mint-color) !important;
  /* 활성화 상태 테두리 색상 */
}

.btn-outline-primary {
  border-color: var(--mint-color) !important;
  /* 비활성화 상태 테두리 색상 */
}

.conditons-btn {
  background-color: var(--orange-color) !important;
  /* 기본 배경색: Orange */
  color: white;
  /* 텍스트 색상 */
  font-size: 18px;
  /* 폰트 크기 */
  padding: 1px 10px;
  /* 내부 여백 */
  border: none;
  /* 테두리 제거 */
  border-radius: 10px;
  /* 둥근 모서리 */
  white-space: nowrap;
}

input[type="checkbox"] {
  transform: scale(1.8);
  /* 체크박스 크기를 1.5배로 확대 */
  margin-left: 10px;
  /* 체크박스와 텍스트 사이 간격 */
}

/* 체크박스가 활성화되었을 때 */
input[type="checkbox"]:checked {
  accent-color: var(--mint-color);
  /* 원하는 활성화 색상으로 변경 */
}
</style>
