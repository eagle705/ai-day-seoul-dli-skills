# 공식 자료로 보완한 Q&A

확인일: 2026-10-28. 강의 슬라이드의 원문을 변경하지 않고 설명을 보완한 자료다. 아래 내용은 공식 문서의 요약이며 실제 실습을 실행한 결과가 아니다. URL·버전·확인 범위는 [sources.json](sources.json)의 `official-web` 항목에도 기록했다.

주제에 해당하는 절만 읽는다. 제품 설정·최신 번호·지원 기능을 답할 때는 해당 공식 페이지를 다시 확인한다. `latest`와 개발 문서는 변할 수 있으며, 여기 적힌 버전을 사용자의 설치 버전으로 가정하지 않는다.

## OWASP / LLM Top 10 / Agentic Top 10

**OWASP는 무엇인가?** Open Worldwide Application Security Project는 소프트웨어 보안을 개선하는 비영리 재단이다. 조직 이름과 그 조직의 개별 Top 10 프로젝트를 구분한다. [OWASP 소개](https://owasp.org/about)

**LLM과 Agentic Top 10은 같은 목록인가?** 서로 보완하는 별도 목록이다. 강의의 OWASP 장표는 **GenAI LLM Top 10 2026**이다. **Top 10 for Agentic Applications 2026**은 계획·실행·위임하는 시스템의 위험을 따로 다룬다. 연도가 같아도 항목 코드가 다르므로 `LLM03:2026`처럼 목록과 연도를 함께 확인한다. 공식 사이트의 메뉴·번역본·작업반 목록에는 이전 번호가 남을 수 있어 목록 자체의 PDF를 기준으로 확인한다. [LLM 프로젝트](https://genai.owasp.org/initiatives/top-10-for-llm-and-genai/), [Agentic 프로젝트](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)

현재 확인한 LLM 2026 PDF의 목차:

| 코드 | 공식 명칭 | 한국어 설명 |
|---|---|---|
| LLM01:2026 | Prompt Injection | 프롬프트 인젝션 |
| LLM02:2026 | Sensitive Information Disclosure | 민감 정보 노출 |
| LLM03:2026 | Excessive Agency | 과도한 기능·권한·자율성 |
| LLM04:2026 | Supply Chain | 공급망 위험 |
| LLM05:2026 | Data and Model Poisoning | 데이터·모델 오염 |
| LLM06:2026 | Unbounded Consumption | 제한 없는 자원 소비 |
| LLM07:2026 | Misinformation | 잘못된 정보 |
| LLM08:2026 | Hidden Context Exposure | 숨겨진 컨텍스트 노출 |
| LLM09:2026 | Vector and Embedding Weaknesses | 벡터·임베딩 취약점 |
| LLM10:2026 | Improper Output Handling | 부적절한 출력 처리 |

번호·명칭 출처: [LLM 2026 공식 PDF, 목차](https://genai.owasp.org/download/56857/?tmstv=1785822482). 한국어는 설명용 번역이다. 2025 번호를 2026 번호와 섞지 않는다.

Agentic 목록의 예는 ASI01 목표 탈취, ASI03 신원·권한 악용, ASI06 메모리·컨텍스트 오염, ASI07 안전하지 않은 에이전트 간 통신, ASI08 연쇄 실패다. 이를 위 LLM 번호와 일대일 대응시키지 않는다. [Agentic 2026 공식 PDF, 목차 및 개요](https://genai.owasp.org/download/52117/?tmstv=1765059207)

## 인젝션 방어 / 출력 검증 / 실험 결과

**필터나 시스템 프롬프트만으로 막을 수 있는가?** OWASP는 입력·지시 분리, 출력 검증, 최소 권한, 사람의 검토, 모니터링을 함께 제시한다. 문자열 필터나 모델 판정 하나의 성공을 전체 보안 보장으로 표현하지 않는다. 출력은 다음 시스템에서 코드·SQL·HTML·툴 인자가 될 수 있으므로 사용하는 맥락에 맞춰 검증한다.

**실험에서 무엇을 측정하는가?** 목표별 관찰값을 나눈다. 승인 상태 변조는 파일 내용, 정보 유출은 보호 표식의 실제 목적지 도달, 권한 차단은 해당 경로의 실제 거부로 판단한다. 공격 성공 여부와 정상 작업을 불필요하게 막았는지도 함께 확인한다. 단일 문자열 탐지나 거절 문구만으로 모든 목표를 채점하지 않는다. 이는 강의의 “실제 효과 확인”을 보완하는 시험 설계다. [OWASP 인젝션 방어 가이드, 방어 및 Smoke-Testing 절](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

## OpenShell / 동적 정책 / audit와 enforce

다음은 확인 시 `Latest (v0.1.6)`으로 표시된 문서 기준이다.

- **정책을 실행 중 바꿀 수 있는가?** 파일시스템·프로세스 통제는 생성 시 고정되어 변경에 샌드박스 재생성이 필요하다. 네트워크 정책 등 동적 통제는 실행 중 갱신할 수 있다. “모든 정책이 즉시 갱신된다”고 답하지 않는다.
- **허용한 호스트는 안전한가?** 허용된 목적지도 반출 경로가 될 수 있다. 목적지 허용과 HTTP 메서드·경로 검사는 다른 범위다. L7 규칙이 없으면 특정 URL만 허용했다고 단정하지 않는다.
- **위반 로그가 있으면 차단된 것인가?** L7의 `audit`는 위반을 기록하면서 전달한다. `enforcement: enforce`에서 규칙 위반을 차단한다. 이 구분을 기본 네트워크 연결 허용·거부 전체에 일반화하지 않는다.
- **키가 모델에게 전달되는가?** 문서는 provider의 실제 키 대신 placeholder를 전달하고 프록시에서 치환하는 방식을 설명한다. 임의의 파일·환경변수·툴 출력에 있는 모든 비밀까지 자동으로 보호한다는 뜻은 아니다.

출처: [OpenShell 보안 모범 사례](https://docs.nvidia.com/openshell/latest/security/best-practices). 정확한 CLI·YAML은 사용자의 버전과 현재 문서로 다시 확인한다. 이 정보는 강의 실습의 배치나 인증 후 명령을 확인한 증거가 아니다. 이후 확보한 [실습 PDF](lab-modules.md)는 v0.1.2를 명시하므로, 해당 실습 절차는 PDF를 우선하고 여기의 v0.1.6 설명과 구분한다.

## 보안 경계 / 하네스 / 위임

**가드레일과 실제 경계는 어떻게 구별하는가?** 행동을 유도하는 검사와 권한을 강제하는 검사를 구분한다. 중요한 것은 제품 이름이나 코드 위치만이 아니라 효과가 생기는 경로를 워커가 우회할 수 있는가다. 인프라 통제도 정책·구현이 잘못되면 실패할 수 있다.

**위험 점수가 낮으면 권한을 늘려도 되는가?** NVIDIA의 설계 지침은 위험 신호를 권한 축소에 사용하고 권한을 추가하는 근거로 사용하지 않도록 한다. 권한은 독립된 인가로 정한다. 자식 작업도 권한 상한을 넘지 못하게 설계해야 한다. 이것은 참조 아키텍처의 원칙이며, 모든 현재 하네스가 그런 격리를 제공한다는 뜻은 아니다. [NVIDIA 에이전트 스택 보안 설계](https://developer.nvidia.com/blog/where-security-fits-in-an-ai-agent-stack/)

## MCP / OAuth / 토큰

**MCP로 연결되면 도구를 믿어도 되는가?** 프로토콜 연결 자체가 도구의 신뢰성이나 사용자 인가를 보장하지 않는다. 공식 보안 가이드는 프록시의 confused deputy, 토큰 대상 불일치, SSRF 등을 다룬다.

**토큰을 그대로 중계하면 왜 문제인가?** MCP 서버는 자신을 대상으로 발급된 토큰인지 검증해야 한다. 검증하지 않은 다른 서비스용 토큰을 받아 그대로 하위 API로 전달하는 token passthrough는 명세에서 금지한 패턴이다. 프록시는 사용자별·클라이언트별 동의를 확인해야 한다. OAuth 메타데이터의 URL도 신뢰할 수 없는 입력이므로 내부 주소·리다이렉트·DNS 변화를 고려한 SSRF 방어가 필요하다. [MCP 공식 보안 가이드, 2026-07-28 문서](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)

**OAuth를 붙이면 권한이 자동으로 최소화되는가?** 아니다. 토큰 권한을 실제 작업에 필요한 최소 범위로 제한해야 한다. RFC 9700은 authorization code 흐름에서 public client에 PKCE를 요구하고 confidential client에도 권고한다. 사용자 암호를 에이전트에 넘기는 방식과 위임된 접근을 구분한다. PKCE·TLS·서명 중 하나만으로 전체 인가를 대체하지 않는다. [IETF OAuth 보안 모범 사례, 2.1.1·2.3절](https://www.rfc-editor.org/rfc/rfc9700.html)

## MITRE ATLAS / OWASP / NIST의 차이

**ATLAS는 무엇인가?** AI 관련 공격자의 전술·기법을 실제 관찰과 현실적인 실험을 바탕으로 정리하는 지식 기반이다. OWASP의 위험 분류와 함께 공격 시나리오를 구체화할 때 사용한다. 정확한 기법 ID는 공식 항목을 확인하고 인용한다. [MITRE ATLAS 소개 자료](https://atlas.mitre.org/pdf-files/MITRE_ATLAS_Fact_Sheet.pdf)

**NIST AI RMF는 무엇을 더하는가?** AI 위험 관리의 조직적 틀이다. 1.0 Core의 네 기능은 GOVERN(책임·정책), MAP(맥락·위험 파악), MEASURE(평가·측정), MANAGE(처리·대응)이며 고정된 일회성 순서가 아니다. GOVERN은 나머지 기능 전반에 걸친다. [NIST AI RMF 1.0 Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)

AI RMF는 자발적 활용을 위한 프레임워크다. 사용했다는 이유만으로 법적 준수나 인증을 보장한다고 답하지 않는다. 확인 시 1.0 개정 작업이 진행 중이므로 향후 버전 상태를 다시 확인한다. [NIST AI RMF 공식 안내](https://www.nist.gov/itl/ai-risk-management-framework)

“OWASP는 위험 점검, ATLAS는 공격 행동 구체화, NIST는 지속적 위험 관리”라는 비교는 위 자료들을 수업에 연결한 설명용 요약이며 세 기관의 공식 일대일 매핑은 아니다.

## 강의의 7가지 설계 차원에 연결하기

아래 질문은 강의와 위 공식 자료를 연결한 **설명용 점검 질문**이며 OWASP의 공식 7요소 표가 아니다.

| 설계 차원 | 보완할 질문 | 읽을 절 |
|---|---|---|
| 입력 신뢰도 | 문서·툴 결과를 지시와 분리했는가? | 인젝션 방어 |
| 접근 민감도 | 목적·사용자·자원에 맞는 권한 범위를 강제하는가? | MCP / OAuth |
| 워크플로우 | 위임된 작업의 권한 상한과 승인 주체는 누구인가? | 보안 경계 |
| 행동 | 텍스트 응답과 외부 효과를 따로 검증하는가? | 출력 검증 |
| 메모리 | 저장한 지시·컨텍스트의 출처와 변경 이력을 확인하는가? | Agentic Top 10 |
| 툴 | 실행 코드·토큰·목적지에 어떤 권한을 부여했는가? | MCP / OpenShell |
| 사용자 인터페이스 | 표시한 승인 내용과 실제 실행 효과가 일치하는가? | 보안 경계 / 실험 결과 |
