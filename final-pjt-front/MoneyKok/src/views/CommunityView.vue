<template>
  <div class="container mt-5">
    <!-- 하단 게시글 섹션 -->
    <section class="all-posts mt-5">
      <div class="table-header">
        <h2 class="section-title">전체 게시글</h2>
        <div>
          <button class="btn-common btn-mint me-2" @click="goMyProfile">내 프로필</button>
          <button class="btn-common btn-mint" @click="goCreateArticle">글쓰기</button>
        </div>
      </div>
      <table class="table table-hover">
        <thead class="table-light">
          <tr>
            <th>No</th>
            <th>제목</th>
            <th>글쓴이</th>
            <th>작성일</th>
            <th>조회수</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(article, index) in paginatedArticles" :key="article.id" @click="goArticleDetail(article.id)">
            <td>{{ currentStartIndex - index }}</td>
            <td>{{ article.title }} ({{ article.comment_count }})</td>
            <td>{{ article.user.nickname }}</td>
            <td>{{ article.created_at.slice(0, 10) }}</td>
            <td>{{ article.view_count }}</td>
          </tr>
        </tbody>
      </table>

      <!-- 페이지네이션 -->
      <nav class="mt-4">
        <ul class="pagination justify-content-center">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link" @click="changePage(currentPage - 1)">&laquo;</button>
          </li>
          <li
            v-for="page in totalPages"
            :key="page"
            class="page-item"
            :class="{ active: currentPage === page }"
          >
            <button class="page-link" @click="changePage(page)">{{ page }}</button>
          </li>
          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <button class="page-link" @click="changePage(currentPage + 1)">&raquo;</button>
          </li>
        </ul>
      </nav>
    </section>
  </div>
</template>

<script setup>
import { useCommunityStore } from "@/stores/community";
import { useUserStore } from "@/stores/user";
import { storeToRefs } from "pinia";
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const communityStore = useCommunityStore();
const userStore = useUserStore();
const { articles } = storeToRefs(communityStore);
const { isLogin } = storeToRefs(userStore);

const goMyProfile = () => {
  router.push({ name: "communityprofile" });
};

const currentPage = ref(1);
const articlesPerPage = 5;
const totalPages = computed(() => Math.ceil(articles.value.length / articlesPerPage));

onMounted(() => {
  if (!isLogin.value) {
    alert("로그인이 필요합니다.");
    router.push({ name: "login" });
    return;
  }

  communityStore.getArticles();
});

const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * articlesPerPage;
  const end = start + articlesPerPage;
  return communityStore.articles.slice(start, end);
});

const currentStartIndex = computed(
  () => articles.value.length - (currentPage.value - 1) * articlesPerPage
);

const changePage = (page) => {
  if (page > 0 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

const goArticleDetail = (articleId) => {
  router.push({ name: "articledetail", params: { article_id: articleId } });
};

const goCreateArticle = () => {
  router.push({ name: "createarticle" });
};
</script>

<style scoped>
.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
}

.table-header > div {
  display: flex;
  gap: 10px;
}

.table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
}

.table thead {
  background-color: #f8f9fa;
}

.table th,
.table td {
  padding: 10px;
  vertical-align: middle;
}

.table th:nth-child(2),
.table td:nth-child(2) {
  width: 50%;
  text-align: left;
  padding-left: 15px;
}

.table-hover tbody tr:hover {
  background-color: #f1f3f5;
}

.table-light th {
  font-weight: bold;
  color: #495057;
}

.pagination .page-item .page-link {
  color: black;
  background-color: #fff;
  border: 1px solid #dee2e6;
}

.pagination .page-item:hover .page-link {
  background-color: #e9ecef;
}

.pagination .page-item.active .page-link {
  background-color: lightgray;
}
</style>
