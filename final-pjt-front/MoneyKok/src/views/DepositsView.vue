<template>
  <div>
    <div class="container mt-5">
      <h2 class="mb-4">예금 상품 조회</h2>

      <!-- 상품 목록 -->
      <div class="row">
        <div
          class="col-12 mb-4"
          v-for="product in store.products"
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
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();
const store = useDepositsStore();

onMounted(() => {
  store.getProducts();
});

const goDepositDetail = function (product_id) {
  router.push({ name: "depositdetail", params: { deposit_id: product_id } });
};
</script>


<style scoped>
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
