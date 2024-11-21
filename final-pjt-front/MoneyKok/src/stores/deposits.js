import { ref, computed, reactive } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const useDepositsStore = defineStore(
  "deposits",
  () => {
    const products = ref([]);

    const filters = reactive({
      term: null,
      amount: null,
      bank: null,
      conditions: ["거래연동", "사용실적"],
    });

    const filteredProducts = ref({
      id: 44,
      fin_prdt_cd: "10511008001166004",
      bank: {
        id: 21,
        fin_co_no: "0010016",
        kor_co_nm: "아이엠뱅크",
      },
      fin_prdt_nm: "iM함께예금",
      etc_note: "계좌당 가입 최저한도 : 100만원",
      join_deny: 1,
      join_member: "실명의 개인 및 개인사업자",
      join_way: "영업점,인터넷,스마트폰",
      spcl_cnd:
        '*최고우대금리: 연0.45%p\n-전월 총 수신 평잔실적 또는 상품 가입 전 첫만남플러스 통장 보유시 \n-당행 주택청약상품보유 \n-신규일 "iM함께적금" 동시 가입 및 만기 보유 \n-당행 오픈뱅킹서비스에 다른 은행 계좌 등록시 \n각 연0.10%p                       \n*해당 상품을 인터넷/모바일뱅킹을 통해 가입 시: 연0.05%p',
      options: [
        {
          id: 174,
          intr_rate_type_nm: "단리",
          intr_rate: 3.05,
          intr_rate2: 3.5,
          save_trm: 12,
          product: 44,
        },
      ],
      special_conditions: [
        {
          category: "거래 연동",
          condition_title: "전월 총 수신 평잔실적",
          condition_content: "전월 총 수신 평잔실적",
          prime_rate: 0.1,
        },
        {
          category: "거래 연동",
          condition_title: "상품 가입 전 첫만남플러스 통장 보유",
          condition_content: "상품 가입 전 첫만남플러스 통장 보유",
          prime_rate: 0.1,
        },
        {
          category: "기타",
          condition_title: "당행 주택청약상품보유",
          condition_content: "당행 주택청약상품보유",
          prime_rate: 0.1,
        },
        {
          category: "신규 가입",
          condition_title: "신규일 iM함께적금 동시 가입 및 만기 보유",
          condition_content: "신규일 iM함께적금 동시 가입 및 만기 보유",
          prime_rate: 0.1,
        },
        {
          category: "거래 연동",
          condition_title: "당행 오픈뱅킹서비스에 다른 은행 계좌 등록",
          condition_content: "당행 오픈뱅킹서비스에 다른 은행 계좌 등록",
          prime_rate: 0.1,
        },
        {
          category: "비대면/모바일 뱅킹",
          condition_title: "인터넷/모바일뱅킹 가입",
          condition_content: "해당 상품을 인터넷/모바일뱅킹을 통해 가입",
          prime_rate: 0.05,
        },
      ],
    });


    // const saveProducts
    const getProducts = () => {
      axios
        .get("http://127.0.0.1:8000/deposits/products-all-list/")
        .then((res) => {
          products.value = res.data;
          console.log(products);
        })
        .catch((error) => {
          console.error("데이터를 불러오는 중 오류가 발생했습니다:", error);
        });
    };

    const productDetail = ref({
      id: 44,
      fin_prdt_cd: "10511008001166004",
      bank: {
        id: 21,
        fin_co_no: "0010016",
        kor_co_nm: "아이엠뱅크",
      },
      fin_prdt_nm: "iM함께예금",
      etc_note: "계좌당 가입 최저한도 : 100만원",
      join_deny: 1,
      join_member: "실명의 개인 및 개인사업자",
      join_way: "영업점,인터넷,스마트폰",
      spcl_cnd:
        '*최고우대금리: 연0.45%p\n-전월 총 수신 평잔실적 또는 상품 가입 전 첫만남플러스 통장 보유시 \n-당행 주택청약상품보유 \n-신규일 "iM함께적금" 동시 가입 및 만기 보유 \n-당행 오픈뱅킹서비스에 다른 은행 계좌 등록시 \n각 연0.10%p                       \n*해당 상품을 인터넷/모바일뱅킹을 통해 가입 시: 연0.05%p',
      options: [
        {
          id: 174,
          intr_rate_type_nm: "단리",
          intr_rate: 3.05,
          intr_rate2: 3.5,
          save_trm: 12,
          product: 44,
        },
      ],
      special_conditions: [
        {
          category: "거래 연동",
          condition_title: "전월 총 수신 평잔실적",
          condition_content: "전월 총 수신 평잔실적",
          prime_rate: 0.1,
        },
        {
          category: "거래 연동",
          condition_title: "상품 가입 전 첫만남플러스 통장 보유",
          condition_content: "상품 가입 전 첫만남플러스 통장 보유",
          prime_rate: 0.1,
        },
        {
          category: "기타",
          condition_title: "당행 주택청약상품보유",
          condition_content: "당행 주택청약상품보유",
          prime_rate: 0.1,
        },
        {
          category: "신규 가입",
          condition_title: "신규일 iM함께적금 동시 가입 및 만기 보유",
          condition_content: "신규일 iM함께적금 동시 가입 및 만기 보유",
          prime_rate: 0.1,
        },
        {
          category: "거래 연동",
          condition_title: "당행 오픈뱅킹서비스에 다른 은행 계좌 등록",
          condition_content: "당행 오픈뱅킹서비스에 다른 은행 계좌 등록",
          prime_rate: 0.1,
        },
        {
          category: "비대면/모바일 뱅킹",
          condition_title: "인터넷/모바일뱅킹 가입",
          condition_content: "해당 상품을 인터넷/모바일뱅킹을 통해 가입",
          prime_rate: 0.05,
        },
      ],
    });

    const fetchFilteredProducts = async () => {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/deposits/filter/",
          filters.value
        );
        products.value = response.data;
      } catch (error) {
        console.error("필터링된 데이터를 가져오는 중 오류가 발생했습니다:", error);
      }
    };

    return { products, getProducts, productDetail, filters, filteredProducts };
  },
  { persist: true }
);
