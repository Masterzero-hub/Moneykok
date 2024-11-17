<template>
    <div>
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <RouterLink :to="{ name : 'home'}" class="navbar-brand">
                <img src="@/assets/logo.png" width="100" alt="logo_img">
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
                <li class="nav-item">
                    <RouterLink :to="{ name : 'savings'}">적금 상품</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink :to="{ name : 'ai'}">AI 상품 추천</RouterLink>                    
                </li>
                <li class="nav-item">
                    <RouterLink :to="{ name : 'community' }">커뮤니티</RouterLink>                    
                </li>
                <li class="nav-item">
                    <RouterLink :to="{ name : 'community' }">은행 찾기</RouterLink>                    
                </li>
                <button></button>
            </ul>
            </div>
        </div>
        </nav> 
    </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';



</script>

<style scoped>

</style>