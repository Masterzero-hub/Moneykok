import { ref, computed, reactive } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRoute } from "vue-router";

export const useDepositsStore = defineStore(
  "deposits",
  () => {
    const products = ref([]);

    const filters = ref({
      join_term: null,
      amount: null,
      bank: [],
      conditions: [],
    });

    const filteredProducts = ref([]);


    // const saveProducts
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


    const getProductDetail = (depositCode) => {
      console.log("API 요청 시작 - depositCode:", depositCode);
      axios
        .get(`http://127.0.0.1:8000/deposits/deposit-detail/${depositCode}/`)
        .then((res) => {
          productDetail.value = res.data;
        })
        .catch((error) => {
          console.error("상세 데이터를 불러오는 중 오류가 발생했습니다:", error);
        });
    };

    // // const saveProducts
    // const  = () => {
    //   axios
    //     .get("http://127.0.0.1:8000/deposits/deposits-list/")
    //     .then((res) => {
    //       products.value = res.data;
    //       console.log(products);
    //     })
    //     .catch((error) => {
    //       console.error("데이터를 불러오는 중 오류가 발생했습니다:", error);
    //     });
    // };

    const productDetail = ref([]);

    const getFilteredProducts = () => {
      // 요청에 사용할 필터 데이터를 JSON 문자열로 변환
      const params = {
        join_term: filters.value.join_term || null, // 단일 값 (가입 기간)
        amount: filters.value.amount || null,      // 단일 값 (가입 금액)
        bank: filters.value.bank.length > 0 ? JSON.stringify(filters.value.bank) : null, // JSON 문자열 (은행 필터)
        conditions: filters.value.conditions.length > 0 ? JSON.stringify(filters.value.conditions) : null, // JSON 문자열 (우대 조건)
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

    return { products, productDetail, filters, filteredProducts,
      getProducts, getProductDetail, getFilteredProducts };
  },
  { persist: true }
);
