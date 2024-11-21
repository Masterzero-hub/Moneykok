<template>
    <div>
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <RouterLink :to="{ name : 'home'}" class="navbar-brand">
                <img src="@/assets/logo.png" width="150" alt="logo_img">
            </RouterLink>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <RouterLink :to="{ name : 'deposits'}">예금 상품</RouterLink>
                    <!-- <a class="nav-link active" aria-current="page" href="#">Home</a> -->
                </li>
                <br>
                <li class="nav-item">
                    <RouterLink :to="{ name : 'savings'}">적금 상품</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink :to="{ name : 'ai' }">AI 상품 추천</RouterLink>                    
                </li>
                <li class="nav-item">
                    <RouterLink :to="{ name : 'bank' }">은행 찾기</RouterLink>                    
                </li>
                <li class="nav-item">
                    <RouterLink :to="{ name : 'exchangerate' }">환율 계산기</RouterLink>                    
                </li>
                <li class="nav-item">
                    <RouterLink :to="{ name : 'community' }">커뮤니티</RouterLink>                    
                </li>
                <template v-if="!store.isLogin">
                    <button class="btn-common btn-orange" @click="goLogin">로그인</button>
                </template>
                <template v-else>
                    <li class="nav-item">
                        <RouterLink :to="{ name : 'userinfo' }">회원정보</RouterLink>                    
                    </li>
                    <button class="btn-common btn-orange" @click="logout">로그아웃</button>
                </template>
            </ul>
            </div>
        </div>
        </nav> 
    </div>
</template>



<script setup>
import { useUserStore } from '@/stores/user';
import { ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import axios from 'axios';

const store = useUserStore()
const router = useRouter()

const goLogin = function() {
    router.push({ name : 'login' })    
}


const logout = function () {
    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/accounts/logout/`,
    })
      .then((res) => {
          store.token = null
          store.name = '';
          store.nickname = '';
          store.email = '';
          store.birthYear = '';
          store.birthMonth = '';
          store.birthDay = '';
          store.birthDate = '';
          store.gender = '';
          store.income = null;
          store.formattedPhone = '';
          store.phone = '';
          store.password = '';
          store.confirmPassword = '';
          store.newPassword = '';
          store.confirmNewPassword = '';
          router.push({ name: 'home' })
          console.log(`토큰값 ${store.token}`)
          console.log('로그아웃 되었습니다.')
      })
      .catch((err) => {
        console.log(err)
      })
  }




</script>



<style scoped>
/* 내비게이션 바 스타일 */
.navbar {
    background-color: #ffffff !important; /* 완전히 흰색 배경 */
    border-bottom: 1px solid #ffffff; /* 하단 경계선도 흰색 */
    padding: 10px 20px; /* 내비게이션 바 내부 여백 */
    display: flex; /* Flexbox 레이아웃 */
    align-items: center; /* 수직 중앙 정렬 */
}

/* 로고 이미지 */
.navbar-brand {
    display: flex; /* Flexbox 사용 */
    align-items: center; /* 수직 중앙 정렬 */
    margin-right: auto; /* 오른쪽 공간 확보 */
}

.navbar-brand img {
    max-height: 50px; /* 로고 이미지 높이 */
}

/* 내비게이션 링크 컨테이너 */
.navbar-nav {
    display: flex; /* Flexbox 설정 */
    justify-content: flex-end; /* 우측 정렬 */
    align-items: center; /* 수직 중앙 정렬 */
    flex-grow: 1; /* 로고와의 간격을 차지하여 우측으로 밀림 */
}

.navbar-nav .nav-item a {
    color: #2C3E50; /* 링크 기본 색상 (짙은 회색) */
    font-weight: 400;
    font-size: 20px;
    text-decoration: none; /* 밑줄 제거 */
    margin-right: 20px; /* 링크 간 간격 */
    padding: 8px 15px; /* 텍스트 내부 여백 */
    border-radius: 30px; /* 동그란 효과를 위한 둥근 모서리 */
    transition: all 0.3s ease; /* 부드러운 전환 효과 */
    display: inline-flex; /* 텍스트와 배경 정렬 */
    justify-content: center; /* 수평 중앙 정렬 */
    align-items: center; /* 수직 중앙 정렬 */
}

/* 마우스 호버 시 스타일 */
.navbar-nav .nav-item a:hover {
    /*background-color: rgba(255, 69, 0, 0.2); /* 호버 배경색 */
    color: #FF7A24; /* 호버 시 텍스트 색상 */
    transform: scale(1.1); /* 살짝 확대 */
    /* box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* 약간의 그림자 */
}

/* 텍스트 아래 밑줄 효과 */
.navbar-nav .nav-item a::after {
    content: ""; /* 가상 요소 */
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px; /* 밑줄 두께 */
    background-color: #FF7A24; /* 밑줄 색상 */
    transition: width 0.3s ease; /* 부드러운 애니메이션 */
}

/* 호버 시 밑줄 확장 */
.navbar-nav .nav-item a:hover::after {
    width: 100%; /* 밑줄이 전체 텍스트 아래로 확장 */
}

/* 활성화된 메뉴 항목 강조 */
.navbar-nav .nav-item .active {
    color: #FF7A24; /* 활성화된 텍스트 색상 */
    background-color: rgba(255, 69, 0, 0.3); /* 활성화된 배경색 */
    border-radius: 30px; /* 활성화된 메뉴도 동그란 효과 */
}



/* 반응형 스타일 */
@media (max-width: 992px) {
    .navbar-nav {
        flex-direction: column; /* 모바일에서는 세로 정렬 */
        margin-top: 10px;
    }

    .navbar-nav .nav-item a {
        margin-right: 0;
        margin-bottom: 10px; /* 모바일에서 간격 추가 */
    }

    .navbar .login-button {
        width: 100%; /* 모바일에서는 버튼이 전체 너비 사용 */
        margin-top: 10px;
    }
}
</style>
