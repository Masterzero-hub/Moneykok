<template>
    <div>
      <div class="container mt-5">
        <h1 class="text-center mb-4">예금 상품 조회</h1>
  
        <!-- 상품 목록 -->
        <div class="row">
          <div
            class="col-12 mb-4"
            v-for="product in store.products"
            :key="product.id"
          >
            <div class="card shadow-sm p-3 bg-white rounded d-flex flex-row align-items-center">
              <!-- 로고 -->
              <div class="logo-container me-3">
                <img
                  :src="`/bank_image/${product.fin_co_no}.jpg`"
                  alt="Bank Logo"
                  class="rounded-circle"
                />
              </div>
  
              <!-- 상품 정보 -->
              <div class="flex-grow-1">
                <h5 class="mb-1">{{ product.fin_prdt_nm }}</h5>
                <div class="d-flex align-items-center">
                  <span class="badge bg-danger me-2">신규 가입</span>
                  <span class="badge bg-info me-2">카드 보유</span>
                  <span class="badge bg-secondary">디지털 서비스</span>
                </div>
              </div>
  
              <!-- 금리 및 버튼 -->
              <div class="d-flex align-items-center">
                <div class="text-center me-3">
                  <p class="mb-0">기본</p>
                  <strong>{{ product.int_rate }}%</strong>
                </div>
                <div class="text-center me-3">
                  <p class="mb-0">최고</p>
                  <strong>{{ product.int_rate2 }}%</strong>
                </div>
                <div class="divider me-3"></div>
                <button
                  class="btn-small-common"
                  data-bs-toggle="modal"
                  :data-bs-target="'#modal-' + product.id"
                >
                  상세 보기
                </button>
              </div>
            </div>
          </div>
        </div>
  
        <!-- 상품 상세 모달 -->
        <div
          v-for="product in store.products"
          :key="'modal-' + product.id"
          class="modal fade"
          :id="'modal-' + product.id"
          tabindex="-1"
          aria-labelledby="'modal-label-' + product.id"
          aria-hidden="true"
        >
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" :id="'modal-label-' + product.id">
                  {{ product.name }}
                </h5>
                <button
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body">
                <p><strong>은행:</strong> {{ product.kor_co_nm }}</p>
                <p><strong>상품명:</strong> {{ product.fin_prdt_nm }}</p>
                <p><strong>우대조건:</strong> {{ product.spcl_cnd }}</p>
                <p><strong>저축기간:</strong> {{ product.save_trm }}개월</p>
                <p><strong>기본금리:</strong> {{ product.int_rate }}%</p>
                <p><strong>최고금리:</strong> {{ product.int_rate2 }}%</p>
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  닫기
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
const store = useDepositsStore()
// 상품 데이터

onMounted(() => {
    store.getProducts()
})

</script>

<style scoped>
.card {
  width: 100%;
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

.badge {
  font-size: 0.85rem;
}</style>
