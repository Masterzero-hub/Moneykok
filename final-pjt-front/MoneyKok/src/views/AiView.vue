<template>
  <div class="container mt-5 ai-recommendation">
    <!-- 제목 -->
    <h2 class="mb-4 text-center">
      <span class="highlight">{{ username }}</span>님 맞춤 상품 추천
    </h2>
    <p class="text-center">
      {{ username }}님의 나이, 성별, 연봉 정보를 바탕으로 유사한 사용자가 많이 가입한 상품을 추천드립니다.
    </p>

    <!-- 상품 카드 섹션 -->
    <div class="row justify-content-center mt-5">
      <!-- 예금 카드 -->
      <div class="col-lg-5 col-md-6 product-card">
        <div class="type-title-group">
          <i class="bi bi-coin"></i>
          <h3 class="type-title"> 예금</h3>
        </div>
        <p class="type-description">
          예금은 일정한 금액에 예치 기간을 정해 저축하는 상품을 뜻합니다.
        </p>
        <blockquote class="testimonial">
          <span>"</span>
          <span class="highlight">안전</span>과
          <span class="highlight">안정성</span>이 중요한 분들에게 추천드려요!"
        </blockquote>
        <button
          class="btn-common btn-mint mt-4"
          :class="{ active: productType === 'deposits' }"
          @click="goRecommendations('deposits')"
        >
          예금 상품 추천받기
        </button>
      </div>

      <!-- 적금 카드 -->
      <div class="col-lg-5 col-md-6 product-card">
        <div class="type-title-group">
          <i class="bi bi-cash-stack"></i>
          <h3 class="type-title ms-1"> 적금</h3>
        </div>
        <p class="type-description">
          적금은 정해진 기간에 한 달 단위로 금액을 저축하는 상품을 뜻합니다.
        </p>
        <blockquote class="testimonial">
          <span>"</span>
          <span class="highlight">목표 달성</span>과
          <span class="highlight">계획적인 저축</span>을 원하는 분들에게 추천드려요!"
        </blockquote>
        <button
          class="btn-common btn-mint mt-4"
          :class="{ active: productType === 'savings' }"
          @click="goRecommendations('savings')"
        >
          적금 상품 추천받기
        </button>
      </div>
    </div>
  </div>
</template>




<script setup>
import { ref,onMounted } from "vue";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import { useAiStore } from "@/stores/ai";
import { useUserStore } from "@/stores/user";

const aiStore = useAiStore();
const userStore = useUserStore()

const { productType } = storeToRefs(aiStore);
const { isLogin } = storeToRefs(userStore)
const router = useRouter();

const username = userStore.name

const productTypesList = [
  { label: "예금", value: "deposits" },
  { label: "적금", value: "savings" },
];

onMounted(() => {
  if (isLogin.value == false) {
    // 로그인 상태가 아니라면 login 페이지로 리다이렉트
    alert('로그인이 필요합니다.')
    router.push({ name: 'login' });
    return;
  }
});

// 상품 유형 선택
// const selectProductType = (type) => {
//   productType.value = type;

// };


const goRecommendations = (type) => {
  productType.value = type; // 선택된 상품 유형 설정
  router.push({
    name: "ai-recommendations",
    params: { productType: type }, // 선택된 유형 전달
  });
};
</script>

<style scoped>
.bi {
  font-size: 50px;
}

/* 공통 스타일 */
.highlight {
  color: var(--orange-color);
  font-weight: bold;
}

h2 {
  font-size: 2rem;
  color: #333;
}

p {
  font-size: 1rem;
  color: #555;
}

/* 카드 스타일 */
.product-card {
  background-color: #fadf9428;
  border-radius: 15px;
  padding: 30px;
  margin: 40px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.product-card p {
  font-size: 25px;
  padding: 0px 20px 5px 20px;
  
}

.type-title-group {
  display: flex; /* Flexbox 사용 */
  align-items: center; /* 세로축 가운데 정렬 */
  justify-content: center; /* 가로축 가운데 정렬 */
  gap: 10px; /* 아이콘과 텍스트 사이 간격 */
  font-size: 40px;
  color: var(--primary-color);
  margin-top: 0px;
  margin-bottom: 25px;
}

.type-description {
  font-size: 1rem;
  color: #555;
  margin-bottom: 20px;
  line-height: 1.5;
}

/* 인용구 스타일 */
.testimonial {
  font-style: italic;

  margin: 15px 0;
  color: #333;
  border-radius: 5px;
}

.testimonial footer {
  font-size: 0.9rem;
  color: #999;
  margin-top: 10px;
  text-align: right;
}

/* 버튼 스타일 */
/* .btn-action {
  display: inline-block;
  padding: 0px 20px;
  font-size: 1rem;
  border-radius: 25px;
  background-color: var(--mint-color);
  color: white;
  border: none;
  transition: background-color 0.3s, transform 0.3s;
} */

.btn-action:hover {
  background-color: var(--secondary-color);
  transform: translateY(-3px);
}

.btn-action.active {
  background-color: var(--secondary-color);
}
</style>
