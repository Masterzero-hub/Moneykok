<template>
    <div class="container mt-5">
      <!-- 제목 -->
      <h2 class="text-center mb-5">
        <span class="username">{{ username }}</span>님의 상품 추천 결과
      </h2>
  
      <!-- 상품 카드 리스트 -->
      <div v-if="recommendedProducts.recommended_products && recommendedProducts.recommended_products.length" class="row">
        <div
          v-for="product in recommendedProducts.recommended_products"
          :key="product.id"
          class="col-lg-4 col-md-6 col-sm-12 d-flex align-items-stretch"
        >
          <div class="product-card">
            <!-- 카드 상단 -->
            <div class="product-header">
              <div class="bank-info d-flex align-items-center justify-content-center">
                <!-- 은행 로고 -->
                <img
                  :src="`/bank_image/${product.bank.fin_co_no}.jpg`"                  alt="Bank Logo"
                  class="bank-logo me-2"
                />
                <!-- 은행 이름 -->
                <h5 class="product-bank mb-0">{{ product.bank.kor_co_nm }}</h5>
              </div>
              <p class="product-name">{{ product.fin_prdt_nm }}</p>
            </div>
  
            <!-- 상세 정보 -->
            <table class="table product-details">
              <tbody>
                <tr>
                  <th>최대 금리</th>
                  <td class="max-rate">{{ getMaxInterestRate(product.options) }}%</td>
                </tr>
                <tr>
                  <th>가입 조건</th>
                  <td>{{ product.join_member }}</td>
                </tr>
                <tr>
                  <th>가입 방법</th>
                  <td>{{ product.join_way }}</td>
                </tr>
                <tr>
                  <th>최소 금액</th>
                  <td>{{ product.deposit_min_amount || "제한 없음" }}원</td>
                </tr>
                <tr>
                  <th>우대 조건</th>
                  <td>
                    <template v-if="product.processed_spcl_cnd">
                          {{ product.processed_spcl_cnd }}
                    </template>
                    <template v-else>
                      없음
                    </template>
                  </td>
                </tr>
              </tbody>
            </table>
  
            <!-- 버튼 -->
            <div class="text-center mt-auto">
              <button class="btn-common btn-mint btn-view" @click="goDetail(product.fin_prdt_cd)">자세히 보기</button>
            </div>
          </div>
        </div>
      </div>



      
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { useRouter, useRoute } from "vue-router";
  import { storeToRefs } from "pinia";
  import { useAiStore } from "@/stores/ai";
  import { useUserStore } from "@/stores/user";

  
  const store = useAiStore();
  const userStore = useUserStore();
  const { recommendedProducts, getRecommendtaion } = storeToRefs(store);
  const route = useRoute()
  const router = useRouter();
  const username = userStore.name
  
// ----- 초기 렌더링 -----
onMounted(() => {
  // 라우터 매개변수에서 productType 값 읽기
  const routeProductType = route.params.productType;

  if (routeProductType) {
    store.productType = routeProductType; // Pinia 상태 업데이트
    store.getRecommendtaion(); // API 호출
  } else {
    console.error("라우터 매개변수 productType이 없습니다.");
  }
});

// 최대 금리 계산 함수
const getMaxInterestRate = (options) => {
  if (!options || options.length === 0) return "정보 없음";
  return Math.max(...options.map((opt) => opt.intr_rate2)).toFixed(2);
};


  const goDetail = function (depositCode) {
    router.push({ name : 'depositdetail', params: { deposit_code : depositCode }})
  }
  
  </script>
  
  <style scoped>
  .row {
  display: flex;
  flex-wrap: wrap;
}

.username {
  color: var(--orange-color);
  font-weight: bold;
}

  /* 제목 스타일 */
  h2 {
    color:black;
  }
  
  /* 상품 카드 스타일 */
  .product-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 100%; /* 카드 너비를 부모의 너비에 맞춤 */
        background-color: #fff;
    border: 1px solid #eaeaea;
    border-radius: 10px;
    padding: 20px;
  }

  .product-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  /* 카드 상단 스타일 */
  .product-header {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .bank-info {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10px;
  }
  
  .bank-logo {
    width: 40px;
    height: 40px;
    object-fit: cover;
    border-radius: 5px;
  }
  
  .product-bank {
    font-size: 20px;
    font-weight: bold;
  }
  
  .product-name {
    font-size: 30px;
    font-weight: bold;
    color: var(--orange-color);
  }
  
  /* 상세 정보 테이블 스타일 */
  .product-details {
    margin-top: 10px;
    font-size: 0.9rem;
  }
  
  .product-details th {
    width: 40%;
    text-align: left;
    background-color: #f9f9f9;
    font-weight: bold;
  }
  
  .product-details td {
    text-align: left;
  }

  .max-rate {
    font-weight: bolder;
    font-size: large;
  }
  
  /* 혜택 리스트 스타일 */
  .benefit-list {
    padding-left: 20px;
    margin: 0;
    list-style: disc;
    font-size: 0.9rem;
  }
  
  /* 버튼 스타일 */
  .btn-view {
    padding: 10px 20px;
    font-size: 1rem;
    border-radius: 5px;
  }
  
  /* 반응형 스타일 */
  @media (max-width: 768px) {
    .product-card {
      padding: 15px;
    }
  
    .product-bank {
      font-size: 1rem;
    }
  
    .product-name {
      font-size: 0.9rem;
    }
  
    .product-details {
      font-size: 0.85rem;
    }
  }
  </style>
  