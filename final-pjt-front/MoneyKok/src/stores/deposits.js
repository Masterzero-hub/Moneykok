import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'


export const useDepositsStore = defineStore('deposits', () => {
    const products = ref([]);

    const getProducts = () => {
        axios
          .get("http://127.0.0.1:8000/deposits/products-all-list/")
          .then((res) => {
            products.value = res.data;
            console.log(products)
          })
          .catch((error) => {
            console.error("데이터를 불러오는 중 오류가 발생했습니다:", error);
          })
      };
  
    return { products, getProducts }
}, { persist: true })
