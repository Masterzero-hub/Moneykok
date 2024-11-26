# Moneykok
 <img src="final-pjt-front\MoneyKok\public\mainpage.jpg">


## 💡 개요
- 진행기간 : 2024.11.18. ~ 2024.11.27.
- 주제 :  예적금 상품 조회 및 추천 서비스
- 서비스명 : 머니콕(MoneyKok)
  
|   팀원    | 역할 |
|--------|-------|
|   장인영  | Back-end 개발, |
|최현정| Front-end 개발, UI/UX 디자인, API 활용 환율 계산기, 은행 찾기 기능 구현 |


## 💷 기획 배경
### 사용자 페인 포인트 및 니즈

1. **금리 정보 부족**
    - **페인포인트**: 기존 예적금 상품 조회 사이트에서는 최고 금리와 기본 금리만을 제공하여, 사용자가 자신에게 적용될 금리를 직관적으로 파악하기 어려움.
    - **니즈**: 각 상품의 우대 조건에 따라 적용 가능한 금리를 이해하기 쉽게 제공 받고 싶어함.
    - 
2. **금융 상품 정보 파악의 어려움**
    - **페인포인트**: 다양한 은행들의 금융 상품에 대한 정보들을 일일이 확인하고 비교하기 번거로움.
    - **니즈**: 나와 유사한 사용자가 가입한 금융 상품은 무엇인지 알고 싶어함.

### 서비스 목적

1. **개인 맞춤형 금리 정보 제공**
    - **해결 방안** :  AI를 활용해 상품별 우대 조건을 키워드로 분류하고, 해당 키워드를 바탕으로 사용자에게 직관적으로 금리를 표시함. 사용자는 최고 금리와 기본 금리를 보면서 각 우대 조건에 따른 차이를 쉽게 이해할 수 있음.
    - 
2. **사용자 맞춤 금융 상품 추천**
    - **해결 방안**: 별도의 조건 선택 없이 사용자와 나이, 성별, 연봉이 비슷한 사람들이 많이 가입한 상품을 추천함. 


## 📄 설계 내용 
### 아키텍처
 <img src="final-pjt-front\MoneyKok\public\readme_image\architecture.png">

### 와이어프레임
 <img src="final-pjt-front\MoneyKok\public\readme_image\wireframe.jpg">

### ERD
 <img src="final-pjt-front\MoneyKok\public\readme_image\ERD.png">




## 서비스 대표 기능
1. 회원 관리
   - 회원 가입 기능 : 이메일 인증 기능
   - 회원 탈퇴 기능
   - 가입한 예적금 상품 조회
   - 커뮤니티 프로필 조회, 수정 기능
   - 개인 정보 조회, 수정 기능 
   
   
2. 예적금 상품 전체 조회
   - 검색 조건 (가입 기간, 가입 금액, 은행, 우대조건)에 따른 필터링 기능


3. 예적금 상품 상세 조회
   - 금리 계산기 : 사용자가 선택하는 가입 옵션에 따라 계산된 금리를 실시간으로 확인 가능
   - 가입하기 기능 : 금리 계산기에서 선택한 가입 기간, 가입 금액, 우대 조건으로 바로 가입 가능


4. 금융 상품 추천 
   - 사용자와 금융 관련 정보가 유사한 사람들의 가입 상품을 추천


5. 커뮤니티 
   - 게시글 작성, 수정, 삭제 기능
   - 댓글 작성, 수정, 삭제 기능 
   - 다른 사용자 프로필 조회 기능


6.  환율 계산기
    - 계산 조건 (송금 받을 때, 송금 보낼 때, 매매 기준율) 선택 가능
    - 원화 -> 외화 환산 기능
    - 외화 -> 원화 환산 기능
  

7.  은행 찾기
    - 지역과 은행을 선택하여 검색 기능
    - 현재 위치 기준 근처 은행 검색 기능


## 🖥️ 금융 상품 추천 알고리즘
### 1. 유사한 사용자 찾기
- User의 소득, 나이(출생년도), 성별을 기준으로 유사도를 계산하고 상위 10명의 유사 사용자 찾습니다.
- scikit-learn 라이브러리의 함수 `cosine_similarity`를 통해 코사인 유사도를 계산합니다.
### 2. 상품 3가지 추천하기
- 유사한 사용자가 가입한 상품 목록을 조회합니다.
- 상품 가입 횟수를 세고 점수화하여, 점수가 높은 순으로 정렬합니다.
- 추천된 상품 중 상위 3가지 상품을 추천합니다.


##  ⚙️ 기술 스택
### Environment
 <img src="https://img.shields.io/badge/GITHUB-181717?style=for-the-badge&logo=GITHUB&logoColor=white"> <img src="https://img.shields.io/badge/GIT-F05032?style=for-the-badge&logo=GIT&logoColor=white"> <img src="https://img.shields.io/badge/Visual Studio Code-007ACC?style=for-the-badge&logo=Visual Studio Code&logoColor=white"/> <img src="https://img.shields.io/badge/figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white"> <img src="https://img.shields.io/badge/notion-000000?style=for-the-badge&logo=notion&logoColor=white">

### Frontend
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white"> <img src="https://img.shields.io/badge/Bootstrap-952B3?style=for-the-badge&logo=Bootstrap&logoColor=white"> <img src="https://img.shields.io/badge/Axios-5A29E4?style=for-the-badge&logo=Axios&logoColor=white">


### Backend
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white">


## 소감
| 팀원     | 소감 |
|--------|-------|
|장인영| 약 3개월동안 배운 프로그래밍 언어로 이렇게 프로젝트를 할 수 있다는 것이 신기했습니다. 개발자는 협업이 가장 중요하다고 했던 것에 조금은 의문이 있었는데, 변수, 요청 url주소, method방법 등 정말 다양한 요소를 맞추어야한다는 것을 깨달았던 프로젝트였던 것 같다. 따라서 기획, 기능명세서, API명세서를 정말 꼼꼼히 작성해야한다는 것도 깨닫게 되었습니다. 함께한 페어가 잘 맞춰주어 프로젝트가 잘 완성될 수 있었던 것 같습니다! AI를 통해 데이터를 가공하고 전처리하는 것이 정말 어렵다는 것도 느끼고, 웹개발도 생각보다 잘 맞고 재밌다는 것도 얻어가는 프로젝트였습니다!|
|최현정| 처음에는 모든 것이 막막했는데 페어와 계속해서 소통하며 눈 앞에 놓인 것들을 해결해 나가다보니 잘 마무리할 수 있었던 것 같습니다. 강의를 통해 배운 내용들을 실제 프로젝트에서 활용해 보니 재미있었고 프론트엔드 개발에 흥미를 더욱 느끼게 되었습니다. 또 프로젝트를 끝내고 나니 설계의 중요성도 더욱 더 실감할 수 있었습니다. 이번 프로젝트에서의 시행착오를 바탕으로 다음 프로젝트는 좀 더 잘할 수 있겠다는 자신감도 얻게 되었습니다. 무엇보다도 페어 인영이와 함께여서 더욱 더 즐겁고 성공적으로 마칠 수 있었던 것 같아 감사함을 전합니다!