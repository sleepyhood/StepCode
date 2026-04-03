---
marp: true
theme: default
paginate: true
class: slide-section
style: |
  /* ==== Font (옵션) ==== */
  @font-face {  
      font-family: 'SDSamliphopangche_Outline';
      src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts-20-12@1.0/SDSamliphopangche_Outline.woff") format('woff');
      font-weight: normal;
      font-style: normal;
  }


  /* ==== Layout & Typography ==== */
  .slide-title, .slide-part {
  display:flex; flex-direction:column; justify-content:center; align-items:center;
  height:100%; text-align:center; color:#000; font-size:2em; font-weight:500;
  }
  .slide-title p { font-size:0.6em; }

  .slide-section { position:relative; height:100%; padding-top:0 !important; margin-top:0 !important; }
  .slide-section h1 { font-size:1.1em; font-weight:500; color:#000; margin-top:-2em; margin-bottom:0.2em; margin-left:-0.6em; }
  .slide-section h1::after { content:""; display:block; width:100%; border-bottom:1px solid #444; margin-top:0.8em; }

  .slide-section p, .slide-section ul, .slide-section ol {
  margin-left:-0.6em; white-space:pre-line; color:#4F6B81; font-size:0.8em; margin-top:0.7em; line-height:0.8;
  }

  img.centered-img { max-width:60vw; display:block; margin:0 auto; }

  .onePage, .onePage-max {
  display:flex; flex-direction:column; justify-content:flex-start; align-items:center;
  margin:0 auto; padding:0; box-sizing:border-box; width:100%; max-height:100%; min-width:500px;
  }
  .onePage table, .onePage-max table {
  color:#4F6B81; font-size:clamp(0.6em, 1.2vw, 0.85em);
  border-collapse:collapse; width:auto; max-width:100%;
  }
  .onePage th, .onePage td { padding:0.4em 0.6em; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }

  .onePage-small, .onePage-middle, .onePage-micro {
  display:flex; justify-content:center; align-items:center; margin:-20px auto; max-height:60vh; color:#4F6B81;
  font-size:clamp(0.6em, 1.2vw, 0.85em);
  }
  .onePage-small  { max-width:50%; }
  .onePage-middle { max-width:80%; }
  .onePage-micro  { max-width:20%; }
  .onePage-max    { display:flex; justify-content:center; align-items:center; margin:0 auto; max-width:100%; }

  .slide-2column { display:flex; justify-content:space-between; gap:20px; align-items:stretch; min-height:300px; --col-left:8; --col-right:2; }
  .slide-2column > div { display:flex; flex-direction:column; justify-content:center; align-items:flex-start; flex:1; }
  .slide-2column img { max-width:100%; height:auto; display:block; }

  .slide-2column.ratio-82 > div:first-child { flex:8; } .slide-2column.ratio-82 > div:last-child { flex:2; }
  .slide-2column.ratio-73 > div:first-child { flex:7; } .slide-2column.ratio-73 > div:last-child { flex:3; }  
  .slide-2column.ratio-37 > div:first-child { flex:3; } .slide-2column.ratio-37 > div:last-child { flex:7; }
  .slide-2column.ratio-72 > div:first-child { flex:7; } .slide-2column.ratio-72 > div:last-child { flex:2; }
  .slide-2column.ratio-64 > div:first-child { flex:6; } .slide-2column.ratio-64 > div:last-child { flex:4; }
  .slide-2column.ratio-46 > div:first-child { flex:4; } .slide-2column.ratio-46 > div:last-child { flex:6; }
  .slide-2column.ratio-55 > div:first-child { flex:5; } .slide-2column.ratio-55 > div:last-child { flex:5; }
  .slide-2column.ratio-19 > div:first-child { flex:1; } .slide-2column.ratio-19 > div:last-child { flex:9; }

  .slide-2column > div:first-child, .slide-2column > div:last-child {
    flex: var(--col-left); align-items: flex-start; justify-content: flex-start; padding: 0em; text-align: left;
  }

  .lh-relaxed, .lh-relaxed p, .lh-relaxed li { line-height:0.8; }
  .lh-relaxed li + li { margin-top:.35em; }
  .lh-relaxed code { line-height:2.2; }

  pre, code { font-size:16px; font-family:'Consolas', monospace; line-height:1.5; background:#f5f5f5; padding:10px; border-radius:4px; overflow-x:auto; }
  .code-lg { margin-top:.35em; align-items:stretch; }
  .code-lg pre { width:90%; max-width:none; font-size:0.95rem; line-height:1.45; padding:0.9rem 1.1rem; }
  .code-lg pre code { font-size:0.95rem; }
  .code-mi { margin-top:.35em; align-items:stretch; }
  .code-mi pre { width:55%; max-width:none; font-size:0.95rem; line-height:1.45; padding:0.9rem 1.1rem; }
  .code-mi pre code { font-size:0.95rem; }
  .caption { font-size:0.4em; color:#666; font-style:italic; text-align:center; }
  .onePage-small .caption { font-size:0.8em; }

  /* ==== Callouts ==== */
  .callout { font-size:20px; border-left:6px solid #4F6B81; background:#f7fbff; padding:0.6em 1.2em; margin:0.8em 0; border-radius:6px; }
  .callout.warn { border-left-color:#d97706; background:#fff7ed; }
  .callout.ok { border-left-color:#059669; background:#ecfdf5; }
  .callout.tip { border-left-color:#3b82f6; }
  .callout.danger { border-left-color:#ef4444; background:#fee2e2; }


  .fig.top100{
    margin-top: -100px;
  }
  .fig.top75{
    margin-top: -75px;
  }
  .fig.top50{
    margin-top: -50px;
  }
  .fig.top25{
    margin-top: -25px;
  }
  .replace-txt{

      display: none;
  }



  .slide-3column { display:flex; justify-content:space-between; gap:20px; align-items:stretch; min-height:300px; --col-left:8; --col-right:3; }
  .slide-3column > div { display:flex; flex-direction:column; justify-content:center; align-items:flex-start; flex:1; }
  .slide-3column img { max-width:100%; height:auto; display:block; }

  .slide-3column > div:first-child, .slide-3column > div:last-child {
    flex: var(--col-left); align-items: flex-start; justify-content: flex-start; padding: 0em; text-align: left;
  }



  .two-col{display:grid;grid-template-columns:1.15fr 1fr;gap:28px;align-items:start}
  .callout{background:#f7fbfe;border:1px solid #d9e7f0;border-radius:14px;padding:14px 16px}
  .kicker{font-weight:800;color:#2f4a5b;margin:0 0 8px 0}
  .note{color:#6e8798;font-size:14px}
  .why{margin-top:16px}
  .foot{margin-top:10px;color:#6e8798;font-size:12px}
  .code-xl pre{font-size:18px;line-height:1.5;padding:14px;border-radius:12px}
---

<!-- Opening Title -->
<section class="slide-title">
클라우드 컴퓨팅 이해 15주차
</section>

<!--SCRIPT
v: 1
id: "15.opening"
title: "오프닝"
ko: |
  안녕하세요. 이번 시간에는 지금까지 배운 클라우드 컴퓨팅에 관해, 연계하여 정리해보도록 하겠습니다. 각 주제에서 “왜 그렇게 설계하는가”를 우선 설명하고 “무엇을 먼저 확인할 것인가”로 마무리하겠습니다. 한 학기 동안 손에 익힌 실습 맥락을 떠올리며, 자신의 서비스에 대입해 보시기 바랍니다.
hangul_pron: ""
-->

---

<section class="slide-section">

<h1>목차</h1>

**■ 클라우드 컴퓨팅 이해 Summary**

<div class = "slide-2column ratio">

<div>

- 15.1 클라우드 핵심 개념 재정의
  (IaaS·PaaS·SaaS, 리전·AZ, 탄력성)
  - 15.1.1 서비스 모델 비교 요점
  - 15.1.2 글로벌 인프라와 가용성의 의미
- 15.2 공유 책임 모델 & 보안 기본기
  - 15.2.1 IAM 최소권한·정책 구성 요점
  - 15.2.2 비밀관리·네트워크 경계(SG/NACL)
- 15.3 비용/과금 감각 정리
  - 15.3.1 리소스 선택 → 비용 영향 경로
  - 15.3.2 태깅·Budget·Cost Explorer 요약
  </div>

<div>

- 15.4 컴퓨팅 선택 지도
  (EC2, Lambda, ECS/EKS, App Runner)
  - 15.4.1 선택 기준(부하 패턴·운영 복잡도)
  - 15.4.2 전환/확장 시 고려사항
- 15.5 컨테이너·이미지·레지스트리 핵심
  (Docker → ECR)
  - 15.5.1 Dockerfile·멀티스테이지·포트 바인딩
  - 15.5.2 태그 vs Digest·불변성
  </div>

</div>

</section>

<!--SCRIPT
v: 1
id: "15.toc-2col-1"
title: "목차(1/2)"
ko: |
  먼저 15.1에서 서비스 모델을 다시 정리합니다. 사례를 중심으로 구분하고, 리전과 가용영역이 왜 물리적으로 분리되었는지, 탄력성과 내결함성이 어떤 운영 비용을 줄여주는지 짚겠습니다. 이어서 15.2에서는 공유 책임 모델을 실무 관점으로 재정리합니다. 클라우드가 보장하는 구간과 사용자가 반드시 책임져야 하는 구간을 구분하고, IAM 최소권한 설계, 정책 구성과 권한 위임, 비밀관리와 네트워크 경계(보안 그룹과 NACL)의 차이를 정리합니다.
  15.3에서는 비용을 기능 목록이 아니라 ‘의사결정의 결과’로 설명합니다. 인스턴스 유형과 저장소·네트워크 선택이 비용에 전파되는 경로를 그림으로 복기하고, 태그 표준화와 Budget, Cost Explorer로 “누가 무엇 때문에 비용을 만들었는가”를 추적하는 기본 절차를 요약하겠습니다. 15.4는 컴퓨팅 선택 지도입니다. 부하 패턴과 운영 복잡도에 따라 어떤 선택이 합리적인지 기준을 제시합니다. 마지막으로 15.5에서 컨테이너 핵심을 빠르게 정리합니다. Dockerfile과 멀티스테이지 빌드, 포트 바인딩의 함정, 이미지 태그와 다이제스트의 의미, 그리고 ECR을 활용한 불변 아티팩트 관리 원칙을 실습 경험과 연결해 되짚겠습니다.
hangul_pron: ""
-->

---

<section class="slide-section">

<h1>목차</h1>

**■ 클라우드 컴퓨팅 이해 Summary**

<div class = "slide-2column ratio">

<div>

- 15.6 네트워킹·트래픽 경로 요약
  (VPC, Subnet, ALB/HTTPS)
  - 15.6.1 L3/4/7 관점의 문제해결 순서
  - 15.6.2 헬스체크·도메인·인증서 포인트
- 15.7 스토리지·데이터베이스 개요
  (S3/EBS/EFS, RDS/DynamoDB, 캐시)
  - 15.7.1 워크로드 특성 → 서비스 매핑
  - 15.7.2 일관성·확장성·백업 요점
- 15.8 모니터링·로깅·알람 최소 세트
  - 15.8.1 CloudWatch Metrics/Logs·지표 읽기
  - 15.8.2 Logs Insights·알람 임계 설계
  </div>

<div>

- 15.9 ML 기본기 총정리(학습·평가·배포)
  - 15.9.1 데이터 분할과 과적합 신호
  - 15.9.2 평가지표 선택 가이드
- 15.10 추론 서비스 경량 MLOps 요약
  (FastAPI → Docker → ECR → App Runner)
  - 15.10.1 헬스체크·환경변수·Start Command
  - 15.10.2 콜드스타트·스케일·로그 연계
  </div>

</div>

</section>

<!--SCRIPT
v: 1
id: "15.toc-2col-2"
title: "목차(2/2)"
ko: |
  후반부는 네트워크에서 시작합니다. 15.6에서 VPC와 서브넷, L3·L4·L7 수준의 문제해결 순서를 다시 세우고, ALB·HTTPS·헬스체크와 도메인·인증서 연계를 통해 “어디가 아픈지 먼저 보이는” 설계를 정리합니다. 15.7에서는 스토리지와 데이터베이스 선택 기준을 워크로드 특성으로 환원합니다. S3·EBS·EFS의 사용 위치, RDS와 DynamoDB의 데이터 모델과 일관성·확장성·백업 전략을 비교하며 캐시를 언제 끼워 넣을지 판단 기준을 남겨두겠습니다.
  15.8은 모니터링·로깅·알람의 최소 세트입니다. CloudWatch 지표와 로그를 함께 읽는 법, Logs Insights로 원인 구간을 좁히는 쿼리 습관, 알람 임계값을 ‘사용자 체감’과 연결해 잡는 방법을 실습 흐름으로 정리합니다. 15.9에서는 머신러닝 기본기를 압축 복습합니다. 학습·검증·테스트 분할과 과적합 신호, 평가지표 선택 가이드를 다시 확인합니다. 15.10에서 FastAPI → Docker → ECR → App Runner로 이어지는 경량 MLOps 경로를 실제 배포 체크리스트로 재정리합니다. 헬스체크와 환경변수, 시작 커맨드, 콜드스타트와 자동 확장, 로그 연계를 하나로 묶어 “배포 직후 무엇을 보고 무엇을 바꿀지”를 분명히 하며 마무리하겠습니다.
hangul_pron: ""
-->

---

<section class="slide-part">
15.1 클라우드 핵심 개념 재정의
<br/>(IaaS·PaaS·SaaS, 리전·AZ, 탄력성)
</section>

<!--SCRIPT
v: 1
id: "15.1-part"
title: "파트 오프닝"
ko: |
  서비스 모델, 글로벌 인프라, 탄력성을 하나의 의사결정 흐름으로 다시 엮겠습니다. 먼저 무엇을 누가 관리하는지부터 분명히 하고, 이어서 어디에 어떻게 배치해야 지연과 장애를 줄일 수 있는지 확인하겠습니다. 마지막으로 트래픽이 급격히 변할 때 애플리케이션이 멈추지 않도록 어떤 원칙과 메커니즘을 준비해야 하는지 정리합니다. 2주차에서 구분했던 IaaS·PaaS·SaaS의 경계, 4주차에서 살펴본 리전과 가용영역, 그리고 실습에서 체험한 오토스케일과 캐시, 매니지드 런타임의 동작을 한 흐름 안에서 재배치해 보겠습니다. 오늘의 목적은 용어 암기가 아니라, 팀이 직접 선택할 때 흔들리지 않을 기준을 머릿속에 남기는 것입니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.1.1 서비스 모델 비교 요점</h1>

**■ 정의 & 대표 예시(2주차 참조)**

<div class = "slide-2column">
<div>

- **IaaS**: 인프라를 빌려 쓰는 모델  
  예) EC2, VPC, EBS, S3(스토리지)
- **PaaS/FaaS**: 애플리케이션 실행 기반 제공  
  예) Elastic Beanstalk, RDS(DBaaS), **Lambda(FaaS)**
- **SaaS**: 완성된 소프트웨어 구독  
 예) Gmail, Office 365, Slack
</div>
<div>

![alt text](assets/w15_image.png)

</div>
</div>

<div class = "fig top100"></div>

**■ 선택 기준(수업 전반)**

- **운영 책임**(패치/확장/백업)을 어디까지 맡을지
- **개발 속도 vs 제어권** 균형
- **비용 구조**(사용량·트래픽 패턴)와 **팀 역량**
</section>

<!--SCRIPT
v: 1
id: "15.1.1-overview"
title: "서비스 모델 핵심"
ko: |
  IaaS는 서버와 네트워크, 스토리지 같은 토대를 필요할 때 즉시 확보하도록 해 주는 층이며, 사용자는 운영체제와 런타임, 미들웨어를 직접 선택하고 유지보수합니다. PaaS와 FaaS는 그 위의 반복적인 관리 부담을 공급자가 가져가서 개발자는 코드와 설정에 집중할 수 있도록 돕습니다. SaaS는 완성된 소프트웨어를 그대로 구독해 업무 문제를 가장 빠르게 해결하는 경로입니다. 선택은 언제나 교환관계의 문제입니다. 세밀한 제어와 맞바꾸는 운영 비용을 감당할 이유가 있는지, 개발 속도를 끌어올려야 할 시점인지, 과금 단위가 실제 트래픽 패턴과 맞물리는지, 그리고 우리 팀의 역량과 책임 범위가 어디까지인지 차분히 따져야 합니다. 같은 워크로드라도 시험 단계와 본운영 단계에서 답이 달라질 수 있음을 전제로, 초기에는 관리형 서비스를 폭넓게 활용하고 필요할 때만 하향 이동하는 전략이 안정적입니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.1.1 서비스 모델 비교 요점</h1>

**■ 관리 책임(Shared Responsibility) 스냅샷**

<div class="onePage">

| 구분          | 공급자 관리                              | 사용자 관리                                        |
| ------------- | ---------------------------------------- | -------------------------------------------------- |
| **IaaS**      | 데이터센터·하드웨어·가상화·기본 네트워크 | OS 설정·패치, 런타임/미들웨어, 데이터·앱, IAM 정책 |
| **PaaS/FaaS** | IaaS + OS·런타임·스케일 엔진·백업 일부   | 애플리케이션 코드, 설정/시크릿, 데이터 스키마      |
| **SaaS**      | 애플리케이션 포함 **대부분**             | 계정/권한, 데이터 품질·보존, 통합 설정             |

</div>

- 실습 연결: **RDS 백업/멀티AZ(7주)**, **Lambda 동시성(9주)**, **App Runner 자동 확장(14주)**
→ “운영 책임의 이동” 체감
</section>

<!--SCRIPT
v: 1
id: "15.1.1-srm"
title: "Shared Responsibility 요약"
ko: |
  책임 분담은 경계의 변화를 체감하는 일입니다. IaaS에서는 데이터센터와 가상화, 기본 네트워크를 공급자가 책임지지만, 운영체제 패치와 미들웨어 설정, 데이터 보안과 애플리케이션 품질은 사용자 몫으로 남습니다. PaaS와 FaaS로 올라가면 운영체제와 런타임, 스케일 엔진, 백업의 일부까지 공급자가 가져가므로 사용자는 코드와 시크릿, 스키마에 집중할 수 있습니다. SaaS에서는 애플리케이션 자체도 공급자가 운영하지만, 계정과 권한, 데이터의 정확성·보존·통합 설정은 여전히 사용자의 의사결정과 관리가 필요합니다. 실습에서 확인했듯이 RDS의 스냅샷과 다중 AZ는 자동으로 제공되지만 테이블 설계와 쿼리 품질은 사용자가 관리해야 했고, Lambda의 동시성은 플랫폼이 확장하지만 타임아웃과 IDLE 연결, 외부 API 한도는 사용자 설계의 문제였습니다. 또한 App Runner의 자동 확장이 편리했어도 시작 커맨드와 헬스체크 경로, 환경변수 관리가 부정확하면 배포가 불안정해졌습니다. 결론적으로 남는 책임은 정책과 자동화, 가시성으로 줄여야 하며, 이는 IAM 최소권한과 시크릿 관리 표준화, 배포 파이프라인의 일관성으로 실천됩니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.1.2 글로벌 인프라와 가용성의 의미</h1>

**■ Region / AZ / Edge(4·6·10주 참조)**

- **Region**: 물리적 권역 단위(규제·지연·비용 기준으로 선택)
- **AZ(가용영역)**: 동일 Region 내 **독립 전원·네트워크** 데이터센터 묶음  
  ↳ ⚠ **AZ 식별문자(a,b,c)는 계정마다 매핑이 다를 수 있음**
- **Edge Location**: **CloudFront**가 전 세계 사용자 가까이서 캐싱

**■ 왜 중요한가**

- **컴플라이언스·데이터 주권**, **지연 최소화**, **장애 도메인 분리**(멀티AZ)
</section>

<!--SCRIPT
v: 1
id: "15.1.2-ginfra"
title: "Region·AZ·Edge 재정의"
ko: |
  리전은 데이터가 실제로 머무는 물리적 권역이며 규제, 지연, 비용을 함께 결정합니다. 가용영역은 동일 리전 안에서 전원과 네트워크가 분리된 데이터센터 묶음으로, 장애 도메인을 물리적으로 분리해 주는 기초 단위입니다. 여기서 주의할 점은 AZ의 식별 문자가 계정별로 다르게 매핑될 수 있다는 사실입니다. 같은 ‘ap-northeast-2a’ 표기라도 다른 계정에서는 서로 다른 물리 영역을 가리킬 수 있으므로, 설계 시에는 반드시 가용영역의 고유 식별자 기준으로 분산 여부를 확인해야 합니다. 엣지 로케이션은 전 세계 사용자 가까이에서 콘텐츠를 제공해 체감 속도를 높이고, 오리진으로 향하는 트래픽과 대역폭 비용을 줄입니다. 배포 관점에서 사용자는 먼저 컴플라이언스를 만족하는 리전을 고르고, 지연과 복구 목표에 맞춰 멀티 AZ를 구성하며, 정적 자산과 이미지·동영상을 엣지에 캐싱해 사용자 경험을 안정화합니다. 이 순서를 지키면 비용과 성능, 가용성을 동시에 설득력 있게 설명할 수 있습니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.1.2 글로벌 인프라와 가용성의 의미</h1>

**■ 탄력성(Elasticity)**

- **수평 확장**: EC2 **Auto Scaling**으로 인스턴스 수 자동 증감(5주)
- **동시성 확장**: **Lambda**가 요청·**GB-초** 기준으로 자동 스케일(9주)
- **매니지드 런타임**: **App Runner**/**ECS(Fargate)** 의 오토스케일(14주)
- **엣지 캐싱**: **CloudFront**로 오리진 호출·대역폭 감축, 체감속도↑(10주)

> 원칙: **무상태(stateless)**, **지표 기반 정책**, **급감·급증 모두에 대한 안전장치**(쿨다운·큐·버짓 알림)

</section>

<!--SCRIPT
v: 1
id: "15.1.2-elasticity"
title: "탄력성 핵심"
ko: |
  탄력성은 “얼마나 큰 용량을 미리 사둘 것인가”의 문제가 아니라 “수요 변화에 얼마나 빠르고 안전하게 따라붙는가”의 문제입니다. EC2에서는 오토 스케일링 그룹을 통해 지표 기반으로 인스턴스 수를 증감시키고, 배치와 헬스체크, 쿨다운을 함께 설계해 과도한 요동을 막아야 합니다. Lambda와 같은 FaaS에서는 요청 수와 실행 시간, 메모리로 표현되는 사용량이 직접 과금과 확장에 연결되므로, 동시성 제한과 타임아웃, 외부 의존성의 연결 재사용을 통해 콜드스타트와 비용을 함께 관리합니다. App Runner나 Fargate 기반의 컨테이너 런타임은 빌드 아티팩트의 불변성, 시작 커맨드의 결정성, 헬스체크 엔드포인트의 신뢰성이 갖춰질 때 예측 가능한 자동 확장이 가능합니다. 여기에 CloudFront의 캐싱을 조합하면 오리진 요청을 줄여 백엔드의 변동 폭 자체를 낮출 수 있습니다. 결국 무상태 설계를 기본으로 하고, 지표와 알람을 통해 확장·축소의 트리거를 명확히 하며, 급증과 급감 모두를 고려한 안전장치—큐잉, 리밋, 예산 알림—를 미리 넣어 두는 것이 탄력성을 품질과 비용의 균형으로 연결하는 방법입니다.
hangul_pron: ""
-->

---

<section class="slide-part">
15.2 공유 책임 모델 & 보안 기본기
</section>

<!--SCRIPT
v: 1
id: "15.2-part"
title: "파트 오프닝 — 공유 책임 & 보안 기본기"
ko: |
  이번 파트에서는 보안을 기능의 나열이 아니라 책임과 운영의 흐름으로 정리하겠습니다. 이어서 비밀을 안전하게 저장·전달·순환하는 방법을 확인하고, 서비스 경계에서 실제로 트래픽을 통제하는 보안그룹과 NACL의 역할을 비교하겠습니다. 루트 계정 보호와 IAM 최소권한, 보안그룹 실습, S3와 CloudFront 원본 보호, 함수·API·배포 파이프라인에서의 시크릿 관리 경험을 하나의 운영 시나리오로 연결해, “누가 무엇을 책임지고 어떤 증거로 안전을 입증할 수 있는가”까지 도달하는 것을 목표로 하겠습니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.2.1 IAM 최소권한·정책 구성 요점</h1>

**■ 공유 책임(Shared Responsibility)과 최소권한**

<div class = "onePage">

![](assets/w15_15.2.1-core.svg)

<!-- 대체텍스트:

# 짧은 설명

클라우드 IAM 최소권한 요약 다이어그램: 공유 책임(사업자 ‘of’ the cloud / 고객 ‘in’ the cloud), 최소권한 원칙(Deny by default·명시적 Deny 우선·MFA·STS), 정책 4요소(Principal·Action·Resource·Condition), 사용자→그룹→역할→EC2·Lambda·App Runner 흐름과 관리형 정책(최소 Allow)·명시적 Deny 경로 표시.

# 상세 설명

이미지는 가로로 긴 한 화면(1500×600) 구성의 개념도이다. 상단에는 세 개의 패널, 하단에는 “조직화 & 권한 부여 흐름” 패널이 가로로 넓게 배치된다.

1. 상단 좌측 패널 ― “공유 책임 & 최소권한”

* 두 개의 상자 비교로 구성.
* 왼쪽 상자: “클라우드 사업자 – 보안 ‘of’ the cloud(물리 인프라, 하이퍼바이저, 관리형 서비스 기반)”.
* 오른쪽 상자: “고객 – 보안 ‘in’ the cloud(계정·IAM, 데이터·네트워크, 애플리케이션)”.

2. 상단 중앙 패널 ― “최소권한 핵심 원칙”

* 경고 색 배경의 리스트로 다음 항목을 제시:
  · 기본 거부(Deny by default)
  · 명시적 Deny가 Allow보다 우선
  · 작은 범위로 시작해 필요한 권한만 단계적으로 허용
  · 루트/고권한 계정은 MFA 필수
  · 임시 자격(STS) 선호, 장기 키 금지 및 순환

3. 상단 우측 패널 ― “정책 = Who·What·Where·When/How”

* 네 개의 동일한 크기 상자에 정책 4요소 표시:
  Principal(누가), Action(무엇을), Resource(어디에), Condition(언제/어떻게).
* 패널 하단에 띠 배지: “아이덴티티 기반(IAM User/Role/Group) · 리소스 기반(S3, Lambda, CloudFront OAC)”.

4. 하단 전체 패널 ― “조직화 & 권한 부여 흐름”

* 좌측 박스는 운영 원칙 체크리스트:
  · 사용자에게 직접 권한 부여 금지 → 역할별 Group에 부여
  · 서비스 실행 권한은 Role로 부여(EC2·Lambda·App Runner)
  · 루트/고권한 MFA 필수, 루트는 비상용
  · STS AssumeRole로 임시 자격 사용
  · 장기 액세스 키 금지 및 키 순환
  · 태그·네이밍 규칙 및 최소 권한 표준화
* 우측은 흐름도:
  “Users(studentA, devB 등)” 상자 → 화살표 → “Group: Developers” 상자 → 화살표 → “Role: app-runtime(AssumeRole, STS·MFA)” 상자 → 아래로 화살표 → 서비스 상자 3개(EC2, Lambda, App Runner).
* Group 옆에는 “Managed Policy(Allow 최소)” 배지가 있으며, 여기서 붉은 화살표로 “명시적 Deny 규칙(조건 불충족 시 차단)” 상자로 이어지는 별도 경로가 표시되어 Deny 우선 적용을 강조.
* 우하단 범례: 파란 배지는 최소 Allow, 갈색 화살표는 Explicit Deny를 뜻함.

핵심 요지: 권한은 사용자→그룹→역할로 조직화하고, 서비스에는 역할을 부여한다. 정책은 Principal·Action·Resource·Condition 네 요소로 최소 범위만 허용하며, 기본 거부와 명시적 Deny, MFA와 STS 중심의 임시 자격 사용이 원칙이다.

 -->

</div>

</section>

<!--SCRIPT
v: 1
id: "15.2.1-core"
title: "최소권한 핵심 원칙"
ko: |
  화면의 다이어그램을 기준으로 보겠습니다. 좌측 상단은 공유 책임의 경계를 보여 줍니다. 물리 인프라와 하이퍼바이저, 관리형 서비스의 기반은 사업자가 책임지지만, 계정과 IAM, 데이터와 네트워크, 애플리케이션 보안은 전적으로 사용자에게 귀속됩니다. 중앙 패널은 최소권한의 규율을 요약합니다. 기본은 거부 상태여야 하며, 명시적 Deny가 Allow보다 먼저 적용됩니다. 권한은 넓게 부여한 뒤 줄이는 방식이 아니라, 작은 범위에서 필요한 동작만 단계적으로 허용하는 방식으로 설계해야 합니다. 루트와 고권한 계정은 반드시 MFA를 강제하고, 장기 액세스 키는 금지하거나 순환 정책 아래 예외적으로만 사용합니다. 운영 시에는 STS를 통한 임시 자격증명을 선호해야 감사를 단순화하고 노출 위험을 줄일 수 있습니다.
  우측 상단은 정책을 구성하는 네 박스입니다. Principal은 ‘누가’, Action은 ‘무엇을’, Resource는 ‘어디에’, Condition은 ‘언제·어떻게’의 문맥을 뜻합니다. 이 네 요소를 좁혀 가며 허용 범위를 최소화하는 것이 설계의 본질입니다. 정책은 아이덴티티 기반과 리소스 기반으로 나뉘며, S3와 Lambda, CloudFront OAC처럼 리소스 자체가 신뢰 가능한 주체의 접근만 허용하도록 잠글 수 있습니다. 하단의 흐름도는 조직화를 보여 줍니다. 사용자는 직접 권한을 갖지 않고 역할별 그룹에 속하며, 실제 서비스 실행 권한은 역할이 보유합니다. EC2·Lambda·App Runner 같은 실행 주체는 이 역할을 위임받아 동작하고, 그룹에는 최소 Allow의 관리형 정책만 연결합니다. 조건에 맞지 않는 행위는 명시적 Deny로 확실히 차단해, 우발적 과권한이 생산 환경으로 흘러들지 못하도록 해야 합니다. 마지막으로 태그와 네이밍 규칙을 표준화해 권한 부여와 감사를 일관된 언어로 수행하는 것이 운영 효율을 좌우합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.2.1 IAM 최소권한·정책 구성 요점</h1>

**■ 정책 설계 체크리스트(실습 연결)**

- **읽기 전용부터 시작** → 운영 작업 별도 Role로 분리(4주차 Role Switching)
- **리소스 스코프 축소**: `arn:aws:s3:::my-bucket/*` 처럼 구체화(6주차)
- **조건 필수화**: `aws:SourceVpce`, `aws:PrincipalTag`, `aws:MultiFactorAuthPresent`
- **태그 기반 권한(ABAC)** 도입으로 팀/프로젝트 확장성↑
- **리소스 기반 정책으로 원본 잠그기**: S3 <-> CloudFront **OAC/OAI** (10주차)
- **감사**: CloudTrail/Access Analyzer/CloudWatch 경보, 비용 알림(4주차)

<div class="onePage">
  
| 상황 | 적용 예시 | 근거 주차 |
|---|---|---|
| 서버 실행 권한 분리 | EC2 운영 Role, 개발자는 읽기(Describe*)만 | 5주차 |
| 함수 권한 최소화 | Lambda 실행 Role에 필요한 S3 PutObject만 | 9주차 |
| 정적 호스팅 보호 | S3 퍼블릭 차단 + CloudFront OAC | 6·10주차 |
| 배포 파이프라인 | ECR/Pull, Secrets 읽기만 허용한 CI Role | 14주차 |

</div>
</section>

<!--SCRIPT
v: 1
id: "15.2.1-check"
title: "정책 체크리스트"
ko: |
  일부 실습에서는 AmazonEC2FullAccess 같은 광범위 관리형 정책을 사용해 실습을 빠르게 진행했습니다. 이는 학습 편의용 설정으로, 운영 표준과는 구분해야 합니다.  실습 종료 시점부터는 권한을 단계적으로 축소하는 절차를 반드시 밟습니다. 먼저 읽기 전용을 기본선으로 두고 운영 작업은 별도 역할로 분리합니다. 이후 CloudTrail 사용 이력을 기반으로 실제로 호출된 동작을 추출해 최소 권한 정책을 생성하고, 리소스 ARN을 구체합니다. 팀과 프로젝트가 늘어나는 구간에서는 태그 기반 권한으로 접근을 분해하고, 퍼블릭 리소스는 허용하지 않으며 S3 원본은 CloudFront OAC로만 연결되도록 리소스 기반 정책을 결합합니다. 실습 단계에서 넓은 정책을 잠시 썼더라도, 운영 이전에는 권한 경계나 조직 수준 정책으로 권한 상승을 방지하고 세션을 임시 자격으로만 발급하며 MFA를 상시 요구합니다. 결과적으로 5주차의 서버 운영 권한은 EC2 전용 역할로 축소되고 개발자는 조회만 허용하며, 9주차 Lambda는 실행 역할에 필요한 S3 PutObject 수준으로 제한됩니다. 6·10주차의 정적 호스팅은 퍼블릭 차단과 OAC로 원본을 잠그고, 14주차 파이프라인은 ECR Pull과 시크릿 읽기만 허용하는 CI 역할로 교체됩니다. 권한과 행위를 분리하고, 조건으로 맥락을 고정합니다. 그리고 감사와 경보로 결과를 검증하는 이 세 축을 실습 이후의 표준 절차로 고정하면, 학습 편의와 운영 안전을 동시에 달성할 수 있습니다.

hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.2.2 비밀관리·네트워크 경계(SG/NACL)</h1>

**■ 시크릿(Secrets) 관리 — “코드·Git에 비밀번호 금지”**

- 저장: **Secrets Manager** 또는 **SSM Parameter Store(암호화/KMS)** (12·13·14주차)
- 사용: 애플리케이션에서 **런타임에 조회**, 환경변수 주입 시 **평문 노출 금지**
- 순환: DB 패스워드 **자동 회전**, 키 관리·권한 분리
- 접근: **애플리케이션 Role**에 `secretsmanager:GetSecretValue` 등 최소 권한만 부여

> 예: 감성분석 API(12~14주)에서 DB/토큰을 Secrets로 보관, 배포 Role은 읽기 전용

</section>

<!--SCRIPT
v: 1
id: "15.2.2-secrets"
title: "시크릿 관리"
ko: |
  비밀번호와 토큰, API 키는 코드나 Git 저장소에 남겨서는 안 됩니다. 시크릿은 Secrets Manager나 SSM Parameter Store에 KMS로 암호화해 보관하고, 애플리케이션은 런타임에 역할을 통해 최소 권한으로 조회해야 합니다. 환경변수를 사용할 수는 있으나, 공급망 단계에서 평문이 노출되지 않도록 배포 파이프라인과 실행 환경 간 경계를 분명히 해야 합니다. 데이터베이스 자격은 자동 회전을 활성화해 유출의 시간을 최소화하고, 접근 주체는 `secretsmanager:GetSecretValue` 등 읽기 범위로 제한합니다. 12에서 14주차 감성분석 API 예제처럼 배포 역할은 시크릿에 대한 읽기 권한만 가지고, 실제 애플리케이션은 실행 역할을 통해 필요한 순간에만 값을 받아 사용해야 합니다. 이렇게 저장·전달·순환의 단계마다 원칙을 적용하면, 사고가 발생하더라도 영향 면적을 작게 유지하고 회복 시간을 단축할 수 있습니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.2.2 비밀관리·네트워크 경계(SG/NACL)</h1>

**■ 네트워크 경계 — SG vs NACL 한눈 비교(5·7주차)**

<div class="onePage">

| 항목      | **Security Group**           | **NACL**                        |
| --------- | ---------------------------- | ------------------------------- |
| 적용 범위 | ENI/인스턴스·LB·DB           | 서브넷                          |
| 상태성    | **Stateful**(응답 자동 허용) | **Stateless**(양방향 규칙 필요) |
| 규칙 유형 | **Allow만**                  | Allow + **Deny**                |
| 용도      | 서비스 단위 세밀 제어        | 서브넷 레벨 1차 차단/분리       |
| 관리      | 리소스 묶음에 부착           | 번호순 평가(우선순위)           |

</div>

- 기본 패턴: **Public Subnet(LB)** ↔ **Private Subnet(EC2/Lambda/ECS/RDS)**, 아웃바운드는 **NAT GW**
- **VPC Endpoint**로 S3/Secrets 내부 통신, **WAF**로 L7 방어, **Flow Logs**로 감사

</section>

<!--SCRIPT
v: 1
id: "15.2.2-network"
title: "네트워크 경계"
ko: |
  네트워크 경계에서는 보안그룹과 NACL의 성격을 구분하는 것이 출발점입니다. 보안그룹은 상태를 기억하는 필터로서 응답 트래픽을 자동으로 허용하므로, 서비스 단위의 세밀한 허용 정책을 표현하는 데 적합합니다. 반대로 NACL은 서브넷에 적용되는 무상태 필터로, 들어오고 나가는 방향 모두에 대해 규칙을 명시해야 하며 번호가 낮은 규칙부터 평가됩니다. 실제 설계에서는 퍼블릭 서브넷에 로드 밸런서를 두고, 애플리케이션과 데이터베이스는 프라이빗 서브넷에 배치해 동서 트래픽을 보안그룹으로 제한합니다. 아웃바운드 인터넷 접근이 필요할 때는 NAT 게이트웨이를 통해 경로를 제어하고, S3나 Secrets 같은 관리형 서비스 연동은 VPC 엔드포인트를 사용해 내부 경로로 고정합니다. 외부에 노출되는 L7 지점에는 WAF로 규칙 기반 방어를 설정하고, Flow Logs로 흐름을 기록해 이상 행위를 사후에 추적할 수 있어야 합니다. 이러한 구성을 통해 경계는 단일 지점이 아니라 계층의 합으로 구현되며, 각 계층에서 허용의 이유를 설명할 수 있을 때 비로소 보안과 가용성을 함께 확보할 수 있습니다.
hangul_pron: ""
-->

---

<section class="slide-part">
15.3 비용/과금 감각 정리
</section>

<!--SCRIPT
v: 1
id: "15.3-part"
title: "파트 오프닝 — 비용/과금 감각 정리"
ko: |
  이번 파트의 목적은 트래픽이 들어와 콘텐츠를 전달하고, 애플리케이션이 실행되어 데이터를 읽고 쓰고, 로그가 수집되는 전 과정을 하나의 비용 경로로 읽어 내는 것입니다. EC2·Lambda·App Runner의 선택이 전체 과금 구조의 형태를 결정하며, S3·CloudFront가 오리진 호출과 전송 비용을 변화시킵니다. 그리고 RDS·DynamoDB가 저장과 IO 비용의 축을 만드며, VPC·NAT 게이트웨이·ALB는 경로를 형성하는 네트워크 요소로서 시간 단가와 처리량 과금을 유발합니다. 이 모든 요소를 태깅과 예산, 분석 절차에 연결해 팀 단위로 책임 있는 비용 통제를 수행하는 방법을 정리하겠습니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<!-- @슬라이드 초과됌 => A/B로 분할됌 -->
<h1>15.3.1 리소스 선택 → 비용 영향 경로</h1>

**■ 비용 경로 개요**

<div class = "onePage">

![](assets/w15_15.3.1-overview.svg)

</div>

<!-- 대체텍스트:

# 짧은 설명

클라우드 비용 경로 개요 다이어그램: 클라이언트 → CloudFront(10주) → ALB/앱 엔드포인트(5·14주) → 컴퓨트 분기(EC2/ECS(Fargate)·Lambda(9주)·App Runner/ECS(14주)) → 데이터 저장(RDS/DynamoDB/S3, 6·7주)·로그/모니터링(CloudWatch, 4주). 하단엔 컴퓨트별 비용 요소: EC2/ECS는 vCPU·메모리 시간, EBS 타입/크기/IOPS, 데이터 전송 등; Lambda는 GB-초, 요청 수, 프로비저닝 동시성 등; App Runner/ECS는 활성 컨커런시, 컴퓨트-분, 요청 수, 오토스케일·스케줄링 고려. 상단 컴퓨트 선택에서 하단 상세 비용으로 연결 화살표가 매핑됨.

# 상세 설명

이미지는 가로 1500×600 구성. 상단 패널에 “비용 경로”, 하단 패널에 “컴퓨트별 비용 구성”이 묶여 있다. 좌측 상단에는 제목이 없다.

1. 상단 패널 ― 비용 경로(좌→우 흐름)

* 박스 1: “클라이언트”.
* 화살표 → 박스 2: “CloudFront (10주)”.
* 화살표 → 박스 3: “ALB / 앱 엔드포인트 (5·14주)”.
* 여기서 아래로 내려가는 화살표가 컴퓨트 3가지로 분기:

  * “EC2 / ECS (Fargate)”.
  * “Lambda (9주)”.
  * “App Runner / ECS (14주)”.
* 컴퓨트 영역 오른쪽에는 두 목적지로 가는 화살표:

  * “데이터 저장: RDS / DynamoDB / S3 (6·7주)”.
  * “로그 · 모니터링: CloudWatch (4주)”.

2. 하단 패널 ― 컴퓨트 선택이 끌고 오는 비용 구성 요소

* 열 1: “EC2 / ECS(Fargate)”

  * vCPU·메모리 시간 과금
  * EBS 타입/크기/IOPS(5주)
  * 데이터 전송(인/아웃)
  * 오토스케일 정책 영향
  * 예약 인스턴스/세이빙즈 플랜 고려
* 열 2: “Lambda”

  * GB-초(메모리×실행시간)
  * 요청 수
  * (옵션) 프로비저닝 동시성(9주)
  * VPC 연결 시 네트워킹 비용
  * 스텝/이벤트 브리지 호출 비용
* 열 3: “App Runner / ECS”

  * 활성 컨커런시
  * 컴퓨트-분(사용 시간)
  * 요청 수(14주)
  * 오토스케일·스케줄링과 함께 고려(5·14주)
  * 이미지 레지스트리/빌드 비용 영향

3. 매핑

* 상단의 각 컴퓨트 선택 박스에서 하단의 해당 비용 열로 갈색 화살표가 내려가며, “컴퓨트 선택 → 비용 세부 항목으로 이어지는 매핑”을 시각화한다.

핵심 메시지

* 트래픽 경로(클라이언트→엣지→LB/엔드포인트→컴퓨트)에서 “컴퓨트 선택”이 전체 비용 구조를 좌우한다.
* EC2/ECS는 인스턴스/스토리지/네트워크가, Lambda는 GB-초·요청·동시성이, App Runner/ECS는 컨커런시·컴퓨트-분·요청과 스케일링 전략이 주요 비용 축이다.
* 데이터 저장과 모니터링은 선택된 컴퓨트의 사용 패턴에 따라 부가 비용을 만든다.

 -->

</section>

<!--SCRIPT
v: 1
id: "15.3.1-overview1"
title: "비용 경로 읽기"
ko: |
  화면의 다이어그램은 클라이언트에서 시작해 CloudFront, 애플리케이션 엔드포인트와 ALB를 거쳐 컴퓨트로 분기하는 경로를 보여 줍니다. 이 지점에서 EC2·ECS(Fargate), Lambda, App Runner·ECS 중 무엇을 택하느냐가 비용의 주축을 결정합니다. EC2·ECS는 vCPU와 메모리 시간, EBS 타입·크기·IOPS, 그리고 인아웃 전송량이 누적되어 비용을 만듭니다. Lambda는 메모리와 실행시간의 곱인 GB-초와 요청 수, 필요 시 프로비저닝 동시성이 핵심이며, VPC 연결과 오케스트레이션 호출 비용까지 함께 고려해야 합니다. App Runner·ECS는 활성 컨커런시와 컴퓨트 사용 시간, 요청 수가 중심이 되며, 자동 확장 설정과 예약 또는 스케줄링 전략이 단가 대비 처리량을 좌우합니다. 다이어그램의 화살표가 상단의 선택과 하단의 세부 항목을 직접 연결하듯, 컴퓨트 선택은 스토리지와 모니터링의 사용 패턴까지 연쇄적으로 바꾸므로, 설계 시 처리량·지연 목표와 함께 과금 단위를 맞추는 것이 우선입니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<!-- @슬라이드 초과됌 => A/B로 분할됌 -->
<h1>15.3.1 리소스 선택 → 비용 영향 경로</h1>

**■ 스토리지/DB 선택이 끌고 오는 비용**

- **S3**: 스토리지 클래스 + 요청(읽기/쓰기) + 전송 + **수명주기**(6주)
- **RDS**: 인스턴스·저장소·IO·**멀티AZ/백업 보존**(7주)
- **DynamoDB**: 온디맨드 vs 프로비저닝(오토스케일) + 스토리지(7주)

**■ 네트워크/엣지/게이트웨이**

- **CloudFront**: 데이터 전송 아웃 + 요청(10주) → 캐시 적중률이 직접 비용에 반영
- **ALB**: 시간 단가 + LCU(처리량/규칙/커넥션)
- **NAT GW**: 시간 + 데이터 처리(5·14주) → **VPC 엔드포인트**로 대체 고려(6·10·14주)
- **AZ 간 전송**: 교차 AZ 트래픽이 비용 유발(4·14주)

> 실무 감각: “요청 수·시간·전송량·저장량·IO”가 어디서 발생하는지 흐름 기준으로 추적

</section>

<!--SCRIPT
v: 1
id: "15.3.1-overview2"
title: "비용 경로 읽기"
ko: |
  이어서 저장과 네트워크의 영향을 보겠습니다. S3는 스토리지 클래스에 따라 보관 단가가 달라지고, 읽기·쓰기 요청과 전송량, 그리고 수명주기 정책에 의한 계층 이동이 합산되어 비용이 결정됩니다. RDS는 인스턴스 사양과 저장소 유형·크기·IO, 멀티 AZ 구성과 백업 보존 기간이 직접적인 변수입니다. DynamoDB는 온디맨드와 프로비저닝 모드 선택이 요청 단가 구조를 바꾸고 오토스케일 설정이 추가 비용을 좌우합니다. CloudFront는 데이터 전송 아웃과 요청 수가 핵심이며 캐시 적중률이 낮으면 오리진 호출과 대역폭 비용이 동시에 증가합니다. ALB는 시간 단가와 LCU로 측정되는 처리량·규칙·커넥션이 합산되고, NAT 게이트웨이는 시간과 처리 바이트에 과금되므로 내부 서비스는 VPC 엔드포인트로 우회해 비용 경로를 줄이는 것이 효과적입니다. 리전 내 교차 AZ 전송 또한 비용을 만들기 때문에 상태 동기화나 로깅 경로에서 불필요한 교차 흐름을 최소화해야 합니다. 실무에서는 요청 수, 실행·대기 시간, 전송량, 저장량, IO라는 다섯 축을 경로에 대입해 어느 구간에서 값이 커지는지 먼저 확인하고, 그 지점의 서비스 선택과 캐싱·배치·스케일 정책을 조정합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<!-- @슬라이드 초과됌 => A/B로 분할됌 -->

<h1>15.3.2 태깅·Budget·Cost Explorer 요약</h1>

**■ 비용 태깅 전략(4·6·7·10·14주 전반 적용)**

- **필수 키**: `Project`, `Env`, `Owner`, `CostCenter`, `App`, `DataClass`
- **배포 강제**: 태그 없으면 생성 불가(정책/파이프라인), **ABAC** 권한과 연동
- **Cost Allocation Tags 활성화** 후 청구서/분석에 반영

</section>

<!--SCRIPT
v: 1
id: "15.3.2-tags-budgets1"
title: "태깅·예산·분석 운영법"
ko: |
  비용 통제의 첫 단계는 태깅 표준을 통한 귀속 명확화입니다. Project, Env, Owner, CostCenter, App, DataClass 같은 핵심 키를 필수로 정의하고, 배포 파이프라인과 정책에서 태그가 없으면 리소스를 만들 수 없도록 강제합니다. 권한 모델에는 ABAC(속성 기반 액세스 제어)를 적용해 태그로 접근을 제어하고, 동일한 스키마로 모니터링 대시보드와 로그 필터를 구성하여 운영 언어를 일치시킵니다. 이후 Cost Allocation Tags를 활성화해 태그가 청구와 분석에 반영되도록 설정하면, 팀·서비스·환경별 비용을 일관된 시점에 비교·설명할 수 있습니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<!-- @슬라이드 초과됌 => A/B로 분할됌 -->
<h1>15.3.2 태깅·Budget·Cost Explorer 요약</h1>

**■ 예산·경보·분석 루틴**

- **AWS Budgets**: 월간 비용/사용량 임계치, **이메일/Chatbot 알림**, RI/SP 활용/커버리지 예산
- **Cost Explorer**: 서비스/리전/태그별 **Group By**, 추세·비정상 탐지, **여신화(Amortized) 보기**
- **CUR**(+Athena/QuickSight 등): 세부 과금 행 단위 분석, 자동 리포트
- **Compute Optimizer/Trusted Advisor**: 권고 기반 **Right-sizing**

<div class="onePage">

| 단계 | 도구            | 핵심 액션         | 기대 효과          |
| ---- | --------------- | ----------------- | ------------------ |
| 1    | 태깅 표준       | 키/값 스키마·검증 | 비용 귀속 명확화   |
| 2    | Allocation Tags | 과금 리포트 반영  | 팀·서비스별 가시성 |
| 3    | Budgets         | 임계치 알림 설정  | 초과 전 선제 대응  |
| 4    | Cost Explorer   | Tag/Service 분석  | 과다 구간 식별     |
| 5    | 리뷰            | 권고사항 실행     | 지속적 최적화      |

</div>

> 운영 팁: **월 1회 비용 리뷰**(팀별 30분), 대시보드 스냅샷 공유, **변경 전/후 비용 영향 기록**

</section>

<!--SCRIPT
v: 1
id: "15.3.2-tags-budgets2"
title: "태깅·예산·분석 운영법"
ko: |
  예산과 분석 루틴은 고정된 주기로 반복합니다. AWS Budgets에서 월간 비용과 사용량의 임계치를 정의하고 이메일 또는 Chatbot으로 알림을 보낸 뒤, 예약·세이빙즈 플랜의 활용과 커버리지도 별도 예산으로 모니터링합니다. Cost Explorer에서는 서비스·리전·태그를 기준으로 그룹핑하여 추세를 확인하고, 비정상 구간을 식별할 때는 여신화 보기로 선결제나 예약의 효과를 반영해 해석합니다. 더 세밀한 분석이 필요하면 CUR를 Athena·QuickSight 등과 결합해 행 단위 리포트를 생성하고 자동화를 통해 정기 보고를 배포합니다. Compute Optimizer와 Trusted Advisor의 권고를 월간 리뷰에 포함해 크기 조정과 미사용 자원 정리를 실행합니다. 운영 절차는 태깅 스키마 확정과 Allocation Tags 반영, 예산 임계 설정, Cost Explorer 기반의 태그·서비스 분석, 권고 실행의 순서로 고정하고, 월 1회의 비용 리뷰에서 대시보드 스냅샷과 변경 전후 비용 영향을 기록해 학습 가능한 체계를 유지합니다.
hangul_pron: ""
-->

---

<section class="slide-part">
15.4 컴퓨팅 선택 지도

(EC2, Lambda, ECS/EKS, App Runner)

</section>

<!--SCRIPT
v: 1
id: "15.4-part"
title: "파트 오프닝 — 컴퓨팅 선택 지도"
ko: |
  이번 파트의 목적은 EC2, Lambda, ECS/EKS, App Runner 중에서 워크로드 특성과 운영 목적에 맞는 실행 환경을 신속하고 일관되게 선택하는 기준을 확립하는 것입니다. 5주 EC2, 9주 Lambda, 14주 App Runner 실습에서 확인한 배포·스케일·관측성의 차이를 공통 축으로 정리하고, 전환과 확장 과정에서 발생하는 위험을 사전에 통제할 수 있도록 점검 항목을 체계화하겠습니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<!-- @슬라이드 초과됌 => A/B로 분할됌 -->
<h1>15.4.1 선택 기준(부하 패턴·운영 복잡도)</h1>

**■ 부하 패턴 / 운영 축으로 고르기(5·9·14주 참조)**

<div class = "onePage">

![](assets/w15_15.4.1-criteria.svg)

</div>

<!-- 대체텍스트:

# 짧은 설명

부하 패턴·콜드스타트 민감도·운영 복잡도에 따라 AWS 실행 환경을 고르는 매트릭스 다이어그램. 상단 축은 “운영 최소화 ↔ 인프라 제어·커스텀 필요”. 중단은 2행×3열 매트릭스(행: 콜드스타트 민감/허용, 열: 운영 최소화/컨테이너 표준화/특수 요구). 셀의 추천: App Runner, ECS(Fargate), EC2/EKS, Lambda, ECS Tasks, EC2 Batch. 오른쪽 박스는 네트워킹·의존성 및 이식성·생태계 고려사항. 하단은 EC2, Lambda, ECS/EKS, App Runner의 빠른 가이드. 화살표는 패턴→매트릭스→추천 서비스로 흐름을 연결하며 텍스트를 가리지 않음.

# 상세 설명

이미지는 가로 1500×600의 한 화면 구성. 좌측 상단에 제목은 없다.

1. 상단 띠(운영 복잡도 축)

* 옅은 파란 띠에 좌측 라벨 “운영 최소화”, 우측 라벨 “인프라 제어 · 커스텀 필요”.
* 의미: 운영 부담이 낮은 쪽부터(좌) 인프라 제어가 필요한 쪽(우)까지 연속 축.

2. 중단 영역(세 부분)
   A. 좌측 박스 “부하 패턴”

* 목록: 상시(steady), 변동(bursty), 이벤트 기반(event-driven), 배치(batch).

B. 중앙 2행×3열 선택 매트릭스

* 열 헤더(좌→우): “운영 최소화”, “컨테이너 표준화”, “특수 요구/커스텀”.
* 행 라벨(위→아래): “콜드스타트 민감”, “콜드스타트 허용”.
* 각 셀의 추천:

  * (민감 × 운영 최소화) App Runner
  * (민감 × 컨테이너 표준화) ECS(Fargate)
  * (민감 × 특수 요구) EC2 / EKS — 부가설명: GPU · 파일시스템 · 장기 연결
  * (허용 × 운영 최소화) Lambda — 부가설명: event/batch
  * (허용 × 컨테이너 표준화) ECS Tasks — 부가설명: 스케줄/큐 소비
  * (허용 × 특수 요구) EC2 Batch — 부가설명: 전용 AMI · 드라이버

C. 우측 박스 두 갈래

* “네트워킹 · 의존성”: VPC 연결/프라이빗 서브넷, 파일시스템(EFS/FSx), 장기 연결(WebSocket), GPU/전용 드라이버.
* “이식성 · 생태계”: 컨테이너 표준화, 쿠버네티스 기능 필요 시 EKS.

3. 흐름 화살표

* 왼쪽 “부하 패턴” 항목들에서 중앙 매트릭스의 대응 셀로 곡선 화살표가 이어짐.
* 매트릭스의 몇몇 셀에서 하단 가이드 박스로 수직 화살표가 내려감.
* 화살표는 도형 위 레이어지만, 모든 텍스트는 위에 다시 그려져 가려지지 않음.

4. 하단 영역 “선택 축과 빠른 가이드”(4개 카드)

* EC2: 상시 트래픽·특수 요구(GPU/파일시스템/장기 연결), 네이티브 OS/에이전트 필요, 지연 민감 워크로드.
* Lambda: 이벤트 기반/단명, 비동기/배치, 콜드스타트 허용 범위 내, 운영 최소화·초당 확장.
* ECS / EKS: 컨테이너 표준화·마이크로서비스, Fargate로 운영 부담↓, K8s 기능 필요 시 EKS.
* App Runner: 운영 최소화 Web/API, 자동 빌드·배포·스케일링, 실시간 HTTP 트래픽 적합.

핵심 메시지(요약)

* 먼저 부하 패턴과 콜드스타트 허용치를 본 뒤, 필요한 운영·커스텀 수준에 맞춰 선택한다.
* 상시·특수 요구 → EC2/EKS, 이벤트·단명 → Lambda, 컨테이너 표준화 → ECS/EKS, 운영 최소화 Web/API → App Runner.
* VPC/파일시스템/GPU 등 의존성과 쿠버네티스 필요 여부를 추가로 검토한다.

 -->

<!-- - **부하 패턴**: 상시(steady) / 변동(bursty) / 이벤트 기반(event-driven) / 배치
- **지연/콜드스타트 허용**: 콜드스타트 민감(실시간) vs 허용(비동기/배치)
- **운영 복잡도**: 인프라 제어·커스텀 필요(네이티브 OS/에이전트) vs **운영 최소화**
- **이식성/생태계**: 컨테이너 표준화, 쿠버네티스 기능 필요성(EKS) 여부
- **네트워킹/의존성**: VPC 연결, 파일시스템, 장기 연결, GPU 등 특수 요구 -->

</section>

<!--SCRIPT
v: 1
id: "15.4.1-criteria"
title: "선택 축과 빠른 가이드"
ko: |
  먼저 부하 패턴이 상시인지, 변동이 큰지, 이벤트 중심인지, 배치성인지 판별합니다. 다음으로 콜드스타트에 대한 허용 범위를 정하여 지연 민감 경로는 별도 보호가 필요함을 전제로 합니다. 마지막으로 운영 복잡도 축에서 운영 최소화가 우선인지, 컨테이너 표준화를 통한 이식성이 중요한지, 혹은 GPU·파일시스템·장기 연결 같은 특수 요구로 인해 인프라 제어가 필요한지를 결정합니다. 콜드스타트 민감 구간에서 운영을 최소화하려면 App Runner가 적합하고, 컨테이너 표준화가 필요하면 ECS(Fargate)로 옮기는 것이 자연스럽습니다. 특수 요구가 있거나 장기 연결·네이티브 드라이버가 필요한 경우에는 EC2 또는 EKS가 안전합니다. 콜드스타트를 허용할 수 있고 이벤트·배치 위주라면 Lambda가 1순위이며, 큐 소비나 스케줄 구동을 컨테이너로 표준화하려면 ECS 태스크가 유용합니다. 의사결정은 이 세 축을 순차적으로 통과시키고, 네트워킹 요구와 외부 의존성, 쿠버네티스 생태계 활용 필요 여부를 추가 검토하는 절차로 마무리합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<!-- @슬라이드 초과됌 => A/B로 분할됌 -->

<h1>15.4.1 선택 기준(부하 패턴·운영 복잡도)</h1>

**■ 빠른 의사결정 가이드**

- **EC2**: 장수명·커스텀 OS/네트워킹/GPU, 자체 에이전트 필요, **완전한 제어**(5주)
- **Lambda**: 이벤트·단명 작업, 스케일-투-제로, 운영 부담 최소(9주)
- **ECS/EKS**: 컨테이너 마이크로서비스, 사이드카/서비스 메시, 점진적 확장
- **App Runner**: 컨테이너/소스 기반 **운영 최소형** 웹 API, 자동 빌드·스케일(14주)

<div class="onePage">

| 항목       | EC2           | Lambda            | ECS/EKS         | App Runner         |
| ---------- | ------------- | ----------------- | --------------- | ------------------ |
| 스케일     | ASG로 분/분   | 초/분 단위 동시성 | 서비스 단위     | 요청·컨커런시 기반 |
| 콜드스타트 | 없음          | 있음(튜닝 가능)   | 컨테이너 기동   | 컨테이너 기동      |
| 운영 부담  | 높음          | 낮음              | 중간~높음(EKS↑) | 낮음               |
| 비용 단위  | 시간+스토리지 | GB-초+요청        | vCPU/메모리-분  | 컨커런시+컴퓨트-분 |
| 적합용도   | 커스텀/상시   | 이벤트/비정기     | 표준화/미들웨어 | 단순 웹/API        |

</div>
</section>

<!--SCRIPT
v: 1
id: "15.4.1-criteria"
title: "선택 축과 빠른 가이드"
ko: |
  EC2는 장수명 서비스나 커스텀 OS·네트워킹·GPU 요구처럼 완전한 제어가 필요한 경우에 적합하며, 오토스케일링 그룹으로 분 단위 확장을 구성합니다. Lambda는 이벤트 기반 단명 작업에서 스케일 투 제로와 초당 수준의 동시성 확장이 장점이지만 콜드스타트와 한도를 함께 설계해야 합니다. ECS/EKS는 컨테이너 마이크로서비스 표준화가 목적일 때 선택하며, 사이드카·메시 등 중간 이상의 운영 복잡도를 감수하는 대신 이식성과 생태계를 확보합니다. App Runner는 웹·API를 운영 최소형으로 제공하려는 경우에 적합하고, 요청과 컨커런시에 따라 자동으로 확장·축소됩니다. 스케일 특성, 콜드스타트 존재 여부, 운영 부담, 과금 단위를 함께 고려하여 현재 단계의 목표에 가장 근접한 대안을 우선 채택하는 것이 효율적입니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.4.1 선택 기준(부하 패턴·운영 복잡도)</h1>

**■ 실습 연결로 보는 패턴 매핑**

- **정적 웹 + API 프런트**: CloudFront(10주) + App Runner(14주) → 운영 최소·오토스케일
- **배치/이벤트 파이프라인**: S3 이벤트 → Lambda(9주) → S3/RDS(6·7주)
- **상시 API + 커스텀 런타임/에이전트**: EC2 ASG(5주) + ALB + RDS(7주)
- **컨테이너 마이크로서비스**: ECR + ECS/EKS(14주 참조) → 블루/그린·카나리 롤아웃

> 원칙: **무상태화 + 외부 스토리지(RDS/S3/DynamoDB)**, 네트워크는 **VPC 엔드포인트**로 비용/보안 동시 확보

</section>

<!--SCRIPT
v: 1
id: "15.4.1-mapping"
title: "실습과 선택 매핑"
ko: |
  실습 시나리오를 기준으로 매핑하겠습니다. 정적 웹과 경량 API 프런트는 CloudFront와 App Runner 조합으로 운영 부담을 낮추면서 자동 확장을 확보했습니다. S3 이벤트를 기점으로 한 배치·이벤트 파이프라인은 Lambda가 적합했고, 결과는 S3나 RDS에 기록하여 상태를 외부화했습니다. 상시 API이며 커스텀 런타임이나 에이전트가 필요한 경우에는 EC2 오토스케일링과 ALB, RDS를 결합해 제어권과 안정성을 동시에 확보했습니다. 다수의 마이크로서비스로 분해된 경우에는 ECR과 ECS/EKS를 통해 배포 단위를 표준화하고, 블루/그린이나 카나리 전략으로 점진적 롤아웃을 수행했습니다. 공통 원칙은 애플리케이션을 무상태로 유지하고, 데이터는 RDS·S3·DynamoDB 같은 외부 스토리지로 분리하며, 내부 통신은 VPC 엔드포인트로 고정해 비용과 보안을 함께 달성하는 것입니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.4.2 전환/확장 시 고려사항</h1>

**■ 아키텍처 전환 체크리스트(EC2 ↔ 컨테이너 ↔ 서버리스)**

- **상태 분리**: 세션/파일을 **RDS·DynamoDB·S3**로 이전, 인스턴스는 무상태화(6·7주)
- **패키징**: 컨테이너 이미지/ECR, 기반 OS 차이로 인한 네이티브 라이브러리 점검(14주)
- **네트워크**: VPC·서브넷·보안그룹 재설계, **NAT 비용**→ VPC 엔드포인트로 우회(5·14주)
- **확장 정책**: 지표(요청·지연·큐 길이) 기반, 쿨다운/버스트 보호(5·9·14주)
- **배포 전략**: 블루/그린·카나리, 헬스체크/리드니스/리미트 설정
- **시크릿/설정**: **Secrets Manager/SSM** + Role 권한 최소화(12·13·14주)
- **관측성**: CloudWatch 로그/메트릭/트레이스, 비용 태그/대시보드(4·14주)

</section>

<!--SCRIPT
v: 1
id: "15.4.2-migration"
title: "전환 체크리스트"
ko: |
  전환의 핵심은 상태를 인스턴스 밖으로 이동시키고, 자동 확장이 지표와 연결된 상태에서 관측 가능하도록 만드는 것입니다. EC2에서 컨테이너 또는 서버리스로 이동할 때는 세션과 파일 저장을 RDS·DynamoDB·S3로 이전하고, 컨테이너 이미지로 패키징하면서 기반 OS 차이에 따른 네이티브 라이브러리를 점검해야 합니다. 네트워크는 VPC·서브넷·보안그룹을 재설계하고, 인터넷 경로가 필요한 워크로드의 NAT 비용을 VPC 엔드포인트로 우회해 줄입니다. 확장 정책은 요청 수, 지연, 큐 길이 같은 지표에 기반하여 쿨다운과 버스트 보호를 포함해야 하며,  헬스체크·리드니스·리미트를 엄격히 적용합니다. 시크릿과 설정은 Secrets Manager 또는 SSM으로 이관하고 역할 기반 최소 권한으로 접근하며, CloudWatch 로그·메트릭과 트레이스를 결합해 전환 전후의 성능과 비용 신호를 비교 가능하게 유지합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.4.2 전환/확장 시 고려사항</h1>

**■ 워크로드별 주의 포인트**

- **EC2 → App Runner/ECS**: 포트/헬스체크/파일쓰기 경로, **읽기 전용 루트** 가정, 스토리지 외부화
- **Lambda로 전환**: 콜드스타트 민감 경로 분리, 메모리/타임아웃 튜닝, **동시성 한도/큐 백프레셔**
- **ECS ↔ EKS**: 오케스트레이션 유연성 vs 운영 복잡도(컨트롤 플레인, CNI, Ingress, 서비스 메시)
- **GPU/고성능**: EC2·EKS(노드 그룹)로, 예약/스팟/세대교체로 단가 최적화(5주)

**■ 비용/성능 균형 팁**

- **캐시/엣지**로 오리진 부하·전송 절감(10주), **오토스케일+스케줄링**(5·14주)
- **로그/지표 표준화**로 이슈 MTTR↓, **Budgets/Explorer**로 비용 가시성↑(15.3 연계)

</section>

<!--SCRIPT
v: 1
id: "15.4.2-scale"
title: "확장 팁과 주의점"
ko: |
  워크로드별 주의점을 정리하겠습니다. EC2를 App Runner나 ECS로 이전할 때는 포트와 헬스체크 경로, 쓰기 경로를 명확히 하고 컨테이너 루트 파일시스템이 읽기 전용일 수 있음을 가정하여 외부 스토리지를 사용해야 합니다. Lambda로 전환하는 경우 지연 민감 엔드포인트를 별도로 구성하고 메모리와 타임아웃을 조정하며 동시성 한도와 큐 기반 백프레셔로 급증 구간을 흡수합니다. ECS와 EKS 간 전환은 오케스트레이션 유연성과 운영 복잡도 사이의 교환관계를 인지하고, 컨트롤 플레인·CNI·Ingress·서비스 메시 요소가 관리 가능한 범위인지 검토합니다. GPU나 고성능이 요구되는 경우 EC2 또는 EKS 노드 그룹을 사용하고, 예약·스팟과 세대 교체로 단가를 최적화합니다. 비용과 성능의 균형을 위해서는 캐시와 엣지로 오리진 부하와 전송을 절감하고, 오토스케일과 스케줄링으로 비활성 구간을 줄입니다. 로그와 지표를 표준화하여 문제 해결 시간을 단축하고 Budgets와 Cost Explorer로 비용 가시성을 상시 유지합니다.
hangul_pron: ""
-->

---

<section class="slide-part">
15.5 컨테이너·이미지·레지스트리

(Docker → ECR)

</section>

<!--SCRIPT
v: 1
id: "15.5-part"
title: "파트 오프닝 — Docker·이미지·ECR 핵심 재정리"
ko: |
  이번 파트에서는 실습에서 만든 Flask·FastAPI 서비스를 컨테이너로 패키징하고, ECR에 등록한 뒤 App Runner·ECS로 배포하는 전 과정을 하나의 표준 흐름으로 정리하겠습니다. 핵심은 Dockerfile 멀티스테이지로 이미지를 슬림화하고, 컨테이너 포트와 ALB 대상 그룹을 일치시켜 네트워크 경로를 명확히 합니다. 태그와 다이제스트를 병행하되 운영 배포는 다이제스트로 고정해 재현성을 확보하는 것입니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<!-- @슬라이드 초과됌 => A/B로 분할됌 -->

<h1>15.5.1 Dockerfile·멀티스테이지·포트 바인딩</h1>

**■ 멀티스테이지 핵심(12·13·14주 연결)**

<div class = "onePage">

![](assets/w15_15.5.1-dockerfile2.svg)

</div>

<!-- 대체텍스트:

# 짧은 설명

Docker 멀티스테이지 파이프라인과 포트 바인딩 개요. 상단은 “빌드 컨텍스트 → 빌드 단계 → 런타임 단계 → 최종 이미지” 흐름과 `.dockerignore`로 불필요 파일을 제외해 이미지를 슬림화(수백 MB → 수십 MB). 하단은 컨테이너 `EXPOSE 8080`과 `docker run -p 80:8080`의 호스트 매핑, 그리고 ALB가 80/443 리스너로 들어온 트래픽을 대상 포트 8080으로 전달하는 구성을 보여준다. 화살표는 흐름을 표시하지만 텍스트를 가리지 않는다.

# 상세 설명

이미지는 가로 1500×620 구성. 좌측 상단에 제목은 없다. 두 개의 큰 패널(상: 멀티스테이지, 하: 포트 바인딩)로 나뉜다.

1. 상단 패널 — 멀티스테이지·슬림화 흐름

* 좌측 상자 “빌드 컨텍스트”: 소스와 매니페스트가 포함됨(예: `src/`, `package.json` 또는 `requirements.txt`, Dockerfile, `assets/`).
* 그 아래 “.dockerignore”: `__pycache__/`, `.git/`, `*.log`, `build/`, `dist/`, `.env` 등 불필요 항목을 제외하여 빌드 컨텍스트를 줄임. 곡선 화살표가 컨텍스트에서 제외되어 빌드 단계로 들어가지 않음을 시각화.
* 중앙 “빌드 단계(compile/pack)”: 예시 코드가 요약됨 — `FROM node:18 AS build`, `WORKDIR /app`, `npm ci`, 소스 복사, `npm run build`. 산출물은 `dist/`나 배포 산출물(휠, 바이너리) 등.
* 오른쪽 “런타임 단계(minimal)”: 예시 — `FROM node:18-slim AS runtime`, 빌드 산출물만 복사(`COPY --from=build /app/dist ./dist`), 최소 실행 파일만 유지, `CMD ["node","dist/server.js"]`. 의존성 최소화·공격면 축소·배포 속도 향상을 강조.
* 최우측 “최종 이미지”: “슬림 이미지(빌드 툴 미포함)”으로 표기된 캡슐형 상자와 배지 “수백 MB → 수십 MB”.
* 직선 화살표가 “빌드 컨텍스트 → 빌드 단계 → 런타임 단계 → 최종 이미지”의 순서를 나타냄.

2. 하단 패널 — 포트 바인딩 개요(EXPOSE vs `-p`)

* 좌측 “컨테이너 내부”: `EXPOSE 8080`과 “앱 리스닝: 0.0.0.0:8080”. 아래 캡슐형 상자 “Container :8080(서비스 포트)”.
* 가운데 “호스트 바인딩”: 명령 예 `docker run -p 80:8080 …`. 아래 캡슐형 상자 “Host :80 → 컨테이너 :8080”. 좌측 컨테이너 상자에서 이 상자로 가는 화살표가 있음.
* 오른쪽 “ALB / 네트워킹”: 텍스트 “ALB 80/443 → TargetGroup 8080, 보안그룹/서브넷 규칙 확인”. 아래 캡슐형 상자 “Application Load Balancer(리스너: 80/443 → 대상포트: 8080)”. 가운데 상자에서 오른쪽 상자로 이어지는 화살표가 있음.
* 요지: `EXPOSE`는 문서화 역할이고, 실제 외부 공개는 `-p` 옵션 또는 ALB 리스너/대상 그룹 구성으로 결정된다.

핵심 메시지(요약)

* 멀티스테이지: 빌드 단계에서만 컴파일·패키징을 수행하고, 런타임 단계에는 결과물만 복사해 이미지 슬림화.
* `.dockerignore`로 컨텍스트를 정리하면 빌드 성능·보안·이미지 크기가 개선됨.
* 포트 공개: 컨테이너는 8080을 노출(EXPOSE)하지만, 실제 외부 접근은 호스트 바인딩(`-p 80:8080`) 또는 ALB(리스너 80/443 → 대상 8080)로 제어한다.


 -->

<!-- - **빌드 단계**: 의존성 컴파일/패키징만 수행
- **런타임 단계**: 실행에 필요한 산출물만 복사 → 이미지 **슬림화**
- **.dockerignore**: `__pycache__/`, `.git/`, 로컬 아티팩트 제외 -->

</section>

<!--SCRIPT
v: 1
id: "15.5.1-dockerfile1"
title: "멀티스테이지·슬림화 포인트"
ko: |
  다이어그램의 상단 흐름을 기준으로 보면, 빌드 컨텍스트에는 실행에 불필요한 산출물이 포함되기 쉬우므로 .dockerignore를 통해 소스 관리 디렉터리와 캐시, 로그, 로컬 빌드 산출물을 제외해 컨텍스트 자체를 줄여야 합니다. 빌드 단계에서는 컴파일과 패키징만 수행하고, 런타임 단계에는 빌드 산출물만 선별적으로 복사하여 빌드 도구와 헤더, 테스트 자원을 제거합니다. 이 구조는 이미지 크기를 수백 MB에서 수십 MB 수준으로 줄여 전송·배포 시간을 단축하고 공격면을 축소합니다. 하단의 포트 바인딩 흐름은 EXPOSE가 문서화 역할임을 전제로 하며, 실제 외부 공개는 docker run의 포트 매핑이나 ALB의 리스너와 대상 그룹 구성이 결정합니다. 앱은 컨테이너 내부에서 0.0.0.0의 서비스 포트로 리슨하고, 호스트나 로드 밸런서는 해당 포트로 정확히 라우팅되어야 하며, 이때 보안 그룹과 서브넷 규칙이 일관되게 적용되어야 합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<!-- @슬라이드 초과됌 => A/B로 분할됌 -->

<h1>15.5.1 Dockerfile·멀티스테이지·포트 바인딩</h1>

**■ 최소 예시(개념)**

```docker
# build
FROM python:3.12-slim AS build
WORKDIR /app
COPY pyproject.toml requirements.txt* ./
RUN pip install --no-cache-dir -r requirements.txt

# run
FROM python:3.12-slim
WORKDIR /app
COPY --from=build /usr/local /usr/local
COPY . .
ENV PORT=8000
EXPOSE 8000
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
```

> 포인트: **비밀/키는 이미지에 굽지 않음**(SSM/Secrets), **non-root 권장**, **건강검사 엔드포인트 제공**

</section>

<!--SCRIPT
v: 1
id: "15.5.1-dockerfile2"
title: "멀티스테이지·슬림화 포인트"
ko: |
  먼저 build 구간에서는 python:3.12-slim을 기반으로 작업 디렉터리를 잡고, 의존성 명세만 선복사하여 설치함으로써 캐시 적중률을 높입니다. 애플리케이션 소스는 그다음 단계에 복사해 코드가 자주 바뀌어도 의존성 레이어를 재사용하도록 하고, 이때 .env나 API 키 같은 시크릿은 이미지를 더럽히지 않도록 절대 포함하지 않습니다.

  이어지는 run 구간은 동일 계열의 슬림 이미지를 사용해 실행에 필요한 파일만 최소로 배치하고, build 단계에서 준비된 런타임만 복사해 공격면과 이미지 크기를 함께 줄입니다. 프로세스는 0.0.0.0:${PORT}로 바인딩하며 EXPOSE는 공개 설정이 아니라 문서화용이라는 점을 상기합니다. 가능하면 비루트 사용자로 실행하고, /health 같은 경량 헬스 엔드포인트를 제공하여 배포 안정성을 확인합니다. 환경설정과 자격증명은 환경 변수와 Secrets Manager·SSM을 통해 런타임에 주입하고, 컨테이너 포트는 App Runner·ECS의 설정과 일치하도록 유지하겠습니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.5.1 Dockerfile·멀티스테이지·포트 바인딩</h1>

**■ 로컬 빌드/검증(14주 실습 리캡)**

```bash
# (1) 빌드: 배포 대상 아키텍처 맞추기
docker buildx build --platform linux/amd64 -t sentiment:1.0.0 .

# (2) 실행: 포트 바인딩(호스트:컨테이너)
docker run --rm -p 8000:8000 sentiment:1.0.0

# (3) 헬스 체크
curl -s http://localhost:8000/health

# (4) 태깅: ECR URI로
docker tag sentiment:1.0.0 <ACCOUNT>.dkr.ecr.<REGION>.amazonaws.com/sentiment:1.0.0
```

- 체크리스트: **0.0.0.0:${PORT} 바인딩**, 헬스 200 OK, 로그(JSON) 출력, 환경변수로 설정 분리
- 문제 해결: **포트 충돌**, 프록시/권한, 플랫폼 미일치(linux/amd64)

</section>

<!--SCRIPT
v: 1
id: "15.5.1-port-health"
title: "포트 바인딩·헬스검증"
ko: |
  주석 번호 (1)에서는 빌드 타깃 아키텍처를 linux/amd64로 고정하여 런타임과의 호환성을 확보합니다. 이어서 (2) 단계에서 호스트 8000을 컨테이너 8000으로 바인딩해 실제 서비스 포트가 외부에서 접근 가능한지 확인합니다. (3) 단계에서는 /health 엔드포인트에 요청하여 200 응답과 예상 페이로드를 검증하고, 이때 로그가 표준 출력으로 구조화되어 노출되는지까지 함께 확인합니다. 마지막 (4) 단계에서 이미지에 ECR URI 태그를 부여하면 이후 푸시와 배포 파이프라인에서 일관된 식별자로 동작합니다. 검증 과정 전반에서 프로세스가 0.0.0.0:${PORT}에 리슨하는지, 동일 포트가 App Runner·ECS의 컨테이너 포트와 일치하는지, 플랫폼 미일치로 인한 실행 오류가 없는지를 순서대로 점검합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.5.2 태그 vs Digest·불변성</h1>

**■ 개념 정리**

- **Tag**: 사람이 읽기 쉬운 라벨(예: `1.0.0`, `latest`) → **가변**(덮어쓰기 가능)
- **Digest**: 이미지 내용 기반 식별자(`sha256:...`) → **불변**, 배포 고정에 사용
- **전략**: “운영은 **Tag + Digest 병행**” → 가시성(Tag) + 재현성(Digest)

**■ ECR 푸시 & Digest 확보(14주 실습)**

```bash
aws ecr get-login-password --region <REGION> \
| docker login --username AWS --password-stdin <ACCOUNT>.dkr.ecr.<REGION>.amazonaws.com

docker push <ACCOUNT>.dkr.ecr.<REGION>.amazonaws.com/sentiment:1.0.0

# Digest 확인(둘 다 가능)
docker inspect --format='{{index .RepoDigests 0}}' sentiment:1.0.0
aws ecr describe-images --repository-name sentiment --image-ids imageTag=1.0.0 \
  --query 'imageDetails[0].imageDigest' --output text
```

</section>

<!--SCRIPT
v: 1
id: "15.5.2-tag-digest"
title: "Tag vs Digest — 왜 둘 다 쓰나"
ko: |
  Tag는 1.0.0이나 latest처럼 사람에게 읽기 좋은 라벨로 대시보드와 협업 맥락을 제공합니다. 반면 Digest는 이미지 내용의 해시로 동일성 보장을 제공하므로 배포 고정과 롤백의 기준이 됩니다. 로그인 후 푸시를 수행한 다음, docker inspect나 ECR API로 Digest 값을 조회하여 릴리스 기록에 함께 남기면 향후 어느 환경에서든 동일 이미지를 재현할 수 있습니다. 운영에서는 태그로 가시성을 확보하되, 실제 배포 대상은 Digest로 지정하여 라벨 변경과 무관하게 동일 이미지를 참조하도록 구성해야 합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.5.2 태그 vs Digest·불변성</h1>

**■ 배포 고정 & 불변성 운영 팁(14주 연계)**

- **App Runner/ECS**: `ImageIdentifier=<repo>@<DIGEST>`로 **릴리스 고정**
- **태그 불변성**: ECR **Immutable tags**(덮어쓰기 방지) + **Lifecycle Policy**로 오래된 이미지 정리
- **스캔/정책**: ECR 이미지 스캔 활성화, 실패 시 배포 차단(파이프라인)
- **릴리스 네이밍**: `app:1.2.3` + Git SHA(주석/릴리스 노트에 **Digest 기록**)
- **롤백 계획**: 직전 Digest로 즉시 전환, 헬스·지표로 검증

> 원칙: 가시성(Tag)과 재현성(Digest)을 분리해 관리하고, ECR 정책으로 **불변·청결**을 자동화합니다.

</section>

<!--SCRIPT
v: 1
id: "15.5.2-immutability"
title: "불변성·릴리스 운영"
ko: |
  프로덕션 배포는 App Runner나 ECS에서 이미지 식별자를 레포지토리와 Digest 조합으로 지정해 릴리스를 고정합니다. ECR의 Immutable tags를 활성화하여 태그 덮어쓰기를 방지하고, 라이프사이클 정책으로 오래된 이미지를 자동 정리하면 저장소의 일관성을 유지할 수 있습니다. 이미지 스캔을 기본값으로 켜고 취약점이 탐지되면 파이프라인 단계에서 배포를 차단하며, 릴리스 노트와 변경 기록에는 Tag와 함께 Digest를 반드시 기재합니다. 문제 발생 시 직전 Digest로 즉시 롤백하고, 헬스 체크와 지표로 정상화 여부를 확인하는 절차를 표준 운영 문서로 고정합니다.
hangul_pron: ""
-->

---

<section class="slide-part">
15.6 네트워킹·트래픽 경로 요약

(VPC, Subnet, ALB/HTTPS)

</section>

<!--SCRIPT
v: 1
id: "15.6-part"
title: "파트 오프닝 — 네트워킹·트래픽 경로"
ko: |
  이어서 VPC와 서브넷, ALB와 HTTPS, S3·CloudFront·App Runner로 이어지는 전체 경로를 L3·L4·L7 계층 관점에서 일관된 절차로 정리합니다. 문제 발생 시 어느 지점부터 확인할지, 헬스체크와 도메인, 인증서 설정을 어떻게 결합할지, 실습에서 사용한 도구와 지표를 기준으로 알아보겠습니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<!-- @슬라이드 초과됌 => A/B로 분할됌 -->
<h1>15.6.1 L3/4/7 관점의 문제해결 순서</h1>

**■ L3→L4→L7 점검 순서: 네트워크·전송·애플리케이션 트러블슈팅**

<div class = "onePage">

![](assets/w15_15.6.1-steps.svg)

</div>

<!-- 대체텍스트:

아래처럼 쓰면 좋아요.

## SVG `<title>` 제안

1. L3→L4→L7 점검 순서: 네트워크·전송·애플리케이션 트러블슈팅
2. L3/4/7 관점의 문제해결 흐름(하위 레이어부터 확인)
3. 네트워크(L3)→전송(L4)→애플리케이션(L7) 점검 가이드

```svg
<svg ...>
  <title>L3→L4→L7 점검 순서: 네트워크·전송·애플리케이션 트러블슈팅</title>
  ...
</svg>
```

## 짧은 설명(alt)

L3→L4→L7 순서로 하위 레이어부터 점검하는 트러블슈팅 다이어그램. L3는 서브넷/라우팅/VPC 엔드포인트·CIDR 중복, L4는 SG/NACL/ALB 리스너·포트, L7은 경로·호스트 규칙/CORS·도메인과 인증서/TLS를 확인하고, 각 단계에는 Reachability Analyzer·Flow Logs·curl -v·ALB 로그·CloudWatch 같은 도구가 제시된다.

## 상세 설명(longdesc/캡션)

이미지(1500×600)는 상단 3패널과 하단 흐름도로 구성된다. 좌측 상단에는 시각적 제목이 없다.

1. 상단 패널

* L3(네트워크) “경로가 있나?”:
  • 서브넷 구분 — Public(IGW)/Private(NAT GW).
  • 라우팅 — Route Table 목적지/다음 홉(IGW, NAT, TGW, VPCE).
  • VPC 엔드포인트(S3/Secrets 등) 존재 여부, CIDR 중복(피어링·온프렘).
  • 도구 — Reachability Analyzer, VPC Flow Logs, traceroute.
* L4(전송) “포트가 열려 있나?”:
  • Security Group — 인바운드/아웃바운드, 소스 범위, Stateful.
  • NACL — 서브넷 1차 차단, 번호순, Stateless.
  • ALB 리스너 — 80/443, 대상 포트 일치, 헬스체크 포트/프로토콜.
* L7(애플리케이션) “HTTP가 맞나?”:
  • 경로/호스트 기반 규칙, CORS/헤더, HTTP→HTTPS 리다이렉트.
  • 도메인(Route 53), 인증서/체인, SNI, 최소 TLS 1.2.
  • 도구 — `curl -v`, ALB TargetHealth, ALB 접근 로그, CloudWatch 지표.

2. 하단 흐름도

* 세 개의 카드가 1→2→3으로 화살표로 연결됨:
  ① L3: 서브넷(Public/Private), 라우트(IGW/NAT/TGW/VPCE), VPC 엔드포인트/대역 중복, 도구(Reachability/Flow Logs/traceroute).
  ② L4: SG(인바/아웃/소스), NACL(번호순·Stateless), ALB 리스너(80/443·대상 포트·HC), 테스트(`nc`/`telnet`).
  ③ L7: 경로·호스트 규칙/CORS, 도메인·인증서·체인/SNI/TLS≥1.2, 리다이렉트, 도구(`curl -v`/TargetHealth/ALB 로그/CloudWatch).
* 상단 각 패널에서 하단 대응 카드로 내려가는 보조 화살표가 있어 “상단 요점 ↔ 하단 실행 순서”를 시각적으로 연결한다.
* 모서리 배지: “순서: L3 → L4 → L7 (하위 레이어부터 확인)”.

핵심: 네트워크 경로(L3) 확인 → 포트·보안(L4) → HTTP·도메인·인증서(L7) 순으로, 하위 레이어부터 원인을 줄여 나간다.

 -->

</section>

<!--SCRIPT
v: 1
id: "15.6.1-steps"
title: "L3→L4→L7 점검 순서"
ko: |
  트러블슈팅은 하위 레이어에서 상위 레이어로 올라가는 순서를 지키는 것이 원칙입니다.
  먼저 L3에서 퍼블릭·프라이빗 서브넷 분리가 올바른지 확인합니다.
  라우트가 IGW·NAT·TGW·VPC 엔드포인트로 정확히 이어지는지도, 다음 홉까지 대조합니다.
  피어링·온프렘 구간의 CIDR 중복 여부도 반드시 점검합니다.
  이 단계는 Reachability Analyzer·VPC Flow Logs·traceroute로 근거를 남깁니다.

  다음은 L4입니다. 보안그룹의 인바운드·아웃바운드와 소스 범위를 세밀하게 확인합니다.
  서브넷 경계의 NACL 규칙은 번호순 평가와 Stateless 특성을 전제로 검토합니다.
  ALB 리스너의 80·443, 대상 그룹 포트, 헬스체크 포트·프로토콜이 앱 설정과 일치하는지도 확인합니다.

  마지막으로 L7에서 경로·호스트 기반 규칙이 실제 Host 헤더와 일치하는지 점검합니다.
  CORS와 HTTP에서 HTTPS 리다이렉트가 루프를 만들지, 필요한 헤더 전달이 누락되지 않았는지 봅니다.
  도메인은 Route 53의 Alias로 연결하고, 인증서 체인·SNI와 최소 TLS 1.2 준수 여부를 검증합니다.
  이 순서를 지키면 원인 범위를 단계적으로 줄이고, 지표와 로그로 동일한 결론을 빠르게 도출할 수 있습니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.6.1 L3/4/7 관점의 문제해결 순서</h1>

**■ 빠른 디버깅 체크리스트(실습 연결)**

- [L3] Public은 **IGW**, Private은 **NAT GW** 경로? VPCE로 내부 통신? (4·5·14주)
- [L4] **SG 소스**를 ALB/서브넷 CIDR로 제한했는가? NACL Deny 규칙에 걸렸나? (5·7주)
- [L4] **헬스체크 포트/패스**가 앱과 일치? 성공 코드 범위(200–399)? (5·14주)
- [L7] **호스트/패스 규칙**과 실제 Host 헤더 일치? HTTP→HTTPS 리다이렉트 루프?
- [관측] ALB **HealthyHostCount**, 5xx/4xx, **TargetResponseTime**(CloudWatch) (5·14주)
- [로그] ALB/앱 접근 로그, **VPC Flow Logs**, **Route 53 쿼리 로그**(10·14주)

> 원칙: **밖→안, 상단→하단**이 아니라 **L3→L4→L7**로 계층 순서대로.

</section>

<!--SCRIPT
v: 1
id: "15.6.1-check"
title: "체크리스트"
ko: |
  점검은 L3에서 네트워크 경로의 존재를 먼저 확정하는 것부터 시작합니다.
  퍼블릭 서브넷은 IGW로, 프라이빗 서브넷은 NAT 게이트웨이로 나가는지 확인합니다.
  내부 서비스 호출은 VPC 엔드포인트를 통하는지, 우회 경로가 없는지도 살핍니다.
  이어서 L4에서 보안그룹의 인바운드·아웃바운드와 소스 CIDR을 재확인합니다.
  NACL은 번호순·Stateless 특성을 고려해 Deny 규칙 충돌 여부를 점검합니다.
  ALB 대상 그룹의 헬스체크 포트·경로가 앱 리슨 포트·엔드포인트와 일치해야 합니다.
  성공 코드 범위는 200에서 399로 설정했는지, 간격·타임아웃 임계도 함께 검토합니다.
  L7에서는 호스트·패스 규칙이 실제 요청의 Host 헤더와 일치하는지 봅니다.
  HTTP에서 HTTPS 리다이렉트가 단방향으로만 동작하는지, 루프가 없는지 확인합니다.
  관측은 ALB HealthyHostCount·4xx·5xx·TargetResponseTime을 기준으로 읽습니다.
  근거는 ALB·애플리케이션 접근 로그, VPC Flow Logs, Route 53 쿼리 로그에 남깁니다.
  항상 밖에서 안이 아니라, L3→L4→L7 순서로 범위를 좁히며 진행합니다.
hangul_pron: ""
-->

---

<section class="slide-section">

<h1>15.6.2 헬스체크·도메인·인증서 포인트</h1>

**■ 헬스체크·도메인(Route 53)·인증서(ACM) 핵심과 트래픽 흐름**

![](assets/w15_15.6.2-hcd.svg)

<!-- 대체텍스트:



# 짧은 설명

헬스체크·도메인(Route 53)·인증서(ACM) 설정 요점을 한 화면에 정리한 다이어그램. 상단 3패널(헬스체크, 도메인, 인증서)과 하단 트래픽 흐름(도메인 → Route 53 → CloudFront/ALB → Target Group → Targets)을 보여주며, CloudFront 인증서는 us-east-1, ALB 인증서는 서비스 리전에서 발급해야 함을 강조한다.

# 상세 설명

이미지 크기 1500×600. 좌측 상단에 화면 제목은 없다.

1. 상단 좌—헬스체크(Health Check)

* “ALB Target Group”: 프로토콜/포트/패스(`/health`), 성공 코드 범위 `200–399`.
* “임계값”: Healthy/Unhealthy Threshold, Interval, Timeout → 불필요한 교체 방지.

2. 상단 중—도메인(Route 53)

* Alias A/AAAA: `api.example.com → ALB/CloudFront`(10·14주).
* 레코드 타입/TTL, 가중·지연·장애조치 라우팅.
* 내부 전용: Private Hosted Zone + VPC 연결.

3. 상단 우—인증서(ACM)

* ALB용 인증서: 서비스 **리전**에서 발급/연결.
* CloudFront용 인증서: **us-east-1**에서 발급(10주).
* SAN/와일드카드, 자동 갱신, 최소 TLS 1.2, SNI 사용.

4. 하단—트래픽 흐름 및 연결

* 왼쪽부터: “도메인(api.example.com)” → “Route 53(Alias A/AAAA, TTL/정책)”.
* 여기서 두 갈래: “CloudFront(ACM: us-east-1)”와 “ALB(ACM: 서비스 리전)”.
* 이후 “Target Group(HC: `/health`, 200–399)” → “Targets(EC2/ECS/Lambda)”.
* 상단에는 CloudFront 관련 보안 요구(TLS ≥ 1.2·SNI·SAN/와일드카드) 배지.
* 좌하단 보조 카드: 앱 측 /health 구현 팁(경량 엔드포인트, DB/외부 API 의존 분리, 임계값과 조합).

5. 표시 방식

* 화살표는 도형 위 레이어지만, 텍스트를 나중에 그려 내용이 가려지지 않는다.

**핵심 메시지**

* 헬스체크는 “가볍고 정확하게”; Route 53은 Alias로 엣지/ALB에 연결.
* 인증서는 CloudFront=us-east-1, ALB=서비스 리전.
* Target Group의 HC 설정과 DNS/ACM 구성을 일관되게 맞추면 안정적 라우팅과 자동 교체가 가능하다.


 -->

<!-- **■ 헬스체크(Health Check)

- **ALB Target Group**: 프로토콜/포트/패스(`/health`), 성공 코드 범위(예: `200-399`)
- 임계값: **Healthy/Unhealthy Threshold**, Interval, Timeout → **불필요한 교체 방지**
- 앱 측: 경량 엔드포인트, 의존성 체크(DB·외부 API) 분리(5·14주)

**■ 도메인(Route 53)

- **Alias A/AAAA**: `api.example.com → ALB/CloudFront` (10·14주)
- 레코드 타입/TTL, **가중/지연/장애조치** 라우팅
- 내부 전용은 **Private Hosted Zone** + VPC 연결

**■ 인증서(ACM)

- **ALB용 인증서**: 서비스 **리전**에서 발급/연결
- **CloudFront용 인증서**: **us-east-1**에서 발급(10주)
- SAN/와일드카드, **자동 갱신**, 최소 **TLS 1.2**, SNI 사용 -->
</section>

<!--SCRIPT
v: 1
id: "15.6.2-hcd"
title: "헬스체크·도메인·인증서 핵심"
ko: |
  헬스체크는 가볍고 정확해야 합니다. 대상 그룹에서 프로토콜·포트·경로를 /health로 명확히 지정하고, 성공 코드는 200에서 399 범위로 설정하며, Healthy·Unhealthy 임계값과 Interval·Timeout을 조정해 불필요한 교체를 막습니다. 애플리케이션의 헬스 엔드포인트는 외부 의존성을 최소화해 응답 지연과 오탐을 줄입니다. 도메인은 Route 53의 Alias 레코드로 CloudFront 또는 ALB에 연결하고, 내부 전용 도메인은 Private Hosted Zone과 VPC 연결로 구성합니다. 인증서는 리소스에 맞는 리전이 핵심입니다. ALB는 서비스가 위치한 리전에서 발급·연결하고, CloudFront는 us-east-1에서 발급한 인증서를 사용해야 동작합니다. SAN·와일드카드 구성을 통해 도메인 변형을 포괄하고, 자동 갱신과 SNI, 최소 TLS 1.2 이상을 기본값으로 유지합니다. 이 세 축을 일관되게 맞추면 DNS와 트래픽 라우팅, 자동 교체가 안정적으로 동작합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.6.2 헬스체크·도메인·인증서 포인트</h1>

**■ 베스트 프랙티스(실습 요약)**

- **HTTP→HTTPS 리다이렉트**: ALB 80 리스너에서 443으로 고정(보안·SEO)
- **HSTS/보안 헤더**: 애플리케이션/엣지에서 추가(10주)
- **OAC/OAI + S3 비공개 원본**: 원본 노출 차단(6·10주)
- **App Runner 커스텀 도메인** + ACM 검증(14주)
- **모니터링**: Route 53 Health Check + CloudWatch 알람, 지표 기반 SLA 관리

<div class="onePage">

| 영역      | 핵심 설정                        | 연결 주차 |
| --------- | -------------------------------- | --------- |
| 헬스체크  | `/health`, 200–399, 임계값 튜닝  | 5·14주    |
| 도메인    | Alias 레코드, 장애조치 라우팅    | 10·14주   |
| 인증서    | ALB=리전, CF=us-east-1, TLS 1.2+ | 10주      |
| 원본 보호 | S3 비공개 + OAC/OAI              | 6·10주    |

</div>
</section>

<!--SCRIPT
v: 1
id: "15.6.2-bp"
title: "운영 팁"
ko: |
  운영 기본값은 HTTP에서 HTTPS로의 리다이렉트를 ALB 80 리스너에서 443으로 고정하는 것입니다. 보안 헤더와 HSTS는 애플리케이션 또는 엣지에서 적용해 전송 보안을 강화합니다. 정적 원본은 S3를 비공개로 유지하고 CloudFront의 OAC 또는 OAI만 허용해 직접 접근을 차단합니다. App Runner는 커스텀 도메인을 연결한 뒤 ACM 검증을 완료해 TLS를 적용합니다. 가용성 관리는 Route 53 헬스체크와 CloudWatch 알람을 조합해 SLA 기준으로 수행하며, 헬스·도메인·인증서 변경은 지표와 로그를 근거로 검증 후 반영합니다.
hangul_pron: ""
-->

---

<section class="slide-part">
15.7 스토리지·데이터베이스 개요

(S3/EBS/EFS, RDS/DynamoDB, 캐시)

</section>

<!--SCRIPT
v: 1
id: "15.7-part"
title: "파트 오프닝 — 스토리지·데이터베이스 총정리"
ko: |
  5주차 EBS, 6주차 S3, 7주차 RDS·DynamoDB, 10주차 CloudFront 실습을 축으로 스토리지와 데이터베이스 선택을 하나의 의사결정 흐름으로 정리합니다. 먼저 워크로드 특성을 기준으로 서비스를 매핑하고, 이어서 일관성과 확장성의 차이를 비교한 뒤, 마지막으로 백업과 복구 전략을 복기합니다. 애플리케이션 내부 캐시와 엣지 캐시의 역할 구분까지 포함하여, 어디에 무엇을 두고 어떤 비용·지연·신뢰성 특성을 얻는지 명확히 하겠습니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.7.1 워크로드 특성 → 서비스 매핑</h1>

**■ 무엇을 어디에 둘까? (실습 연결: 5·6·7·10주)**

<div class="onePage">

| 워크로드 특성                  | 권장 서비스                      | 이유/핵심 포인트                             | 연결 주차 |
| ------------------------------ | -------------------------------- | -------------------------------------------- | --------- |
| 정적 자산(이미지/HTML)         | **S3** (+ **CloudFront**)        | 저비용·무한 확장, 엣지 캐시로 지연↓·전송↓    | 6·10주    |
| 블록 스토리지(EC2 루트/데이터) | **EBS**                          | 고성능 블록 IO, 타입(gp3/io2)·IOPS 선택      | 5주       |
| 다수 인스턴스 공유 파일        | **EFS**                          | POSIX 공유, 탄력 확장, 컨테이너/EC2 간 공유  | (개념)    |
| 관계형 데이터(트랜잭션)        | **RDS**(MySQL/PostgreSQL 등)     | ACID, 멀티AZ·백업 자동, 읽기 복제본          | 7주       |
| 대규모 키값/저지연             | **DynamoDB**                     | 서버리스, 초당 수만 RPS, 온디맨드/프로비저닝 | 7주       |
| 애플리케이션 캐시              | **ElastiCache**(Redis/Memcached) | 읽기 지연↓, DB 부하↓, TTL·Invalidation       | (개념)    |
| 엣지 캐시                      | **CloudFront**                   | 전 세계 캐시, 오리진 보호·전송 절감          | 10주      |

</div>

> 기본 원칙: **정적은 S3(+CF), 상태는 DB/키값, 실행 서버의 디스크는 EBS**, 여러 서버가 공유하면 **EFS**

</section>

<!--SCRIPT
v: 1
id: "15.7.1-map"
title: "서비스 매핑 한눈에"
ko: |
  정적 자산은 S3에 두고 CloudFront로 전 세계에 캐시하면 지연과 전송 비용을 동시에 낮출 수 있습니다. 실행 서버의 디스크는 고성능 블록 IO가 필요한 영역이므로 EBS가 기준이 됩니다. 여러 인스턴스가 같은 파일을 동시에 읽고 써야 한다면 POSIX 공유가 가능한 EFS가 적합합니다. 강한 트랜잭션과 조인이 중요한 온라인 트랜잭션 처리에는 RDS가 중심이며, 읽기 규모가 커지면 복제본으로 분리합니다. 스키마 유연성과 수평 확장, 초저지연 키값 접근이 필요하면 DynamoDB를 고려합니다. 애플리케이션 응답 지연이 병목이면 내부 캐시는 ElastiCache, 글로벌 전송 최적화는 CloudFront로 해결합니다. 기준은 간단합니다. 정적은 S3와 엣지, 상태와 무결성은 RDS, 대규모 키값은 DynamoDB를 선택합니다. 실행 환경의 디스크는 EBS, 다중 서버 파일 공유는 EFS입니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.7.1 워크로드 특성 → 서비스 매핑</h1>

**■ 빠른 결정 가이드(질문 → 선택)**

- 파일을 **웹으로 직접 제공**? → **S3** (+ CloudFront 캐시 정책)
- **인스턴스가 부팅/로컬 쓰기** 필요? → **EBS 타입** 선택(gp3 기본, io2는 미션크리티컬)
- **여러 서버가 동시에 읽고/쓰기**? → **EFS**(Throughput/Burst 모드, NFS)
- **강한 트랜잭션·조인**? → **RDS** + 멀티AZ/읽기 복제본
- **스키마 유연·수평 확장**? → **DynamoDB**(파티션키 설계, GSI/LSI)
- **응답 지연이 병목**? → **ElastiCache(애플리케이션)** 또는 **CloudFront(엣지)**

> 비용 연계: 저장단가(S3 클래스), IO/IOPS(EBS·RDS), 요청/처리량(DynamoDB), 전송/요청(CloudFront)

</section>

<!--SCRIPT
v: 1
id: "15.7.1-guide"
title: "질문형 선택 가이드"
ko: |
  결정을 빠르게 내리려면 세 가지 질문을 순서대로 적용합니다. 첫째, 데이터를 어디서 어떻게 제공하고 접근하는가입니다. 웹에서 직접 제공한다면 S3에 두고 캐시 정책을 CloudFront로 정의합니다. 인스턴스 부팅과 로컬 쓰기처럼 블록 장치가 필요한 경우에는 gp3를 기본으로 선택하고 고성능 IO가 필수인 경우 io2로 상향합니다. 여러 서버가 동시에 접근해야 한다면 NFS 기반 EFS로 전환합니다. 둘째, 트랜잭션과 조인이 필요한가입니다. 그렇다면 RDS를 선택하고 멀티 AZ와 읽기 복제본으로 가용성과 읽기 확장을 준비합니다. 반대로 스키마가 유연하고 수평 확장이 우선이면 파티션 키 중심의 모델링으로 DynamoDB를 설계합니다. 셋째, 응답 지연이 병목인가입니다. 애플리케이션 경로는 ElastiCache로, 글로벌 전송 경로는 CloudFront로 캐시 계층을 추가합니다. 이때 저장 단가, IO와 IOPS, 요청·처리량, 전송·요청 과금이 각각 어디에서 발생하는지까지 함께 떠올리며 선택합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.7.2 일관성·확장성·백업 요점</h1>

**■ 일관성(Consistency)**

- **S3**: 객체 **강한 일관성**(신규/갱신/삭제 반영, 전 리전) → 버전닝·오브젝트 락과 함께 사용(6주)
- **RDS**: 트랜잭션 **강한 일관성**, **읽기 복제본은 지연** 가능 → 읽기 전용 트래픽 분리(7주)
- **DynamoDB**: 기본 **최종 일관성**, **강한 일관성 Read** 옵션·**트랜잭션** 지원(7주)

**■ 확장성(Scalability)**

- **S3/EFS**: 자동 확장(버킷/파일시스템), S3는 무한 수준(6주)
- **EBS**: 타입·크기·IOPS 조정, gp3로 비용/성능 균형(5주)
- **RDS**: 수직 확장 + 읽기 복제본(수평 읽기), 멀티AZ로 고가용성(7주)
- **DynamoDB**: 온디맨드/프로비저닝 + 오토스케일, **파티션 키** 설계가 성능의 핵심(7주)
- **캐시**: **ElastiCache** 클러스터링, **CloudFront** 캐시 정책·오리진 쉴딩(10주)

</section>

<!--SCRIPT
v: 1
id: "15.7.2-consistency"
title: "일관성과 확장성"
ko: |
  일관성은 읽기가 얼마나 빠르게 최신 쓰기를 반영하는가의 문제입니다. S3는 신규·갱신·삭제에 대해 강한 일관성을 제공하므로 버전닝과 오브젝트 락을 결합하면 무결성과 보존을 함께 확보할 수 있습니다. RDS는 트랜잭션에 대해 강한 일관성을 보장하지만 읽기 복제본에는 지연이 존재할 수 있으므로 읽기 전용 트래픽을 분리하고 쓰기 경로와의 차이를 인지해야 합니다. DynamoDB는 기본이 최종 일관성이며 필요 시 강한 일관성 읽기와 트랜잭션을 옵션으로 사용합니다. 확장성은 자원별 전략이 다릅니다. S3와 EFS는 관리형으로 자동 확장되고, EBS는 타입·크기·IOPS 조정으로 성능과 비용을 균형 있게 맞춥니다. RDS는 수직 확장과 읽기 복제본 조합으로 확장하며 멀티 AZ로 고가용성을 확보합니다. DynamoDB는 온디맨드 또는 프로비저닝 모드에 오토스케일을 결합하되 파티션 키 설계가 성능의 핵심이라는 점을 잊지 말아야 합니다. 캐시는 ElastiCache의 클러스터링과 CloudFront의 캐시 정책·오리진 쉴딩으로 계층을 구성해 원본 부하와 지연을 동시에 줄입니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.7.2 일관성·확장성·백업 요점</h1>

**■ 백업·보호(Backup & DR)**

- **S3**: 버전닝 + 수명주기 + **CRR/SRR**(교차/동일 리전 복제), **Object Lock**(WORM), Glacier 보관(6주)
- **EBS**: **스냅샷**(증분) 주기화, 템플릿으로 복구 테스트(5주)
- **RDS**: 자동 백업·보존 기간 + **PITR**, 스냅샷/크로스리전 복제, 장애조치 연습(7주)
- **DynamoDB**: **PITR** + 온디맨드 백업/복원, 글로벌 테이블로 다중 리전(7주)
- **EFS**: 백업 서비스/라이프사이클(EFS-IA)로 비용 최적화

**■ 운영 체크리스트**

- 복구목표(**RTO/RPO**)를 **서비스별로 문서화**하고, **정기 복구 드릴** 실행
- 백업/스냅샷에 **태그** 적용해 비용·책임 구분(15.3 연계)
- 민감 데이터는 **KMS** 암호화(S3/EBS/EFS/RDS/DynamoDB), 키 로테이션

</section>

<!--SCRIPT
v: 1
id: "15.7.2-backup"
title: "백업·DR 핵심"
ko: |
  백업의 목적은 저장이 아니라 검증된 복구입니다. S3는 버전닝과 수명주기 정책, 교차·동일 리전 복제와 오브젝트 락, Glacier 보관으로 보존과 비용을 함께 관리합니다. EBS는 증분 스냅샷을 주기화하고 템플릿으로 복구 과정을 실제로 검증해야 합니다. RDS는 자동 백업과 보존 기간, 시점 복구를 활용하고 스냅샷과 크로스 리전 복제를 통해 장애 조치 훈련을 정례화합니다. DynamoDB는 시점 복구와 온디맨드 백업·복원을 사용하며, 다중 리전 요구가 있으면 글로벌 테이블로 설계합니다. EFS는 백업 서비스와 Infrequent Access 계층을 조합해 비용을 최적화합니다. 모든 리소스에는 KMS 암호화를 적용하고 키 로테이션 정책을 유지하며, RTO와 RPO를 서비스별로 문서화해 정기 복구 드릴로 검증합니다. 백업과 스냅샷, 복제 리소스에도 일관된 태그를 부여해 비용과 책임 귀속을 명확히 하는 것으로 마무리합니다.
hangul_pron: ""
-->

---

<section class="slide-part">
15.8 모니터링·로깅·알람 최소 세트
</section>

<!--SCRIPT
v: 1
id: "15.8-part"
title: "파트 오프닝 — 모니터링·로깅·알람 최소 세트"
ko: |
  이번 파트의 목표는 CloudWatch Metrics와 Logs, Logs Insights, 그리고 알람을 하나의 운용 루틴으로 묶어 “항상 켜두는 최소 세트”를 명확히 하는 것입니다. 대시보드는 사용자 경로에서 시작해 애플리케이션과 데이터 계층으로 내려가는 순서로 배치하고, 로그는 구조화 포맷과 상관키를 공통 규칙으로 적용합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.8.1 CloudWatch Metrics/Logs·지표 읽기</h1>

**■ 대시보드 빠른 구성**

![](assets/w15_15.8.1-dashboard.svg)

<!-- 대체텍스트:

# 짧은 설명

CloudWatch 대시보드 + 로그 파이프라인 개요 다이어그램. 상단은 사용자 경로(CloudFront/ALB 요청·4xx/5xx·p95 지연), 애플리케이션(Lambda Errors/Throttles/Duration p95, App Runner CPU/Memory, 연결 지표), 데이터층(RDS CPU/FreeStorage/Connections, DynamoDB Throttle/용량, S3 5xx)을 위→아래로 배치. 우측에는 NAT 처리량, VPC 엔드포인트 트래픽 등 비용·전송 보조 지표. 하단은 CloudWatch Logs → Logs Insights → 구독 필터 → S3 저장소·OpenSearch로 흐르는 로그 파이프라인과 “INFO 일부 샘플링, ERROR 전량 저장” 원칙이 표시됨. 원칙: 사용자 경로 기준으로 위→아래 정렬.

# 상세 설명

이미지(1500×600)는 상단 “대시보드” 영역과 하단 “로그 파이프라인” 영역으로 나뉜다. 좌측 상단에 시각적 제목은 없다.

1. 상단 왼쪽(대시보드 1페이지)

* 위 행(사용자 경로):
  • CloudFront 박스 — Requests, 4xx/5xx, p95 Latency.
  • ALB 박스 — RequestCount, HTTP 4xx/5xx, TargetResponseTime p95.
  • “사용자 경로 요약” 카드 — 5xx 합계, p95 지연, 트래픽 스파이크.
* 가운데 행(애플리케이션):
  • Lambda — Errors/Throttles, Duration p95.
  • App Runner — CPUUtilization, MemoryUtilization.
  • 연결 지표 — 에러율·서킷브레이커, 큐 깊이/지연.
* 아래 행(데이터):
  • RDS — CPU, FreeStorage, DBConnections.
  • DynamoDB — Throttle, Read/Write Capacity.
  • S3 — 5xx Error Rate.
* 세 행 사이에는 위→아래로 짧은 화살표가 있어 “사용자 경로에서 앱, 데이터로 내려가며 확인” 흐름을 강조한다.

2. 상단 오른쪽(보조 지표)

* NAT 데이터 처리 — BytesProcessed, ActiveConnections.
* VPC 엔드포인트 트래픽 — BytesIn/Out, 연결 오류/거부, 비용 추정(GB).

3. 하단(로그 파이프라인)

* 순서 박스와 화살표: CloudWatch Logs → Logs Insights → 구독 필터 → (분기) S3 저장소 · OpenSearch.
* “샘플링 & 보존” 안내 카드:
  • INFO는 일부 샘플링, ERROR/경고는 전량 저장.
  • 고트래픽 서비스는 레이트 리밋 적용.
* 우측 배지: “원칙: 사용자 경로 위→아래 정렬, 메트릭·로그를 같은 축으로 정렬”.

핵심 메시지

* 장애/이상 징후 확인은 사용자 경로(CF/ALB) 상단부터 애플리케이션, 데이터로 내려간다.
* 로그는 운영 분석(Logs Insights)과 장기 보관·검색(S3/OpenSearch)을 구독 필터로 분리한다.
* 비용·전송 지표(NAT, VPC 엔드포인트)도 같은 축에서 함께 본다.

 -->

<!--
- 위: **사용자 경로** — CloudFront/ALB `Requests, 4xx/5xx, p95 Latency`
- 중: **애플리케이션** — Lambda `Errors/Throttles/Duration p95`, App Runner `CPU/Memory`
- 하: **데이터** — RDS `CPU/FreeStorage/Connections`, DynamoDB `Throttle`, S3 `5xx`
- 우측: **비용·전송 보조** — NAT 데이터 처리, VPC 엔드포인트 트래픽(15.3 연계)

**■ 로그 파이프라인

- CloudWatch Logs → **Logs Insights**(운영 분석) → **구독 필터**로 S3/OpenSearch 적재(장기/검색)
- **샘플링**: 고트래픽 서비스는 INFO 일부 샘플링, ERROR/경고는 전량 저장

> 원칙: “사용자 경로 위에서 아래로” 배치하고, 메트릭·로그가 서로 답을 줄 수 있게 같은 축(서비스/경로)로 정렬 -->

</section>

<!--SCRIPT
v: 1
id: "15.8.1-dashboard"
title: "운영 대시보드 구성"
ko: |
  대시보드는 사용자의 체감 경로를 맨 위에 두고 읽어야 합니다.
  CloudFront와 ALB에서 요청 수, 4xx·5xx 비율, p95 지연을 함께 보며
  문제 징후가 생기면 아래 계층으로 내려가 원인을 좁힙니다.

  애플리케이션 영역에서는 Lambda의 Errors·Throttles·Duration p95와
  App Runner의 CPU·메모리를 묶어 보고, 서비스 연결 지표로 증상을 교차 확인합니다.
  데이터 영역은 RDS의 CPU·FreeStorage·Connections과
  DynamoDB의 용량·Throttled, S3의 5xx로 병목을 판별합니다.

  NAT 처리량과 VPC 엔드포인트 트래픽 같은 전송·비용 지표는
  같은 시간 축으로 정렬해 상단 지표와의 상관을 바로 확인합니다.
  로그는 CloudWatch Logs를 운영 분석에, 구독 필터를 통해
  S3·OpenSearch를 장기 보관·검색에 쓰며 서로 간섭하지 않게 분리합니다.

  원칙은 단순합니다. 위에서 아래로, 같은 시간 축과 단위로,
  메트릭과 로그가 서로 답을 줄 수 있게 배치하는 것입니다.
hangul_pron: ""
-->

---

<!-- @SVG 추가 수정함 -->
<section class="slide-section">
<!-- @슬라이드 초과됌 => A/B로 분할됌 -->
<h1>15.8.1 CloudWatch Metrics/Logs·지표 읽기</h1>

**■ Logs(표준)**

- **구조화 JSON 로그**: `timestamp, level, traceId, path, status, latencyMs, userId`
- **로그 그룹 네이밍**: `/app/{env}/{service}` · **보존기간** 환경별 분리(개발 짧게/운영 길게)
- **상관키**: `traceId`를 프런트→백엔드→DB 호출 체인에 전파, X-Ray/OTel로 트레이스(선택)

<div class = "fig top25"></div>

![](assets/w15_15.8.1-cloudwatch-logs-diagram-v2.svg)

</section>

<!--SCRIPT
v: 1
id: "15.8.1-metrics"
title: "계층별 최소 메트릭·로그 표준"
ko: |
  로그는 JSON으로 구조화하여 timestamp, level, traceId, path, status, latencyMs, userId를 공통 필드로 기록하고, 서비스 전 구간에 traceId를 전파해 프런트엔드부터 백엔드, 데이터 계층까지 호출 연쇄를 잃지 않도록 합니다. 로그 그룹은 /app/{env}/{service}와 같은 규칙으로 네이밍하고, 개발 환경은 짧고 운영은 긴 보존 기간을 적용해 비용과 규정을 동시에 충족합니다. 메트릭은 대시보드의 위에서 아래로 흐르는 사용자 경로에 맞춰 동일한 지표명을 유지하고, 로그의 latencyMs와 메트릭의 p95 지연이 같은 구간과 경로 기준으로 비교 가능하도록 단위를 일치시킵니다. 선택적으로 X-Ray 또는 OpenTelemetry 트레이싱을 도입해 지연 분해와 외부 의존성 병목을 식별합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<!-- @슬라이드 초과됌 => A/B로 분할됌 -->
<h1>15.8.2 Logs Insights·알람 임계 설계</h1>

**■ Logs Insights — 실전 쿼리**

- **애플리케이션 에러 Top N**

```sql
fields @timestamp, @message, level, path
| parse @message /"level":"(?<level>[^"]+)"/
| parse @message /"path":"(?<path>[^"]+)"/
| filter level = "ERROR"
| stats count() as errors by path
| sort errors desc
| limit 10
```

- **지연 p95 (JSON 로그에 latencyMs가 있을 때)**

```sql
fields @timestamp, latencyMs, path
| parse @message /"latencyMs":(?<latencyMs>\d+)/
| stats pct(latencyMs,95) as p95 by bin(5m), path
| sort bin(5m) desc
```

</section>
<!--SCRIPT
v: 1
id: "15.8.2-queries"
title: "Logs Insights 실전 쿼리1"
ko: |
  애플리케이션 오류 상위 경로를 찾는 쿼리는 메시지에서 level과 path를 파싱해 ERROR만 필터링한 뒤 경로별로 집계합니다. 이렇게 얻은 Top N은 대시보드의 5xx와 p95 지표 상승 구간과 대조하여 어느 엔드포인트에서 오류가 집중되는지 바로 파악하게 해 줍니다. 지연 분석은 로그에 기록한 latencyMs를 파싱해 5분 구간으로 버킷팅한 p95를 경로별로 계산하고, ALB의 TargetResponseTime p95와 동일 구간으로 비교하여 애플리케이션 처리 지연인지 네트워크 요인인지 구분합니다. 두 쿼리의 결과는 즉시 대응 순서를 결정하는 근거가 되므로, 대시보드 링크와 함께 운영 핸드북에 고정하는 것이 바람직합니다.
hangul_pron: ""
-->

---

<!-- @ 수정하기 -->

<section class="slide-section">
<!-- @슬라이드 초과됌 => A/B로 분할됌 -->
<h1>15.8.2 Logs Insights·알람 임계 설계</h1>

**■ Logs Insights — 실전 쿼리**

- **ALB 5xx 스파이크 감지(액세스 로그 수집 시)**

```sql
fields @timestamp, elb_status_code, target_status_code, request_url
| filter elb_status_code like /5\d\d/ or target_status_code like /5\d\d/
| stats count() as fiveXX by bin(1m)
| sort bin(1m) desc
```

</section>

<!--SCRIPT
v: 1
id: "15.8.2-queries"
title: "Logs Insights 실전 쿼리"
ko: |
  ALB 접근 로그를 수집하는 경우에는 elb_status_code와 target_status_code를 기준으로 5xx 패턴을 필터링하고 1분 구간으로 집계해 스파이크를 탐지합니다. 이 결과를 ALB 메트릭의 5xx 비율과 교차 검증하면 로드 밸런서 단계에서의 오류 상승이 실제 사용자 체감으로 이어지고 있는지 구분할 수 있습니다. 특정 분기에서 target_status_code만 상승한다면 백엔드 대상 그룹의 헬스체크와 애플리케이션 로그로 진단 범위를 즉시 좁힐 수 있습니다. 이렇게 얻은 시계열은 짧은 보존 기간의 경고 알림과 장기 보관의 추세 분석 모두에 활용됩니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<!-- @슬라이드 초과됌 => A/B로 분할됌 -->
<h1>15.8.2 Logs Insights·알람 임계 설계</h1>

**■ CloudWatch 알람 임계**

![](assets/w15_15.8.2-alarms1.svg)

<!-- 대체 텍스트:

## 짧은 설명(alt)
CloudWatch 알람 임계치를 신호등 표로 정리한 다이어그램. 열은 지표/경고(노랑)/심각(빨강)/액션이며, 사용자 체감(CF·ALB 5xx, ALB p95), 애플리케이션(Lambda Throttles/Errors, App Runner CPU·메모리), 데이터(RDS CPU·FreeStorage·Connections)가 한눈에 보인다. 우측에는 “3대 실패 원인(포트·헬스 경로·ENV)”과 안정성 보강(Anomaly Detection, Composite Alarm, Auto Scaling, 주 1회 리뷰) 및 DynamoDB Throttled 요약이 있다.

## 상세 설명(longdesc/캡션)
이미지 크기 1500×600. 좌측 상단에 시각적 제목은 없고, 좌측은 신호등 테이블, 우측은 보조 패널로 구성된다.

1) 신호등 테이블(왼쪽 큰 패널)
- 열 헤더: 지표 / 경고(노랑) / 심각(빨강) / 액션.
- 섹션:
  • 사용자 체감
  ─ CloudFront/ALB 5xx 비율: 경고=상승 추세 또는 임계 80% 접근(최근 5 중 2개 상승), 심각=5xx > 1% (5분 중 3/5), 액션=페이지·알림, 오리진/WAF 원인 추적, 롤백/장애조치 검토.
  ─ ALB p95 응답시간: 경고=600–800ms 또는 2/5 상승, 심각=> 800ms(연속 3/5), 액션=오토스케일·캐시/쿼리 최적화·대상 그룹/헬스 확인.
  • 애플리케이션
  ─ Lambda Throttles/Errors: 경고=버스트 증가·예약 동시성 임계 접근, 심각=Throttles > 0(1 데이터포인트) 또는 Error Rate > 2%, 액션=동시성 예약/버스트·재시도/큐·콜드스타트·의존성 점검.
  ─ App Runner CPU/Memory: 경고=CPU > 70% 또는 메모리 > 75%(5분), 심각=CPU > 80% 또는 메모리 > 85%(5분), 액션=컨커런시/스케일 조정·리소스 상향·메모리 튜닝.
  • 데이터
  ─ RDS CPU: 경고=70–80% 상승 추세, 심각=> 80% 15분 지속, 액션=인덱스/쿼리 최적화·스케일업·리드 리플리카.
  ─ RDS FreeStorage: 경고=< 30%, 심각=< 20%, 액션=스토리지 확장/청소·수명주기 정책 확인.
  ─ RDS Connections: 경고=완만한 증가, 심각=급증/풀 소진, 액션=풀/커넥션 제한·스케일 조정.

2) 보조 패널(오른쪽)
- 3대 실패 원인: ① 포트 불일치 ② 헬스 경로 오타 ③ ENV 누락.
- 안정성 보강: Anomaly Detection(변동 밴드), Composite Alarm(“5xx↑ ∧ p95↑”), Auto Scaling 연동(EC2/ECS/AR), 주 1회 후속 리뷰/임계 재조정, 그리고 “Logs Insights로 원인 분석 쿼리” 문구.
- DynamoDB Throttled 요약: 경고=임계 접근/스파이크, 심각=ThrottledRequests > 0(5분), 액션=RCU/WCU 조정·파티션키 설계 점검.

핵심 메시지: 각 계층의 핵심 지표를 경고/심각 임계와 즉시 취할 액션으로 표준화하고, 우측 보강 항목(3대 실패 원인·Anomaly/Composite/Auto Scaling·Logs Insights)으로 탐지 노이즈를 줄이며 대응 속도를 높인다.

 -->

<!-- - **사용자 체감**
  - CloudFront/ALB **5xx 비율 > 1%** (5분 중 3개 이상) → 알림 (10·5주)
  - ALB **TargetResponseTime p95 > 800ms** (연속 3/5 데이터포인트)
- **애플리케이션**
  - Lambda **Throttles > 0**(1 데이터포인트) 또는 Error Rate > **2%** (9주)
  - App Runner **CPU > 80% or Memory > 85%** (5분) → 스케일/컨커런시 검토 (14주)
- **데이터**
  - RDS **CPU > 80% 15분**, **FreeStorage < 20%**, **DB Connections 급증** (7주)
  - DynamoDB **ThrottledRequests > 0**(5분) → WCU/RCU 조정 or 파티션키 점검 (7주) -->

</section>
<!--SCRIPT
v: 1
id: "15.8.2-alarms1"
title: "임계값·알람 운용"
ko: |
  알람은 사용자 체감 지표를 우선합니다. CloudFront 또는 ALB의 5xx 비율이 5분 중 3개 구간에서 1%를 초과할 때를 심각 상태로 정의합니다. ALB의 p95 응답 시간이 800ms를 연속 3개 이상의 데이터포인트에서 초과하면 성능 저하로 분류해 페이지 알림과 함께 오토스케일, 캐시, 쿼리 튜닝을 즉시 검토합니다. 애플리케이션 계층에서는 Lambda의 Throttles가 단 한 데이터포인트라도 0을 초과하거나 오류율이 2%를 넘으면 동시성 예약과 재시도 정책, 외부 의존성 시간을 재점검합니다. App Runner는 CPU 80% 또는 메모리 85%가 5분 이상 지속되면 컨커런시와 스케일 파라미터를 조정합니다. 데이터 계층에서는 RDS CPU가 15분 동안 80%를 넘을 때 인덱스·쿼리 최적화와 스케일업·읽기 복제본을 순서대로 적용하고, FreeStorage가 20% 이하로 내려가면 즉시 확장하거나 데이터 정리를 수행합니다. DynamoDB는 ThrottledRequests가 5분 구간에 단 한 건이라도 발생하면 RCU·WCU와 파티션 키 설계를 점검합니다. 빈번한 오검을 줄이기 위해 이상 탐지 밴드를 적용하고, 5xx 상승과 p95 상승을 동시에 만족할 때만 페이지하도록 합성 알람을 구성합니다. 현장에서 자주 발생하는 실패 원인은 대상 포트 불일치, 헬스 체크 경로 오타, 환경 변수 누락으로 수렴하므로, 알람 메시지에 세 항목의 즉시 점검 지시를 포함시켜 대응을 표준화합니다. 마지막으로 알람 임계는 주 1회 리뷰에서 최근 추세에 맞게 재조정하고, 각 알람에는 대응 액션과 대체 배포·롤백 절차 링크를 함께 제공해 복구 시간을 단축합니다.
hangul_pron: ""
-->

---

<section class="slide-part">
15.9 ML 기본기 총정리(학습·평가·배포)
</section>

<!--SCRIPT
v: 1
id: "15.9-part"
title: "파트 오프닝 — ML 기본기 총정리"
ko: |
  11주차의 모델 직렬화와 핸들링, 12·13주차의 Flask·FastAPI 기반 추론 API 구현, 14주차의 AWS 배포 경험을 축으로 학습–평가–배포 전 과정을 다시 점검합니다. 데이터 분할은 누수를 차단하는 절차라는 전제에서 시작하고, 과적합 여부는 학습과 검증 지표의 괴리로 판정합니다. 평가지표는 문제의 비용 함수를 먼저 명시한 뒤 이를 가장 정확히 반영하는 지표를 선택해 보고하며, 배포 이후에는 오프라인 지표와 온라인 품질 지표를 함께 감시하여 모델이 실제 환경에서 목표를 지속 충족하는지 확인하겠습니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<!-- @슬라이드 초과됌 => 2열로 분할됌 -->
<h1>15.9.1 데이터 분할과 과적합 신호</h1>

**■ 분할 원칙(누적 실습 맥락)**

- **Train/Validation/Test = 6:2:2**(권장) · **고정 시드** · **중복 제거**
- **Stratified Split**: 불균형 분류에서 클래스 비율 보존
- **Time-based Split**: 시간누수 방지(이전 데이터로 학습, 이후 데이터로 검증)
- **K-Fold(5/10)**: 데이터가 작을수록 유효, **GroupKFold**로 사용자/세션 누수 차단
- **전처리 파이프라인**: 학습 스케일러/토크나이저를 **Train에만 적합** → Val/Test에는 transform만

<div class = "slide-2column ratio-64">
<div>

**■ 데이터 누수 체크**

- 라벨 정보가 특징에 스며든 컬럼 제거
  (예: 이후 로그, 정답 유추 가능 키)
- 텍스트 전처리 사전 구축/어휘 확장: **Train 기반**으로만
</div>
<div>

**■ 과적합 신호(High Variance)**

- Train 점수 ↑, **Val/Test 점수 정체/하락**
- **학습/검증 손실 간격 확대**, Val 손실 진동
- **모델 용량↑·특징↑** 에 비해 표본 수가 부족

</div>
</div>
</section>

<!--SCRIPT
v: 1
id: "15.9.1-split"
title: "분할 원칙과 과적합 신호"
ko: |
  데이터 분할은 재현 가능한 기준과 누수 차단으로부터 시작해야 합니다. 학습·검증·시험을 6:2:2로 나누고 고정 시드를 사용하며 중복 샘플을 제거한 뒤, 불균형 분류에서는 클래스 비율을 보존하도록 계층화 분할을 적용합니다. 시계열이나 로그 데이터는 과거로 학습하고 이후 구간으로 검증하는 시간 기반 분할로 미래 정보가 학습에 섞이지 않도록 해야 합니다. 사용자·세션처럼 상호 의존적인 단위가 있을 때는 GroupKFold로 묶음을 유지해 누수를 차단합니다. 전처리기는 학습 세트에만 적합시키고 검증·시험에는 변환만 적용하여 어휘나 스케일이 학습 데이터에서 결정되도록 합니다. 과적합은 학습 점수만 상승하고 검증·시험 점수가 정체 또는 하락하는 고분산 패턴, 학습과 검증 손실의 격차 확대, 표본 수 대비 과도한 모델 용량과 특징 수에서 뚜렷하게 나타납니다. 학습 로그와 곡선으로 이러한 신호를 조기에 식별해야 합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.9.1 데이터 분할과 과적합 신호</h1>

**■ 완화 전략(실습 연결)**

- **정규화/규제**: L2, 드롭아웃, 데이터 증가/클린, 간단한 모델로 **강한 베이스라인** 확보
- **얼리 스토핑**: Val 손실 n회 상승 시 중단, **최고 성능 시점의 가중치** 저장
- **하이퍼파라미터 탐색**: 범위를 넓게 → 점점 좁게(Bayesian/Random Search)
- **피처 선택/엔지니어링**: 상관 높은 중복 제거, 누수 가능 파생변수 금지
- **교차검증 점수의 평균±표준편차**로 안정성 확인

**■ 실무 체크리스트**

- [ ] Split 후 **클래스 분포/시간 범위** 요약
- [ ] **학습곡선**: 샘플 수↑에 따른 Val 점수 추세 확인
- [ ] **Seed 3회 이상** 재현 실험 · 평균 리포트
- [ ] 저장: **model.pkl + preproc.pkl + metrics.json**(11주 직렬화 연계)
</section>

<!--SCRIPT
v: 1
id: "15.9.1-mitigation"
title: "과적합 완화·체크리스트"
ko: |
  완화는 단순한 강한 기준선에서 출발합니다. L2 규제와 드롭아웃, 데이터 정제·증강을 우선 적용하고 필요 시 모델 용량을 줄여 가며 안정 구간을 찾습니다. 검증 손실이 n회 연속 상승하면 학습을 중단하고 최고 성능 시점의 가중치를 보존하는 얼리 스토핑을 기본으로 사용합니다. 하이퍼파라미터 탐색은 넓은 구간의 랜덤 또는 베이지안 탐색으로 후보를 수집한 뒤 유망 영역을 좁혀 정밀 조정하며, 파생 특징은 누수 가능성을 사전에 점검해 제외합니다. 의사결정은 교차검증 평균과 표준편차로 안정성을 함께 보고, 학습 곡선으로 샘플 증가에 따른 검증 점수의 수렴 여부를 확인합니다. 실험 후에는 model.pkl, preproc.pkl, metrics.json을 함께 직렬화해 저장하고, 서로 다른 시드를 최소 세 번 반복해 평균과 분산을 보고하여 재현성을 확보합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<!-- @슬라이드 초과됌 => A/B로 분할됌 -->

<h1>15.9.2 평가지표 선택 가이드</h1>

**■ 지표 선택 가이드: 분류·회귀·순위/추천**

![](assets/w15_15.9.2-metrics.svg)

<!-- 대체텍스트:

## 짧은 설명(alt)

평가지표 선택을 한 화면에 정리한 다이어그램. 상단 배너는 “문제의 비용 함수”를 먼저 정의하라고 강조하고, 아래 3열은 분류(Accuracy, Precision/Recall/F1, ROC-AUC/PR-AUC, Confusion Matrix, Calibration), 회귀(MAE, RMSE, R², MAPE, 퀀타일 손실), 순위/추천(NDCG, MAP, Recall@K)을 요약한다. 각 열은 상단 원칙에서 화살표로 연결되며, 하단에는 “보고는 비용 함수와 연결해 해석” 배지가 있다.

## 상세 설명(longdesc/캡션)

이미지 크기 1500×600. 좌측 상단에는 화면 제목이 없다.

1. 상단 배너(원칙)

* 문구: “먼저 ‘문제의 비용 함수’를 정의하고, 그 비용을 가장 잘 반영하는 지표를 선택/보고합니다.”
* 이 배너에서 세로 화살표가 아래 3개의 영역(분류/회귀/순위)로 내려간다.

2. 중단 3열 패널
   A. 분류(Classification)

* 핵심 지표:
  • 정확도(Accuracy): 클래스가 균형일 때만 대표성.
  • 정밀도/재현율/F1: 오탐·미탐 비용에 따라 선택(스팸·의료 등은 재현율 우선).
  • ROC-AUC: 전반적 분리력; 심한 불균형일 땐 PR-AUC 권장.
* 보조 카드: Confusion Matrix(에러 유형 파악, 극단적 불균형에 유용), Calibration(확률 보정: Brier, Reliability Curve)과 임계값 조정.

B. 회귀(Regression)

* 핵심 지표: MAE(해석 쉬움), RMSE(큰 오차에 민감), R²(설명력), MAPE(0 근처 값 주의).
* 보조 카드: 퀀타일 손실(Pinball)로 p90 등 특정 분위수 중심의 SLA 예측.

C. 순위/추천(Ranking/Recommendation)

* 핵심 지표: NDCG(순위 가중 품질), MAP(평균 정밀도의 평균), Recall@K(상위 K 내 재현율).
* 주의 카드: 데이터/시나리오별 K 설정 근거 명시, 후보 생성/재랭킹 단계별 지표 분리, 미추천/오추천 등 사용자 비용 정의와 정렬.

3. 하단 배지(요약 원칙)

* 텍스트: “보고는 비용 함수와 연결해 해석”.

핵심 메시지

* 지표 선택은 항상 “문제의 비용 함수”에서 출발한다.
* 분류/회귀/순위·추천 각각의 최소 세트와 보조 지표를 상황(불균형, SLA, 사용자 비용)에 맞춰 고른다.


 -->

<!-- **■ 분류(Classification)**

- **정확도(Accuracy)**: 클래스 균형일 때만 대표성
- **정밀도/재현율/ F1**: 오탐/미탐 비용에 따라 가중 — 스팸·의료 등은 **재현율 우선**
- **ROC-AUC**: 전반적 분리력, **불균형 심하면 PR-AUC** 권장
- **Confusion Matrix**: 에러 유형 파악(특히 극단적 불균형)
- **Calibration**: 확률 보정(Brier, Reliability Curve), 임계값 조정

**■ 회귀(Regression)**

- **MAE**: 절대 오차(해석 쉬움), **RMSE**: 큰 오차에 민감
- **R²**: 설명력, **MAPE**: 비율 오차(0 근처 값 주의)
- **퀀타일 손실(Pinball)**: p90 SLA 예측 등 분포 하이라이트 -->

</section>

<!--SCRIPT
v: 1
id: "15.9.2-metrics"
title: "지표 선택의 원칙"
ko: |
  지표 선택은 문제의 비용 함수를 먼저 정의하는 작업입니다. 분류 문제에서는 클래스가 균형일 때만 정확도를 대표값으로 사용하고, 오탐·미탐 비용이 비대칭이면 정밀도·재현율 또는 F1로 목적을 구체화합니다. 전반적 분리력 평가는 ROC-AUC로 가능하지만 극단적 불균형에서는 PR-AUC가 더 설명력이 높습니다. 혼동행렬로 오류 유형을 분해하고, 확률 기반 의사결정이 중요할 때는 Brier 점수와 신뢰도 곡선으로 보정 상태를 확인한 뒤 임계값을 조정합니다. 회귀 문제에서는 해석이 쉬운 MAE와 큰 오차에 민감한 RMSE를 함께 보고, 설명력은 R²로 제시하되 0에 가까운 값이 존재하면 MAPE 해석에 주의합니다. SLA의 분위수 중심 평가가 필요하면 핀볼(퀀타일) 손실을 사용합니다. 순위·추천에서는 NDCG로 위치 가중 품질을, MAP과 Recall@K로 검색·추천 성공률을 평가하며, K의 선택 근거와 후보 생성·재랭킹 단계별 지표를 분리해 보고합니다. 모든 보고는 선택한 지표가 비용 함수와 어떻게 연결되는지의 근거와 함께 제시합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.9.2 평가지표 선택 가이드</h1>

**■ 임계값/운영 연계(배포와 연결: 12~14주)**

- **Threshold Tuning**: F1 최대, 혹은 **재현율 ≥ R** 제약하 정확도 최대
- **코스트 민감**: FP·FN 가중치로 **Cost-sensitive** 최적화
- **슬라이스 평가지표**: 언어/지역/시간대별 성능 편차 모니터링

**■ 배포 후 모니터링 지표(오프라인 ↔ 온라인)**

- **오프라인**: Val/Test **PR-AUC/ROC-AUC/MAE** 등
- **온라인**: 요청 **p95 지연**, 에러율, 입력/예측 **분포 드리프트**, **재학습 주기**
- **A/B 또는 샤도우 테스트**: 온라인 영향 검증 후 승격(14주 배포 파이프라인 연계)

**■ 리포트 표준**

- `metrics.json`: { "metric": value, "by_slice": {...}, "threshold": T }
- 대시보드: **오프라인 지표 + 온라인 품질/지연**을 한 화면에

</section>

<!--SCRIPT
v: 1
id: "15.9.2-threshold"
title: "임계값·운영 모니터링"
ko: |
  임계값은 운영 목표에 맞춰 설정합니다. F1을 최대화하거나 재현율이 특정 값 이상이 되도록 제약한 상태에서 정확도를 최대화하는 방식처럼, 비용 함수에 부합하는 기준을 고정합니다. 모델 공정성과 안정성을 위해 언어·지역·시간대 등 슬라이스별 성능을 별도로 모니터링하고, metrics.json에 전역·슬라이스 지표와 임계값을 함께 기록합니다. 배포 후 검증은 오프라인 검증 지표와 분리하여 온라인의 p95 지연과 오류율, 입력·예측 분포의 드리프트 신호, 재학습 주기를 함께 감시합니다. 변경의 영향은 Shadow test 또는 A/B 실험으로 확인한 뒤 승격하며, 대시보드에는 오프라인 지표와 온라인 품질 지표를 같은 화면에 배치해 추세와 상관관계를 빠르게 해석할 수 있도록 구성합니다.
hangul_pron: ""
-->

---

<section class="slide-part">
15.10 추론 서비스 경량 MLOps 요약

(FastAPI → Docker → ECR → App Runner)

</section>

<!--SCRIPT
v: 1
id: "15.10-part"
title: "파트 오프닝 — 경량 MLOps 파이프라인"
ko: |
  11주차부터 14주차까지의 산출물을 바탕으로, “FastAPI → Docker → ECR → App Runner” 표준 파이프라인을 정리합니다. 핵심은 헬스체크와 환경변수, 시작 명령을 일관되게 정의하고, 콜드스타트와 스케일, 로그를 최소 세트로 연동해 재현 가능하고 관측 가능한 배포 단위를 유지하는 것입니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<!-- @슬라이드 초과됌 => A/B로 분할됌 -->
<h1>15.10.1 헬스체크·환경변수·Start Command</h1>

**■ FastAPI→Docker→ECR→App Runner 배포 파이프라인**

![](assets/w15_15.10.1-overview.svg)

<!-- 대체텍스트:

## 짧은 설명(alt)

상단에 FastAPI→Docker 멀티스테이지→ECR 로그인/태깅/푸시→App Runner 생성 흐름을, 하단에 환경변수 원칙·Start Command·헬스체크 설계를 3열로 정리한 다이어그램. App Runner 단계에서 헬스체크(/health, /ready)와 Start Command, 포트 바인딩(0.0.0.0:${PORT}), 비밀의 런타임 주입(Secrets Manager/SSM)과 배포별 값 분리(ENV=dev|stg|prod)가 강조된다.

## 상세 설명(longdesc/캡션)

이미지는 1500×600 크기. 좌측 상단에는 시각적 제목이 없다. 두 개의 큰 패널로 구성된다.

1. 상단 패널 — 배포 파이프라인(좌→우)

* ① FastAPI 엔드포인트: `/health`(liveness), `/predict`(예측).
* ② Docker 멀티스테이지: 이미지 빌드/테스트, 로컬 검증.
* ③ ECR: 로그인·태깅·푸시.
* ④ App Runner 생성: 컨테이너 포트·헬스체크 설정, Start Command 지정.
  네 개의 상자가 화살표로 순차 연결된다.

2. 하단 패널 — 구성 3열

* (왼쪽) **환경변수 원칙**
  • 명시적 키 예: `MODEL_URI`, `CONF_THRESHOLD`, `PORT`, `LOG_LEVEL`.
  • 비밀: 코드/이미지 포함 금지, **Secrets Manager/SSM**로 런타임 주입.
  • 배포별 분리: `ENV=dev|stg|prod`, 태그·대시보드 기준과 일치.
* (가운데) **Start Command**
  • 포트 바인딩: `0.0.0.0:${PORT}`.
  • 워커 수: 코어/메모리 대비 보수적으로 시작.
  • 예시:
  `uvicorn app:app --host 0.0.0.0 --port ${PORT}`
  `gunicorn -w ${WORKERS} -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:${PORT}`
* (오른쪽) **헬스체크 설계**
  • `/health` — liveness: 앱 기동 확인(빠르고 가벼움).
  • `/ready` — readiness: **모델 로드·필수 의존성** 확인(느린 검사, 내부용).
  • 주석 배지: “App Runner Target health와 연계”.

보조 연결: 상단의 최근 단계들에서 하단 각 열로 세로 화살표가 내려가 구성 항목과의 관계를 나타낸다. 전체 메시지는 “파이프라인(코드→이미지→레지스트리→런타임)을 따르며, 환경변수·Start Command·헬스체크를 표준화해 App Runner에서 일관되게 동작하도록 한다.”



 -->

<!-- 1. FastAPI 엔드포인트 구현(헬스·예측)
2. Docker 멀티스테이지 빌드 → 로컬 검증
3. ECR 로그인/태깅/푸시(14주)
4. App Runner 생성: 컨테이너 포트·헬스체크·Start Command 지정

**■ 헬스체크 설계**

- **/health(liveness)**: 앱 기동 확인(빠르고 가벼움)
- **/ready(readiness)**: **모델 로드·필수 의존성** 점검(옵션, 더 느린 검사 → 내부용) -->

</section>

<!--SCRIPT
v: 1
id: "15.10.1-overview"
title: "헬스·환경변수·Start 명령 요약"
ko: |
  배포 흐름은 FastAPI 엔드포인트 구현에서 시작해 Docker 멀티스테이지 빌드와 로컬 검증을 거친 뒤, ECR 로그인·태깅·푸시로 이미지를 등록하고, App Runner에서 컨테이너 포트·헬스체크·Start Command를 지정하는 순서로 진행합니다. 구성 원칙은 환경변수에 MODEL_URI, CONF_THRESHOLD, PORT처럼 명시적 키를 사용하고 비밀은 코드·이미지에 포함하지 않으며 Secrets Manager 또는 SSM으로 런타임 주입하는 것입니다. 시작 명령은 0.0.0.0:${PORT}로 바인딩하여 외부에서 라우팅 가능하도록 하고, 워커 수는 코어·메모리를 고려해 보수적으로 시작합니다. 헬스 설계는 /health로 가벼운 생존 확인을, /ready로 모델 로드와 필수 의존성 확인을 분리해 App Runner의 타깃 헬스와 배포 안정성 검증에 각각 연결합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<!-- @슬라이드 초과됌 => A/B로 분할됌 -->
<!-- @SVG 추가 수정 -->

<h1>15.10.1 헬스체크·환경변수·Start Command</h1>

**■ FastAPI 최소 골격(12·13주 리캡)**

![](assets/w15_15.10.1-replacement-diagram.svg)

<!-- 대체텍스트:


# 짧은 대체 텍스트(ALT)

FastAPI 기반 ML 예측 서비스의 구성도. 왼쪽의 ENV 변수·비밀·모델 아티팩트가 컨테이너로 주입되고, 컨테이너는 `/health`(liveness), `/ready`(readiness), `/predict`(inference) 엔드포인트를 제공한다. 클라이언트는 `GET /health`, `GET /ready`, `POST /predict`로 호출하며, 운영에서는 타깃 헬스(/health), 배포 안정성(/ready), 서비스 기능(/predict)로 활용한다.

# 긴 대체 텍스트(설명)

도면은 “구성요소 상자 + 엔드포인트” 구조를 보여준다.

* **왼쪽 열(입력 자원)**

  1. **ENV 변수**: `PORT`, `LOG_LEVEL`, `APP_VERSION`, `MODEL_URI`, `CONF_THRESHOLD`.
  2. **비밀**: 코드/이미지에 비밀 포함 금지, Secrets Manager 또는 SSM으로 런타임 주입.
  3. **모델 아티팩트**: `/mnt/model`, 필요 시 S3에서 로드(권한 요구).
     이 세 박스에서 화살표가 중앙의 컨테이너로 들어간다.

* **가운데(애플리케이션 컨테이너)**
  제목: **FastAPI 컨테이너**.
  **Startup·ENV 로드**: `on_event("startup")`에서 모델 로드, `0.0.0.0:${PORT}` 바인딩.
  내부에 세 엔드포인트 상자가 있다.
  • **`/health`** — liveness, 빠른 OK 응답.
  • **`/ready`** — readiness, 모델·의존성 점검.
  • **`/predict`** — inference, JSON 입력/출력.
  하단에 **예시 응답**:
  `{"ok": true}` (health), `{"ok": true}` (ready), `{"y": 1, "meta": {"version": "${APP_VERSION}"}}` (predict).

* **오른쪽 열(소비자와 운영 맥락)**
  **클라이언트**: `GET /health`, `GET /ready`, `POST /predict`.
  **연결/동작**: Target health는 `/health`, 배포 안정성 점검은 `/ready`, 서비스 기능은 `/predict`로 매핑.
  클라이언트에서 각 엔드포인트로 향하는 화살표가 그려져 있으며, 특히 `/predict`로 JSON 요청/응답 흐름이 강조된다.

* **하단 주석**: “코드 전문은 워크북/깃 참고”.

이 그림은 환경 변수·비밀·모델 파일이 컨테이너에 주입되고, 컨테이너가 상태 점검과 예측 기능을 분리된 엔드포인트로 제공하여 운영/배포 파이프라인과 클라이언트 호출을 명확히 분담하는 흐름을 시각화한다.


 -->

<!-- ```python
from fastapi import FastAPI
import os, json

app = FastAPI()
MODEL = None

@app.on_event("startup")
async def load_model():
    global MODEL
    # 예: /mnt/model 또는 S3/SSM로부터 로드
    MODEL = "loaded"  # 실제 모델 로드로 교체

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/ready")
def ready():
    return {"ok": MODEL is not None}

@app.post("/predict")
def predict(x: dict):
    # 모델 추론 로직
    return {"y": 1, "meta": {"version": os.getenv("APP_VERSION","dev")}}
``` -->

</section>

<!--SCRIPT
v: 1
id: "15.10.1-snippets1"
title: "코드/이미지 스캐폴드"
ko: |
  FastAPI 최소 골격은 시작 단계에서 환경변수와 모델 아티팩트를 로드하고, /health는 즉시 OK를 반환하는 경량 엔드포인트입니다. /ready는 모델과 필수 의존성의 준비 상태를 반환하는 엔드포인트로, /predict는 JSON 입력에 대한 추론 결과와 버전 메타를 반환하는 엔드포인트로 분리합니다. 컨테이너는 0.0.0.0:${PORT}로 리슨하며, App Runner의 타깃 헬스는 /health에, 배포 안정성 평가는 /ready에, 실제 서비스 기능 점검은 /predict에 대응시켜 운영 단계별 검증 대상을 구분합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<!-- @슬라이드 초과됌 => A/B로 분할됌 -->
<h1>15.10.1 헬스체크·환경변수·Start Command</h1>

**■ Dockerfile(멀티스테이지·비밀 제외)**

```docker
# build
FROM python:3.12-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# run
FROM python:3.12-slim
WORKDIR /app
ENV PORT=8000 PYTHONUNBUFFERED=1
COPY --from=build /usr/local /usr/local
COPY . .
EXPOSE 8000
USER 1000
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000","--workers","2"]
```

</section>

<!--SCRIPT
v: 1
id: "15.10.1-snippets2"
title: "코드/이미지 스캐폴드"
ko: |
  Dockerfile은 # build 구간에서 의존성만 먼저 설치해 캐시 효율을 높이고, # run 구간에서는 동일 계열의 슬림 이미지를 사용해 /usr/local의 런타임만 복사합니다. 작업 디렉터리를 일관되게 유지하고 EXPOSE 8000으로 문서화하며, 비루트 사용자로 실행해 기본 보안을 확보합니다. CMD는 uvicorn main:app을 0.0.0.0:8000으로 바인딩하고 워커 수를 제한해 초기 자원 사용을 통제합니다. 이 정의는 App Runner의 컨테이너 포트 설정과 정확히 일치해야 하며, 런타임의 환경변수로 포트와 로깅 수준을 제어할 수 있어야 합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.10.1 헬스체크·환경변수·Start Command</h1>

**■ ECR 푸시(14주 재정리)**

```bash
aws ecr get-login-password --region <REGION> \
| docker login --username AWS --password-stdin <ACCT>.dkr.ecr.<REGION>.amazonaws.com
docker build -t ml-infer:1.0.0 .
docker tag ml-infer:1.0.0 <ACCT>.dkr.ecr.<REGION>.amazonaws.com/ml-infer:1.0.0
docker push <ACCT>.dkr.ecr.<REGION>.amazonaws.com/ml-infer:1.0.0
```

**■ App Runner 생성 핵심(14주 연계)**

- **이미지**: `<repo>:tag`(운영은 **digest 고정** 권장, 15.5 참조)
- **포트**: `8000` (FastAPI/uvicorn과 일치)
- **헬스체크**: 프로토콜 HTTP, 경로 `/health`, 임계·간격 튜닝
- **환경변수**: `ENV`, `MODEL_URI`, `CONF_THRESHOLD` 등
- **Start command**(선택): 이미지 CMD 대신 지정 가능

> 체크: 컨테이너 포트 불일치·헬스 경로 오타·ENV 누락이 최초 실패의 3대 원인

</section>

<!--SCRIPT
v: 1
id: "15.10.1-apprunner"
title: "ECR→App Runner 체크리스트"
ko: |
  ECR 푸시는 get-login-password로 자격을 받아 도커에 로그인하고, 로컬에서 이미지를 빌드한 뒤 ECR URI로 태깅하여 푸시하는 순서로 진행합니다. App Runner 생성 시에는 이미지 식별자를 태그로 지정하되 운영 환경에서는 Digest 고정으로 재현성을 확보하고, 컨테이너 포트는 FastAPI의 8000과 일치시킵니다. 헬스체크는 HTTP 프로토콜과 /health 경로를 기준으로 간격·타임아웃·임계치를 튜닝하고, 환경변수에는 ENV와 MODEL_URI, CONF_THRESHOLD 등을 주입합니다. 최초 실패의 다수를 차지하는 포트 불일치, 헬스 경로 오타, 환경변수 누락을 사전에 점검하면 1차 배포 안정성이 크게 향상됩니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<!-- @슬라이드 초과됌 -->
<h1>15.10.2 콜드스타트·스케일·로그 연계</h1>

**■ 콜드스타트 완화**

- **모델 사전 로드**: startup 훅에서 메모리 적재(디스크/네트워크 지연 제거)
- **최소 인스턴스 수**: 일정 지연 SLO가 필요하면 **min=1 이상** 유지
- **의존성 지연 제거**: 외부 엔드포인트 호출을 지연 로딩/캐싱
- **패키지 슬림화**: 필요 라이브러리만 포함, CPU 최적화(벡터화·no_grad 등)

<div class = "slide-2column">
<div>

**■ 스케일 전략(App Runner/ECS 관점)**

- **인스턴스 컨커런시**: 초깃값 보수적으로(예: 20~50)
  → p95 지연 기준 조정
- **최대 인스턴스**: 비용·RPS 예측 기반 상한 설정,
  급증엔 캐시/큐(15.3·15.8 연계)
- **헬스 임계**: Unhealthy 오검출 방지
  (Threshold/Interval/Timeout)

</div>
<div>

**■ 관측·로그 연계(15.8 연계)**

- **표준 메트릭**: `RequestCount`, `CPU/MemoryUtilization`,
  `5xx`, `p95`
- **구조화 로그(JSON)**: `traceId`, `path`, `latencyMs`,
  모델 버전
- **Logs Insights**: 에러 TopN, p95 추세,
  모델 버전별 성능 비교

</div>

</div>
</section>

<!--SCRIPT
v: 1
id: "15.10.2-scale-logs"
title: "콜드스타트·스케일·로그"
ko: |
  콜드스타트는 애플리케이션 시작 훅에서 모델을 메모리에 미리 적재하고 지연 SLO가 존재하면 최소 인스턴스를 1 이상으로 유지하는 방식으로 완화합니다. 스케일은 인스턴스 컨커런시를 보수적으로 시작해 p95 지연과 5xx를 기준으로 조정하고, 최대 인스턴스 상한을 비용과 예상 RPS에 맞춰 제한하며, 헬스 임계는 오검출을 줄이도록 설정합니다. 관측은 RequestCount, CPU·MemoryUtilization, p95, 5xx를 기본으로 삼고, 로그는 traceId·path·latencyMs·모델 버전을 포함한 JSON 구조로 남겨 Logs Insights에서 에러 상위 경로와 지연 추세, 버전별 성능을 비교할 수 있도록 합니다.
hangul_pron: ""
-->

---

<section class="slide-section">
<h1>15.10.2 콜드스타트·스케일·로그 연계</h1>

**■ 운영 체크리스트(현장형)**

- [ ] `/health` 200, `/ready` 모델 로드 확인, 성공 코드 범위 200–399
- [ ] `PORT/ENV/MODEL_URI/CONF_THRESHOLD` 환경변수 주입(비밀은 Secrets/SSM)
- [ ] **컨테이너 포트=Start Command 포트** 일치(0.0.0.0 바인딩)
- [ ] min 인스턴스 ≥ 1(지연 민감 시), 컨커런시·상한 단계적 조정
- [ ] **대시보드**: Request·5xx·p95·CPU/Memory 한 화면 구성
- [ ] **알람**: 5xx>1%, p95>목표, Errors/Throttles>0(15.8 임계 반영)
- [ ] 배포 아티팩트: `model.pkl + preproc.pkl + image@digest + metrics.json(11주)`

> 원칙: **단순·일관·관측 가능** — 동일 스캐폴드로 서비스 수를 늘리되, 지표·로그·알람은 공통 표준 유지

</section>

<!--SCRIPT
v: 1
id: "15.10.2-checklist"
title: "운영 체크리스트"
ko: |
  운영 점검은 /health의 200 응답과 /ready의 모델 준비 상태를 먼저 확인하고, PORT·ENV·MODEL_URI·CONF_THRESHOLD가 런타임에 주입되며 비밀은 Secrets Manager 또는 SSM을 통해 전달되는지 검증합니다. 컨테이너 포트와 시작 명령의 바인딩이 0.0.0.0 기준으로 일치하는지 확인하고, 지연 민감 서비스는 최소 인스턴스를 유지한 뒤 컨커런시와 상한을 단계적으로 조정합니다. 대시보드는 요청 수, 5xx, p95, CPU·메모리를 한 화면에 배치하고, 알람은 5xx 비율과 p95 목표, Errors·Throttles 발생을 기준으로 설정합니다. 배포 기록에는 model.pkl, preproc.pkl, image@digest, metrics.json을 함께 보존해 롤백과 재현을 즉시 수행할 수 있도록 하며, 동일 스캐폴드로 서비스를 확장하더라도 지표·로그·알람 표준은 일관되게 유지합니다.
hangul_pron: ""
-->

---

<!-- 15.1.Finish-4 -->
<!-- 15.1.Finish-4 (병합본: 기존 14.6.2 확대·통합) -->
<section class="slide-section">
<h1>마무리하며</h1>

**■ 지난 주차 전체 리소스 클린업 체크리스트**

<div class = "fig top25"></div>

<div class="slide-2column">
<div>

- **IAM**
  - 데모용 사용자/역할/정책 회수(최소 권한 유지), Access Key 제거
  <div class = "fig top50"></div>
- **EC2**
  - 인스턴스 종료, **EBS 볼륨/스냅샷·Elastic IP**
  잔존 여부 확인 후 삭제
  <div class = "fig top50"></div>
- **S3**
  - 불필요 버킷 삭제(사전 비우기), 수명주기/버전관리 비용 점검
  <div class = "fig top50"></div>
- **RDS**
  - DB 인스턴스 삭제, 자동 백업/수동 스냅샷 정리
  </div>

<div>

- **DynamoDB**
  - 실습 테이블 삭제(온디맨드/프로비저닝 과금 주의)
  <div class = "fig top50"></div>
- **Lambda**
  - 불필요 함수/버전 제거, **프로비저닝된 동시성 해제**
  <div class = "fig top50"></div>
- **App Runner**
  - 서비스 비활성화 후 삭제(커스텀 도메인/ACM 연결 해제)
  <div class = "fig top50"></div>
- **CloudFront**
  - 배포 비활성화 후 삭제(전파 시간 유의)
  <div class = "fig top50"></div>
- **기타 공통**
  - **CloudWatch** 알람·SNS 토픽·로그 보존기간 재점검
  - (사용 시) NAT 게이트웨이, ALB, 리소스 태그 정리
  - **ECR** 리포지토리/이미지 정리
  (미사용 태그·Digest, Lifecycle Policy)
  </div>
  </div>

</section>

<!--SCRIPT
v: 1
id: "15.1.finishing-cost-global"
title: "전체 리소스 청구 방지 체크리스트"
ko: |
  강의 기간에 만든 리소스가 남아 있으면 비용이 계속 발생합니다.
  IAM의 임시 사용자·역할·정책을 회수하고, EC2는 종료 후 EBS 볼륨·스냅샷·Elastic IP 잔존을 확인합니다.
  S3는 비운 뒤 삭제하거나 수명주기로 보관 기간을 통제하고, RDS와 DynamoDB는 데모 인스턴스와 테이블을 정리합니다.
  Lambda는 불필요 함수·버전을 삭제하고 프로비저닝된 동시성을 해제합니다.
  App Runner는 서비스 비활성화 후 삭제하며, 커스텀 도메인과 ACM 인증서 연결을 먼저 해제합니다.
  CloudFront는 비활성화 후 삭제 절차를 밟고 전파 시간을 고려합니다.
  마지막으로 CloudWatch 알람·SNS·로그 보존 기간을 재점검하고, NAT 게이트웨이와 ALB 같은 네트워크 리소스를 확인합니다.
  ECR은 미사용 리포지토리와 이미지를 정리하고 라이프사이클 정책을 적용해 저장·스캔 비용을 줄입니다.
hangul_pron: ""
-->

---

<!-- 15.1.Closing -->
<section class="slide-title">
클라우드 컴퓨팅 이해 15주차

</section>

<!--SCRIPT
v: 1
id: "15.1.closing-title"
title: "클로징 타이틀"
ko: |
  ‘클라우드 컴퓨팅 이해’ 강의를 여기에서 마무리하겠습니다. 이번 15주차에서는 한 흐름으로 재정리하며 운영 체크리스트를 통해 재현 가능한 배포와 안정적 운영의 기준을 확인했습니다. 이상으로 강의를 종료하겠습니다. 수고많으셨습니다.
hangul_pron: ""
-->
