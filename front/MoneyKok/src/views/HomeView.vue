<template>
  <!-- Main Section -->
  <main class="main-content">
    <!-- Hero Section -->
    <section class="intro">
      <div class="intro-content">
        <h1>필요한 예적금, 한번에 콕! <strong>머니콕</strong></h1>
        <p>최적의 금융 상품을 AI로 추천받아보세요.</p>
        <button class="intro-button">AI 상품 바로가기</button>
      </div>
      <img src="@/assets/main_image/1.png" width="880" alt="intro Illustration" class="intro-image" />
    </section>

    <!-- Services Section -->
    <section class="services">
      <div class="service-card">
        <h2>내 조건에 딱 맞는 예적금 상품을 찾을 수 있어요</h2>
        <p>은행 · 저축은행을 포함한 3,000여 금융 상품을 비교하고 신청할 수 있어요.</p>
        <button>예적금 상품 조회하기</button>
        <img src="@/assets/main_image/2.png" alt="Hero Illustration" class="hero-image" />
      </div>
      <div class="service-card">
        <h2>내 근처 은행을 찾을 수 있어요</h2>
        <p>지도와 함께 내 근처에 있는 모든 은행 정보를 찾아보세요.</p>
        <button>내 근처 은행 찾기</button>
        <img src="@/assets/main_image/3.png" alt="Hero Illustration" class="hero-image" />
      </div>
      <div class="service-card">
        <h2>AI가 선호에 맞는 상품을 추천해줄 수 있어요</h2>
        <p>입력한 조건을 분석하여 맞춤형 예적금 상품을 추천받아보세요.</p>
        <button>AI 추천 받기</button>
        <img src="@/assets/main_image/4.png" alt="Hero Illustration" class="hero-image" />
      </div>
    </section>

    <!-- Community Section -->
    <section class="community">
      <h2>금융 초년생들의 저축 커뮤니티</h2>
      <p>나와 같은 상품을 선택한 사용자들과 정보도 공유하고, 함께 배울 수 있어요.</p>
      <button>커뮤니티 바로가기</button>
      <img src="@/assets/main_image/5.png" alt="Community Illustration" />
    </section>
  </main>
</template>


<script setup>
  
</script>



<style scoped>
/* Main Content Styles */
.main-content {
  padding: 0 20px; /* 전체 메인 콘텐츠의 좌우 여백 */
  margin-top: 100px; /* 페이지 상단과의 간격 */
  margin-bottom: 100px; /* 페이지 하단과의 간격 */
}

/* Section 공통 스타일 */
section {
  margin-bottom: 500px; /* 각 섹션 간의 간격 */
}

/* Hero Section */
.intro {
  height: 800px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #a1c1817e;
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

.intro-button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* Services Section */
.services {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.service-card {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.service-card h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

.service-card p {
  font-size: 16px;
  color: #666;
}

.service-card button {
  background-color: #28a745;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* Community Section */
.community {
  background-color: #f9f2ec;
  padding: 40px 20px;
  border-radius: 8px;
  text-align: center;
}

.community h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

.community p {
  font-size: 16px;
  margin-bottom: 20px;
}

.community button {
  background-color: #ffc107;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>