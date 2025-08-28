# Week 3 — UE5 Remote Control API와 Python 스크립팅 기초

## 1) 주차 개요
이번 주는 UE5의 **Remote Control API**를 사용해 **블루프린트/파이썬으로 노출된 함수**를 원격 호출하는 방법을 학습하였다. 더불어 Python Editor Script를 통해 **콘솔 명령 실행**, **에디터 상태 제어**를 실습하였다.

## 2) 학습 목표
- Remote Control 서버(HTTP/WS) 엔드포인트 구조 이해  
- 오브젝트 경로(objectPath)와 함수 호출(functionName) 방식 학습  
- Python Script Library를 통해 에디터 콘솔 명령을 실행

## 3) Remote Control 서버 확인
- 에디터 실행 후 플러그인 패널에서 **Enable Server**  
- (옵션) 콘솔에서 서버 시작: 설정에 따라 포트/프로토콜 제어  
- 로컬 브라우저/HTTP 클라이언트로 헬스체크 엔드포인트 확인

## 4) 오브젝트/함수 호출 모델
- 엔진/블루프린트 객체는 **objectPath**로 식별  
- **/remote/object/call** (PUT)로 함수 호출
- 파라미터는 JSON으로 전달

### 4-1) Python 실행(예시)
아래는 Python Script Library의 고급 실행 노드에 상대하는 호출 방식 개념 예시이다.
```json
PUT /remote/object/call
{
  "objectPath": "/Script/PythonScriptPlugin.Default__PythonScriptLibrary",
  "functionName": "ExecutePythonCommandAdvanced",
  "parameters": {
    "PythonCommand": "import unreal; unreal.log('Hello from Remote Control')",
    "ExecutionMode": "EvaluateStatement"
  },
  "generateTransaction": false
}
```
- 결과: 에디터 출력창에 로그가 기록된다.

## 5) 실습: 뷰포트/월드에 콘솔 명령 전달
Python에서 콘솔명령을 실행하여 Viewport/World 타깃을 지정할 수 있다.
```python
import unreal
world = unreal.EditorLevelLibrary.get_editor_world()
unreal.SystemLibrary.execute_console_command(world, "stat fps")
```
- 기대: 에디터 뷰포트에 FPS 표시

## 6) 블루프린트 노출 함수 호출 실습
- 샘플 Actor `BP_RemoteEcho` 제작, `EchoMessage`(String → Print String) 함수 노출  
- Remote Control로 `EchoMessage("Remote OK")` 호출 후, 뷰포트에 메시지 출력 확인

## 7) 문제 해결 사례
- **objectPath 불일치**: CDO 경로(`/Script/...Default__...`)와 레벨 인스턴스 경로(`/Game/...`) 혼동 → 정확한 경로 확인 필요  
- **파라미터 명**: UFUNCTION 파라미터 이름과 JSON 키가 일치해야 함  
- **보안/방화벽**: 로컬호스트만 허용 후 점진적으로 네트워크 개방

## 8) 체크리스트
- [x] Remote Control 서버 on/off, 엔드포인트 헬스체크  
- [x] Python Script Library를 통한 콘솔명령 실행  
- [x] 블루프린트 함수 원격 호출 성공  
- [x] 오류 로그 수집 및 원인 분석

## 9) 주차 회고
원격 호출의 **경로 식별**과 **파라미터 매핑**이 핵심 포인트였다. Python을 통해 콘솔 명령을 프록시하는 패턴을 익혔고, 다음 주에는 이 호출을 MCP **커스텀 브리지 서버**(Node/TS)로 표준화하여, 모델이 쉽게 사용할 수 있는 **툴** 형태로 제공할 계획이다.
