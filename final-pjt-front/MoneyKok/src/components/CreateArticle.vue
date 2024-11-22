<template>
    <div class="container mt-5">
      <!-- 게시글 작성 헤더 -->
      <div class="row align-items-center mb-4">
        <h2 class="section-title col">게시글 작성</h2>
        <button class="btn-common btn-mint col-auto" @click="goBack">
          목록으로 돌아가기
        </button>
      </div>
  
      <!-- 게시글 작성 카드 -->
      <div class="card shadow-sm p-4">
        <div class="card-body">
          <div class="mb-3">
            <label for="title" class="form-label">제목</label>
            <input
              type="text"
              id="title"
              v-model="title"
              class="form-control"
              placeholder="제목을 입력하세요"
              required
            />
          </div>
  
          <div class="mb-3">
            <label for="content" class="form-label">내용</label>
            <textarea
              id="content"
              v-model="content"
              class="form-control"
              rows="8"
              placeholder="내용을 입력하세요"
              required
            ></textarea>
          </div>
  
          <div class="d-flex justify-content-end">
            <button class="btn-common btn-mint" @click="submitArticle">
              게시글 작성
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  import { storeToRefs } from 'pinia'
  import { useCommunityStore } from "@/stores/community";
  const store = useCommunityStore()
  const { recommendedFriends, posts, articles, title, content } = storeToRefs(store)
  const router = useRouter();

  
  const goBack = () => {
    router.push({ name: "community" }); // 메인 페이지로 돌아가기
  };
  
  const submitArticle = () => {
    if ( title.value == '' || content.value == '') {
      alert("제목과 내용을 모두 입력해주세요.");
      return;
    }
  
    // 게시글 데이터를 서버로 전송 (예: Axios 요청)
    console.log("게시글 데이터:", title.value, content.value);
  
    // 게시 완료 후 메인 페이지로 이동
    router.push({ name: "community" });
  };
  </script>
  
  <style scoped>
  .card {
    background-color: #fff; /* 배경색 */
  border: 1px solid #cacaca; /* 테두리 */
  border-radius: 8px; /* 둥근 모서리 */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
  transition: box-shadow 0.3s ease, transform 0.3s ease; /* 전환 효과 */
  padding: 20px; /* 내부 여백 */
  }
  
  .form-label {
    font-weight: bold;
  }
  
  .form-control {
    border-radius: 5px;
    border: 1px solid #dee2e6;
  }
  
  textarea.form-control {
    resize: none; /* 사용자가 크기를 변경하지 못하도록 고정 */
  }
  
  .btn-common {
    padding: 10px 20px;
    border-radius: 5px;
  }
  
  .btn-mint {
    background-color: var(--mint-color);
    color: white;
    border: none;
    transition: background-color 0.2s ease-in-out;
  }
  
  .btn-mint:hover {
    background-color: #3cb371;
  }
  
  .section-title {
    font-size: 24px;
    font-weight: bold;
  }
  </style>
  