import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {

  // Refs for data
  const name = ref("");
  const nickname = ref("");
  const email = ref("");
  const password = ref("");
  const confirmPassword = ref("");
  const phone = ref("");
  const formattedPhone = ref(""); 
  const birthYear = ref("");
  const birthMonth = ref("");
  const birthDay = ref("");
  const gender = ref("");
  const salary = ref(null);
  const verificationCode = ref("");
  const codeSent = ref(false);
  const token = ref(null)
  
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })




  return { isLogin, name, nickname, email, password, confirmPassword, phone, formattedPhone, birthYear, birthMonth, birthDay, gender, salary, verificationCode, codeSent, token }
}, { persist: true })
