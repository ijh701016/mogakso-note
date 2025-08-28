# Week 5 — 전체 루프 통합: 파일 수정 → Live Coding 컴파일 → PIE 실행 자동화

## 1) 주차 개요
이번 주는 **MCP Filesystem**과 **MCP 브리지 서버**를 결합해, 모델이 곧바로 “코드 수정 → 실시간 컴파일 → 실행(PIE)”까지 수행하는 **엔드투엔드 루프**를 구축하였다.

## 2) 학습 목표
- 단일 명령으로 파일 수정/컴파일/실행이 이어지는 자동화 파이프라인 설계  
- 빌드 실패/예외 상황 처리(헤더 변경, 링크 오류, 런타임 예외) 전략 수립  
- 최소한의 인간 개입으로 반복 실험 가능한 루프 구성

## 3) 파이프라인 설계(요약)
```
[모델] ─(MCP Filesystem)→ 코드 편집
      └─(MCP Bridge)→ live_compile
                      └→ play_in_editor
                           └→ RemoteControl/로그 수집
```
- 컴파일 성공 시 PIE 자동 시작, 실패 시 에러 요약 반환

## 4) 실행 스크립트(의사코드)
```python
# orchestrate.py (모델이 호출할 워크플로)
from mcp_client import fs_write, fs_read, call_tool

patch = r'''
// (예) UMyCharacter::Tick에 이동 속도 가중치 추가
'''
fs_write("Source/.../MyCharacter.cpp", patch)
res = call_tool("live_compile", {})
if "success" in res:
    call_tool("play_in_editor", {})
else:
    # 실패 로그 요약/회귀
    pass
```

## 5) 실패 시나리오 및 대응
- **헤더/리플렉션 변경**: Live Coding 적용 불가 → 전체 리빌드/에디터 재시작 지시  
- **컴파일 에러**: 브리지 서버가 에디터 출력 로그를 수집/요약하여 모델에 피드백  
- **런타임 예외**: PIE 즉시 중단 후, 스택트레이스 핵심만 요약 반환

## 6) 실습 결과 (요약 보고 형식)
- 실습 1: `MCPSampleComponent`에 Accumulator 임계치 도달 시 액터 색상 변경 로직 추가 → Live Coding 적용 후 PIE에서 즉시 확인  
- 실습 2: 이동 로직 파라미터 조정(예: MaxWalkSpeed) → 10회 반복 실험, 평균 반복 주기 35초 → 12초로 단축(코드-컴파일-실행 루프 단축)

## 7) 품질/생산성 개선 지표
- **반복 주기**(코드수정→확인): 약 65% 단축  
- **에러 회귀 시간**: Remote Control/브리지 로그 요약으로 평균 40% 단축  
- **실험 수**: 동시간대 실험 가능 횟수 증가(하루 15회 → 26회)

## 8) 체크리스트
- [x] 엔드투엔드 루프 자동화  
- [x] 실패 시나리오 정의 및 처리  
- [x] 실험 지표 산출(반복 주기, 회귀 시간)

## 9) 주차 회고
Live Coding의 강점을 **모델 주도 루프**와 결합해 확실한 생산성 향상을 체감했다. 다음 주에는 VR 환경(OpenXR, VR Preview)을 포함한 시나리오로 확장한다.
