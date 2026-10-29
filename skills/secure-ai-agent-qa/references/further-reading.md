# 더 읽을거리: 질문과 실습에 연결하기

확인일: 2026-10-29. 과정 홈의 더 읽을거리와 공격 카드의 원 출처를 확인했다. 논문은 아래에 명시한 버전의 제목·초록을 중심으로 검토했으며, 전문의 모든 실험이나 코드를 재현한 것은 아니다. 공식 기술 문서와 연구자 자신의 논문·발견 보고서를 우선한다. 논문 초록의 성능 수치를 현재 제품이나 실습의 성공률로 재사용하지 않는다.

이 문서의 실습 연결·점검 질문은 원 자료를 수업에 적용한 해설이다. 원 논문의 공식 모듈 매핑이나 실험 결과가 아니다. 기본 답변에는 필요한 읽을거리만 골라 **무엇을 이해하기 위한 자료인지** 함께 설명한다. 단순 링크 나열이나 질문과 관계없는 전체 목록을 매번 출력하지 않는다.

## 과정 홈에서 권하는 기본 읽기

**ReAct — 추론과 행동이 어떻게 연결되는가?**

- [ReAct: Synergizing Reasoning and Acting in Language Models, v3](https://arxiv.org/abs/2210.03629v3). 추론 텍스트와 외부 행동을 번갈아 구성해 정보를 얻고 계획을 갱신하는 접근을 제시한다.
- 모듈 1 연결: 제안된 단계, 실행된 툴 호출, 반환된 관찰을 분리해 추적한다. ReAct는 권한 강제 기법이 아니며, 모든 하네스가 동일하게 구현된다는 뜻도 아니다.
- 꼬리 질문: “관찰값을 누가 만들고, 거기에 지시가 섞이면 누가 결정하는가?”

**간접 프롬프트 인젝션 — 사용자 메시지가 없어도 왜 공격되는가?**

- [Not what you've signed up for, v2](https://arxiv.org/abs/2302.12173v2). 검색·외부 데이터에 심은 지시가 LLM 통합 애플리케이션의 행동을 바꿀 수 있음을 분석한다.
- 모듈 3·5 연결: 정상 인덱싱 작업은 그대로 두고 읽는 문서만 바꾸는 이유를 설명한다. 검색 결과가 지시 권한을 갖지 않는다는 경계를 짚는다.
- 꼬리 질문: “모델이 문서를 읽었다는 증거와 그 지시를 따랐다는 증거는 각각 무엇인가?”

**The Confused Deputy — 누구의 권한으로 실행했는가?**

- [Norm Hardy, The Confused Deputy (1988), 대학 보관본](https://www.cs.umd.edu/~jkatz/security/downloads/capabilities.html). 대리 프로그램이 호출자의 요청과 자신의 특권을 혼동해 보호 파일을 덮어쓴 사례다.
- 모듈 3~5 연결: 요청자가 파일에 직접 접근하지 못해도 권한이 큰 에이전트·헬퍼를 이용할 수 있다. 인증된 호출과 그 행동에 필요한 인가는 별개다.
- 꼬리 질문: “자원 이름을 전달한 것과 그 자원에 대한 권한을 위임한 것은 같은가?”

**Saltzer–Schroeder — 최소 권한과 완전한 중재는 무엇인가?**

- [The Protection of Information in Computer Systems: Basic Principles](https://web.mit.edu/Saltzer/www/publications/protection/Basic.html). 필요한 최소 권한, 모든 접근에 대한 검사, 기본 거부 등 보호 원칙을 설명한다.
- 모듈 8·10 연결: 네트워크 경로만 검사하면 로컬 파일 쓰기 경로는 남을 수 있다. UI에서 버튼을 감추거나 연결 한 번을 승인하는 것과 모든 실제 접근을 중재하는 것은 다르다.
- 꼬리 질문: “동일한 효과로 가는 다른 경로를 빠뜨리지 않았는가?”

**Reflexion — 학습과 메모리 변경은 어떻게 다른가?**

- [Reflexion: Language Agents with Verbal Reinforcement Learning, v4](https://arxiv.org/abs/2303.11366v4). 가중치를 갱신하는 대신 언어 피드백을 에피소드 메모리에 남겨 다음 시도에 활용한다.
- 과정 홈이 모듈 11 읽을거리로 연결한다. 다만 모듈 11 상세 PDF는 제공되지 않았다. 저장한 절차의 개선과 모델 파인튜닝을 혼동하지 않도록 설명한다.
- 꼬리 질문: “개선됐다는 절차를 수정에 쓰지 않은 사례와 공격에도 시험했는가?” 이는 스킬의 평가 제안이다.

**AgentDojo — 공격 거부와 업무 성공을 어떻게 함께 평가하는가?**

- [AgentDojo, v3](https://arxiv.org/abs/2406.13352v3). 신뢰할 수 없는 툴 데이터를 사용하는 에이전트의 작업·공격·방어를 확장 가능하게 평가하는 환경이다. 공격이 없어도 작업 실패가 생길 수 있음을 보고한다.
- 과정 홈의 모듈 11 연결: 정상 입력의 업무 성공, 공격 입력에서의 업무 성공, 공격 목표 달성을 각각 본다. 현재 실습에 AgentDojo가 설치되어 있거나 이 점수가 최종 평가 점수라는 뜻은 아니다.
- 꼬리 질문: “전부 거절해서 공격이 실패한 방어를 유용한 방어라고 볼 수 있는가?”

OWASP·ATLAS·NIST는 홈의 다른 기본 읽을거리다. 정의와 차이는 [공식 자료 보완 Q&A](web-security.md)의 해당 절을 읽는다. 특히 실습 카드의 OWASP **2025** 번호와 강의의 **2026** 번호를 그대로 섞지 않는다.

## 모듈 5: 검색·툴·유출 경로

| 읽을거리 | 이해할 내용 | 실습에 적용할 질문 |
|---|---|---|
| [PoisonedRAG](https://arxiv.org/abs/2402.07867) | 검색 저장소의 소수 악성 문서로 특정 답을 유도하는 공격을 연구 | 검색 상위에 올랐다는 것과 그 문장을 따랐다는 것을 따로 확인했는가? |
| [Invariant의 Tool Poisoning 발견 보고](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) | 모델이 읽는 툴 설명에 지시를 심는 공격 | 실제 코드가 같아도 설명만 바꾸면 어떤 결과가 달라지는가? |
| [Invariant의 GitHub MCP 공격 시연](https://invariantlabs.ai/blog/mcp-github-vulnerability) | 공개 이슈가 넓은 권한의 에이전트를 거쳐 비공개 데이터를 공개 PR로 옮기는 흐름 | 문서 진입점·민감 자원·반출 채널의 권한을 누가 보유하는가? |
| [Simon Willison의 Lethal Trifecta 원문](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) | 민감 데이터·신뢰 불가 입력·외부 통신의 위험한 결합 | 한 연결을 끊고 다른 경로까지 확인했는가? |

이들은 발표 당시의 연구·시연이다. 특정 제품이 지금도 같은 취약점을 가진다고 단정하지 않는다. 실습 출력함은 실습 밖으로 나가지 않는 모형이므로 위 실세계 시연과 효과 범위가 다르다.

## 모듈 6~7: 멀티턴·메모리·공급망

| 읽을거리 | 이해할 내용 | 실습에 적용할 질문 |
|---|---|---|
| [Crescendo](https://arxiv.org/abs/2404.01833) | 무해해 보이는 대화에서 이전 답을 이용해 점진적으로 요청을 확대하는 멀티턴 탈옥 | 메시지 한 개 검사와 대화 누적 효과 검사는 어떻게 다른가? |
| [How Johnny Can Persuade LLMs to Jailbreak Them](https://arxiv.org/abs/2401.06373) | 설득 전략을 이용한 공격을 연구 | 직함·긴급성·승인 주장과 검증된 인가 증거를 구분했는가? |
| [Prompt Infection](https://arxiv.org/abs/2410.07283) | 서로 연결된 에이전트 사이에 지시가 복제·전파되는 공격을 연구 | 인계 파일이 어떤 세션을 거쳐 다음 파일로 전달됐는가? |
| [PyTorch-nightly 공급망 사고 공식 공지](https://pytorch.org/blog/compromised-nightly-dependency/) | 2022년 12월 Linux nightly의 악성 torchtriton 의존성 사건 | 정상 출력 외의 파일 접근·효과와 실행 계정 권한도 확인했는가? |

연구의 공격 성공률은 해당 모델·데이터·시도 예산의 결과다. 모든 최신 모델이 같은 비율로 실패한다고 답하지 않는다. PyTorch 공지의 역사적 제거 명령을 현재 사용자 환경에 진단 없이 실행하도록 제안하지 않는다.

## 모듈 8·10: 버전과 정책 증명의 범위

- [OpenShell v0.1.2 릴리스](https://github.com/NVIDIA/OpenShell/releases/tag/v0.1.2): PDF의 실습 버전을 확인하는 기준이다. 기존 웹 보완 자료가 확인한 v0.1.6 문법·기능을 자동으로 이 실습에 적용하지 않는다.
- [Policy Prover 문서, PDF가 링크한 고정 커밋](https://github.com/NVIDIA/OpenShell/blob/6648bd0c290efbc41ba131ee9831ee45cd431f94/docs/how-it-works/policies/prover.mdx): SMT 모델 안에서 정책이 경계를 초과하는지 검사한다. 문서는 boundary check와 proposal risk check가 서로 다른 질문이며 하나의 통과가 다른 통과를 뜻하지 않는다고 설명한다. 지원하지 않는 정책 특징도 있다. CLI는 정책을 적용·승인하는 도구가 아니다.
- 이 고정 커밋 문서를 읽었다는 사실만으로 v0.1.2에 해당 도구가 포함된다고 추론하지 않는다. 모듈 10의 짧은 정책 검사 스크립트는 실제 요청 시험이나 SMT 엔진과 구별한다.

## 관련 연구를 더 찾을 때

추가 검색으로 확인한 [USENIX Security 2024: Formalizing and Benchmarking Prompt Injection Attacks and Defenses](https://www.usenix.org/conference/usenixsecurity24/presentation/liu-yupei)는 공격·방어를 공통 기준에서 평가하는 연구다. 모듈 9~10의 평가 질문을 구체화할 때 읽는다. 발표 소개·초록을 확인한 범위이므로 상세 지표·실험 수치를 답하려면 논문 해당 절을 추가로 읽는다.

검색에서 발견한 자료와 직접 읽은 자료를 구분한다. [lab-reading-links.json](lab-reading-links.json)은 PDF에서 추출한 **46개 URL의 위치 목록**이며 모든 링크의 내용을 검토했다는 뜻이 아니다. CISA 링크는 403, MSRC 링크는 JavaScript 안내만 반환해 본문을 확인하지 못했다. 그런 자료의 패치 상태·기술 세부사항은 현재 확인된 사실로 쓰지 않는다.
