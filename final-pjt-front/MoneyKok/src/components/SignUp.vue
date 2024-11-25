<template>
  <div class="container mt-5">
    <form @submit.prevent="handleSubmit">
      <!-- 이름 -->
      <div class="mb-3">
        <label for="name" class="form-label">이름</label>
        <input
          type="text"
          id="name"
          class="form-control"
          v-model="store.name"
          placeholder="홍길동"
          :class="{ 'is-invalid': store.nameError }"
        />
        <div class="invalid-feedback" v-if="store.nameError">
          {{ store.nameError }}
        </div>
      </div>

      <!-- 닉네임 -->
      <div class="mb-3">
        <label for="nickname" class="form-label">닉네임</label>
        <input
          type="text"
          id="nickname"
          class="form-control"
          v-model="store.nickname"
          placeholder="동에 번쩍 서에 번쩍 홍길동"
        />
      </div>

      <!-- 이메일 -->
      <div class="mb-3">
        <label for="email" class="form-label">이메일</label>
        <div class="email-input">
          <input
            type="email"
            id="email"
            class="form-control"
            v-model="store.email"
            @blur="store.checkEmail"
            placeholder="example@example.com"
            :class="{ 'is-invalid': store.emailHasError }"
          />
          <div class="invalid-feedback" v-if="store.emailHasError">
            {{ store.emailError }}
          </div>
          <button
            type="button"
            class="btn-small-common btn-mint"
            @click="sendVerificationCode"
            v-if="!store.codeSent"
          >
            인증번호 발송
          </button>
          <button
            type="button"
            class="btn-small-common btn-mint"
            @click="resendVerificationCode"
            v-if="store.codeSent"
          >
            인증번호 재발송
          </button>
        </div>

        <!-- 인증 번호 입력 필드 -->
        <div v-if="store.codeSent" class="verification-code mt-3">
          <input
            type="text"
            id="verificationCode"
            class="form-control"
            v-model="store.verificationCode"
            placeholder="인증번호를 입력하세요"
          />
          <button
            type="button"
            class="btn-small-common btn-mint"
            @click="checkVerificationCode"
          >
            인증번호 확인
          </button>
        </div>
      </div>

      <!-- 비밀번호 -->
      <div class="mb-3">
        <label for="password" class="form-label">비밀번호</label>
        <input
          type="password"
          id="password"
          class="form-control"
          v-model="store.password"
          @blur="store.checkPassword"
          placeholder="비밀번호를 입력하세요"
          :class="{ 'is-invalid': store.passwordHasError }"
        />
        <div class="invalid-feedback" v-if="store.passwordHasError">
          {{ store.passwordError }}
        </div>
      </div>

      <!-- 비밀번호 확인 -->
      <div class="mb-3">
        <label for="confirmPassword" class="form-label">비밀번호 확인</label>
        <input
          type="password"
          id="confirmPassword"
          class="form-control"
          v-model="store.confirmPassword"
          @blur="store.checkConfirmPassword"
          placeholder="비밀번호를 다시 입력하세요"
          :class="{ 'is-invalid': store.confirmPasswordError }"
        />
        <div class="invalid-feedback" v-if="store.confirmPasswordError">
          {{ store.confirmPasswordError }}
        </div>
      </div>

      <!-- 휴대폰 번호 -->
      <div class="mb-3">
        <label for="phone" class="form-label">휴대폰 번호</label>
        <input
          type="text"
          id="phone"
          class="form-control"
          v-model="store.formattedPhone"
          @input="store.formatPhoneNumber"
          placeholder="010-1234-5678"
          :class="{ 'is-invalid': store.phoneHasError }"
        />
        <div class="invalid-feedback" v-if="store.phoneHasError">
          {{ store.phoneError }}
        </div>
      </div>

      <!-- 생년월일 -->
      <div class="mb-3">
        <label class="form-label">생년월일</label>
        <div class="row">
          <div class="col">
            <input
              type="text"
              class="form-control"
              v-model="store.birthYear"
              placeholder="년 (예 : 2000)"
            />
          </div>
          <div class="col">
          <select class="form-select" v-model="store.birthMonth">
            <option disabled value="">월을 선택하세요</option> <!-- Placeholder 역할 -->
            <option v-for="month in 12" :key="month" :value="month">{{ month }}</option>
          </select>
          </div>
          <div class="col">
            <input
              type="text"
              class="form-control"
              v-model="store.birthDay"
              placeholder="일 (예 : 10)"
            />
          </div>
        </div>
      </div>

      <!-- 성별 -->
      <div class="mb-3">
        <label class="form-label">성별</label>
        <div class="gender-radios">
          <div class="radio-group">
            <input
              type="radio"
              id="male"
              value="남성"
              v-model="store.gender"
            />
            <label for="male" class="form-check-label">남성</label>
            <input
              type="radio"
              id="female"
              value="여성"
              v-model="store.gender"
            />
            <label for="female" class="form-check-label">여성</label>
          </div>
        </div>
      </div>

      <!-- 연봉 -->
      <div class="mb-3">
        <label for="salary" class="form-label">연봉 (만원)</label>
        <input
          type="number"
          id="salary"
          class="form-control"
          v-model="store.salary"
          placeholder="예: 3000"
        />
      </div>

      <!-- 제출 버튼 -->
      <button type="submit" class="btn-small-common btn-mint">가입하기</button>
    </form>
  </div>
</template>


<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
const store = useUserStore()
const router = useRouter()

const sendVerificationCode = () => {
  store.checkEmail(); // `store.` 추가
  if (store.emailHasError) return; // `store.` 추가

  axios
    .post("http://127.0.0.1:8000/accounts/signup/send-code-email/", {
      email: store.email, // `store.` 추가
    })
    .then(() => {
      store.codeSent = true; // `store.` 추가
      alert("인증번호가 전송되었습니다.");
    })
    .catch(() => {
      alert("인증번호 전송에 실패했습니다.");
    });
};

const resendVerificationCode = () => {
  sendVerificationCode();
};

const checkVerificationCode = () => {
  axios
    .post("http://127.0.0.1:8000/accounts/signup/verify-email/", {
      email: store.email, // `store.` 추가
      code: store.verificationCode, // `store.` 추가
    })
    .then(() => {
      store.codeSent = true; // `store.` 추가
      alert("이메일 인증에 성공하였습니다.");
      store.verificationCode = null
      store.codeSent = false
    })
    .catch(() => {
      alert("이메일 인증에 실패했습니다.");
    });
};

const handleSubmit = () => {
  store.checkName(); // `store.` 추가
  store.checkEmail(); // `store.` 추가
  store.checkPassword(); // `store.` 추가
  store.checkConfirmPassword(); // `store.` 추가
  store.checkPhone(); // `store.` 추가

  if (
    !store.nameError && // `store.` 추가
    !store.emailHasError && // `store.` 추가
    !store.passwordHasError && // `store.` 추가
    !store.confirmPasswordError && // `store.` 추가
    !store.phoneHasError // `store.` 추가
  ) {
    const payload = {
      name: store.name, // `store.` 추가
      email: store.email, // `store.` 추가
      nickname: store.nickname, // `store.` 추가
      password: store.password, // `store.` 추가
      phone: store.formattedPhone, // `store.` 추가
      birthdate: `${store.birthYear}-${store.birthMonth}-${store.birthDay}`, // `store.` 추가
      gender: store.gender, // `store.` 추가
      income: store.salary, // `store.` 추가
    };

    console.log("Payload data being sent:", payload);

    axios
      .post("http://127.0.0.1:8000/accounts/signup/", payload)
      .then(() => {
        
        alert("회원가입이 완료되었습니다!");
        return axios.post("http://127.0.0.1:8000/accounts/login/", {
          email: store.email, // `store.` 추가
          password: store.password, // `store.` 추가
        });
      })
      .then((res) => {
        console.log(res.data);
        store.token = res.data.key; // `store.` 추가
        console.log("자동 로그인되었습니다!");
        router.push({ name: "home" });
      })
      .catch((err) => {
        console.error(err);
        alert("회원가입 중 오류가 발생했습니다.");
      });
  }
};
</script>


<style>
/* 회원가입 페이지 스타일 */
.container {
  max-width: 600px; /* 페이지의 최대 너비 */
  margin: 0 auto; /* 가운데 정렬 */
  padding: 60px 0px 80px ;  /* 내부 여백 */
}

.email-input {
  display: flex; /* 요소들을 가로로 배치 */
  align-items: center; /* 버튼과 입력 필드의 세로 정렬 */
  gap: 10px; /* 입력 필드와 버튼 사이의 공백 */
}

.email-input input[type="email"] {
  flex-grow: 1; /* 입력 필드가 가능한 한 넓게 확장되도록 설정 */
}

.email-input button {
  white-space: nowrap; /* 버튼 텍스트 줄바꿈 방지 */
}

.verification-code {
    display: flex; /* 요소들을 가로로 배치 */
    align-items: center; /* 버튼과 입력 필드의 세로 정렬 */
    gap: 10px; /* 입력 필드와 버튼 사이의 공백 */
}

.radio-group {
  display: flex;
  align-items: center;
  gap: 5px; /* 라디오 버튼과 라벨 사이의 간격 */
}

button[type="submit"] {
  display: block; /* 블록 요소로 설정 */
  margin: 20px auto 0 auto; /* 상단 여백 추가, 좌우 중앙 정렬 */
}

/* 반응형 */
@media (max-width: 576px) {
  .container {
    padding: 10px; /* 작은 화면에서는 패딩 감소 */
  }

  .email-input {
    flex-direction: column; /* 작은 화면에서 세로 배치 */
    align-items: stretch; /* 입력 필드와 버튼을 전체 너비로 */
  }

  .row .col {
    margin-bottom: 10px; /* 작은 화면에서 각 열 간 간격 */
  }
}
</style>