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
        store.token = res.data.key
        // store.isLogin = true
        console.log(store.isLogin)
        router.push({ name : 'home'})
      })
      .catch((err) => {
        console.log('로그인 실패')
        console.log(err)
        console.log(store.isLogin)
        console.log(store.token)
      })
  }

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