import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios';
import { useUserStore } from './user';


export const useCommunityStore = defineStore('community', () => {      
      const articles = ref([])
      const article = ref([])

      const userStore = useUserStore()
      const token = computed(() => userStore.token);

      const title = ref("");
      const content = ref("");



      const getArticles = function() {
        axios.get("http://127.0.0.1:8000/communities/",
          {
            headers: {
              Authorization: `Token ${token.value}`
            },
          }
        )
          .then((res) => {
            articles.value = res.data
            console.log('게시글 조회 성공', res.data)
          })
          .catch((error) => {
            console.error("게시글 조회 오류", error);
          });
      }


      const createArticle = function({title, content}) {
          axios.post("http://127.0.0.1:8000/communities/",
            { title,
              content },
            {
              headers: {
                Authorization: `Token ${token.value}`
              },
            }
          )
            .then((res) => {
              console.log('게시글 작성 완료', res.data.title)
            })
            .catch((error) => {
              console.error("게시글 생성 오류", error);
            });
        };
    
      
      // 단일 게시글 상세 정보 요청 함수
      const getArticleDetail = function (articleId) {
        return axios
          .get(`http://127.0.0.1:8000/communities/${articleId}/`, {
            headers: {
              Authorization: `Token ${token.value}`,
            },
          })
          .then((res) => {
            console.log("게시글 상세 조회 성공", res.data);
            article.value = res.data
            return res.data;
          })
          .catch((error) => {
            console.error("게시글 상세 조회 오류", error);
          });
      };  


      const updateArticle = function (updatedArticle) {
        return axios
          .patch(`http://127.0.0.1:8000/communities/${updatedArticle.id}/`, updatedArticle,
            {
            headers: {
              Authorization: `Token ${token.value}`,
            },
          })
          .then((res) => {
            console.log("게시글 수정 완료", res.data.title);
            return res.data;
          })
          .catch((error) => {
            console.error("게시글 수정 오류", error);
          });
      };
            
      const deleteArticle = function (articleId) {
        return axios
          .delete(`http://127.0.0.1:8000/communities/${articleId}/`, {
            headers: {
              Authorization: `Token ${token.value}`,
            },
          })
          .then((res) => {
            console.log("게시글 삭제 완료", res.data);
          })
          .catch((error) => {
            console.error("게시글 삭제 오류", error);
          });
      };
      
      // 댓글 상태
      const comment = ref("");
    
      // 댓글 추가 메서드
      const addComment = (articleId, content) => {
        return axios
          .post(
            `http://127.0.0.1:8000/communities/${articleId}/comments/`,
            { content },
            {
              headers: {
                Authorization: `Token ${token.value}`,
              },
            }
          )
          .then((res) => {
            console.log("댓글 생성 완료:", res.data);
            return res.data; // 생성된 댓글 데이터를 반환
          })
          .catch((error) => {
            console.error("댓글 생성 오류", error);
          });
      };

      // 댓글 삭제 메서드
      const deleteComment = (articleId, commentId) => {
        return axios
          .delete(`http://127.0.0.1:8000/communities/${articleId}/comments/${commentId}/`, {
            headers: {
              Authorization: `Token ${token.value}`,
            },
          })
          .then((res) => {
            console.log("댓글 삭제 완료:", res.data);
            return res.data; // 삭제 결과 반환
          })
          .catch((error) => {
            console.error("댓글 삭제 오류", error);
          });
      };


      // 댓글 수정 메서드
      const updateComment = (articleId, commentId, content) => {
        return axios
          .patch(
            `http://127.0.0.1:8000/communities/${articleId}/comments/${commentId}/`,
            { content },
            {
              headers: {
                Authorization: `Token ${token.value}`,
              },
            }
          )
          .then((res) => {
            console.log("댓글 수정 완료:", res.data);
            return res.data;
          })
          .catch((error) => {
            console.error("댓글 수정 오류", error);
          });
      };

  return { articles, article, title, content, comment,
    getArticles, createArticle, getArticleDetail, updateArticle, deleteArticle, addComment, deleteComment, updateComment }
})