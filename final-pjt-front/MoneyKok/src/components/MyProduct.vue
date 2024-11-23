<template>
    <div class="container mt-5">
      <!-- 가입한 상품 목록 -->
      <div v-if="subscribedProducts.length > 0">
        <div
          v-for="product in subscribedProducts"
          :key="product.id"
          class="card shadow-sm mb-3"
        >
          <div class="card-body d-flex align-items-center">
            <!-- 상품 로고 -->
            <img
              :src="product.logoUrl"
              alt="Bank Logo"
              class="product-logo me-3"
            />
  
            <!-- 상품 정보 -->
            <div class="flex-grow-1">
              <h5 class="card-title mb-1">{{ product.name }}</h5>
              <p class="card-text text-muted mb-2">
                {{ product.bankName }} | {{ product.subscriptionDate }}
              </p>
              <p class="card-text">
                <strong>이율:</strong> {{ product.interestRate }}%
              </p>
            </div>
  
            <!-- 버튼 -->
            <button class="btn-small-common btn-outline-danger" @click="cancelSubscription(product.id)">
              해지하기
            </button>
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
  
  const subscribedProducts = ref([]); // 가입한 상품 데이터
  
  // 더미 데이터 (API 통신 구현 전)
  const mockData = [
    {
      id: 1,
      name: "우리은행 스마트예금",
      bankName: "우리은행",
      subscriptionDate: "2024-01-01",
      interestRate: 3.2,
      logoUrl: "/bank_image/0010001.jpg",
    },
    {
      id: 2,
      name: "카카오뱅크 정기예금",
      bankName: "카카오뱅크",
      subscriptionDate: "2024-02-15",
      interestRate: 2.8,
      logoUrl: "/bank_image/0015130.jpg",
    },
  ];
  
  // 페이지 로드 시 데이터 가져오기
  onMounted(() => {
    // 실제 구현 시, 서버로부터 데이터를 받아오는 로직을 추가
    subscribedProducts.value = mockData; // 더미 데이터를 초기값으로 설정
  });
  
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
  
  .card-text {
    font-size: 0.9rem;
  }
  
  .btn-small-common {
    padding: 5px 10px;
    font-size: 0.9rem;
  }
  </style>