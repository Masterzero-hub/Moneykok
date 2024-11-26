<template>
  <div class="container mt-5">
    <!-- 게시글 상세 조회 헤더 -->
    <div class="row align-items-center mb-4">
      <h2 class="section-title col"></h2>
      <button class="btn-common btn-mint col-auto" @click="goBack">
        목록으로 돌아가기
      </button>
    </div>

    <!-- 게시글 상세 카드 -->
    <div v-if="article" class="card shadow-sm p-4" :class="{ 'editing-mode': isEditing }">
      <div class="card-body">
        <!-- 제목 -->
        <div class="mb-3" v-if="isEditing">
          <label for="title" class="form-label">제목</label>
          <input
            type="text"
            id="title"
            v-model="editableTitle"
            class="form-control"
          />
        </div>
        <h3 v-else class="post-title mb-2">{{ editableTitle }}</h3>
        <!-- 작성자 닉네임 -->
        <p v-if="article.user && article.user.nickname" @click="goUserProfile(article.user?.email)">
          작성자: {{ article.user.nickname }}
        </p>
        <p v-else>
          작성자: 알 수 없음
        </p>
        <p class="created_at text-muted mt-0">
          작성일시: {{ article.created_at ? article.created_at.slice(0, 19) : '날짜 정보 없음' }}
        </p>
        <!-- 내용 -->
        <div v-if="isEditing" class="mb-3">
          <label for="content" class="form-label">내용</label>
          <textarea
            id="content"
            v-model="editableContent"
            class="form-control"
            rows="8"
          ></textarea>
        </div>
        <p v-else class="post-content">{{ editableContent }}</p>

        <!-- 버튼 섹션 -->
        <div class="button-container" v-if="isCurrentUserAuthor">
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
      <div v-if="article?.comments?.length > 0">
        <ul class="list-group">
          <li
            v-for="comment in article.comments"
            :key="comment.id"
            class="list-group-item"
          >
            <div class="d-flex justify-content-between">
              <div class="comment-meta">
                <strong>{{ comment.user.nickname }}</strong>
                <small class="text-muted ms-2">{{
                  comment.created_at ? comment.created_at.slice(0, 19) : '날짜 정보 없음'
                }}</small>
              </div>
              <div v-if="isCommentAuthor(comment)">
                <button
                  v-if="!comment.isEditing"
                  class="btn btn-sm"
                  @click="enableEditComment(comment)"
                >
                  수정
                </button>
                <button
                  v-else
                  class="btn btn-sm"
                  @click="submitCommentEdit(comment)"
                >
                  저장
                </button>
                <button class="btn btn-sm" @click="removeComment(comment.id)">
                  삭제
                </button>
              </div>
            </div>
            <div v-if="comment.isEditing">
              <textarea
                v-model="comment.editingContent"
                class="form-control mt-2"
                rows="2"
                placeholder="댓글을 수정하세요"
              ></textarea>
            </div>
            <p v-else class="comment-content mt-2 mb-0">
              {{ comment.content }}
            </p>
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
              class="btn-common btn-mint mt-3"
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
import { ref, onMounted, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { storeToRefs } from "pinia"; // storeToRefs 사용
import { useCommunityStore } from "@/stores/community";
import { useUserStore } from "@/stores/user";

const router = useRouter();
const route = useRoute();
const store = useCommunityStore();
const userStore = useUserStore();

const {
  article,
  comment,
  getArticleDetail,
  addComment,
  deleteComment,
  updateComment,
} = storeToRefs(store);

const { getUserCommunityInfo, userCommunityInfo } = storeToRefs(userStore)

console.log(article.value);

// 게시글 작성자인지 확인 (닉네임)
const { nickname } = storeToRefs(userStore);
const isCurrentUserAuthor = computed(() => {
  return article.value.user?.nickname === nickname.value;
});

// 댓글 작성자인지 확인 (닉네임)
const isCommentAuthor = (comment) => {
  return comment.user.nickname === nickname.value;
};

// 상태 변수
const articleId = route.params.article_id;
const editableTitle = ref("");
const editableContent = ref("");
const isEditing = ref(false);

// 목록으로 돌아가기
const goBack = () => {
  router.push({ name: "community" });
};

const goUserProfile = function (userEmail) {
  router.push({ name : 'userprofile', params: { user_email : userEmail}})
}

onMounted(async () => {
  try {
    const data = await store.getArticleDetail(articleId);
    article.value = data; // 반응형 변수에 데이터 할당
    editableTitle.value = data.title || '';
    editableContent.value = data.content || '';
  } catch (error) {
    console.error('게시글 로딩 오류:', error);
  }
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
      article.value.comments = article.value.comments.filter(
        (c) => c.id !== commentId
      );
      alert("댓글이 삭제되었습니다.");
    });
  }
};

// 댓글 수정 활성화
const enableEditComment = (comment) => {
  comment.isEditing = true;
  comment.editingContent = comment.content; // 기존 내용을 기본값으로 설정
};

// 댓글 수정 저장
const submitCommentEdit = (comment) => {
  if (!comment.editingContent.trim()) {
    alert("내용을 입력해주세요.");
    return;
  }

  store
    .updateComment(articleId, comment.id, comment.editingContent)
    .then(() => {
      comment.content = comment.editingContent; // 수정된 내용 반영
      comment.isEditing = false; // 수정 모드 종료
      alert("댓글이 수정되었습니다.");
    });
};
</script>

<style scoped>
.card {
  background-color: #fff;
  border: 1px solid #cacaca;
  border-radius: 8px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
  transition: none !important; /* 카드 전환 효과 제거 */
}

/* 호버 효과 완전히 제거 */
.card:hover {
  box-shadow: none; /* 호버 시 그림자 변화 제거 */
  transform: none; /* 호버 시 이동 효과 제거 */
}

.card.editing-mode {
  border: 2px solid var(--mint-color);
}

.post-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.author-name {
  font-size: 1rem;
  font-weight: 400;
  color: #6c757d; /* muted color */
  cursor: pointer; /* 호버 시 커서를 포인터로 변경 */
}

.author-name:hover {
  font-weight: 700; /* 볼드 처리 */
  color: #000000; /* 약간 더 어두운 색으로 변경 */
}

.reated_at {
  font-size: 1rem;
  font-weight: 400;
  color: #6c757d; /* muted color */
}


.post-content {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #555;
}

.form-label {
  font-weight: bold;
}

textarea.form-control {
  resize: none;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
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

.section-title {
  font-size: 24px;
  font-weight: bold;
}

/* 댓글 목록 스타일 */
.list-group-item {
  border: none;
  padding: 15px 0;
  border-bottom: 1px solid #dee2e6;
}

.list-group-item:last-child {
  border-bottom: none;
}

.comment-meta {
  font-size: 0.9rem;
  color: #495057;
}

.comment-content {
  font-size: 1rem;
  color: #212529;
  line-height: 1.5;
}

.comment-meta strong {
  font-weight: bold;
}

.comment-meta small {
  color: #868e96;
}

.text-muted {
  color: #adb5bd !important;
}
</style>
