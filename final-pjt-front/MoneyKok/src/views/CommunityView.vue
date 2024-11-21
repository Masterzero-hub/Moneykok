<template>
    <div class="container mt-5">
      <!-- 추천 친구 섹션 -->
      <section class="recommend-friends mt-5">  
        <h2 class="mb-4">추천 친구</h2>
        <div class="row">
          <div
            v-for="friend in recommendedFriends"
            :key="friend.id"
            class="col-md-3 mb-4"
          >
            <div class="card shadow friend-card">
              <img
                :src="friend.image"
                class="card-img-top friend-card-img"
                :alt="friend.name"
              />
              <div class="card-body text-center">
                <h5 class="card-title">{{ friend.name }}</h5>
                <p class="card-text friend-card-text">{{ friend.description }}</p>
                <button class="btn-small-common btn-mint">친구 추가</button>
              </div>
            </div>
          </div>
        </div>
      </section>
  
      <!-- 전체 게시글 섹션 -->
      <section class="all-posts mt-5">
      <div class="table-header">
          <h2 class="mb-0" >전체 게시글</h2>
          <button class="btn-common btn-mint">글쓰기</button>
      </div>
      <!-- 게시판 테이블 -->
      <table class="table table-hover">
        <thead class="table-light">
          <tr>
            <th>No</th>
            <th>제목</th>
            <th>글쓴이</th>
            <th>작성일</th>
            <th>댓글</th>
            <th>좋아요</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(post, index) in paginatedPosts" :key="post.id">
            <td>{{ currentStartIndex - index }}</td>
            <td>{{ post.title }}</td>
            <td>{{ post.nickname }}</td>
            <td>{{ post.date }}</td>
            <td>{{ post.comments }}</td>
            <td>{{ post.likes }}</td>
          </tr>
        </tbody>
      </table>
  
      <!-- 페이지네이션 -->
      <nav class="mt-4">
        <ul class="pagination justify-content-center">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link" @click="changePage(currentPage - 1)">
              &laquo;
            </button>
          </li>
          <li
            v-for="page in totalPages"
            :key="page"
            class="page-item"
            :class="{ active: currentPage === page }"
          >
            <button class="page-link" @click="changePage(page)">
              {{ page }}
            </button>
          </li>
          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <button class="page-link" @click="changePage(currentPage + 1)">
              &raquo;
            </button>
          </li>
        </ul>
      </nav>
  
      
    </section>
    </div>
  </template>
  
  <script setup>
  import { useCommunityStore } from "@/stores/community";
  import { storeToRefs } from "pinia";
  import { computed, ref } from "vue";
  const store = useCommunityStore();
  
  const { recommendedFriends, posts } = storeToRefs(store);
  
  const currentPage = ref(1);
  const postsPerPage = 5;
  
  // 총 페이지 계산
  const totalPages = computed(() => Math.ceil(posts.value.length / postsPerPage));
  
  // 현재 페이지에 표시할 게시글
  const paginatedPosts = computed(() => {
    const start = (currentPage.value - 1) * postsPerPage;
    const end = start + postsPerPage;
    return posts.value.slice(start, end);
  });
  
  // 현재 페이지 시작 인덱스 계산 (No 열에 표시)
  const currentStartIndex = computed(() => posts.value.length - (currentPage.value - 1) * postsPerPage);
  
  // 페이지 변경 함수
  const changePage = (page) => {
    if (page > 0 && page <= totalPages.value) {
      currentPage.value = page;
    }
  };
  </script>
  
  <style scoped>
  .friend-card {
    width: 100%;
    height: 300px; /* 카드의 높이 고정 */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center; /* 수평으로 가운데 정렬 */
    border-radius: 10px;
    padding: 1rem;
    text-align: center; /* 텍스트 가운데 정렬 */
    box-sizing: border-box; /* 패딩을 포함한 크기 계산 */
  }
  
  .friend-card-img {
    width: 120px;
    height: 120px;
    object-fit: cover;
    border-radius: 50%; /* 원형으로 변경 */
    border: 2px solid #ddd; /* 테두리 추가 */
    /* margin-bottom: 1rem; 이미지와 텍스트 사이 간격 */
  }
  
  .friend-card-text {
    font-size: 11px; /* 텍스트 크기 조정 */
    color: #6c757d; /* 텍스트 색상 조정 */
    overflow: hidden; /* 내용이 넘치면 숨김 */
    text-overflow: ellipsis; /* 말줄임표 표시 */
    white-space: nowrap; /* 한 줄로 제한 */
    width: calc(100% - 2rem); /* 카드 패딩을 제외한 너비 */
    max-width: 100%; /* 부모 카드의 최대 너비에 맞춤 */
    text-align: center; /* 텍스트 가운데 정렬 */
    display: inline-block; /* Flexbox의 영향을 최소화 */
  }
  
  .card-body {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between; /* 텍스트와 버튼 간의 간격 유지 */
    align-items: center;
    text-align: center;
    width: 100%; /* 부모 카드의 너비를 따름 */
  }
  
  .btn {
    margin-top: auto; /* 버튼을 카드 하단에 고정 */
  }
  
  
  .table-header {
    display: flex;
    justify-content: space-between;
    align-items: center; /* 수평으로 가운데 정렬 */
    padding-bottom: 20px;
  }
  
  /* 테이블 스타일 */
  .table {
    width: 100%; /* 테이블의 너비를 컨테이너에 맞게 설정 */
    border-collapse: collapse;
    text-align: center;
  }
  
  .table thead {
    background-color: #f8f9fa; /* 테이블 헤더 배경 */
  }
  
  .table th,
  .table td {
    padding: 10px;
    vertical-align: middle; /* 텍스트 가운데 정렬 */
  }
  
  /* 세로줄 제거 */
  .table th,
  .table td {
    border-right: none; /* 세로줄 제거 */
    border-left: none; /* 세로줄 제거 */
  }
  
  /* "제목" 열을 넓게 설정 */
  .table th:nth-child(2),
  .table td:nth-child(2) {
    width: 50%; /* "제목" 열의 너비 */
    text-align: left; /* 텍스트를 왼쪽 정렬 */
    padding-left: 15px; /* 왼쪽 여백 추가 */
  }
  
  /* 나머지 열의 너비를 균등하게 설정 */
  .table th:nth-child(1),
  .table td:nth-child(1),
  .table th:nth-child(3),
  .table td:nth-child(3),
  .table th:nth-child(4),
  .table td:nth-child(4),
  .table th:nth-child(5),
  .table td:nth-child(5) {
    width: 10%; /* 다른 열은 10%로 균등하게 */
  }
  
  /* 행 호버 효과 */
  .table-hover tbody tr:hover {
    background-color: #f1f3f5; /* 행 호버 시 배경색 */
  }
  
  .table-light th {
    font-weight: bold;
    color: #495057; /* 헤더 텍스트 색상 */
  }
  
  /* 기본 페이지네이션 스타일 */
  .pagination .page-item .page-link {
    color: black; /* 기본 텍스트 색상 */
    background-color: #fff; /* 기본 배경색 */
    border: 1px solid #dee2e6; /* 기본 테두리 */
  }
  
  .pagination .page-item:hover .page-link {
    color: black; /* 호버 시 텍스트 색상 */
    background-color: #e9ecef; /* 호버 시 배경색 */
  }
  
  .pagination .page-item.active .page-link {
    color: var(--dark-color); /* 활성 페이지 텍스트 색상 */
    background-color: lightgray; /* 활성 페이지 배경색 */
  }
  </style>