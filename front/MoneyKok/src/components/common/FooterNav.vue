<template>
    <div>
        <footer class="footer">
            <!-- Newsletter Section -->
            <div class="newsletter">
              <div class="newsletter-container">
                <label class="newsletter-label">Newsletter</label>
                <div class="newsletter-form">
                  <input type="email" placeholder="your-email@example.com" class="newsletter-input" />
                  <button class="newsletter-button">
                     <i class="bi bi-send-fill"></i>
                  </button>
                </div>
              </div>
            </div>

            <!-- Footer Navigation Links -->
            <nav class="footer-nav">
            <ul class="footer-links">
                <li><RouterLink :to="{ name: 'home' }">홈</RouterLink></li>
                <li><RouterLink :to="{ name: 'deposits' }">예금 상품</RouterLink></li>
                <li><RouterLink :to="{ name: 'savings' }">적금 상품</RouterLink></li>
                <li><RouterLink :to="{ name: 'ai' }">AI 추천</RouterLink></li>
                <li><RouterLink :to="{ name: 'bank' }">은행 찾기</RouterLink></li>
                <li><RouterLink :to="{ name: 'exchangerate' }">환율 계산기</RouterLink></li>
            </ul>
            </nav>

            <!-- Copyright Section -->
            <div class="copyright">
              © Copyright 2024 - Choi HyeonJeong, Jang Inyoung
            </div>
        </footer>
    </div>
</template>

<script setup>

</script>

<style scoped>
@import 'bootstrap-icons/font/bootstrap-icons.css';

.footer {
  background-color: #f9fafc; /* Footer 배경색 */
  padding: 80px; /* 내부 여백 */
  text-align: center;
  height: 400px;
  color: #2c3e50; /* 텍스트 기본 색상 */
  font-size: 16px;
  /* 수직 정렬을 위한 Flexbox 설정 */
  display: flex;
  flex-direction: column; /* 요소들을 수직 정렬 */
  align-items: center; /* 수평 중앙 정렬 */
  gap: 30px; /* 각 섹션 간의 간격 */
}

.newsletter {
  margin-bottom: 10px;
}

/* Newsletter 컨테이너 스타일 */
.newsletter-container {
  display: flex; /* Flexbox 사용 */
  justify-content: center; /* 중앙 정렬 */
  align-items: center; /* 수직 중앙 정렬 */
  gap: 20px; /* 라벨과 입력 필드 간격 */
}

/* Newsletter 라벨 스타일 */
.newsletter-label {
  font-weight: bold;
  font-size: 18px;
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
}

/* Newsletter 입력 필드와 버튼 */
.newsletter-form {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.newsletter-input {
  padding: 10px 15px;
  border: 1px solid #d9d9d9;
  border-radius: 50px;
  font-size: 16px;
  width: 300px;
  outline: none;
  transition: border-color 0.3s;
}

.newsletter-input:focus {
  border-color: #007bff; /* 입력 시 강조 색상 */
}

.newsletter-button {
  background-color: #007bff; /* 파란색 버튼 */
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
}

.newsletter-button:hover {
  background-color: #0056b3; /* 호버 시 버튼 색상 변경 */
}

.footer-nav {
  margin: 20px 0;
}

.footer-links {
  list-style: none;
  padding: 0;
  display: flex;
  justify-content: center;
  gap: 30px;
}

.footer-links li {
  display: inline;
}

.footer-links a {
  text-decoration: none;
  color: #2c3e50;
  font-size: 16px;
  transition: color 0.3s;
}

.footer-links a:hover {
  color: #007bff; /* 호버 시 색상 */
}

.copyright {
  font-size: 14px;
  color: #999;
  margin-top: 10px;
}
</style>