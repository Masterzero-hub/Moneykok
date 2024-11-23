<template>
  <div class="container mt-5">
    <div v-if="productDetail && productDetail.options">
    <!-- 데이터 로드 완료 -->
    <div class="card">
      <!-- Header Section -->
      <div class="card-header">
          <!-- Left Section: 로고와 상품명 -->
          <div class="card-header-left">
            <img
              :src="`/bank_image/${productDetail.bank.fin_co_no}.jpg`"
              alt="Bank Logo"
              class="logo-img rounded-circle"
            />
            <h2 class="mb-0">{{ productDetail.fin_prdt_nm }}</h2>
          </div>

          <!-- Right Section: 가입하기 버튼 -->
          <div>
            <button
              class="btn btn-primary"
              data-bs-toggle="modal"
              data-bs-target="#joinModal"
            >
              가입하기
            </button>
          </div>
        </div>

        <!-- 가입하기 모달 -->
    <div
      class="modal fade"
      id="joinModal"
      tabindex="-1"
      aria-labelledby="joinModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="joinModalLabel">가입하기</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <!-- 가입 기간 선택 -->
            <div class="mb-3">
              <label for="termSelect" class="form-label">가입 기간</label>
              <select
                id="termSelect"
                class="form-select"
                v-model="joinTerm"
              >
                <option v-for="term in terms" :key="term" :value="term">
                  {{ term }}개월
                </option>
              </select>
            </div>

            <!-- 가입 금액 입력 -->
            <div class="mb-3">
              <label for="amountInput" class="form-label">가입 금액 (만원)</label>
              <input
                type="number"
                id="amountInput"
                v-model="joinAmount"
                class="form-control"
                placeholder="가입 금액을 입력하세요"
              />
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              취소
            </button>
            <button
              type="button"
              class="btn btn-primary"
              data-bs-dismiss="modal"
              @click="submitJoin"
            >
              입력하기
            </button>
          </div>
        </div>
      </div>
    </div>



      <div class="card-body">
        <!-- 기본 정보 -->
        <h4 class="card-title">기본 정보</h4>
        <p><strong>상품 코드:</strong> {{ productDetail.fin_prdt_cd }}</p>
        <p><strong>가입 대상:</strong> {{ productDetail.join_member }}</p>
        <div v-if="productDetail.join_deny === 1">
          <p>
            <strong>가입 제한:</strong>
            {{ joinDenyContent(productDetail.join_deny) }}
          </p>
        </div>
        <p><strong>가입 방법:</strong> {{ productDetail.join_way }}</p>
        <p>
          <strong>우대 조건:</strong>
          <button
                v-for="condition in productDetail.special_conditions"
                :key="condition"
                class="condition-buttons"
                :class="
                  filters.conditions.includes(condition)
                    ? 'btn-primary'
                    : 'btn-outline-primary'
                "
              >
                {{ condition.category }}
              </button>
        </p>
        <p><strong>기타 안내:</strong></p>
        <pre>{{ productDetail.etc_note }}</pre>

        <!-- 가입 불가 여부 -->
        <!-- <div v-if="productDetail.join_deny === 1" class="alert alert-danger" role="alert">
              <strong>주의:</strong> 이 상품은 가입이 제한되어 있습니다.
            </div> -->

        <!-- 옵션 테이블 -->
        <!-- <h5 class="mt-4">이자율 정보</h5>
          <table class="table table-striped">
            <thead>
              <tr>
                <th>저축 기간 (개월)</th>
                <th>이율 (기본)</th>
                <th>이율 (우대)</th>
                <th>이자 계산 방식</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="option in productDetail.options" :key="option.id">
                <td>{{ option.save_trm }}</td>
                <td>{{ option.intr_rate }}%</td>
                <td>{{ option.intr_rate2 }}%</td>
                <td>{{ option.intr_rate_type_nm }}</td>
              </tr>
            </tbody>
          </table> -->
        <div class="container mt-5">
          <hr />
          <h2 class="text-center mb-4 mt-5">이자 계산기</h2>

          <!-- 선택된 금리 정보 -->
          <div class="text-center mb-4">
            <h3 class="text-success">
              {{ calculatedInterestRate.toFixed(2) }}%
            </h3>
            <p class="text-muted">
              <span>기본 {{ baseInterestRate }}%</span>
              <span v-if="selectedConditions.length > 0">
                + 우대 {{ additionalRate.toFixed(2) }}%
              </span>
            </p>
          </div>
          <!-- 개월 수 선택 -->
          <div class="d-flex justify-content-center gap-3 flex-wrap mb-4">
            <button
              v-for="option in productDetail.options"
              :key="option.id"
              class="btn-outline-primary"
              :class="{ active: selectedTerm === option.save_trm }"
              @click="selectTerm(option.save_trm)"
            >
              <p class="mb-1">{{ option.save_trm }}개월</p>
              <p class="mb-0">기본 {{ option.intr_rate }}%</p>
            </button>
          </div>

          <!-- 우대 조건 체크 -->
          <div class="mb-4">
            <h5>우대 조건</h5>
            <div
              v-for="condition in productDetail.special_conditions"
              :key="condition.condition_title"
              class="d-flex align-items-center justify-content-between mb-2"
            >
              <p class="mb-0">{{ condition.condition_title }}</p>
              <div>
                <span class="me-2 text-primary"
                  >+{{ condition.prime_rate }}%</span
                >
                <input
                  type="checkbox"
                  :value="condition"
                  v-model="selectedConditions"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- 총 이자율 계산 결과 -->
        <!-- <div class="text-center">
        <h5 class="text-secondary">
          총 이자율: {{ calculatedRate.toFixed(2) }}%
        </h5>
      </div> -->
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
import { onMounted, ref, computed } from "vue";
import { storeToRefs } from "pinia";
import { useRoute } from "vue-router";
const route = useRoute();
const depositCode = route.params.deposit_code;
const store = useDepositsStore();
const {
  products,
  productDetail,
  filters,
  filteredProducts,
  getProducts,
  getProductDetail,
  getFilteredProducts,
  joinTerm,
  joinAmount
} = storeToRefs(store);


// 가입 가능 기간 목록
const terms = [6, 12, 24, 36];
// 가입 상태 변수


onMounted(() => {
  store.getProductDetail(depositCode);
  console.log(productDetail.value);
});

const joinDenyContent = function (num) {
  if (num == 1) {
    return "제한 사항 없음";
  }
};

// 상태
const selectedTerm = ref(null); // 선택된 저축 기간
const selectedConditions = ref([]); // 선택된 우대 조건

// 계산된 값
const baseInterestRate = computed(() => {
  const option = productDetail.value.options.find(
    (opt) => opt.save_trm === selectedTerm.value
  );
  return option ? option.intr_rate : 0; // 선택된 기간의 기본 이율
});

const additionalRate = computed(() =>
  selectedConditions.value.reduce((total, cond) => total + cond.prime_rate, 0)
);

const calculatedInterestRate = computed(() => {
  return baseInterestRate.value + additionalRate.value; // 총 이자율 계산
});

// 메서드
const selectTerm = (term) => {
  selectedTerm.value = term; // 선택된 기간 설정
  selectedConditions.value = []; // 조건 초기화
};
</script>




<style scoped>
/* 카드 스타일 */
.card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

/* 헤더 스타일 */
.card-header {
  display: flex;
  justify-content: space-between; /* 왼쪽과 오른쪽 공간 나누기 */
  align-items: center; /* 세로축 가운데 정렬 */
  padding: 15px 20px; /* 여백 설정 */
  border-bottom: 1px solid #ddd; /* 카드 헤더 하단 구분선 */
}

.card-header-left {
  display: flex;
  align-items: center; /* 로고와 상품명을 세로 정렬 */
  gap: 10px; /* 로고와 상품명 간격 */
}

/* 은행명 스타일 */
.bank {
  font-size: 25px;
  font-weight: 400;
  text-align: right; /* 오른쪽 정렬 */
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

.card p {
  margin: 0;
}

.condition-buttons {
  margin: 0px 10px;
  font-size: 15px;
}


/* 버튼 스타일 */
.btn-outline-primary {
  border-width: 2px;
}
</style>
