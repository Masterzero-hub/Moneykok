<template>
  <div class="container mt-5 community-profile">
    <!-- 좌측 프로필 카드 -->
    <div class="profile-card">
      <img src="/현정언니다옹.png" alt="Profile Image" class="profile-image" />
      <h2 class="profile-name mt-3">{{ myCommunityInfo.nickname }}</h2>
      <p class="profile-description mt-5">
        안녕하세요, 반갑습니다!
      </p>
    </div>

    <!-- 우측 게시글 및 댓글 -->
    <div class="content-section">
      <!-- 내가 쓴 게시글 -->
      <div class="content-block">
        <h3 class="content-title">내가 쓴 게시글</h3>
        <ul class="list-group">
          <li 
            class="list-group-item list-item"
            v-for="(article, index) in myCommunityInfo.article_set" 
            :key="index"
            @click="goDetailPage(article.id)"
          >
            {{ article.content }}
          </li>
        </ul>
      </div>

      <!-- 내가 쓴 댓글 -->
      <div class="content-block">
        <h3 class="content-title">내가 쓴 댓글</h3>
        <ul class="list-group">
          <li 
            class="list-group-item list-item"
            v-for="(comment, index) in myCommunityInfo.comment_set" 
            :key="index"
            @click="goDetailPage(comment.article)"
          >
            {{ comment.content }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from "@/stores/user";
import { ref, onMounted } from "vue";
import { storeToRefs } from "pinia"; // storeToRefs 사용
import { useRouter } from "vue-router";
const router = useRouter()
const store = useUserStore()
const { myArticles, myComments, myCommunityInfo, getMyCommunityInfo } = storeToRefs(store)

onMounted(() => {
  store.getMyCommunityInfo()
});


// 상세 페이지로 이동
const goDetailPage = (articleId) => {
  // alert(`페이지로 이동: ${item.title} (ID: ${item.id})`);
  router.push({ name : 'articledetail', params : { article_id : articleId } })
};
</script>

<style scoped>
/* 전체 컨테이너 */
.community-profile {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 20px;
}

/* 좌측 프로필 카드 */
.profile-card {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 20px;
}

.profile-name {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.profile-description {
  font-size: 0.9rem;
  color: #666666;
}

/* 우측 콘텐츠 섹션 */
.content-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

/* 콘텐츠 블록 */
.content-block {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.content-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: var(--mint-color);
  margin-bottom: 15px;
}

/* 목록 스타일 */
.list-group {
  list-style: none;
  padding: 0;
  margin: 0;
}

.list-group-item {
  cursor: pointer;
  padding: 10px;
  border: 1px solid #ddd;
  margin-bottom: 5px;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.list-group-item:hover {
  background-color: #f0f0f0;
}
</style>