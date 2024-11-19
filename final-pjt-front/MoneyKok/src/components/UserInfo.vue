<template>
  <div class="container mt-5">
    <!-- <h3>회원가입</h3> -->
    <form @submit.prevent="handleSubmit">
      <!-- 이름 -->
      <div class="mb-3">
        <label for="name" class="form-label">이름</label>
        <input
          disabled
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
          disabled
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
      <button type="submit" class="btn-small-common btn-mint">수정하기</button>
    </form>
  </div>
</template>

<script setup>

</script>

<style scoped>

</style>