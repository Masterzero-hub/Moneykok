import { defineStore } from "pinia";
import { ref } from "vue";
import axios from 'axios';

export const useExchangeStore = defineStore("exchange", () => {

  // 상태 정의
  const curName = ref([]);
  const exchangeInfo = ref([]);

  // 환율 정보 가져오기 함수
  const getExchangeInfo = () => {
    axios.get('http://127.0.0.1:8000/exchange/')
      .then((res) => {
        console.log(res)
        // res.data.forEach(item => {
        //   curName.value = item.cur_nm);
        //   exchangeInfo.value = item;
        // });
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return { getExchangeInfo, exchangeInfo, curName };
});