import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";

export const useAiStore = defineStore("ai", () => {
  const filters = ref({
    productType: "",
    joinTerm: null,
    amount: null,
    bank: [],
    conditions: [],
  });

  const recommendedProducts = ref([
    {
      id: 37,
      fin_prdt_cd: "10120116100011",
      bank: {
        id: 16,
        fin_co_no: "0014807",
        kor_co_nm: "수협은행",
      },
      fin_prdt_nm: "Sh첫만남우대예금",
      etc_note: "-1인 1계좌\n-최저 100만원 이상",
      join_deny: 1,
      join_member: "실명의 개인",
      join_way: "인터넷,스마트폰",
      spcl_cnd:
        "* 최대우대금리:1.05%\n1. 첫거래우대 : 1.0% (신규시) \n  - 최근 1년간 수협은행 예적금 활동계좌 미보유 고객포함\n2. 마케팅전체동의 : 0.05%(신규시) \n3. 스마트폰뱅킹의 상품알리기 : 0.80%(만기시)\n※단위:연%p",
      deposit_min_amount: 100,
      deposit_max_amount: null,
      options: [
        {
          id: 144,
          intr_rate_type_nm: "단리",
          intr_rate: 2.55,
          intr_rate2: 3.6,
          save_trm: 12,
          product: 37,
        },
      ],
      final_intr_rate: 3.6,
      special_conditions: [
        {
          category: "신규 가입",
          condition_title: "첫거래우대",
          condition_content:
            "최근 1년간 수협은행 예적금 활동계좌 미보유 고객 포함",
          prime_rate: 1.0,
        },
        {
          category: "마케팅 및 기타 동의",
          condition_title: "마케팅전체동의",
          condition_content: "신규시",
          prime_rate: 0.05,
        },
        {
          category: "비대면/모바일 뱅킹",
          condition_title: "스마트폰뱅킹의 상품알리기",
          condition_content: "만기시",
          prime_rate: 0.8,
        },
      ],
    },
    {
      id: 3,
      fin_prdt_cd: "10511008000996000",
      bank: {
        id: 3,
        fin_co_no: "0010016",
        kor_co_nm: "아이엠뱅크",
      },
      fin_prdt_nm: "iM주거래우대예금(첫만남고객형)",
      etc_note: "계좌당 가입 최저한도 : 100만원",
      join_deny: 1,
      join_member: "실명의 개인",
      join_way: "영업점,인터넷,스마트폰",
      spcl_cnd:
        "* 최고우대금리 : 연0.65%p              \n - 목돈굴리기예금 최초 가입시 : 연0.20%p\n - 상품 가입 전 최근 1개월 이내 신용(체크)카드 신규 발급 : 연0.20%p\n - 상품 가입 전 최근 1개월 이내 인터넷.폰.모바일앱뱅킹 가입 : 연0.20%p\n * 해당 상품을 인터넷/모바일뱅킹을 통해 가입 : 연0.05%p",
      deposit_min_amount: null,
      deposit_max_amount: null,
      options: [
        {
          id: 11,
          intr_rate_type_nm: "단리",
          intr_rate: 2.22,
          intr_rate2: 2.87,
          save_trm: 6,
          product: 3,
        },
        {
          id: 12,
          intr_rate_type_nm: "단리",
          intr_rate: 2.91,
          intr_rate2: 3.56,
          save_trm: 12,
          product: 3,
        },
        {
          id: 13,
          intr_rate_type_nm: "단리",
          intr_rate: 2.78,
          intr_rate2: 3.43,
          save_trm: 24,
          product: 3,
        },
        {
          id: 14,
          intr_rate_type_nm: "단리",
          intr_rate: 2.8,
          intr_rate2: 3.45,
          save_trm: 36,
          product: 3,
        },
      ],
      final_intr_rate: 3.56,
      special_conditions: [
        {
          category: "신규 가입",
          condition_title: "목돈굴리기예금 최초 가입",
          condition_content: "목돈굴리기예금 최초 가입시",
          prime_rate: 0.2,
        },
        {
          category: "신규 가입",
          condition_title: "신용(체크)카드 신규 발급",
          condition_content:
            "상품 가입 전 최근 1개월 이내 신용(체크)카드 신규 발급",
          prime_rate: 0.2,
        },
        {
          category: "비대면/모바일 뱅킹",
          condition_title: "인터넷/폰/모바일앱뱅킹 가입",
          condition_content:
            "상품 가입 전 최근 1개월 이내 인터넷/폰/모바일앱뱅킹 가입",
          prime_rate: 0.2,
        },
        {
          category: "비대면/모바일 뱅킹",
          condition_title: "인터넷/모바일뱅킹 가입",
          condition_content: "해당 상품을 인터넷/모바일뱅킹을 통해 가입",
          prime_rate: 0.05,
        },
      ],
    },
    {
      id: 3,
      fin_prdt_cd: "10511008000996000",
      bank: {
        id: 3,
        fin_co_no: "0010016",
        kor_co_nm: "아이엠뱅크",
      },
      fin_prdt_nm: "iM주거래우대예금(첫만남고객형)",
      etc_note: "계좌당 가입 최저한도 : 100만원",
      join_deny: 1,
      join_member: "실명의 개인",
      join_way: "영업점,인터넷,스마트폰",
      spcl_cnd:
        "* 최고우대금리 : 연0.65%p              \n - 목돈굴리기예금 최초 가입시 : 연0.20%p\n - 상품 가입 전 최근 1개월 이내 신용(체크)카드 신규 발급 : 연0.20%p\n - 상품 가입 전 최근 1개월 이내 인터넷.폰.모바일앱뱅킹 가입 : 연0.20%p\n * 해당 상품을 인터넷/모바일뱅킹을 통해 가입 : 연0.05%p",
      deposit_min_amount: null,
      deposit_max_amount: null,
      options: [
        {
          id: 11,
          intr_rate_type_nm: "단리",
          intr_rate: 2.22,
          intr_rate2: 2.87,
          save_trm: 6,
          product: 3,
        },
        {
          id: 12,
          intr_rate_type_nm: "단리",
          intr_rate: 2.91,
          intr_rate2: 3.56,
          save_trm: 12,
          product: 3,
        },
        {
          id: 13,
          intr_rate_type_nm: "단리",
          intr_rate: 2.78,
          intr_rate2: 3.43,
          save_trm: 24,
          product: 3,
        },
        {
          id: 14,
          intr_rate_type_nm: "단리",
          intr_rate: 2.8,
          intr_rate2: 3.45,
          save_trm: 36,
          product: 3,
        },
      ],
      final_intr_rate: 3.56,
      special_conditions: [
        {
          category: "신규 가입",
          condition_title: "목돈굴리기예금 최초 가입",
          condition_content: "목돈굴리기예금 최초 가입시",
          prime_rate: 0.2,
        },
        {
          category: "신규 가입",
          condition_title: "신용(체크)카드 신규 발급",
          condition_content:
            "상품 가입 전 최근 1개월 이내 신용(체크)카드 신규 발급",
          prime_rate: 0.2,
        },
        {
          category: "비대면/모바일 뱅킹",
          condition_title: "인터넷/폰/모바일앱뱅킹 가입",
          condition_content:
            "상품 가입 전 최근 1개월 이내 인터넷/폰/모바일앱뱅킹 가입",
          prime_rate: 0.2,
        },
        {
          category: "비대면/모바일 뱅킹",
          condition_title: "인터넷/모바일뱅킹 가입",
          condition_content: "해당 상품을 인터넷/모바일뱅킹을 통해 가입",
          prime_rate: 0.05,
        },
      ],
    },
    // 추가 상품 데이터 생략
  ]);

  
  // ai 상품 추천 요청 함수
  const getRecommendtaion = function(depositCode) {
    axios
      .post(
        `http://127.0.0.1:8000/deposits/join/${depositCode}/`,
        {
          joinTerm: joinTerm.value,
          joinAmount: joinAmount.value,
          finalJoinRate: finalJoinRate.value,
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

  return { filters, recommendedProducts, getRecommendtaion };
});
