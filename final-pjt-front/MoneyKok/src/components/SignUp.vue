<template>
  <div class="container mt-5">
    <!-- <h3>회원가입</h3> -->
    <form @submit.prevent="handleSubmit">
      <!-- 이름 -->
      <div class="mb-3">
        <label for="name" class="form-label">이름</label>
        <input
          type="text"
          id="name"
          class="form-control"
          v-model="name"
          placeholder="홍길동"
          :class="{ 'is-invalid': nameError }"
        />
        <div class="invalid-feedback" v-if="nameError">
          {{ nameError }}
        </div>
      </div>

      <!-- 이메일 -->
      <div class="mb-3">
        <label for="email" class="form-label">이메일</label>
        <div class="email-input">
        <input
          type="email"
          id="email"
          class="form-control"
          v-model="email"
          @blur="checkEmail"
          placeholder="example@example.com"
          :class="{ 'is-invalid': emailHasError }"
        />
        <div class="invalid-feedback" v-if="emailHasError">
          {{ emailError }}
        </div>
        <button
          type="button"
          class="btn-small-common btn-mint"
          @click="sendVerificationCode"
          v-if="!codeSent"
        >
          인증번호 발송
        </button>
        <button
          type="button"
          class="btn-common btn-dark"
          @click="resendVerificationCode"
          v-if="codeSent"
        >
          인증번호 재발송
        </button>
        <div v-if="codeSent" class="mt-3">
          <label for="verificationCode" class="form-label">인증번호</label>
          <input
            type="text"
            id="verificationCode"
            class="form-control"
            v-model="verificationCode"
            placeholder="인증번호를 입력하세요"
          />
        </div>
        </div>
      </div>


      <!-- 비밀번호 -->
      <div class="mb-3">
        <label for="password" class="form-label">비밀번호</label>
        <input
          type="password"
          id="password"
          class="form-control"
          v-model="password"
          @blur="checkPassword"
          placeholder="비밀번호를 입력하세요"
          :class="{ 'is-invalid': passwordHasError }"
        />
        <div class="invalid-feedback" v-if="passwordHasError">
          {{ passwordError }}
        </div>
      </div>

      <!-- 비밀번호 확인 -->
      <div class="mb-3">
        <label for="confirmPassword" class="form-label">비밀번호 확인</label>
        <input
          type="password"
          id="confirmPassword"
          class="form-control"
          v-model="confirmPassword"
          @blur="checkConfirmPassword"
          placeholder="비밀번호를 다시 입력하세요"
          :class="{ 'is-invalid': confirmPasswordError }"
        />
        <div class="invalid-feedback" v-if="confirmPasswordError">
          {{ confirmPasswordError }}
        </div>
      </div>

      <!-- 휴대폰 번호 -->
      <div class="mb-3">
        <label for="phone" class="form-label">휴대폰 번호</label>
        <input
          type="text"
          id="phone"
          class="form-control"
          v-model="formattedPhone"
          @input="formatPhoneNumber"
          placeholder="010-1234-5678"
          :class="{ 'is-invalid': phoneHasError }"
        />
        <div class="invalid-feedback" v-if="phoneHasError">
          {{ phoneError }}
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
              v-model="birthYear"
              placeholder="년(4자)"
            />
          </div>
          <div class="col">
            <select class="form-select" v-model="birthMonth">
              <option disabled selected>월</option>
              <option v-for="month in 12" :key="month" :value="month">{{ month }}</option>
            </select>
          </div>
          <div class="col">
            <input
              type="text"
              class="form-control"
              v-model="birthDay"
              placeholder="일"
            />
          </div>
        </div>
      </div>

      <!-- 성별 -->
      <div class="mb-3">
        <label class="form-label">성별</label>
        <div>
          <input
            type="radio"
            id="male"
            value="남성"
            v-model="gender"
          />
          <label for="male" class="form-check-label">남성</label>
          <input
            type="radio"
            id="female"
            value="여성"
            v-model="gender"
          />
          <label for="female" class="form-check-label">여성</label>
        </div>
      </div>

      <!-- 연봉 -->
      <div class="mb-3">
        <label for="salary" class="form-label">연봉 (만원)</label>
        <input
          type="number"
          id="salary"
          class="form-control"
          v-model="salary"
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

// Refs for data
const name = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const formattedPhone = ref(""); // 포맷팅된 휴대폰 번호
const birthYear = ref("");
const birthMonth = ref("");
const birthDay = ref("");
const gender = ref("");
const salary = ref(null);
const verificationCode = ref("");
const codeSent = ref(false);

// Error states
const nameError = ref("");
const emailError = ref("");
const emailHasError = ref(false);
const passwordError = ref("");
const passwordHasError = ref(false);
const confirmPasswordError = ref("");
const phoneError = ref("");
const phoneHasError = ref(false);

// Validation methods
const checkName = () => {
  const specialCharRegex = /[~!@#$%^&*()_+|<>?:{}]/;
  if (!name.value) {
    nameError.value = "이름을 입력해주세요.";
  } else if (specialCharRegex.test(name.value)) {
    nameError.value = "이름에는 특수문자를 사용할 수 없습니다.";
  } else {
    nameError.value = "";
  }
};

const checkEmail = () => {
  const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
  if (!email.value) {
    emailError.value = "이메일을 입력해주세요.";
    emailHasError.value = true;
  } else if (!emailRegex.test(email.value)) {
    emailError.value = "유효한 이메일 형식이 아닙니다.";
    emailHasError.value = true;
  } else {
    emailError.value = "";
    emailHasError.value = false;
  }
};

const checkPassword = () => {
  const passwordRegex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/;
  if (!password.value) {
    passwordError.value = "비밀번호를 입력해주세요.";
    passwordHasError.value = true;
  } else if (!passwordRegex.test(password.value)) {
    passwordError.value =
      "비밀번호는 최소 8자, 영문, 숫자, 특수문자를 포함해야 합니다.";
    passwordHasError.value = true;
  } else {
    passwordError.value = "";
    passwordHasError.value = false;
  }
};

const checkConfirmPassword = () => {
  if (!confirmPassword.value) {
    confirmPasswordError.value = "비밀번호 확인을 입력해주세요.";
  } else if (password.value !== confirmPassword.value) {
    confirmPasswordError.value = "비밀번호가 일치하지 않습니다.";
  } else {
    confirmPasswordError.value = "";
  }
};

const checkPhone = () => {
  const phoneRegex = /^010-\d{4}-\d{4}$/;
  if (!phone.value) {
    phoneError.value = "휴대폰 번호를 입력해주세요.";
    phoneHasError.value = true;
  } else if (!phoneRegex.test(phone.value)) {
    phoneError.value = "유효한 휴대폰 번호 형식이 아닙니다.";
    phoneHasError.value = true;
  } else {
    phoneError.value = "";
    phoneHasError.value = false;
  }
};

// 휴대폰 번호 포맷팅
const formatPhoneNumber = () => {
  let digits = formattedPhone.value.replace(/\D/g, ""); // 숫자만 추출
  if (digits.length <= 3) {
    formattedPhone.value = digits;
  } else if (digits.length <= 7) {
    formattedPhone.value = `${digits.slice(0, 3)}-${digits.slice(3)}`;
  } else {
    formattedPhone.value = `${digits.slice(0, 3)}-${digits.slice(3, 7)}-${digits.slice(7, 11)}`;
  }
};

// Axios requests
const sendVerificationCode = () => {
  checkEmail();
  if (emailHasError.value) return;

  axios
    .post("http://127.0.0.1:8000/accounts/send-verification-code/", {
      email: email.value,
    })
    .then(() => {
      codeSent.value = true;
      alert("인증번호가 전송되었습니다.");
    })
    .catch(() => {
      alert("인증번호 전송에 실패했습니다.");
    });
};

const resendVerificationCode = () => {
  sendVerificationCode();
};

const handleSubmit = () => {
  checkName();
  checkEmail();
  checkPassword();
  checkConfirmPassword();
  checkPhone();

  if (
    !nameError.value &&
    !emailHasError.value &&
    !passwordHasError.value &&
    !confirmPasswordError.value &&
    !phoneHasError.value
  ) {
    const payload = {
      name: name.value,
      email: email.value,

      password: password.value,
      formattedPhone: phone.value,
      birthdate: `${birthYear.value}-${birthMonth.value}-${birthDay.value}`,
      gender: gender.value,
      salary: salary.value,
    };

    axios
      .post("http://127.0.0.1:8000/accounts/signup/", payload)
      .then(() => {
        alert("회원가입이 완료되었습니다!");
      })
      .catch((err) => {
        console.error(err);
        alert("회원가입 중 오류가 발생했습니다.");
      });
  } 
//     alert("모든 항목을 작성해 주세요.");
//   }
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