# 맞춤형 청년정책 추천 AI 챗봇  (Youth Policy Recommendation AI ChatBot Using Microsoft Azure AI)

**Microsoft Azure OpenAI와 Azure Speech Studio를 활용하여 누구나 쉽게 사용할 수 있고 직관적인 청년정책 추천 AI 챗봇을 개발하였습니다.**

현재 대한민국에서 시행 중인 청년 정책은 약 **300개**에 이르며, 다양한 분야에서 청년의 삶을 지원하고 있습니다. 그러나 정부 포털 사이트, SNS 등 **여러 매체에 정책 정보가 분산되어 있어, 필요한 정보를 찾고 세부 내용을 확인하는 데 많은 시간이 소요되는 문제**가 있었습니다. 이러한 배경을 바탕으로, **사용자가 원하는 정책을 쉽고 빠르게 탐색할 수 있도록 AI 챗봇을 개발하게 되었습니다.**

챗봇은 웹 페이지 형태로 제공되며, **Python, HTML, CSS, JavaScript와 Google Cloud Platform(GCP)**을 활용하여 구현 및 배포하였습니다. 또한, **Azure Speech Studio의 Custom Voice 및 TTS(Text-to-Speech) 서비스**를 활용해 음성 인터페이스를 추가하여, 보다 **자연스러운 대화형 경험을 제공**할 수 있도록 하였습니다.

또한, **Azure AI Studio의 OpenAI(GPT-4o), AI Search, 채팅 플레이그라운드 등을 활용하여 챗봇과의 대화 품질을 최적화**하였습니다. 이를 통해, **프롬프트 튜닝과 페르소나 설정을 조정하여 보다 정확하고 친숙한 응답을 제공할 수 있도록 개선**하였습니다.    


----



**An intuitive AI chatbot for youth policy recommendations developed using Microsoft Azure OpenAI and Azure Speech Studio.**  

South Korea currently has around **300 youth policies**, but information is scattered across various platforms, making searches time-consuming. To solve this, an **AI chatbot was developed to help users quickly find relevant policies**.  

The **web-based** chatbot was built using **Python, HTML, CSS, JavaScript, and GCP**, with **Azure Speech Studio’s TTS** for a natural voice interface. Additionally, **Azure AI Studio’s OpenAI (GPT-4o), AI Search,** and **Chat Playground** were used to enhance conversation quality through fine-tuned prompts and persona settings.  




## :pushpin: 프로젝트의 목표 및 필요성 (Project Goal & Necessity)
* **정책 접근성 향상**  
사용자가 다양한 정책에 쉽게 접근할 수 있도록 지원하여 정책 참여율 증가에 기여함.  

* **효율적인 정보 제공**  
정책의 핵심 내용과 신청 방법을 신속하고 정확하게 제공해 사용자가 필요한 정보를 빠르게 얻을 수 있도록 함.   

* **정책 홍보 강화 및 사업성**   
유명 캐릭터나 연예인의 음성을 활용한 지속적인 정책 홍보가 가능하며 이를 통한 사업의 확장성 기대. (음성 사용 시, 인공지능 윤리 원칙을 반드시 준수할 것)  

* **사용자 맞춤형 경험 제공**  
개별 사용자의 요구에 맞춘 서비스를 제공해 사용자 만족도를 높이고 정책의 활용도를 증가시키는 효과 기대.

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

* 모델 생성 (Model Creation)    
   * **Azure AI Studio** (OpenAI GPT-4o, AI Search)   
   * **Azure Speech Studio** (TTS, Custom Voice, Personal Voice)   

* 웹 구현 및 배포 (Web Implementaion & Deploy)  
   * **웹 구현 (Web Implementaion)** : HTML, CSS, JS, Python Flask  
   * **웹 배포 (Web Deploy)** : Google Cloud Platform  


## :pushpin: 실행 화면 (Result)
![Image](https://github.com/user-attachments/assets/cc05b1cb-3c08-4cab-ac54-764ac6b59df5)
![Image](https://github.com/user-attachments/assets/d348d7ff-c663-48c4-9d45-3a481ecab202)
![Image](https://github.com/user-attachments/assets/f18a6f3a-a583-4a0e-8b0b-2564c40ff3dc)
![Image](https://github.com/user-attachments/assets/c40e5500-ce39-4baf-8590-60150424e9d2)
![Image](https://github.com/user-attachments/assets/caaaf82f-0a24-43bd-b73c-f222dcb18cb2)
![Image](https://github.com/user-attachments/assets/7c5c0927-f76e-4957-bbd6-ff11bae8257d)

## :pushpin: 참고사항 (Notes)
  이 챗봇은 실제 ‘온통청년’ 사이트와 연결된 것이 아니라, 프로젝트를 위한 가상의 화면입니다.  
  이 프로젝트는 Microsoft Azure 서비스를 활용하였으며, 코드를 실행하려면 Azure 서비스의 API 키와 EndPoint 값이 필요합니다.
  
  This chatbot is not connected to the actual '온통청년' website; it is a mock interface created for the project.  
  This project utilizes Microsoft Azure services, and an API key and endpoint for the Azure service are required to use the code.
