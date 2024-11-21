<template>
  <div>
    <div class="container mt-5">
      <h2 class="mb-4">예금 상품 조회</h2>
      <!-- 검색 조건 -->
      <div class="search-card p-4 mb-5 shadow-sm">
        <h5 class="mb-4">검색 조건</h5>

        <!-- 가입 기간 -->
        <div class="row mb-3 align-items-center">
          <label class="col-md-2 col-form-label">가입 기간</label>
          <div class="col-md-10">
            <div class="btn-group">
              <button
                v-for="term in terms"
                :key="term"
                class="btn"
                :class="filters.term === term ? 'btn-primary' : 'btn-outline-primary'"
                @click="setTerm(term)"
              >
                {{ term }}
              </button>
            </div>
          </div>
        </div>

        <!-- 가입 금액 -->
        <div class="row mb-3 align-items-center">
          <label class="col-md-2 col-form-label">가입 금액</label>
          <div class="col-md-10">
            <button
              class="btn btn-success btn-block"
              data-bs-toggle="modal"
              data-bs-target="#amountModal"
            >
              가입 금액 입력하기
            </button>
            <p v-if="filters.amount" class="mt-2">
              입력 금액: {{ filters.amount.toLocaleString() }}원
            </p>
          </div>
        </div>

        <!-- 가입 금액 입력 모달 -->
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
                  가입 금액 입력
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
                  placeholder="가입 금액을 입력하세요"
                />
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-success"
                  data-bs-dismiss="modal"
                >
                  확인
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 은행 선택 -->
        <div class="row mb-3 align-items-center">
          <label class="col-md-2 col-form-label">은행 선택</label>
          <div class="col-md-10">
            <button
              class="btn btn-success btn-block"
              data-bs-toggle="modal"
              data-bs-target="#bankModal"
            >
              은행 선택하기
            </button>
            <p v-if="filters.bank" class="mt-2">
              선택된 은행: {{ filters.bank }}
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
                <div class="list-group">
                  <button
                    v-for="bank in banks"
                    :key="bank"
                    class="list-group-item list-group-item-action"
                    @click="selectBank(bank)"
                    data-bs-dismiss="modal"
                  >
                    {{ bank }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 우대 조건 -->
        <div>
          <div class="d-flex gap-2 flex-wrap" style="align-items: center;">
            <h6 class="mb-0" style="margin-right: 70px;">우대 조건</h6>
            <button
              v-for="condition in conditions"
              :key="condition"
              class="btn"
              :class="filters.conditions.includes(condition) ? 'btn-primary' : 'btn-outline-primary'"
              @click="toggleCondition(condition)"
            >
              {{ condition }}
            </button>
          </div>
        </div>
      </div>

      <!-- 상품 목록 -->
      <div class="row">
        <div
          class="col-12 mb-4"
          v-for="product in products"
          :key="product.id"
        >
          <div
            class="card shadow-sm p-3 bg-white rounded d-flex flex-row align-items-center"
          >
            <!-- 로고 -->
            <div class="logo-container me-3">
              <img
                :src="`/bank_image/${product.bank.fin_co_no}.jpg`"
                alt="Bank Logo"
                class="rounded-circle"
              />
            </div>

            <!-- 상품 정보 -->
            <div class="flex-grow-1">
              <h5 class="mb-1">{{ product.fin_prdt_nm }}</h5>
              <div class="d-flex align-items-center">
                <span
                  v-for="(category, index) in [
                    ...new Set(
                      product.special_conditions.map((cond) => cond.category)
                    ),
                  ]"
                  :key="index"
                  class="special_conditions"
                >
                  {{ category }}
                </span>
              </div>
            </div>

            <!-- 금리 및 버튼 -->
            <div class="d-flex align-items-center">
              <div class="text-center me-3">
                <p class="mb-0">기본</p>
                <strong>
                  {{
                    product.options.length > 0
                      ? product.options[product.options.length - 1].intr_rate
                      : "N/A"
                  }}%
                </strong>
              </div>
              <div class="text-center me-3">
                <p class="mb-0">최고</p>
                <strong>
                  {{
                    product.options.length > 0
                      ? product.options[product.options.length - 1].intr_rate2
                      : "N/A"
                  }}%
                </strong>
              </div>
              <div class="divider me-3"></div>
              <button
                class="btn-small-common"
                @click="goDepositDetail(product.id)"
              >
                비교하기 +
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useDepositsStore } from "@/stores/deposits";
import { onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";

const store = useDepositsStore();
const { products, getProducts, productDetail, filters, filteredProducts } =
  storeToRefs(store);
const router = useRouter();

onMounted(() => {
  getProducts();
});

const goDepositDetail = function (product_id) {
  router.push({ name: "depositdetail", params: { deposit_id: product_id } });
};

// 가입 기간, 은행 목록, 우대 조건 목록 정의
const terms = ["6개월", "12개월", "24개월", "36개월"];
const banks = ["국민은행", "우리은행", "신한은행", "하나은행", "카카오뱅크"];
const conditions = [
  "신규 가입",
  "거래 연동",
  "사용 실적",
  "비대면/모바일",
  "마케팅 동의",
  "기타",
];

console.log(filters);


const setTerm = (term) => {
  filters.term = term;
};

const selectBank = (bank) => {
  filters.bank = bank;
};

// 우대 조건 추가/제거 함수
const toggleCondition = (condition) => {
  const index = filters.value.conditions.indexOf(condition);

  // 조건이 이미 포함된 경우: 제거
  if (index > -1) {
    filters.value.conditions.splice(index, 1);
    console.log(filters.value.conditions)
  } 
  // 조건이 포함되지 않은 경우: 추가
  else {
    filters.value.conditions.push(condition);
    console.log(filters.value.conditions)
  }
};

// 필터 변경 사항 확인
watch(
  () => filters,
  (newFilters) => {
    console.log("현재 필터 상태:", newFilters);
  },
  { deep: true }
);
</script>



<style scoped>
.search-card {
  background-color: #fff; /* 배경색 */
  border: 1px solid #cacaca; /* 테두리 */
  border-radius: 8px; /* 둥근 모서리 */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
  transition: box-shadow 0.3s ease, transform 0.3s ease; /* 전환 효과 */
  padding: 20px; /* 내부 여백 */
}

.search-card:hover {
  box-shadow: none; /* 검색 조건 카드 호버 효과 제거 */
  transform: none; /* 호버 확대 효과 제거 */
}


.card {
  width: 100%;
}

.card:hover {
  box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.2); /* 호버 시 그림자 강조 */
  transform: scale(1.02); /* 호버 시 살짝 확대 */
}

.logo-container img {
  width: 60px;
  height: 60px;
}

.divider {
  width: 1px;
  height: 40px;
  background-color: #ddd;
}

.card h5 {
  font-size: 1.25rem;
}

.special_conditions {
  /* display: inline-block; 블록 요소처럼 표시 */
  background-color: var(--mint-color); /* 기본 배경색: Orange */
  color: white; /* 텍스트 색상 */
  /* font-weight: bold; 굵은 글씨 */
  font-size: 17px; /* 폰트 크기 */
  padding: 2px 10px; /* 내부 여백 */
  border: none; /* 테두리 제거 */
  margin-right: 5px;
  border-radius: 10px; /* 둥근 모서리 */
  transition: all 0.3s ease; /* 부드러운 전환 효과 */
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
  text-align: center; /* 텍스트 가운데 정렬 */
  pointer-events: none; /* 버튼 기능 제거 */
}
</style>
