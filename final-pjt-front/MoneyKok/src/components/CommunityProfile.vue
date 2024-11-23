<template>
    <div class="container mt-5 community-profile">
      <!-- 좌측 프로필 카드 -->
      <div class="profile-card">
        <img src="/favicon.ico" alt="Profile Image" class="profile-image" />
        <h2 class="profile-name">박소프</h2>
        <p class="profile-description">
          안녕하세요, 저는 2년차 직장인 박소프 입니다! 열심히 저축해서 내 집 마련하겠습니다!
        </p>
      </div>
  
      <!-- 우측 게시글 및 댓글 -->
      <div class="content-section">
        <!-- 내가 쓴 게시글 -->
        <div class="content-block">
          <h3 class="content-title">내가 쓴 게시글</h3>
          <div class="accordion" id="postsAccordion">
            <div class="accordion-item" v-for="(post, index) in posts" :key="index">
              <h2 class="accordion-header" :id="'postHeading' + index">
                <button
                  class="accordion-button"
                  type="button"
                  data-bs-toggle="collapse"
                  :data-bs-target="'#postCollapse' + index"
                  aria-expanded="true"
                  :aria-controls="'postCollapse' + index"
                >
                  {{ post.title }}
                </button>
              </h2>
              <div
                :id="'postCollapse' + index"
                class="accordion-collapse collapse"
                :class="{ show: index === 0 }"
                :aria-labelledby="'postHeading' + index"
                data-bs-parent="#postsAccordion"
              >
                <div class="accordion-body">{{ post.content }}</div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- 내가 쓴 댓글 -->
        <div class="content-block">
          <h3 class="content-title">내가 쓴 댓글</h3>
          <div class="accordion" id="commentsAccordion">
            <div class="accordion-item" v-for="(comment, index) in comments" :key="index">
              <h2 class="accordion-header" :id="'commentHeading' + index">
                <button
                  class="accordion-button"
                  type="button"
                  data-bs-toggle="collapse"
                  :data-bs-target="'#commentCollapse' + index"
                  aria-expanded="true"
                  :aria-controls="'commentCollapse' + index"
                >
                  {{ comment.title }}
                </button>
              </h2>
              <div
                :id="'commentCollapse' + index"
                class="accordion-collapse collapse"
                :class="{ show: index === 0 }"
                :aria-labelledby="'commentHeading' + index"
                data-bs-parent="#commentsAccordion"
              >
                <div class="accordion-body">{{ comment.content }}</div>
              </div>
            </div>
          </div>
        </div>
  


      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  // 데이터
  const posts = ref([
    { title: "Accordion header one", content: "내가 작성한 게시글 내용 1" },
    { title: "Accordion header two", content: "내가 작성한 게시글 내용 2" },
  ]);
  
  const comments = ref([
    { title: "Accordion header three", content: "내가 작성한 댓글 내용 1" },
    { title: "Accordion header four", content: "내가 작성한 댓글 내용 2" },
  ]);
  
  const likedPosts = ref([
    { title: "Accordion header five", content: "내가 좋아요 한 게시글 내용 1" },
    { title: "Accordion header six", content: "내가 좋아요 한 게시글 내용 2" },
  ]);
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
    color: #004d00; /* 진한 초록색 */
    margin-bottom: 15px;
  }
  
  /* 아코디언 */
  .accordion-button {
    font-size: 1rem;
  }
  
  .accordion-body {
    font-size: 0.9rem;
    color: #333333;
  }
  </style>
  