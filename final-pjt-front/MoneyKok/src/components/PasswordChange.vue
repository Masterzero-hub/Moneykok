<template>
    <div class="container mt-5">
        <h3>비밀번호 수정</h3>
        <form @submit.prevent="handleUpdate">
        <div class="mb-3">
            <label for="password" class="form-label">새 비밀번호</label>
            <input
            type="password"
            id="password"
            class="form-control"
            v-model="store.newPassword"
            @blur="store.checkNewPassword"
            placeholder="비밀번호를 입력하세요"
            :class="{ 'is-invalid': store.passwordHasError }"
            />
            <div class="invalid-feedback" v-if="store.passwordHasError">
            {{ store.passwordError }}
            </div>
        </div>

        <!-- 비밀번호 확인 -->
        <div class="mb-3">
            <label for="confirmPassword" class="form-label">새 비밀번호 확인</label>
            <input
            type="password"
            id="confirmPassword"
            class="form-control"
            v-model="store.confirmNewPassword"
            @blur="store.checkNewConfirmPassword"
            placeholder="비밀번호를 다시 입력하세요"
            :class="{ 'is-invalid': store.confirmPasswordError }"
            />
            <div class="invalid-feedback" v-if="store.confirmPasswordError">
            {{ store.confirmPasswordError }}
            </div>
        </div>

        <!-- 제출 버튼 -->
        <button type="submit" class="btn-small-common btn-mint">수정하기</button>
        </form>
    </div>
</template>


<script setup>
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import { useRouter } from 'vue-router';
const router = useRouter()
const store = useUserStore()

const handleUpdate = () => {
    store.checkNewPassword()
  if (
    !store.passwordError 
  ) {
    const payload = {
      new_password1 : store.newPassword,
      new_password2 : store.confirmNewPassword
    };

    console.log("Payload data being sent:", payload);

    axios
      .post(`http://127.0.0.1:8000/accounts/password/change/`, payload, {
        headers: {
          Authorization: `Token ${store.token}`}, // 인증 헤더 추가
      })
      .then((res) => {
        store.password = store.newPassword
        console.log(store.password);
        alert("회원정보 수정이 완료되었습니다!");
        router.push({ name: "home" });
      })
      .catch((err) => {
        console.error(err);
        alert("회원정보 수정 중 오류가 발생했습니다.");
      });
  }
};



</script>

<style scoped>
h3 {
    padding: 40px 0px;
}
</style>