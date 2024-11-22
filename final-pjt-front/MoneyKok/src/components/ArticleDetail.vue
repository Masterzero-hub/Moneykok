<template>
  <div class="container mt-5">
    <!-- 게시글 상세 조회 헤더 -->
    <div class="row align-items-center mb-4">
      <h2 class="section-title col">게시글 상세</h2>
      <button class="btn-common btn-mint col-auto" @click="goBack">
        목록으로 돌아가기
      </button>
    </div>

    <!-- 게시글 상세 카드 -->
    <div class="card shadow-sm p-4">
      <div class="card-body">
        <div class="mb-3">
          <label for="title" class="form-label">제목</label>
          <input
            type="text"
            id="title"
            v-model="editableTitle"
            class="form-control"
            :disabled="!isEditing"
          />
        </div>

        <div class="mb-3">
          <label for="content" class="form-label">내용</label>
          <textarea
            id="content"
            v-model="editableContent"
            class="form-control"
            rows="8"
            :disabled="!isEditing"
          ></textarea>
        </div>

        <!-- 버튼 섹션 -->
        <div class="button-container">
          <div v-if="!isEditing">
            <button
              class="btn-common btn-outline-primary"
              @click="isEditing = true"
            >
              수정
            </button>
            <button class="btn-common btn-danger" @click="deleteArticle">
              삭제
            </button>
          </div>
          <div v-else class="d-flex gap-3">
            <button
              class="btn-common btn-outline-secondary"
              @click="cancelEdit"
            >
              취소
            </button>
            <button class="btn-common btn-mint" @click="submitChanges">
              저장
            </button>
          </div>
        </div>
      </div>
    </div>


    <!-- 댓글 목록 -->
    <div class="card shadow-sm p-4 mt-4">
    <h3 class="section-title mb-3">댓글</h3>
    <div v-if="article.comments?.length > 0">
        <ul class="list-group">
        <li
            v-for="comment in article.comments"
            :key="comment.id"
            class="list-group-item d-flex flex-column"
        >
            <div class="d-flex justify-content-between align-items-center">
            <div>
                <strong>{{ comment.author }}</strong>
                <small class="text-muted ms-2">{{ comment.created_at }}</small>
            </div>
            <button
                class="btn btn-sm btn-danger"
                @click="removeComment(comment.id)"
            >
                삭제
            </button>
            </div>
            <p class="mb-0 mt-2 text-secondary">{{ comment.content }}</p>
        </li>
        </ul>
    </div>
    <div v-else>
        <p class="text-muted text-center">아직 댓글이 없습니다.</p>
    </div>
    </div>

    <!-- 댓글 작성 -->
    <div class="card shadow-sm p-4 mt-4">
      <h3 class="section-title">댓글 작성</h3>
      <textarea
        class="form-control mt-3"
        rows="3"
        v-model="comment"
        placeholder="댓글을 입력하세요"
      ></textarea>
      <div class="text-end">
        <button
          class="btn-common mt-3"
          @click="submitComment"
          :disabled="comment.trim() === ''"
        >
          댓글 작성
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { storeToRefs } from "pinia"; // storeToRefs 사용
import { useCommunityStore } from "@/stores/community";

const router = useRouter();
const route = useRoute();
const store = useCommunityStore();

const { article, comment, getArticleDetail, addComment, deleteComment  } = storeToRefs(store); 

console.log(article.value);


// 상태 변수
const articleId = route.params.article_id;
const editableTitle = ref("");
const editableContent = ref("");
const isEditing = ref(false);


// 목록으로 돌아가기
const goBack = () => {
  router.push({ name: "community" });
};

// 게시글 데이터 로드
onMounted(() => {
  store.getArticleDetail(articleId).then((article) => {
    editableTitle.value = article.title;
    editableContent.value = article.content;
  });
});

// 수정 취소
const cancelEdit = () => {
  isEditing.value = false;
  getArticleDetail(articleId).then((article) => {
    editableTitle.value = article.title;
    editableContent.value = article.content;
  });
};

// 수정 저장
const submitChanges = () => {
  const updatedArticle = {
    id: articleId, // articleId를 추가
    title: editableTitle.value,
    content: editableContent.value,
  };
  store.updateArticle(updatedArticle).then(() => {
    alert("수정이 완료되었습니다.");
    isEditing.value = false;
  });
};

// 게시글 삭제
const deleteArticle = () => {
  if (confirm("정말로 삭제하시겠습니까?")) {
    store.deleteArticle(articleId).then(() => {
      alert("게시글이 삭제되었습니다.");
      router.push({ name: "community" }); // 삭제 후 목록으로 이동
    });
  }
};

// 댓글 작성
const submitComment = () => {
  store.addComment(articleId, comment.value).then((newComment) => {
    // 새 댓글을 article.comments에 추가
    if (article.value.comments) {
      article.value.comments.push(newComment);
    } else {
      article.value.comments = [newComment];
    }

    // 댓글 입력 필드 초기화
    comment.value = "";
    alert("댓글이 작성되었습니다.");
  });
};

const removeComment = (commentId) => {
  if (confirm("댓글을 삭제하시겠습니까?")) {
    store.deleteComment(articleId, commentId).then(() => {
      // 댓글 목록에서 삭제
      article.value.comments = article.value.comments.filter((c) => c.id !== commentId);
      alert("댓글이 삭제되었습니다.");
    });
  }
};

</script>

<style scoped>
.card {
  background-color: #fff;
  border: 1px solid #cacaca;
  border-radius: 8px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.form-label {
  font-weight: bold;
}

.form-control {
  border-radius: 5px;
  border: 1px solid #dee2e6;
}

textarea.form-control {
  resize: none;
}


/* 버튼 컨테이너 스타일 */
.button-container {
  display: flex;
  justify-content: flex-end; /* 버튼을 오른쪽으로 정렬 */
  gap: 10px; /* 버튼 사이의 간격 */
}

.btn-common {
  padding: 10px 20px;
  border-radius: 5px;
  margin: 10px;
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
