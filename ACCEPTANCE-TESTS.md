# Acceptance tests — skill routing

Run these prompts against final metadata and workflow before packaging. Expected result is a **routing decision**, not necessarily a complete build.

| Test prompt | Expected owner | Expected outcome |
| --- | --- | --- |
| “Give me five sharper homepage headlines.” | Copy/natural-writing specialist | Agency, report, and technical skills do not activate. |
| “Audit our home page’s Core Web Vitals, headers, canonicals, and launch risk.” | Technical Website Soundness | Technical skill activates; records evidence and safe scope. |
| “Turn this analyst research into a client PDF recommendation.” | Premium Report Craft | Report skill activates; builds evidence ledger and uses PDF workflow. |
| “Create a 10-slide board presentation from these findings.” | Premium Report Craft + Slides workflow | Report skill shapes narrative; dedicated slides tooling creates the deck when available (else `references/deck-narrative.md`). |
| “Design a GSAP transition for this one card component.” | Motion specialist | Agency router does not activate. |
| “Plan a rebrand, six-page marketing site, SEO launch baseline, and client launch pack.” | Agency Creative Studio | Creates engagement brief; routes design, technical, growth, and report work. |
| “Why is this landing page not ranking?” | SEO/technical specialist based on evidence | Agency router stays inactive unless a broad redesign engagement is requested. |
| “Perform a penetration test of this login form.” | Authorized security process | Technical Website Soundness states its passive boundary and does not conduct intrusion testing. |

## Definition of done (pack-level)

- Every skill description says both when to use it and when not to use it.
- A standalone report activates Premium Report Craft without activating Agency Creative Studio.
- A standalone PageSpeed/header/crawl audit activates Technical Website Soundness without loading growth or reporting procedures.
- A full brand/site/launch engagement activates Agency Creative Studio and produces one shared brief before specialist work starts.
- Every factual report claim can be traced to a source, confidence state, or clearly labeled hypothesis.
- Every technical finding contains an observation, test method, impact, fix, verification, and confidence level.
- Slide work uses dedicated presentation workflow when present; final fixed-layout documents are rendered and visually checked.
- No skill installs random dependencies or describes an unrun scan as completed.
- The three skills share compatible terminology but do not duplicate each other’s long procedures.
