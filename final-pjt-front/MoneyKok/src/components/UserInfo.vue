<template>
  <div class="container">
    <!-- 상단 네비게이션 -->
    <nav class="nav nav-tabs">
      <router-link
        :to="{ name: 'myproduct' }"
        class="nav-link"
        :class="{ active: $route.name === 'myproduct' }"
      >
        가입상품
      </router-link>

      <router-link
        :to="{ name: 'communityprofile' }"
        class="nav-link"
        :class="{ active: $route.name === 'communityprofile' }"
      >
        커뮤니티
      </router-link>

      <router-link
        :to="{ name: 'personalinfo' }"
        class="nav-link"
        :class="{ active: $route.name === 'personalinfo' }"
      >
        개인정보
      </router-link>
    </nav>

    <!-- 하위 라우트 -->
    <div>
      <router-view style="margin-top: 0; padding: 0;"></router-view>
    </div>
  </div>
</template>

<script setup>

</script>

<style scoped>
.nav-tabs {
  margin-bottom: 1rem;
}

.nav-link {
  color: black; /* 비활성화된 탭의 글자 색 */
  font-weight: normal; /* 비활성화된 탭은 기본 폰트 두께 */
  text-decoration: none; /* 기본 밑줄 제거 */
}

.nav-link.active {
  font-weight: bold; /* 활성화된 탭은 볼드 */
  color: var(--orange-color)!important; /* 활성화된 탭의 글자 색 (오렌지) */
  border-bottom: none; /* 하단 테두리 제거 */
  border-left: 1px solid transparent; /* 다른 테두리 유지 (필요 시 추가) */
  border-right: 1px solid transparent;
  border-top: 1px solid transparent;
}

.nav-link:hover {
  color: black; /* 호버 시 검정색 유지 */
  font-weight: bold; /* 호버 시 볼드 처리 */
  text-decoration: none; /* 호버 시 밑줄 제거 */
}
</style>