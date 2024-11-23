<template>
  <div>
    <div class="container mt-5">
      <h2 class="mb-4">예금 상품 조회</h2>

      <!-- 검색 조건 -->
      <div class="search-card p-4 mb-5 shadow-sm">
        <!-- 1. 가입 기간 -->
        <div class="row mb-3 align-items-center">
          <label class="col-md-2 col-form-label">가입 기간</label>
          <div class="col-md-10">
            <div class="search-btn">
              <button
                v-for="term in terms"
                :key="term"
                class="btn"
                :class="
                  filters.join_term === term
                    ? 'btn-primary'
                    : 'btn-outline-primary'
                "
                @click="selectTerm(term)"
              >
                {{ term }}개월
              </button>
            </div>
          </div>
        </div>

        <!-- 2. 가입 금액 -->
        <div class="row mb-3 align-items-center">
          <label class="col-md-2 col-form-label">가입 금액</label>
          <div class="col-md-10 d-flex align-items-center">
            <button
              class="btn-small-common btn-mint"
              data-bs-toggle="modal"
              data-bs-target="#amountModal"
            >
              가입 금액 입력하기
            </button>
            <p
              v-if="filters.amount"
              class="mt-2"
              style="margin-left: 10px; margin-bottom: 10px"
            >
              입력 금액:
              <span class="highlight">{{
                filters.amount.toLocaleString()
              }}</span>
              만원
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
                  placeholder="가입 금액을 입력하세요"
                />
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn-small-common btn-mint"
                  data-bs-dismiss="modal"
                >
                  확인
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. 은행 선택 -->
        <div class="row mb-3 align-items-center">
          <label class="col-md-2 col-form-label">은행 선택</label>
          <div class="col-md-10 d-flex align-items-center">
            <button
              class="btn-small-common btn-mint"
              data-bs-toggle="modal"
              data-bs-target="#bankModal"
            >
              은행 선택하기
            </button>
            <p
              v-if="filters.bank.length > 0"
              class="mt-2"
              style="margin-left: 10px; margin-bottom: 10px"
            >
              선택된 은행:
              <span
                v-for="(bankCode, index) in filters.bank"
                :key="index"
                class="highlight"
              >
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

        <!-- 4. 우대 조건 -->
        <div class="row align-items-start mb-3">
          <label class="col-md-2 col-form-label mt-2">우대 조건</label>
          <div class="col-md-10">
            <div class="search-btn">
              <button
                v-for="condition in conditions"
                :key="condition"
                class="btn"
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


      <!-- 상품 목록 -->
      <div class="row">
        <div
          class="col-12 mb-4"
          v-for="product in paginatedProducts"
          :key="product.id"
        >
          <div
            class="card shadow-sm p-3 bg-white rounded d-flex flex-row align-items-center"
            @click="goDepositDetail(product.fin_prdt_cd)"
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
              <!-- 상품 이름과 은행명 -->
              <div class="d-flex align-items-center">
                <h5 class="mb-0" style="font-size: 30px">
                  {{ product.fin_prdt_nm }}
                </h5>
                <div class="divider mx-3"></div>
                <!-- 세로선 -->
                <p class="mb-0 text-muted">{{ product.bank.kor_co_nm }}</p>
              </div>

              <!-- 우대조건 -->
              <div class="d-flex align-items-center mt-2">
                <div v-if="product.special_conditions">
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
            </div>

            <!-- 금리 -->
            <div
              class="interest-info d-flex justify-content-around align-items-center"
            >
              <!-- 기본 금리 -->
              <div class="interest-item text-center">
                <p class="interest-title">기본 금리</p>
                <strong class="interest-rate">
                  {{ getInterestRate(product.options, "intr_rate") }}%
                </strong>
                <p class="interest-term">
                  <small>{{ `${getSaveTrm(product.options)}개월 기준` }}</small>
                </p>
              </div>

              <!-- 최고 금리 -->
              <div class="interest-item text-center">
                <p class="interest-title">최고 금리</p>
                <strong class="interest-rate">
                  {{ getInterestRate(product.options, "intr_rate2") }}%
                </strong>
                <p class="interest-term">
                  <small>{{ `${getSaveTrm(product.options)}개월 기준` }}</small>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 페이지네이션 -->
      <nav class="mt-4">
        <ul class="pagination justify-content-center">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link" @click="changePage(currentPage - 1)">
              &laquo;
            </button>
          </li>
          <li
            v-for="page in totalPages"
            :key="page"
            class="page-item"
            :class="{ active: currentPage === page }"
          >
            <button class="page-link" @click="changePage(page)">
              {{ page }}
            </button>
          </li>
          <li
            class="page-item"
            :class="{ disabled: currentPage === totalPages }"
          >
            <button class="page-link" @click="changePage(currentPage + 1)">
              &raquo;
            </button>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script setup>
import { useDepositsStore } from "@/stores/deposits";
import { onMounted, ref, watch, computed } from "vue";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";

const store = useDepositsStore();
const {
  products,
  getProducts,
  productDetail,
  filters,
  filteredProducts,
  getFilteredProducts,
} = storeToRefs(store);
const router = useRouter();


// ----- 초기 렌더링 -----
onMounted(() => {
  store.getProducts();
  console.log(products);
});


// ----- 검색 조건에 따른 필터링 -----
// 검색조건 (가입 기간, 은행 목록, 우대 조건) 목록 정의
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

// 검색 조건 설정 로직
const selectTerm = (term) => {
  store.filters.join_term = store.filters.join_term === term ? null : term;
  console.log(filters.value);
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

// 검색 조건 
const filteredFilters = computed(() => ({
  join_term: filters.value.join_term,
  amount: filters.value.amount,
  bank: filters.value.bank,
  conditions: filters.value.conditions,
}));

// 검색 조건 변경 시 getFilteredProducts 호출
watch(
  filteredFilters,
  (newFilters) => {
    console.log("필터 변경 감지:", newFilters);
    store.getFilteredProducts(); // getFilteredProducts 호출
    console.log(filteredProducts);
  },
  { deep: true, immediate: true } // 깊은 감시 및 즉시 실행
);

// 사용자가 선택한 필터에 따라 표시할 상품 계산
const displayedProducts = computed(() => {
  // 필터가 적용되지 않은 경우: 전체 상품 표시
  if (
    !filters.value.join_term &&
    !filters.value.amount &&
    filters.value.bank.length === 0 &&
    filters.value.conditions.length === 0
  ) {
    return products.value;
  }
  // 필터가 적용된 경우: 필터링된 상품 표시
  return filteredProducts.value;
});


// ----- 개별 상품 관련 -----
// 상세페이지 이동
const goDepositDetail = function (product_code) {
  router.push({
    name: "depositdetail",
    params: { deposit_code: product_code },
  });
};

// 대표 금리 처리 (12개월 기준, 12개월 옵션 없으면 가장 긴 기간 금리 기준)
const getInterestRate = (options, field) => {
  if (!options || options.length === 0) {
    return "N/A";
  }
  // save_trm이 12인 항목 찾기
  const target = options.find((option) => option.save_trm === 12);
  // save_trm이 12인 데이터가 있으면 해당 필드 반환, 없으면 마지막 항목 기준
  return target ? target[field] : options[options.length - 1][field];
};

// 대표 금리 기간 처리 
const getSaveTrm = (options) => {
  if (!options || options.length === 0) {
    return null;
  }
  // save_trm이 12인 항목 찾기
  const target = options.find((option) => option.save_trm === 12);
  // save_trm이 12인 데이터가 있으면 해당 save_trm 반환, 없으면 마지막 항목 기준
  return target ? target.save_trm : options[options.length - 1].save_trm;
};


// ---- 페이지네이션 -----
const currentPage = ref(1);
const itemsPerPage = 10;

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return displayedProducts.value.slice(start, end);
});

const totalPages = computed(() =>
  Math.ceil(displayedProducts.value.length / itemsPerPage)
);

const changePage = (page) => {
  if (page > 0 && page <= totalPages.value) {
    currentPage.value = page;
  }
};
</script>


<style scoped>
.highlight {
  color: var(--orange-color);
  font-weight: bold;
}
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

.search-btn .btn {
  border-color: var(--mint-color) !important; /* 새로운 테두리 색상 */
  margin-right: 15px;
  color: var(--mint-color);
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

.card {
  width: 100%;
}

.card:hover {
  box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.2); /* 호버 시 그림자 강조 */
  transform: scale(1.02); /* 호버 시 살짝 확대 */
}

.logo-container img {
  width: 80px;
  height: 80px;
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
  background-color: var(--orange-color); /* 기본 배경색: Orange */
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

.bank-item.selected-bank {
  background-color: var(--mint-color); /* 선택된 은행의 배경색 */
  color: white; /* 선택된 텍스트 색상 */
}

.interest-info {
  padding: 10px 0;
  /* border-top: 1px solid #ddd;
  border-bottom: 1px solid #ddd; */
  margin: 5px 0;
}

.interest-item {
  flex: 1; /* 동일한 크기로 분배 */
  margin: 0 10px;
}

.interest-title {
  font-size: 15px;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.interest-rate {
  font-size: 29px;
  color: var(--dark-color);
  font-weight: 900;
  margin-bottom: 5px;
}

.interest-term {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0px;
}

/* 기본 페이지네이션 스타일 */
.pagination .page-item .page-link {
  color: black; /* 기본 텍스트 색상 */
  background-color: #fff; /* 기본 배경색 */
  border: 1px solid #dee2e6; /* 기본 테두리 */
}

.pagination .page-item:hover .page-link {
  color: black; /* 호버 시 텍스트 색상 */
  background-color: #e9ecef; /* 호버 시 배경색 */
}

.pagination .page-item.active .page-link {
  color: black; /* 활성 페이지 텍스트 색상 */
  background-color: lightgray; /* 활성 페이지 배경색 */
}
</style>
