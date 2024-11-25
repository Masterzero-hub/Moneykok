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
    .then((response) => {
      response.data.forEach(item => {
        curName.value.push(item.cur_nm);
        exchangeInfo.value.push(item)
      });
      console.log('curNa')
    })
      .catch((error) => {
        console.log(error);
      });
  };

  return { getExchangeInfo, exchangeInfo, curName };
});