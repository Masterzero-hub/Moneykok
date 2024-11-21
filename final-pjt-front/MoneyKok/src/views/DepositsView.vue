<은행 모달 구현 전 코드>
<template>
  <div>
    <div class="container mt-5">
      <h2 class="mb-4">예금 상품 조회</h2>
      <!-- 검색 조건 -->
      <div class="search-card p-4 mb-5 shadow-sm">
        <!-- 가입 기간 -->
        <div class="row mb-3 align-items-center">
          <label class="col-md-2 col-form-label">가입 기간</label>
          <div class="col-md-10">
            <div class="search-btn">
              <button
                v-for="term in terms"
                :key="term"
                class="btn"
                :class="filters.join_term === term ? 'btn-primary' : 'btn-outline-primary'"
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
              class="btn-small-common btn-mint"
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
                  class="btn-small-common btn-mint"
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
              class="btn-small-common btn-mint"
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
                      @click="selectBank(bank.name)"
                      data-bs-dismiss="modal"
                    >
                      <img
                        :src="bank.logo"
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

        <!-- 우대 조건 -->
        <div>
          <div class="d-flex gap-2 flex-wrap" style="align-items: center">
            <h6 class="mb-0" style="margin-right: 70px">우대 조건</h6>
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
                @click="toggleCondition(condition)"
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
const { products, getProducts, productDetail, filters, filteredProducts } =
  storeToRefs(store);
const router = useRouter();

onMounted(() => {
  store.getProducts();
  console.log(products)
});

const goDepositDetail = function (product_id) {
  router.push({ name: "depositdetail", params: { deposit_id: product_id } });
};

// 가입 기간, 은행 목록, 우대 조건 목록 정의
const terms = ["6개월", "12개월", "24개월", "36개월"];
const banks = [
  { name: "KDB산업은행", logo: "/bank_logo/kdb.png" },
  { name: "SC제일은행", logo: "/bank_logo/sc.png" },
  { name: "iM뱅크", logo: "/bank_logo/im.png" },
  { name: "경남은행", logo: "/bank_logo/kyungnam.png" },
  { name: "광주은행", logo: "/bank_logo/gwangju.png" },
  { name: "국민은행", logo: "/bank_logo/kb.png" },
  { name: "기업은행", logo: "/bank_logo/ibk.png" },
  { name: "농협은행", logo: "/bank_logo/nh.png" },
  { name: "부산은행", logo: "/bank_logo/busan.png" },
  { name: "수협은행", logo: "/bank_logo/suhyup.png" },
  { name: "신한은행", logo: "/bank_logo/shinhan.png" },
  { name: "씨티은행", logo: "/bank_logo/citi.png" },
  { name: "우리은행", logo: "/bank_logo/woori.png" },
  { name: "우체국", logo: "/bank_logo/post.png" },
  { name: "전북은행", logo: "/bank_logo/jeonbuk.png" },
  { name: "제주은행", logo: "/bank_logo/jeju.png" },
  { name: "카카오뱅크", logo: "/bank_logo/kakao.png" },
  { name: "케이뱅크", logo: "/bank_logo/kbank.png" },
  { name: "토스뱅크", logo: "/bank_logo/toss.png" },
  { name: "하나은행", logo: "/bank_logo/hana.png" },
];
const conditions = [
  "신규 가입",
  "거래 연동",
  "사용 실적",
  "비대면/모바일",
  "마케팅 동의",
  "기타",
];



const setTerm = (term) => {
  store.filters.join_term = store.filters.join_term === term ? null : term;
  console.log(filters.value);
};

const selectBank = (bankName) => {
  if (!filters.bank) {
    filters.bank = [];
  }

  const index = filters.bank.indexOf(bankName);

  // 이미 선택된 은행이면 제거
  if (index > -1) {
    filters.bank.splice(index, 1);
  } else {
    // 선택되지 않은 은행이면 추가
    filters.bank.push(bankName);
  }
};

// 우대 조건 추가/제거 함수
const toggleCondition = (condition) => {
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

// 필터 변경 사항 확인
// watch(
//   () => filters,
//   (newFilters) => {
//     console.log("현재 필터 상태:", newFilters);
//   },
//   { deep: true }
// );


// 페이지네이션 로직
const currentPage = ref(1);
const itemsPerPage = 10;

const totalPages = computed(() => Math.ceil(products.value.length / itemsPerPage));
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return products.value.slice(start, end);
});

const changePage = (page) => {
  if (page > 0 && page <= totalPages.value) {
    currentPage.value = page;
  }
};


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
