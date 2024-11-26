# Moneykok
 <img src="final-pjt-front\MoneyKok\public\mainpage.jpg">


## 💡 개요
- 진행기간 : 2024.11.18. ~ 2024.11.27.
- 주제 :  예적금 상품 조회 및 추천 서비스
- 서비스명 : 머니콕(MoneyKok)
  
|   팀원    | 역할 |
|--------|-------|
|장인영| Back-end 개발, API 요청, AI활용 및 데이터 전처리 |
|최현정| Front-end 개발, UI/UX 디자인, API 활용 환율 계산기, 은행 찾기 기능 구현 |

<br>

##  ⚙️ 기술 스택

### Frontend
<img src="https://img.shields.io/badge/Vue-4FC08D?style=for-the-badge&logo=Vue.js&logoColor=white"> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white"> <img src="https://img.shields.io/badge/Bootstrap-952B3?style=for-the-badge&logo=Bootstrap&logoColor=white"> <img src="https://img.shields.io/badge/Axios-5A29E4?style=for-the-badge&logo=Axios&logoColor=white">


### Backend
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white"> <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=SQLite&logoColor=white">

### Environment
 <img src="https://img.shields.io/badge/GITHUB-181717?style=for-the-badge&logo=GITHUB&logoColor=white"> <img src="https://img.shields.io/badge/GIT-F05032?style=for-the-badge&logo=GIT&logoColor=white"> <img src="https://img.shields.io/badge/notion-000000?style=for-the-badge&logo=notion&logoColor=white"> <img src="https://img.shields.io/badge/Visual Studio Code-007ACC?style=for-the-badge&logo=Visual Studio Code&logoColor=white"/> <img src="https://img.shields.io/badge/figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white"> <img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white"> 

<br>

## 💷 기획 배경
### 사용자 페인 포인트 및 니즈

1. **금리 정보 부족**
    - 페인포인트: 기존 예적금 상품 조회 사이트에서는 최고 금리와 기본 금리만을 제공하여, 사용자가 자신에게 적용될 금리를 직관적으로 파악하기 어려움.
    - 니즈: 각 상품의 우대 조건에 따라 적용 가능한 금리를 이해하기 쉽게 제공 받고 싶어함.
    - 
2. **금융 상품 정보 파악의 어려움**
    - 페인포인트: 다양한 은행들의 금융 상품에 대한 정보들을 일일이 확인하고 비교하기 번거로움.
    - 니즈: 나와 유사한 사용자가 가입한 금융 상품은 무엇인지 알고 싶어함.

### 서비스 목적

1. **개인 맞춤형 금리 정보 제공**
    -  AI를 활용해 상품별 우대 조건을 키워드로 분류하고, 해당 키워드를 바탕으로 사용자에게 직관적으로 금리를 표시함. 사용자는 최고 금리와 기본 금리를 보면서 각 우대 조건에 따른 차이를 쉽게 이해할 수 있음.
  
2. **사용자 맞춤 금융 상품 AI 추천**
    - 별도의 조건 선택 없이 사용자와 나이, 성별, 연봉이 비슷한 사람들이 많이 가입한 상품을 추천함. 




<br>

## 📄 설계 
### 아키텍처
 <img src="final-pjt-front\MoneyKok\public\readme_image\architecture.png">

### 와이어프레임
 <img src="final-pjt-front\MoneyKok\public\readme_image\wireframe.jpg">

### ERD
 <img src="final-pjt-front\MoneyKok\public\readme_image\ERD.png">



<br>

## 💰 서비스 대표 기능
**1. 회원 관리**
   - 회원 가입 기능
      - 기본 ID를 이메일로 설정 및 커스텀 모델 구축
      - 이메일 인증 기능
   - 개인 정보 조회, 수정 기능 
   - 커뮤니티 프로필 조회, 수정 기능
   - 가입한 예적금 상품 조회
   - 회원 탈퇴 기능
   
   
**2. 예적금 상품 전체 조회**
   - 검색 조건 (가입 기간, 가입 금액, 은행, 우대조건)에 따른 필터링 기능


**3. 예적금 상품 상세 조회**
   - 금리 계산기 : 사용자가 선택하는 가입 옵션에 따라 계산된 금리를 실시간으로 확인 가능
   - 가입하기 기능 : 금리 계산기에서 선택한 가입 기간, 가입 금액, 우대 조건으로 바로 가입 가능


**4. 금융 상품 추천**
   - 사용자와 유사한 사람들이 가장 많이 가입한 상품 추천

**5. 커뮤니티**
   - 게시글 작성, 수정, 삭제 기능
   - 댓글 작성, 수정, 삭제 기능 
   - 다른 사용자 프로필 조회 기능


**6. 환율 계산기**
   - 계산 조건 (송금 받을 때, 송금 보낼 때, 매매 기준율) 선택 가능
   - 원화 -> 외화 환산 기능
   - 외화 -> 원화 환산 기능
  

**7.  은행 찾기**
   - 지역과 은행을 선택하여 검색 기능
   - 현재 위치 기준 근처 은행 검색 기능


<br>

## 🖥️ 페이지 프리뷰
1. 메인 페이지
https://github.com/user-attachments/assets/d47aa9af-dccf-44fb-a54f-e33ef9ce1fa6
- 페이지 이동시 스크롤 위치 초기화

2. 회원가입
https://github.com/user-attachments/assets/c8674736-270d-4bb0-9c8a-99d69db2314c
- 이메일 인증 요청 및 인증 성공 시 alter창 알림
- 이메일 인증 여부에 따라 버튼 및 입력창 토글
- 휴대폰 번호 사이 '-' 자동 생성
- 이메일, 비밀번호, 휴대폰 형식 유효성 검사 
 - 이메일 : 영문,숫자 + @ + 영문,숫자 + . 영문
 - 비밀번호 : 최소 8자, 영문, 숫자, 특수문자를 포함
 - 휴대폰 번호 : 010-4자리 숫자-4자리 숫자
- 비밀번호 재확인
 - 회원가입 이후 자동으로 로그인되고 메인페이지로 이동함

1. 회원 가입
   - 이메일
2. 회원정보
   - 가입한 상품 
   - 커뮤니티 프로필
   - 개인 정보
3. 예금 상품 전체 조회
   - 페이지010-\d{4}-\d{4}$네이션
   - 검색 조건 필터링
4. 예금 상품 상세 **조회** 
   - 이자율 계산하기
   - 가입하기
5. 금융 상품 AI 추천
6. 커뮤니티 (게시글 및 댓글 CRUD)

   - 게시글 작성, 수정, 삭제 
   - 게시글 조회 (작성자 프로필로 이동)
   - 댓글 작성, 수정, 삭제

7. 환율 계산기
   - 원화 -> 외화
   - 외화 -> 원화
8.  은행 찾기
   - 검색으로 찾기
   - 근처 은행 찾기


<br>

## 🖇️ 금융 상품 추천 알고리즘
**1. 유사한 사용자 찾기**
- User의 소득, 나이(출생년도), 성별을 기준으로 유사도를 계산하고 상위 10명의 유사 사용자 찾습니다.
- scikit-learn 라이브러리의 함수 `cosine_similarity`를 통해 코사인 유사도를 계산합니다.
  
**2. 상품 3가지 추천하기**
- 유사한 사용자가 가입한 상품 목록을 조회합니다.
- 상품 가입 횟수를 세고 점수화하여, 점수가 높은 순으로 정렬합니다.
- 추천된 상품 중 상위 3가지 상품을 추천합니다.

```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from django.db.models import Count
from rest_framework.response import Response

def recommend_products(user):
    """
    금융 상품 추천 알고리즘
    - 사용자 정보를 기반으로 유사한 사용자를 찾고 추천 상품 반환
    """

    # **1. 유사한 사용자 찾기**
    # 현재 사용자의 데이터를 배열로 변환
    user_data = np.array([[user.income, user.birthdate.year, 1 if user.gender == '남성' else 0]])

    # 다른 사용자 데이터 가져오기
    all_users = User.objects.exclude(id=user.id)  # 현재 사용자는 제외
    similar_users = []

    for other_user in all_users:
        # 비교 대상 사용자 데이터를 배열로 변환
        other_data = np.array([[other_user.income, other_user.birthdate.year, 1 if other_user.gender == '남성' else 0]])

        # 코사인 유사도 계산
        similarity = cosine_similarity(user_data, other_data)
        similar_users.append((other_user, similarity[0][0]))

    # 유사도가 높은 상위 10명의 사용자 추출
    similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)[:10]
    similar_user_ids = [u[0].id for u in similar_users]  # 상위 사용자들의 ID 추출

    # **2. 상품 3가지 추천하기**
    # 유사한 사용자가 가입한 상품 조회
    joined_deposits = JoinedDeposits.objects.filter(user_id__in=similar_user_ids)

    # 상품별 가입 횟수 점수화
    product_scores = (
        joined_deposits
        .values('product_id')  # 상품별 그룹화
        .annotate(score=Count('product_id'))  # 가입 횟수 집계
        .order_by('-score')  # 점수가 높은 순으로 정렬
    )

    # 상위 3개의 상품 선택
    recommended_product_ids = [p['product_id'] for p in product_scores[:3]]
    recommended_products = DepositProducts.objects.filter(id__in=recommended_product_ids)

    # 결과 직렬화 및 반환
    serializer = DepositProductsGETSerializer(recommended_products, many=True)
    return Response({'recommended_products': serializer.data})
```


<br>

## 🤖 생성형 AI 활용 
### AI를 활용한 금융 데이터 전처리

##### 2. 우대조건 데이터 카테고리화 (parse_special_conditions)
: 금융 상품의 우대조건 텍스트에서 각 조건의 상세 설명, 금리 정보, 카테고리를 추출하여 구조화된 JSON 데이터로 변환

핵심 코드 리뷰
```python
# Prompt 생성: 텍스트 분석 및 조건 추출 규칙 정의
prompt = f"""
다음 텍스트는 특정 금융 상품의 우대조건을 포함하고 있습니다. ...
#### 응답 형식
[
    {{
        "category": "카테고리 이름",
        "condition_content": "우대조건 상세 설명",
        "prime_rate": 숫자형 금리
    }},
    ...
]
"""

# AI 응답 생성
response = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "당신은 우대조건 정보를 분석하는 전문가입니다."},
        {"role": "user", "content": prompt},
    ],
    model="llama-3.2-90b-text-preview",
    temperature=0.2,
    max_tokens=4096,
    top_p=0.9,
)
```

#### 가입 금액 데이터 전처리 (preprocess_deposit_amounts_with_ai)

금융 상품의 가입 조건을 나타내는 텍스트(etc_note)에서 최소 금액과 최대 금액을 추출하여 데이터베이스에 저장.
```python
# Prompt 생성: 가입 금액 추출 규칙 정의
prompt = f"""
다음 텍스트에서 가입금액과 관련된 최소 및 최대 금액을 분석하세요. ...
#### 응답 형식:
{{
    "min_amount": 최소 금액 (만원 단위),
    "max_amount": 최대 금액 (만원 단위)
}}
"""

# AI 응답 생성 및 JSON 처리
response = client.chat.completions.create(...)
amount_data = json.loads(assistant_message)

# 결과 저장: 최소/최대 금액 데이터베이스에 반영
product.savings_min_amount = amount_data.get("min_amount")
product.savings_max_amount = amount_data.get("max_amount")
product.save()
```


<br>

## 소감
| 팀원     | 소감 |
|--------|-------|
|장인영| 약 3개월동안 배운 프로그래밍 언어로 이렇게 프로젝트를 할 수 있다는 것이 신기했습니다. 개발자는 협업이 가장 중요하다고 했던 것에 조금은 의문이 있었는데, 변수, 요청 url주소, method방법 등 정말 다양한 요소를 맞추어야한다는 것을 깨달았던 프로젝트였던 것 같습니다. 따라서 기획, 기능명세서, API명세서를 정말 꼼꼼히 작성해야한다는 것도 깨닫게 되었습니다. 함께한 페어 현정언니가 잘 맞춰주어 프로젝트가 잘 완성될 수 있었던 것 같습니다! AI를 통해 데이터를 가공하고 전처리하는 것이 정말 어렵다는 것도 느끼고, 웹개발도 생각보다 잘 맞고 재밌다는 것도 얻어가는 프로젝트였습니다!|
|최현정| 처음에는 모든 것이 막막했는데 페어와 계속해서 소통하며 눈 앞에 놓인 것들을 해결해 나가다보니 잘 마무리할 수 있었던 것 같습니다. 강의를 통해 배운 내용들을 실제 프로젝트에서 활용해 보니 재미있었고 프론트엔드 개발에 흥미를 더욱 느끼게 되었습니다. 또 프로젝트를 끝내고 나니 설계의 중요성도 더욱 더 실감할 수 있었습니다. 이번 프로젝트에서의 시행착오를 바탕으로 다음 프로젝트는 좀 더 잘할 수 있겠다는 자신감도 얻게 되었습니다. 무엇보다도 페어 인영이와 함께여서 더욱 더 즐겁고 성공적으로 마칠 수 있었던 것 같아 감사함을 전합니다!
