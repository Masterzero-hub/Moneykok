<template>
    <div>
        <div class="card-container d-flex justify-content-center align-items-center">
            <div class="card p-4" style="width: 400px;">
            <h3 class="card-title text-center">로그인</h3>
            <form @submit.prevent="handleLogin">
                <!-- 이메일 입력 필드 -->
                <div class="mb-3">
                <label for="email" class="form-label">이메일</label>
                <input
                    type="email"
                    id="email"
                    v-model="email"
                    class="form-control"
                    placeholder="이메일을 입력하세요"
                    required
                />
                </div>
                <!-- 비밀번호 입력 필드 -->
                <div class="mb-3">
                <label for="password" class="form-label">비밀번호</label>
                <input
                    type="password"
                    id="password"
                    v-model="password"
                    class="form-control"
                    placeholder="비밀번호를 입력하세요"
                    required
                />
                </div>
                <!-- 로그인 버튼 -->
                <div class="d-grid">
                <button type="submit" class="btn-common" @click="login">로그인</button>
                </div>
            </form>
            <!-- 회원가입 버튼 -->
            <div class="d-grid mt-3">
                <button type="submit" class="btn-common btn-mint" @click="goSignUp">회원가입</button>
            </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
const store = useUserStore()
const router = useRouter()

// 장고에서 처리하는 변수 이름 정해져있으므로, email 대신 username으로 변수 선언
const email = ref(null) 
const password = ref(null)

const login = function () {
    // const email = email.value
    // const password = password.value
    axios({
      method: 'post',
      url : `http://127.0.0.1:8000/accounts/login/`,
      data: {
        email: email.value, 
        password: password.value,
      }
    })
    .then((res) => {
      // 1. 로그인 성공: 토큰 저장
      store.token = res.data.key;
      store.email = email.value
      store.password = password.value

      // console.log('로그인 성공:', store.email);
      // router.push({ name: 'home' }); // 홈 화면으로 이동
      
      // 2. 사용자 정보 가져오기
      return axios.get(`http://127.0.0.1:8000/accounts/${store.email}/`, {
        headers: {
          Authorization: `Token ${store.token}`, // 인증 토큰 헤더 추가
        },
      });
      
    })
    .then((userInfoResponse) => {
      // 3. 사용자 정보를 store에 저장 
      console.log(userInfoResponse)
      const userInfo = userInfoResponse.data;
      store.name = userInfo.name;
      store.formattedPhone = userInfo.phone;
      store.phone = userInfo.phone;
      store.nickname = userInfo.nickname;
      store.birthDate = userInfo.birthdate;
      store.birthYear = userInfo.birthdate.slice(0, 4); // 맨 앞 4자리 추출
      store.birthMonth = userInfo.birthdate.slice(5, 7); // 월 추출 (필요 시)
      store.birthDay = userInfo.birthdate.slice(8, 10); // 일 추출 (필요 시)
      store.gender = userInfo.gender;
      store.income = userInfo.income;

      
      console.log('로그인 성공');
      console.log(store.name)
      console.log(store.email)
      console.log(store.nickname)
      console.log(store.formattedPhone)
      console.log(store.birthDate)
      console.log(store.birthYear)
      console.log(store.birthMonth)
      console.log(store.birthDay)
      console.log(store.gender)
      console.log(store.income)
      router.push({ name: 'home' }); // 홈 화면으로 이동
    })
    .catch((err) => {
      console.error('로그인 실패:', err);
      alert('로그인에 실패했습니다. 이메일과 비밀번호를 확인해주세요.');
    });
};


const goSignUp = function() {
    router.push({ name : 'signup' })
}


</script>





<style scoped>
/* .card-container {
  height: 100vh;
} */

/* 카드 스타일 */
.card {
  width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  margin: 300px;
}

/* 제목 스타일 */
.custom-title {
  font-weight: bold;
  color: #343a40;
  margin-bottom: 20px;
}

.btn-common {
    width: 100%;
}
</style>