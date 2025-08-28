# Week 1 — MCP와 UE5 연동을 위한 기초 환경 구축

## 1) 주차 개요
본 주차에서는 **MCP(Model Context Protocol)** 의 핵심 개념을 파악하고, Unreal Engine 5(이하 UE5)에서 원격 제어 및 실시간 컴파일(= Live Coding) 환경을 준비하였다. 목표는 **AI가 UE5 프로젝트 파일을 수정하고, 에디터가 실행 중인 상태에서 곧바로 컴파일 및 실행 검증**이 가능한 기반을 마련하는 것이다.

## 2) 학습 목표
- MCP의 목적과 아키텍처를 이해한다.  
- UE5에서 **Remote Control**, **Python Editor Script**, **Live Coding** 기능을 활성화하고 기본 동작을 확인한다.  
- 차주차에 사용할 **샘플 UE5 C++ 프로젝트**를 생성하고 버전관리를 준비한다.

## 3) 사전 지식 및 준비물
- OS: Windows 11  
- 개발 도구: Node.js LTS(≥18), Python(≥3.10), Git(≥2.4x), VS 2022, UE5.3/5.4(테스트 버전 표기)  
- 권장 하드웨어: 16GB RAM 이상, SSD, 중급형 GPU  
- 보안: 회사/기관 네트워크 정책에 맞는 포트 사용 허용(기본적으로 Remote Control HTTP/WS 포트 사용)

## 4) MCP 개념 요약
- **정의**: AI 모델이 파일시스템/도구/API 등 **외부 리소스에 일관된 인터페이스**로 접근할 수 있도록 표준화한 프로토콜.  
- **구성**: *서버*가 도구(툴)와 리소스를 노출하고, *클라이언트(모델)*가 이를 호출한다.  
- **특징**
  - 안전한 샌드박스: 접근 루트/권한을 제한해 오남용 방지
  - 표준화된 스키마: 입력/출력 검증이 쉬움
  - 호환성: 다양한 언어/런타임에 구현 가능

### 4-1) 본 프로젝트 맥락에서의 MCP
- **Filesystem 서버**: AI가 `Source/`의 C++ 파일, `Config/` 등을 읽고 수정.  
- **Bridge 서버(커스텀)**: AI가 버튼 하나로 **Live Coding 컴파일**, **PIE 실행** 등 UE5 제어 명령을 원격 호출.

## 5) UE5 환경 구축 절차

### 5-1) 샘플 프로젝트 생성
1. UE5 실행 → **Games → C++ → Third Person** 템플릿 선택  
2. 프로젝트 명: `McpLiveCodingDemo`  
3. 소스 구조 확인: `Source/McpLiveCodingDemo/`

### 5-2) 플러그인 활성화
- **Remote Control**: 에디터의 오브젝트/함수/프로퍼티를 HTTP/WS로 제어  
- **Python Editor Script Plugin**: 에디터에서 Python 명령/스크립트 실행  
- (권장) **Editor Scripting Utilities**: 에디터 자동화 편의 기능

### 5-3) Live Coding 설정
- 메뉴: *Editor Preferences > General > Live Coding*  
- 옵션: `Enable Live Coding` 체크, `Automatically Compile...` 옵션은 필요 시만  
- 단축키: `Ctrl + Alt + F11` (컴파일 트리거)

### 5-4) Remote Control 서버 확인
- 콘솔에서 `RemoteControl.OpenWebSocket` 혹은 플러그인 패널에서 **Enable Server**  
- (기관 보안 정책 상) 포트가 막혀 있으면 로컬 전용으로 진행하고, 외부 접근은 VPN/프록시를 통한다.

## 6) 형상관리 초기화
```bash
git init
git add .
git commit -m "chore: UE5 demo project initialized for MCP live coding"
```

## 7) 리스크 및 제약
- **헤더/리플렉션 변경**: Live Coding이 재시작 없이 반영하기 어렵다. 이 경우 전체 리빌드 필요.  
- **포트 충돌**: Remote Control 기본 포트가 다른 서비스와 충돌할 수 있음 → 설정 변경 필요.  
- **권한**: MCP Filesystem 루트 설정 부주의 시 과도한 디렉터리 접근 가능 → 반드시 최소 권한 원칙 적용.

## 8) 검증 체크리스트
- [x] UE5 C++ 프로젝트 생성  
- [x] Live Coding 활성화 및 단축키 동작 확인  
- [x] Remote Control/Python 플러그인 활성화  
- [x] Git 초기화 및 기본 커밋

## 9) 주차 회고
MCP의 목적(“AI↔도구/파일 표준 인터페이스”)을 명확히 이해했고, UE5 측의 에디터 자동화/원격제어 기능과 결합 가능성을 확인했다. 다음 주엔 MCP **Filesystem 서버** 설치 및 단독 구동 테스트를 진행해 AI가 프로젝트 파일을 안전하게 읽고 수정할 수 있는 기초를 완성할 것이다.
