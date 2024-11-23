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
              class="btn-small-common"
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
        <h4 class="card-title mt-3">기본 정보</h4>
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
          <strong>우대 조건:   </strong>
          <button
                v-for="condition in productDetail.special_conditions"
                :key="condition"
                class="conditons-btn me-3"
              >
                {{ condition.category }}
              </button>
        </p>
        <p><strong>기타 안내: </strong>{{ productDetail.etc_note }}</p>
        <!-- <pre>{{ productDetail.etc_note }}</pre> -->

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
            <h3 class="cal-rate">
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
              class="option-btn btn-outline-primary"
              :class="{ active: selectedTerm === option.save_trm }"
              @click="selectTerm(option.save_trm)"
            >
              <p class="mb-1">{{ option.save_trm }}개월</p>
              <p class="mb-0">기본 {{ option.intr_rate }}%</p>
            </button>
          </div>

          <!-- 우대 조건 체크 -->
          <div class="mb-4">
            <h4>우대 조건</h4>
            <div
              v-for="condition in productDetail.special_conditions"
              :key="condition.condition_title"
              class="d-flex align-items-center justify-content-between mb-2"
            >
              <p class="mb-0">{{ condition.condition_title }}</p>
              <div>
                <span class="me-2"
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
import { useRoute, useRouter } from "vue-router";
const router = useRouter()
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
  joinAmount,
  // submitJoin
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


const submitJoin = function () {
      if (!joinTerm.value || !joinAmount.value) {
        console.error("가입 기간 또는 가입 금액이 설정되지 않았습니다.");
        alert("가입 기간과 가입 금액을 입력해주세요.");
        return;
      }
    
      console.log(`가입 완료: 기간=${joinTerm.value}개월, 금액=${joinAmount.value}만원`);
      
      // myproduct 경로로 이동
      router.push({ name: 'myproduct' });
    };
</script>




<style scoped>
p {
  font-size: 20px!important; /* 글자 크기 설정 (단위: px, em, rem, %) */
  line-height: 2.0!important; /* 줄 간격 */
}

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

.card-body p {
  margin: 10px 0; /* 줄글 사이에 여백 추가 */
  line-height: 1.6; /* 줄 간격 증가로 가독성 향상 */
  font-size: 16px; /* 글자 크기 조정 */
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
  border-color: var(--mint-color) !important; /* 새로운 테두리 색상 */
  margin-right: 15px;
  color: var(--mint-color)!important;
}

.option-btn.active {
  background-color: var(--mint-color) !important; /* 활성화된 상태에서 배경색 유지 */
  color: white  !important; /* 활성화된 상태에서 텍스트 색상 */
}

/* 호버 시 버튼 스타일 */
.option-btn:hover {
  background-color: var(--mint-color)!important; /* 호버 시 배경색 변경 */
  color: white!important; /* 호버 시 글자색 변경 */
  border-color: var(--mint-color); /* 호버 시 테두리 색상 변경 */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
}

.btn-primary {
  background-color: var(--mint-color)!important;;
  color: white;
  border-color: var(--mint-color) !important; /* 활성화 상태 테두리 색상 */
}

.btn-outline-primary {
  border-color: var(--mint-color) !important; /* 비활성화 상태 테두리 색상 */
}

.conditons-btn {
  background-color: var(--mint-color)!important; /* 기본 배경색: Orange */
  color: white; /* 텍스트 색상 */
  font-size: 18px; /* 폰트 크기 */
  padding: 1px 10px; /* 내부 여백 */
  border: none; /* 테두리 제거 */
  border-radius: 10px; /* 둥근 모서리 */
  white-space: nowrap;
}


input[type="checkbox"] {
  transform: scale(1.8); /* 체크박스 크기를 1.5배로 확대 */
  margin-left: 10px; /* 체크박스와 텍스트 사이 간격 */
}
/* 체크박스가 활성화되었을 때 */
input[type="checkbox"]:checked {
  accent-color: var(--mint-color); /* 원하는 활성화 색상으로 변경 */
}

</style>
