<template>
  <div class="container mt-5">
    <!-- 가입한 상품 목록 -->
    <div v-if="joinedProducts.length > 0">
      <div
        v-for="product in joinedProducts"
        :key="product.id"
        class="card shadow-sm mb-3"
      >
        <div class="card-body d-flex align-items-center">
          <!-- 상품 로고 -->
          <img
            :src="`/bank_image/${product.bank.fin_co_no}.jpg`"
            alt="Bank Logo"
            class="product-logo me-3"
          />

          <!-- 상품 정보 -->
          <div class="flex-grow-1">
            <!-- 상품 이름과 은행 이름 -->
            <div class="d-flex align-items-center ">
              <h5 class="card-title mb-1 me-2" style="font-weight: 550;">{{ product.product.fin_prdt_nm }}</h5>
              <div class="divider"></div>
              <p class="card-text bank-name ms-2">{{ product.bank.kor_co_nm }}</p>
            </div>
            <!-- 가입일과 만기일 -->
            <p class="card-text text-mute" style="font-size: 14px;">
              가입일 : {{ product.joined_date }}  |  만기일 : {{ product.expired_date }}
            </p>
          </div>

          <!-- 가입 이율과 버튼 -->
          <div class="d-flex align-items-center gap-3">
            <span class="card-text m-0" style="font-size: large;">
              적용 금리 :
            </span>
            <span class="card-rate-text m-0">
               {{ formatRate(product.final_intr_rate) }}%
            </span>
            <button
              class="btn-small-common btn-mint"
              @click="cancelSubscription(product.id)"
            >
              해지하기
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 가입한 상품이 없는 경우 -->
    <div v-else>
      <p class="text-muted text-center">가입한 상품이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useDepositsStore } from "@/stores/deposits";
import { useRoute, useRouter } from "vue-router";
import { storeToRefs } from "pinia";
const router = useRouter();
const route = useRoute();
const store = useDepositsStore();
const { joinedProducts, getJoinedProducts } = storeToRefs(store);

// 페이지 로드 시 데이터 가져오기
onMounted(() => {
  // 실제 구현 시, 서버로부터 데이터를 받아오는 로직을 추가
  store.getJoinedProducts()
  console.log(joinedProducts)
});

const formatRate = (rate) => {
  if (typeof rate !== "string") {
    // 숫자 또는 null/undefined일 경우 처리
    return rate ? rate.toString().slice(0, 4) : "N/A"; // 값이 없으면 "N/A" 반환
  }
  return rate.slice(0, 4); // 문자열이면 slice 적용
};
// 해지 버튼 클릭 시 동작 (현재는 console.log)
const cancelSubscription = (productId) => {
  console.log(`상품 ID ${productId} 해지 요청`);
  // 실제 API 호출로 해지 로직 구현 예정
};
</script>

<style scoped>
.section-title {
  font-size: 1.5rem;
  font-weight: bold;
}

.product-logo {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}

.card {
  border: 1px solid #cacaca;
  border-radius: 8px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: scale(1.02);
  box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.2);
}

.card-title {
  font-size: 1.25rem;
}

/* .card-text {
  font-size: 0.9rem;
} */

.card-rate-text {
  font-size: 23px;
  color: var(--orange-color);
  font-weight: 600;
}

.btn-small-common {
  padding: 5px 10px;
  font-size: 0.9rem;
}

.divider {
  height: 20px;
  width: 1px;
  background-color: #ccc;
  margin-left: 8px;
  margin-right: 8px;
  display: inline-block;
}
</style>
