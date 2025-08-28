# Week 6 — VR 확장: OpenXR 기반 VR Preview 제어 및 원격 상호작용

## 1) 주차 개요
본 주는 VR 환경으로 확장하였다. **OpenXR** 플러그인을 활성화하고, VR Preview를 원격으로 트리거하여 **HMD 상태 감지**, **VR 입력 이벤트 시뮬레이션(가능 범위)**, **성능 HUD** 등을 실습하였다.

## 2) 학습 목표
- OpenXR/HMD 플러그인 활성화 및 프로젝트 설정  
- VR Preview 실행/종료를 원격 제어(Remote Control/Python)  
- VR에서의 성능 지표(FPS, 프레임 타임) 관찰 자동화

## 3) 프로젝트 설정
- 플러그인: **OpenXR**, **VR Template(옵션)** 활성화  
- 프로젝트 세팅: HMD 우선 실행, 스테레오 렌더링 옵션 점검  
- 입력 매핑: 모션 컨트롤러/트리거 버튼 등 바인딩 확인

## 4) VR Preview 원격 트리거(예시 Python)
```python
import unreal
# VR 프리뷰 실행 (엔진/버전별로 호출 방식 상이할 수 있으므로 프로젝트에 맞게 사용)
unreal.EditorLevelLibrary.editor_play_in_viewport()  # 필요 시 VR 프리뷰로 전환하는 콘솔/함수 호출 병행
unreal.SystemLibrary.execute_console_command(None, "stereo on")
unreal.SystemLibrary.execute_console_command(None, "hmd enable")
```
- 실무에서는 에디터 커맨드렛/툴바 액션을 Python 또는 블루프린트로 래핑 후 Remote Control로 호출

## 5) 성능 관찰 자동화
```python
import unreal
unreal.SystemLibrary.execute_console_command(None, "stat fps")
unreal.SystemLibrary.execute_console_command(None, "stat unit")
```
- 브리지 서버에서 로그/스크린샷(옵션: 에디터 자동화 툴) 수집 후, 모델이 리포트에 반영하도록 설계

## 6) 이슈 및 해결
- **HMD 미연결**: VR Preview 실패 → 장치 유무를 먼저 질의 후 분기 처리  
- **스테레오 토글 충돌**: 일부 뷰포트/모드 전환 시 콘솔명령 순서 의존 → 통합 함수로 안전하게 래핑  
- **성능 저하**: 에디터/VR 동시 실행 시 GPU 과부하 → 테스트 씬 간소화, 화면해상도 축소

## 7) 체크리스트
- [x] OpenXR 활성화 및 VR 설정  
- [x] VR Preview 원격 트리거 성공  
- [x] 성능 HUD 자동화(통계 켜기/끄기)  
- [x] 에러 케이스 분기 처리

## 8) 주차 회고
VR 환경에서도 **MCP 기반 자동화 루프**가 유효함을 확인했다. VR 특성상 안정적 재현을 위해 장치 상태 체크/콘솔 커맨드 순서를 더 엄격히 관리해야 한다. 다음 주에는 전체 결과를 통합하여 **제출용 산출물**(보고서/스크립트/코드 스니펫)을 정리한다.
