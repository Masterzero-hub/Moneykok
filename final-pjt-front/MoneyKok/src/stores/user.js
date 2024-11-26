import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from "axios";

export const useUserStore = defineStore('user', () => {

  // Refs for data
  const name = ref("");
  const nickname = ref("");
  const email = ref("");
  const password = ref("");
  const confirmPassword = ref("");
  const newPassword = ref("");
  const confirmNewPassword = ref("");
  const phone = ref("");
  const formattedPhone = ref(""); 
  const birthYear = ref("");
  const birthMonth = ref("");
  const birthDay = ref("");
  const birthDate = ref("");
  const gender = ref("");
  const income = ref(null);
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

  const checkNewPassword = () => {
  const passwordRegex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/;
  if (!newPassword.value) {
      passwordError.value = "비밀번호를 입력해주세요.";
      passwordHasError.value = true;
  } else if (!passwordRegex.test(newPassword.value)) {
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

  const checkNewConfirmPassword = () => {
  if (!confirmNewPassword.value) {
      confirmPasswordError.value = "비밀번호 확인을 입력해주세요.";
  } else if (newPassword.value !== confirmNewPassword.value) {
      confirmPasswordError.value = "비밀번호가 일치하지 않습니다.";
  } else {
      confirmPasswordError.value = "";
  }
  };

  const checkPhone = () => {
  const phoneRegex = /^010-\d{4}-\d{4}$/;
  if (!formattedPhone.value) {
      phoneError.value = "휴대폰 번호를 입력해주세요.";
      phoneHasError.value = true;
  } else if (!phoneRegex.test(formattedPhone.value)) {
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


  const myCommunityInfo = ref([]);

  // 내가 작성한 게시글 및 댓글 조회 요청
  const getMyCommunityInfo = function() {
    axios.get(`http://127.0.0.1:8000/communities/profile/${email.value}/`,
      {
        headers: {
          Authorization: `Token ${token.value}`
        },
      }
    )
      .then((res) => {
        myCommunityInfo.value = res.data
        console.log('내 게시글 및 댓글 조회 성공', res.data)
      })
      .catch((error) => {
        console.error("내 게시글 및 댓글 조회 오류", error);
      });
  }

  const userCommunityInfo = ref([]);

  const getUserCommunityInfo = function(userEmail) {
    axios.get(`http://127.0.0.1:8000/communities/profile/${userEmail}/`,
      {
        headers: {
          Authorization: `Token ${token.value}`
        },
      }
    )
      .then((res) => {
        userCommunityInfo.value = res.data
        console.log('내 게시글 및 댓글 조회 성공', res.data)
      })
      .catch((error) => {
        console.error("내 게시글 및 댓글 조회 오류", error);
      });
  }

  return { isLogin, name, nickname, email, password, confirmPassword, newPassword, confirmNewPassword, phone, formattedPhone, birthYear, birthMonth, birthDay, birthDate, gender, income, verificationCode, codeSent, token,
    nameError, emailError, emailHasError, passwordError, passwordHasError, confirmPasswordError, phoneError, phoneHasError,
    myCommunityInfo, userCommunityInfo,
    checkName, checkEmail, checkPassword, checkNewPassword, checkConfirmPassword, checkNewConfirmPassword, checkPhone, formatPhoneNumber, getMyCommunityInfo, getUserCommunityInfo
   }
},{ persist: true }
)
