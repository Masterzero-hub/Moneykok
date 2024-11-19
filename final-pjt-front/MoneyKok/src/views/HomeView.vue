<template>
  <!-- Main Section -->
  <main class="main-content">
    <!-- intro Section -->
    <section class="intro">
      <div class="intro-content">
        <h1>필요한 예적금, 한번에 콕! <strong>머니콕</strong></h1>
        <p>최적의 금융 상품을 AI로 추천 받아보세요.</p>
        <button class="btn-common">AI 추천 바로가기</button>
      </div>
      <img src="@/assets/main_image/1.png" width="880" alt="intro Illustration" class="intro-image" />
    </section>

    <!-- Services Section -->
    <section class="services">
      <div class="service-card">
        <img
          src="@/assets/main_image/2.png"
          alt="money Illustration"
          class="service-card-image"
        />
        <div class="service-card-content">
          <h2>내 조건에 딱 맞는 예적금 상품을 찾을 수 있어요</h2>
          <p>은행 · 저축은행을 포함한 3,000여 금융 상품을 비교하고 신청할 수 있어요.</p>
          <button class="btn-common">예적금 상품 조회하기</button>
        </div>
      </div>

      <div class="service-card">
        <img
          src="@/assets/main_image/3.png"
          alt="bank Illustration"
          class="service-card-image"
        />
        <div class="service-card-content">
          <h2>내 근처 은행을 찾을 수 있어요</h2>
          <p>지도와 함께 내 근처에 있는 모든 은행 정보를 찾아보세요.</p>
          <button class="btn-common">내 근처 은행 찾기</button>
        </div>
      </div>

      <div class="service-card">
        <img
          src="@/assets/main_image/4.png"
          alt="dollar Illustration"
          class="service-card-image"
        />
        <div class="service-card-content">
          <h2>현재 환율에 따른 환산 금액을 확인할 수 있어요</h2>
          <p>실시간 환율 정보를 확인하고 주요 세계 통화의 환산 금액을 손쉽게 계산해 보세요 .</p>
          <button class="btn-common">AI 추천 받기</button>
        </div>
      </div>
    </section>

    <!-- Community Section -->
    <section class="community">
        <div class="community-content">
          <h2>금융 초년생들의 저축 커뮤니티</h2>
          <p>나와 같은 상품을 선택한 사용자들과 정보도 공유하고, 함께 배울 수 있어요.</p>
          <button class="btn-common">커뮤니티 바로가기</button>
        </div>
        <img src="@/assets/main_image/5.png" alt="Community Illustration" />
    </section>
  </main>
</template>


<script setup>
import { ref } from 'vue';

const isLogin = ref(false)

</script>



<style scoped>
/* Main Content Styles */
.main-content {
  padding: 0 20px; /* 전체 메인 콘텐츠의 좌우 여백 */
  margin-top: 100px; /* 페이지 상단과의 간격 */
  margin-bottom: 100px; /* 페이지 하단과의 간격 */
}


/* intro Section */
.intro {
  height: 800px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #a1c181;
  padding-left: 50px;
  border-radius: 8px;
}

.intro-content h1 {
  font-size: 50px;
  font-weight: bold;
  line-height: 1.4;
  /* padding: 10px 15px; */
}

.intro-content p {
  font-size: 18px;
  margin: 10px 0;
  padding: 20px 0px;
}


/* Section 공통 스타일 */
section {
  margin-bottom: 200px; /* 각 섹션 간의 간격 */
}

/* Services Section */
.services {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.service-card {
  height: 600px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #e6f5e6;
  padding: 30px;
  margin: 50px 0px;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.service-card-content {
  width: 600px;
  margin: 30px;
}

.service-card h2 {
  font-size: 40px;
  margin-bottom: 15px;
  font-weight: bold;
  color: #233d4d;
}

.service-card p {
  font-size: 18px;
  color: #666;
  margin: 50px 0px;
  line-height: 1.6;
  margin-bottom: 20px;
}

.service-card-image {
  width: 700px;
  border-radius: 10px;
}

/* Community Section */
.community {
  height: 800px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: var(--mint-color);
  padding: 30px;
  margin: 50px 0px;
  border-radius: 8px;
  color: white;
  padding-left: 70px;
}
.community h2 {
  font-size: 50px;
  font-weight: bold;
  margin-bottom: 10px;
}

.community p {
  font-size: 18px;
  margin: 30px 0;
}

</style>