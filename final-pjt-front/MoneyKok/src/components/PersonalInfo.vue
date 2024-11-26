<template>
  <div class="container mt-5">
    <form>
      <!-- 이름 -->
      <div class="mb-3">
        <label for="name" class="form-label">이름</label>
        <input
          disabled
          type="text"
          id="name"
          class="form-control"
          v-model="store.name"
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
            disabled
            type="email"
            id="email"
            class="form-control"
            v-model="store.email"
            @blur="store.checkEmail"
            :class="{ 'is-invalid': store.emailHasError }"
          />
          <div class="invalid-feedback" v-if="store.emailHasError">
            {{ store.emailError }}
          </div>
        </div>
      </div>

      <!-- 비밀번호 -->
      <div class="mb-3">
        <label for="password" class="form-label">비밀번호</label>
        <br />
        <button
          type="button"
          class="btn-small-common btn-mint"
          style="width: 100%"
          @click="goPasswordChange"
        >
          비밀번호 수정하기
        </button>
      </div>

      <!-- 휴대폰 번호 -->
      <div class="mb-3">
        <label for="phone" class="form-label">휴대폰 번호</label>
        <input
          type="text"
          id="phone"
          class="form-control"
          v-model="store.formattedPhone"
          @input="store.formattedPhone"
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
              placeholder="년(ex.2000)"
            />
          </div>
          <div class="col">
            <select class="form-select" v-model="store.birthMonth">
              <option disabled value="">월을 선택하세요</option>
              <!-- Placeholder 역할 -->
              <option v-for="month in 12" :key="month" :value="month">
                {{ month }}
              </option>
            </select>
          </div>
          <div class="col">
            <input
              type="text"
              class="form-control"
              v-model="store.birthDay"
              placeholder="일(ex.10)"
            />
          </div>
        </div>
      </div>

      <!-- 성별 -->
      <div class="mb-3">
        <label class="form-label">성별</label>
        <div class="gender-radios">
          <div class="radio-group">
            <input type="radio" id="male" value="남성" v-model="store.gender" />
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
        <label for="income" class="form-label">연봉 (만원)</label>
        <input
          type="number"
          id="income"
          class="form-control"
          v-model="store.income"
        />
      </div>

      <!-- 제출 버튼 -->
      <div class="btn-group">
        <button
          type="submit"
          class="btn-small-common btn-mint"
          @click.prevent="handleUpdate"
        >
          수정하기
        </button>
        <button
          type="submit"
          class="btn-small-common btn-dark"
          @click.prevent="handleSignOut"
        >
          회원탈퇴
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';
import { storeToRefs } from "pinia"; // storeToRefs 사용
import { useUserStore } from "@/stores/user";

const router = useRouter();
const route = useRoute();
const store = useUserStore()

const { isLogin, name, nickname, email, password, confirmPassword, newPassword, confirmNewPassword, phone, formattedPhone, birthYear, birthMonth, birthDay, birthDate, gender, income, verificationCode, codeSent, token,
nameError, emailError, emailHasError, passwordError, passwordHasError, confirmPasswordError, phoneError, phoneHasError,
checkName, checkEmail, checkPassword, checkNewPassword, checkConfirmPassword, checkNewConfirmPassword, checkPhone, formatPhoneNumber
} = storeToRefs(store);


const handleUpdate = () => {
store.checkPhone(); // store. 추가

if (
    !store.phoneHasError // store. 추가
) {
    const payload = {
    nickname: store.nickname, // store. 추가
    phone: store.formattedPhone, // store. 추가
    birthdate: `${store.birthYear}-${store.birthMonth}-${store.birthDay}`, // 백틱으로 수정
    gender: store.gender, // store. 추가
    income: store.income // store. 추가
    };

    console.log("Payload data being sent:", payload);

    axios
    .patch(`http://127.0.0.1:8000/accounts/${store.email}/`, payload, 
    {
        headers: {
        Authorization: `Token ${store.token}`, // 인증 헤더 추가
        }
    })
    .then((res) => {
        console.log('수정한 정보:', res.data);
        // store.name = userInfo.name;
        // store.formattedPhone = userInfo.phone;
        // store.phone = userInfo.phone;
        // store.nickname = res.data.nickname;
        // store.birthDate = userInfo.birthdate;
        // store.birthYear = userInfo.birthdate.slice(0, 4); // 맨 앞 4자리 추출
        // store.birthMonth = userInfo.birthdate.slice(5, 7); // 월 추출 (필요 시)
        // store.birthDay = userInfo.birthdate.slice(8, 10); // 일 추출 (필요 시)
        // store.gender = userInfo.gender;
        // store.income = userInfo.income;

        alert("회원정보 수정이 완료되었습니다!");
        router.push({ name: "home" });
    })
    .catch((err) => {
        console.error(err);
        alert("회원정보 수정 중 오류가 발생했습니다.");
    });
}
};


const goPasswordChange = function() {
router.push({ name : 'passwordchange' })
}

const handleSignOut = function() {
if (!confirm("정말로 탈퇴하시겠습니까?")) {
    return; // 사용자가 취소한 경우
}

// 회원 탈퇴 API 호출
axios
    .delete(`http://127.0.0.1:8000/accounts/${store.email}/`, {
    headers: {
        Authorization: `Token ${store.token}`, // 인증 토큰 전달
    },
    })
    .then(() => {
    alert("회원 탈퇴가 완료되었습니다.");

    // store 초기화
    token = null
    name = '';
    nickname = '';
    email = '';
    birthYear = '';
    birthMonth = '';
    birthDay = '';
    birthDate = '';
    gender = '';
    income = null;
    formattedPhone = '';
    phone = '';
    password = '';
    confirmPassword = '';
    newPassword = '';
    confirmNewPassword = '';
    router.push({ name: 'home' })
    console.log(`토큰값 ${token}`)
    console.log('회원탈퇴 되었습니다.')

    // 홈 화면으로 리다이렉트
    router.push({ name: 'home' });
    })
    .catch((error) => {
    console.error("회원 탈퇴 중 오류 발생:", error);
    alert("회원 탈퇴에 실패했습니다. 다시 시도해주세요.");
    });
}
</script>

<style scoped>
.radio-group {
  display: flex;
  align-items: center;
  gap: 5px; /* 라디오 버튼과 라벨 사이의 간격 */
}

.btn-group {
  display: flex; /* Flexbox를 활성화 */
  justify-content: center; /* 자식 요소들을 수평 가운데 정렬 */
  margin-top: 20px; /* 버튼 그룹의 상단 여백 */
}
</style>
