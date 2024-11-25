import { defineStore } from "pinia";
import { ref, computed } from "vue";
import axios from "axios";
import { useUserStore } from './user';

export const useAiStore = defineStore("ai", () => {
  const productType = ref("")

  const recommendedProducts = ref([])


  const userStore = useUserStore()
  const token = computed(() => userStore.token);


  // ai 상품 추천 요청 함수
  const getRecommendtaion = function() {
    axios
      .get(
        `http://127.0.0.1:8000/${productType.value}/recommend-products/`,
        // {
        //   productType: productType.value,
        //   joinTerm: joinTerm.value,
        //   joinAmount: joinAmount.value,
        //   finalJoinRate: finalJoinRate.value,
        // },
        {
          headers: {
            Authorization: `Token ${token.value}`,
          },
        }
      )
      .then((res) => {
        console.log("ai 추천 :", res.data);
        recommendedProducts.value = res.data
      })
      .catch((error) => {
        console.error("AI 상품 추천 오류:", error.response?.data || error);
      });
  };

  return { productType, recommendedProducts, getRecommendtaion };
});
