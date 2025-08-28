# Week 2 — MCP Filesystem 서버 구축 및 프로젝트 파일 수정 자동화

## 1) 주차 개요
이번 주는 **MCP Filesystem 서버**를 설치·구동하고, UE5 프로젝트 내 파일(C++/INI)을 **AI가 안전하게 읽고 수정**할 수 있도록 환경을 완성한다. 또한 최소 권한 원칙(least privilege)에 맞춰 접근 루트와 허용 패턴을 명확히 설정한다.

## 2) 학습 목표
- Filesystem 서버 설치 및 구동  
- 접근 루트/권한 제한 설계  
- 샘플 C++ 소스 수정 → Live Coding 수동 트리거까지의 기본 루프 경험

## 3) 설치 및 실행
```bash
# (권장) Node.js LTS 기반
npm i -g @modelcontextprotocol/server-filesystem

# 로컬 테스트 (루트는 UE 프로젝트 디렉터리)
mcp-filesystem "C:\Projects\McpLiveCodingDemo"
# 또는
npx -y @modelcontextprotocol/server-filesystem "C:\Projects\McpLiveCodingDemo"
```
- 환경 변수로 `MCP_FS_ROOTS` 등을 제공해 복수 루트를 제한적으로 노출 가능.

## 4) 보안/권한 설계
- **허용 루트**: `Source/`, `Config/`, `Content/`(텍스트 에셋만), `Scripts/`  
- **차단 대상**: OS 전역 경로, 엔진 설치 디렉터리, 빌드/중간 산출물(`Binaries`, `Intermediate`)  
- **파일 패턴**: `*.h`, `*.cpp`, `*.ini`, `*.py`, `*.uasset`은 텍스트만(바이너리는 수정 금지)  
- **로그**: 읽기/쓰기 트랜잭션에 대한 감사 로그 남김(추후 보고서에 활용)

## 5) 실습: 샘플 C++ 수정
- 대상: `Source/McpLiveCodingDemo/Player/MCPSampleComponent.cpp` (신규 컴포넌트 추가)  
- 목표: BeginPlay에서 로그 출력 + Tick에서 간단한 값 변화

```cpp
// MCPSampleComponent.h
#pragma once
#include "Components/ActorComponent.h"
#include "MCPSampleComponent.generated.h"

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class MCPLIVECODINGDEMO_API UMCPSampleComponent : public UActorComponent {
  GENERATED_BODY()
public:
  UMCPSampleComponent();
protected:
  virtual void BeginPlay() override;
public:
  virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;
private:
  float Accumulator = 0.f;
};
```

```cpp
// MCPSampleComponent.cpp
#include "MCPSampleComponent.h"
#include "Engine/Engine.h"
#include "GameFramework/Actor.h"

UMCPSampleComponent::UMCPSampleComponent() {
  PrimaryComponentTick.bCanEverTick = true;
}

void UMCPSampleComponent::BeginPlay() {
  Super::BeginPlay();
  UE_LOG(LogTemp, Log, TEXT("[MCP] Component attached to %s"), *GetOwner()->GetName());
}

void UMCPSampleComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) {
  Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
  Accumulator += DeltaTime;
  if (FMath::FloorToInt(Accumulator) % 2 == 0) {
    // 2초마다 화면 메시지 출력 (에디터 플레이 중 확인)
    if (GEngine) GEngine->AddOnScreenDebugMessage(-1, 0.f, FColor::Green, TEXT("MCP Tick OK"));
  }
}
```

- AI(혹은 사람이 MCP Filesystem을 통해) 위 소스를 생성/수정 → 저장  
- 에디터에서 **Ctrl+Alt+F11**로 Live Coding 수동 트리거 (자동 설정은 아직 비활성)

## 6) 검증 및 로그 예시(요약 형식)
- `logs/filesystem/2025-08-XX.txt`
  - `WRITE Source/McpLiveCodingDemo/Player/MCPSampleComponent.h`  
  - `WRITE Source/McpLiveCodingDemo/Player/MCPSampleComponent.cpp`  
  - `READ  Config/DefaultEngine.ini`
- 성공 기준: 컴포넌트가 에디터 실행 중 정상 컴파일되고, BeginPlay/온스크린 로그가 출력됨.

## 7) 문제 해결
- npx 실행 에러 → 전역 설치로 해결  
- 경로에 공백 포함 → 따옴표로 경로 감싸기  
- 바이너리 파일 쓰기 시도 → 서버 측 MIME/확장자 필터로 거부 처리

## 8) 체크리스트
- [x] Filesystem 서버 설치/실행  
- [x] 루트/패턴/감사로그 설정  
- [x] 샘플 C++ 수정 → Live Coding 트리거  
- [x] 오작동 사례 재현 및 차단 정책 점검

## 9) 주차 회고
파일 접근을 MCP로 표준화함으로써, AI 주도의 코드 편집이 **재현 가능**하고 **감사 가능한** 형태가 되었다. 다음 주에는 UE의 **Remote Control API**를 익혀, 에디터 내부 함수 호출과 파이썬 실행을 원격으로 트리거하는 기반을 갖춘다.
