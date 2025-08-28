# Week 4 — MCP 브리지 서버(Typescript) 제작: UE5 제어 툴 표준화

## 1) 주차 개요
모델이 UE5를 제어하기 쉽게, Remote Control 호출을 감싼 **MCP 브리지 서버**(Node/Typescript)를 제작하였다. 본 서버는 MCP SDK로 툴을 등록해 **표준화된 이름과 스키마**로 기능을 노출한다.

## 2) 학습 목표
- MCP TS SDK 사용법 이해(`registerTool` 패턴)  
- UE5 Remote Control 호출 래퍼 구현  
- 필수 툴 3종 제공: `ue_call`, `live_compile`, `play_in_editor`

## 3) 프로젝트 구조
```
ue5-mcp-bridge/
 ├─ src/
 │   └─ server.ts
 ├─ package.json
 ├─ tsconfig.json
 └─ .env  (UE_HOST=http://127.0.0.1:30010)
```

## 4) 주요 코드 (요약)
```ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import axios from "axios";
import { z } from "zod";

const UE_HOST = process.env.UE_HOST ?? "http://127.0.0.1:30010";

async function rcCall(objectPath: string, functionName: string, parameters: any = {}, generateTransaction = false) {
  const url = `${UE_HOST}/remote/object/call`;
  const { data } = await axios.put(url, { objectPath, functionName, parameters, generateTransaction }, {
    headers: { "Content-Type": "application/json" }
  });
  return data;
}

const server = new McpServer({ name: "ue5-bridge", version: "0.1.0" });

server.registerTool("ue_call", {
  title: "UE object call",
  description: "Call Blueprint/Python-exposed function via Remote Control API",
  inputSchema: {
    objectPath: z.string(),
    functionName: z.string(),
    parameters: z.record(z.any()).optional(),
    generateTransaction: z.boolean().optional(),
  }
}, async (args) => {
  const out = await rcCall(args.objectPath, args.functionName, args.parameters ?? {}, !!args.generateTransaction);
  return { content: [{ type: "text", text: JSON.stringify(out, null, 2) }] };
});

server.registerTool("live_compile", {
  title: "Live Coding Compile",
  description: "Trigger Live Coding compile"
}, async () => {
  const python = `
import unreal
world = unreal.EditorLevelLibrary.get_editor_world()
unreal.SystemLibrary.execute_console_command(world, "LiveCoding.Compile")
`;
  const out = await rcCall(
    "/Script/PythonScriptPlugin.Default__PythonScriptLibrary",
    "ExecutePythonCommandAdvanced",
    { PythonCommand: python, ExecutionMode: "EvaluateStatement" },
    false
  );
  return { content: [{ type: "text", text: `Triggered Live Coding.\n${JSON.stringify(out)}` }] };
});

server.registerTool("play_in_editor", {
  title: "PIE: Simulate",
  description: "Start Play-In-Editor simulate"
}, async () => {
  const python = `
import unreal
unreal.EditorLevelLibrary.editor_play_simulate()
`;
  const out = await rcCall(
    "/Script/PythonScriptPlugin.Default__PythonScriptLibrary",
    "ExecutePythonCommandAdvanced",
    { PythonCommand: python, ExecutionMode: "EvaluateStatement" },
    false
  );
  return { content: [{ type: "text", text: `PIE simulate started.\n${JSON.stringify(out)}` }] };
});

const transport = new StdioServerTransport();
await server.connect(transport);
```
> 주: 실제 배포 시에는 예외 처리, 타임아웃, 재시도 정책을 포함한다.

## 5) 빌드/실행
```bash
npm i
npm run build
node dist/server.js
# 또는 MCP 호스트에 명령/인자 형태로 등록
```

## 6) 테스트 시나리오
1. `ue_call`로 `BP_RemoteEcho.EchoMessage("Hello MCP")` 호출 → 뷰포트 로그 확인  
2. `live_compile` 호출 → Live Coding 성공 토스트/로그 확인  
3. `play_in_editor` 호출 → 에디터에서 Simulate 시작 확인

## 7) 보안/운영 고려
- `.env`로 UE 호스트/포트 관리, 외부 노출 시 HTTPS/인증 적용  
- 툴 입력 스키마에 zod 검증 적용(예상치 못한 파라미터 차단)  
- 감사 로그: 호출자, 시각, 파라미터, 결과/에러

## 8) 체크리스트
- [x] MCP TS SDK 기반 툴 등록  
- [x] Remote Control 래퍼 구현  
- [x] 3대 툴 정상 동작  
- [x] 예외/보안 항목 TODO 도출

## 9) 주차 회고
모델이 이해하기 쉬운 **표준 툴 명세**로 UE5 기능을 노출하는 데 성공. 다음 주에는 Filesystem + Bridge를 **하나의 워크플로**로 묶어 “수정→컴파일→실행→관찰” 루프를 완성한다.
