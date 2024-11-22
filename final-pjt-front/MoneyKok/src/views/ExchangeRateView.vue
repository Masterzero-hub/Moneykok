<template>
    <div>
        <div class="container">
            <h2 class="mb-4">환율 계산기</h2>

            <!-- 검색 조건 -->
            <div class="search-card p-4 mb-5 shadow-sm">

                <!-- 상태 선택 -->
                <div class="row mb-3 align-items-center">
                    <label class="col-md-2 col-form-label">상태 선택</label>
                    <div class="col-md-10">
                        <div class="search-btn">
                            <button v-for="item in states" :key="item" class="btn"
                                :class="{ 'btn-primary': state === item, 'btn-outline-primary': state !== item }"
                                @click="setState(item)">
                                {{ item }}
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 통화 선택 -->
                <div class="row mb-3 align-items-center">
                    <label class="col-md-2 col-form-label">통화 선택</label>
                    <div class="col-md-10">
                        <select v-model="country" class="form-select">
                            <option v-for="(currency, index) in currencies" :key="index" :value="currency">
                                {{ currency }}
                            </option>
                        </select>
                    </div>
                </div>

            </div>

            <!-- 금액 입력 -->
            <div class="row mb-3 align-items-center">
                <label class="col-md-2 col-form-label">금액 입력</label>
                <div class="col-md-10">
                    <input type="number" v-model="exchangeBefore" class="form-control"
                        placeholder="금액을 입력하세요 (해당 통화)" />
                </div>
            </div>

            <!-- 계산 결과 -->
            <div class="result-card p-4 mb-5 shadow-sm">
                <h5 class="mb-3">계산 결과</h5>
                <div>
                    <p v-if="exchangeAfter !== '조건을 입력해주세요.'">
                        계산 결과는
                        <strong>
                            {{ exchangeBefore }} ({{ country }}) ->
                            {{ exchangeAfter }}
                        </strong>
                        입니다.
                    </p>
                    <p v-else>결과를 보기 위해 상태, 통화, 금액을 모두 입력하세요.</p>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import { ref, watch, onMounted } from "vue";
import { useExchangeStore } from "@/stores/exchangerate"; // 환율 정보를 가져올 Store 사용

const store = useExchangeStore();

// 상태 (송금 받을 때, 송금 보낼 때, 매매 기준율)
const states = ["송금 받을 때", "송금 보낼 때", "매매 기준율"];
const state = ref(""); // 현재 선택된 상태

// 선택 가능한 통화
const currencies = [
    "아랍에미리트 (AED)",
    "호주 (AUD)",
    "바레인 (BHD)",
    "브루나이 (BND)",
    "캐나다 (CAD)",
    "스위스 (CHF)",
    "중국 (위안화, CNY)",
    "덴마크 (DKK)",
    "유럽연합 (유로, EUR)",
    "영국 (GBP)",
    "홍콩 (HKD)",
    "인도네시아 (IDR)",
    "일본 (JPY)",
    "한국 (KRW)",
    "쿠웨이트 (KWD)",
    "말레이시아 (MYR)",
    "노르웨이 (NOK)",
    "뉴질랜드 (NZD)",
    "사우디아라비아 (SAR)",
    "스웨덴 (SEK)",
    "싱가포르 (SGD)",
    "태국 (THB)",
    "미국 (USD)",
];

// 선택된 통화 및 환율 정보
const country = ref(""); // 선택된 통화
const exchangeDetail = ref({}); // 선택된 통화의 세부 정보
const exchangeBefore = ref(""); // 입력된 금액
const exchangeAfter = ref("조건을 입력해주세요."); // 계산 결과

// Store에서 환율 정보 가져오기
onMounted(() => {
    store.getExchangeInfo();
});

// 상태 선택
const setState = (item) => {
    state.value = state.value === item ? "" : item; // 상태 토글
    console.log("현재 상태:", state.value); // 상태 저장 확인
    updateExchangeDetail();
};


// 선택된 통화 및 상태 변경 시 환율 정보 업데이트
const updateExchangeDetail = () => {
    // 선택된 통화의 상세 정보 검색
    exchangeDetail.value =
        store.exchangeInfo.find((item) => item.cur_nm.includes(country.value)) ||
        {};
};

// 환율 계산
const calculateExchange = () => {
    console.log("계산 전 상태:", state.value, country.value, exchangeBefore.value);
    if (!(state.value && country.value && exchangeBefore.value)) {
        exchangeAfter.value = "조건을 입력해주세요.";
        return;
    }

    if (state.value == "송금 받을 때" && exchangeDetail.value.ttb) {
        exchangeDetail.value.ttb = exchangeDetail.value.ttb.replace(",", "");
        exchangeAfter.value =
            Number(exchangeBefore.value) * Number(exchangeDetail.value.ttb);
    } else if (state.value == "송금 보낼 때" && exchangeDetail.value.tts) {
        exchangeDetail.value.tts = exchangeDetail.value.tts.replace(",", "");
        exchangeAfter.value =
            Number(exchangeBefore.value) * Number(exchangeDetail.value.tts);
    } else if (state.value == "매매 기준율" && exchangeDetail.value.deal_bas_r) {
        exchangeDetail.value.deal_bas_r = exchangeDetail.value.deal_bas_r.replace(
            ",",
            ""
        );
        exchangeAfter.value =
            Number(exchangeBefore.value) * Number(exchangeDetail.value.deal_bas_r);
    } else if (!(state.value && country.value && exchangeBefore.value)) {
        exchangeAfter.value = "조건을 입력해주세요.";
    };
}
onMounted(() => {
    store.getExchangeInfo();
    console.log("가져온 환율 정보:", store.exchangeInfo); // Store 데이터 확인
});

// 조건이 충족될 때 자동으로 `calculateExchange` 실행
watch(
    [state, country, exchangeBefore],
    ([newState, newCountry, newBefore]) => {
        if (newState && newCountry && newBefore) {
            calculateExchange();
        } else {
            exchangeAfter.value = "조건을 입력해주세요.";
        }
    }
);
</script>

<style scoped>
.search-card,
.result-card {
    background-color: #fff;
    border: 1px solid #cacaca;
    border-radius: 8px;
    padding: 20px;
}

.search-btn .btn {
    border-color: var(--mint-color) !important;
    margin-right: 15px;
    color: var(--mint-color);
}

.search-btn .btn:hover {
    background-color: var(--mint-color);
    color: white;
    border-color: var(--mint-color) !important;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.search-btn .btn-primary {
    background-color: var(--mint-color);
    color: white;
    border-color: var(--mint-color) !important;
}

.search-btn .btn-outline-primary {
    border-color: var(--mint-color) !important;
}
</style>