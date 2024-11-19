<template>
    <div>
        <div id="carouselExampleCaptions" class="carousel slide" data-bs-ride="carousel">
            <div class="carousel-indicators">
                <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
                <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="1" aria-label="Slide 2"></button>
                <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="2" aria-label="Slide 3"></button>
            </div>
            <div class="carousel-inner">
                <div class="carousel-item active">
                <img src="..." class="d-block w-100" alt="...">
                <div class="carousel-caption d-none d-md-block">
                    <h5>First slide label</h5>
                    <p>Some representative placeholder content for the first slide.</p>
                </div>
                </div>
                <div class="carousel-item">
                <img src="..." class="d-block w-100" alt="...">
                <div class="carousel-caption d-none d-md-block">
                    <h5>Second slide label</h5>
                    <p>Some representative placeholder content for the second slide.</p>
                </div>
                </div>
                <div class="carousel-item">
                <img src="..." class="d-block w-100" alt="...">
                <div class="carousel-caption d-none d-md-block">
                    <h5>Third slide label</h5>
                    <p>Some representative placeholder content for the third slide.</p>
                </div>
                </div>
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
            </button>
            </div>




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
                    v-model="username"
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
import { ref } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter()

// 장고에서 처리하는 변수 이름 정해져있으므로, email 대신 username으로 변수 선언
const username = ref(null) 
const password = ref(null)

const login = function (payload) {
    const { username, password } = payload
    axios({
      method: 'post',
      url : `http://127.0.0.1:8000/accounts/login/`,
      data: {
        username, password
      }
    })
      .then((res) => {
        console.log('로그인 성공')
        console.log(res.data)
        token.value = res.data.key
        router.push({ name : 'home'})
      })
      .catch((err) => {
        console.log('로그인 실패')
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