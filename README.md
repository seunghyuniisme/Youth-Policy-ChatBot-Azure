# 맞춤형 청년정책 추천 AI 챗봇  (Youth Policy Recommendation AI ChatBot Using Microsoft Azure AI)

**Microsoft Azure OpenAI와 Azure Speech Studio를 활용하여 누구나 쉽게 사용할 수 있고 직관적인 청년정책 추천 AI 챗봇을 개발하였습니다.**

현재 대한민국에서 시행 중인 청년 정책은 약 **300개**에 이르며, 다양한 분야에서 청년의 삶을 지원하고 있습니다. 그러나 정부 포털 사이트, SNS 등 **여러 매체에 정책 정보가 분산되어 있어, 필요한 정보를 찾고 세부 내용을 확인하는 데 많은 시간이 소요되는 문제**가 있었습니다. 이러한 배경을 바탕으로, **사용자가 원하는 정책을 쉽고 빠르게 탐색할 수 있도록 AI 챗봇을 개발하게 되었습니다.**

챗봇은 웹 페이지 형태로 제공되며, **Python, HTML, CSS, JavaScript와 Google Cloud Platform(GCP)**을 활용하여 구현 및 배포하였습니다. 또한, **Azure Speech Studio의 Custom Voice 및 TTS(Text-to-Speech) 서비스**를 활용해 음성 인터페이스를 추가하여, 보다 **자연스러운 대화형 경험을 제공**할 수 있도록 하였습니다.

또한, **Azure AI Studio의 OpenAI(GPT-4o), AI Search, 채팅 플레이그라운드 등을 활용하여 챗봇과의 대화 품질을 최적화**하였습니다. 이를 통해, **프롬프트 튜닝과 페르소나 설정을 조정하여 보다 정확하고 친숙한 응답을 제공할 수 있도록 개선**하였습니다.    


----



**An intuitive and easy-to-use AI chatbot for recommending youth policies has been developed using Microsoft Azure OpenAI and Azure Speech Studio.**  

Currently, there are approximately **300 youth policies** in effect in South Korea, supporting various aspects of young people's lives. However, policy information is scattered across multiple platforms such as government portals and social media, making it time-consuming to search for and review details. To address this issue, an **AI chatbot was created to help users quickly and easily find the policies they need.**  

The chatbot is provided as a **web-based service**, implemented and deployed using **Python, HTML, CSS, JavaScript, and Google Cloud Platform (GCP)**. Additionally, **Azure Speech Studio's Custom Voice and Text-to-Speech (TTS) services** were integrated to enhance the chatbot with a natural and interactive voice interface.     

Furthermore, **Azure AI Studio’s OpenAI (GPT-4o), AI Search, and Chat Playground** were utilized to optimize the chatbot's **conversation quality**. By fine-tuning prompts and persona settings, the chatbot’s ability to deliver **more accurate and user-friendly responses** has been improved.




## :pushpin: 프로젝트의 목표 및 필요성 (Project Goal & Necessity)
* **정책 접근성 향상**  
사용자가 다양한 정책에 쉽게 접근할 수 있도록 지원하여, 정책 참여율 증가에 기여한다.  

* **효율적인 정보 제공**  
정책의 핵심 내용과 신청 방법을 신속하고 정확하게 제공해, 사용자가 필요한 정보를 빠르게 얻을 수 있도록 한다.  

* **정책 홍보 강화 및 사업성**   
유명 캐릭터나 연예인의 음성을 활용한 지속적인 정책 홍보가 가능하며, 이를 통해 사업의 확장성도 기대할 수 있다. (음성 사용 시, 인공지능 윤리 원칙을 반드시 준수할 것.)  

* **사용자 맞춤형 경험 제공**  
개별 사용자의 요구에 맞춘 서비스를 제공해, 사용자 만족도를 높이고 정책의 활용도를 증가시키는 효과를 기대한다.

---

* Improved Policy Accessibility  
* Efficient Information Delivery  
* Enhanced Policy Promotion & Business Potential    
* Personalized User Experience    



## :pushpin: 업무 분담 


## :pushpin: 주요 기능 (Key Features)
1. AI Search 








## :pushpin: 활용 기술 (Tech)
* 개발 언어 (Language) : Python  
* 데이터 수집 (Data Collection) : XML Parsing  

* **모델 생성 (Model Creation)**    
   * **Azure AI Studio** (OpenAI GPT-4o, AI Search)   
   * **Azure Speech Studio** (TTS, Custom Voice, Personal Voice)   

* **웹 구현 및 배포 (Web Implementaion & Deploy)**  
   * **웹 구현 (Web Implementaion)** : HTML, CSS, JS, Python Flask  
   * **웹 배포 (Web Deploy)** : Google Cloud Platform  


## :pushpin: 실행 화면 (Result)
이미지 첨부

## :pushpin: 참고사항 (Notes)
  실제 ‘온통청년’ 사이트와 연결된 챗봇이 아니며 프로젝트를 위한 가상의 화면입니다.   
  이 프로젝트는 Microsoft Azure 서비스를 활용했습니다. 해당 코드를 활용하기 위해서는 Azure 서비스의 API 키와 EndPoint 값이 필요합니다.  
  
  This is not an actual chatbot connected to the '온통청년(youthcenter.go.kr)' website.
  This project utilizes Microsoft Azure services. To use these codes, an API key and endpoint for the Azure service are required.
