import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCommunityStore = defineStore('community', () => {
    const recommendedFriends = ref([
        {
          id: 1,
          name: "김현성",
          image: "https://via.placeholder.com/150",
          description: "Hi, I'm a data scientist and love machine learning.",
        },
        {
          id: 2,
          name: "박스프",
          image: "https://via.placeholder.com/150",
          description: "I enjoy discussing finance and technology trends.",
        },
        {
          id: 3,
          name: "최낙우",
          image: "https://via.placeholder.com/150",
          description: "Passionate about AI and innovative technologies.",
        },
        {
          id: 4,
          name: "최낙우",
          image: "https://via.placeholder.com/150",
          description: "Passionate about AI and innovative technologies.",
        },
      ]);
      
      const posts = ref([
        { id: 1, title: "게시글 1", nickname: 'user', comments: 5, views: 48, date: "2024.05.07", likes: 0 },
        { id: 2, title: "게시글 2", nickname: 'user', comments: 0, views: 22, date: "2024.05.07", likes: 0 },
        { id: 3, title: "게시글 3", nickname: 'user', comments: 0, views: 11, date: "2024.05.07", likes: 0 },
        { id: 4, title: "게시글 4", nickname: 'user', comments: 2, views: 23, date: "2024.05.07", likes: 0 },
        { id: 5, title: "게시글 5", nickname: 'user', comments: 1, views: 3, date: "2024.05.07", likes: 0 },
        { id: 6, title: "게시글 1", nickname: 'user', comments: 5, views: 48, date: "2024.05.07", likes: 0 },
        { id: 7, title: "게시글 2", nickname: 'user', comments: 0, views: 22, date: "2024.05.07", likes: 0 },
        { id: 8, title: "게시글 3", nickname: 'user', comments: 0, views: 11, date: "2024.05.07", likes: 0 },
        { id: 9, title: "게시글 4", nickname: 'user', comments: 2, views: 23, date: "2024.05.07", likes: 0 },
        { id: 10, title: "게시글 5", nickname: 'user', comments: 1, views: 3, date: "2024.05.07", likes: 0 },
        { id: 11, title: "게시글 2", nickname: 'user', comments: 0, views: 22, date: "2024.05.07", likes: 0 },
        { id: 12, title: "게시글 3", nickname: 'user', comments: 0, views: 11, date: "2024.05.07", likes: 0 },
        { id: 13, title: "게시글 4", nickname: 'user', comments: 2, views: 23, date: "2024.05.07", likes: 0 },
      ]);




  return { recommendedFriends, posts }
}, { persist: true })