import { ref, computed, reactive } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRoute, useRouter } from "vue-router";
import { useUserStore } from './user';

export const useDepositsStore = defineStore("deposits", () => {
  // 전체 예금 상품 정보
  const products = ref([]);

  // 전체 예금 상품 정보 조회
  const getProducts = () => {
    axios
      .get("http://127.0.0.1:8000/deposits/deposits-list/")
      .then((res) => {
        products.value = res.data;
      })
      .catch((error) => {
        console.error("데이터를 불러오는 중 오류가 발생했습니다:", error);
      });
  };


  // 개별 예금 상품 상세 정보
  const productDetail = ref([]);

  // 개별 예금 상품 상세 정보 조회 요청
  const getProductDetail = (depositCode) => {
    axios
      .get(`http://127.0.0.1:8000/deposits/deposit-detail/${depositCode}/`)
      .then((res) => {
        productDetail.value = res.data;
      })
      .catch((error) => {
        console.error("상세 데이터를 불러오는 중 오류가 발생했습니다:", error);
      });
  };

  
  
  // 사용자가 입력한 검색 조건
  const filters = ref({
    join_term: null,
    amount: null,
    bank: [],
    conditions: [],
  });
  
  // 검색 조건에 따라 필터링된 상품들
  const filteredProducts = ref([]);

  // 검색 조건에 따라 필터링된 상품 정보 요청
  const getFilteredProducts = () => {
    // 요청에 사용할 필터 데이터를 JSON 문자열로 변환
    const params = {
      join_term: filters.value.join_term || null, // 단일 값 (가입 기간)
      amount: filters.value.amount || null, // 단일 값 (가입 금액)
      bank:
      filters.value.bank.length > 0
      ? JSON.stringify(filters.value.bank)
      : null, // JSON 문자열 (은행 필터)
      conditions:
      filters.value.conditions.length > 0
      ? JSON.stringify(filters.value.conditions)
      : null, // JSON 문자열 (우대 조건)
    };
    
    axios
    .get("http://127.0.0.1:8000/deposits/deposits-list/", { params })
    .then((res) => {
      filteredProducts.value = res.data;
      console.log("필터링 결과:", filteredProducts.value);
    })
    .catch((error) => {
      console.error("필터링 요청 중 오류:", error.response?.data || error);
    });
  };
  

  // 개별 상품 가입 기간 및 금액 
  const joinTerm = ref(null);
  const joinAmount = ref(null);
  const finalJoinRate = ref(null);
  // 선택한 우대조건 담을 변수 (axios로 넘겨주진 않음)
  const joinConditions = ref([]);
  
  // 가입 조건 상태 초기화 함수
  const resetState = () => {
    joinTerm.value = null;
    joinAmount.value = null;
    finalJoinRate.value = null;
    joinConditions.value = [];
  };

  // 로그인 한 사용자 토큰 가져오기
  const userStore = useUserStore()
  const token = computed(() => userStore.token);

  // 예금 상품 가입 처리 함수
  const joinProduct = function(depositCode) {
    axios
      .post(
        `http://127.0.0.1:8000/deposits/deposit-detail/${depositCode}/join/`,
        {
          save_trm: joinTerm.value,
          save_amount: joinAmount.value,
          final_intr_rate: finalJoinRate.value,
        },
        {
          headers: {
            Authorization: `Token ${token.value}`,
          },
        }
      )
      .then((res) => {
        console.log("예금 상품 가입 완료:", res.data);
      })
      .catch((error) => {
        console.error("예금 상품 가입 오류:", error.response?.data || error);
      });
  };

  // 가입 상품 조회
  const joinedProducts = ref([]);

  const getJoinedProducts = () => {
    axios
      .get("http://127.0.0.1:8000/joined-products/", 
        {
          headers: {
            Authorization: `Token ${token.value}`,
          },
        }
      )
      .then((res) => {
        joinedProducts.value = res.data;
      })
      .catch((error) => {
        console.error("가입 상품 데이터를 불러오는 중 오류가 발생했습니다:", error);
      });
  };


  return {
    products,
    productDetail,
    filters,
    filteredProducts,
    joinTerm,
    joinAmount,
    finalJoinRate,
    joinConditions,
    joinedProducts,
    getProducts,
    getProductDetail,
    getFilteredProducts,
    resetState,
    joinProduct,
    getJoinedProducts
  };
});
