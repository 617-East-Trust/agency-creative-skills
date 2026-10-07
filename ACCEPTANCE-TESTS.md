# Acceptance tests — skill routing

Run these prompts against final metadata and workflow before packaging. Expected result is a **routing decision**, not necessarily a complete build.

| Test prompt | Expected owner | Expected outcome |
| --- | --- | --- |
| “Give me five sharper homepage headlines.” | Copy/natural-writing specialist | Agency, report, technical, and GSC skills do not activate. |
| “Audit our home page’s Core Web Vitals, headers, canonicals, and launch risk.” | Technical Website Soundness | Technical skill activates; records evidence and safe scope. |
| “Why is this landing page slow on mobile?” | Technical Website Soundness | Collects/uses live PageSpeed/CrUX and production evidence; GSC may provide impact context only. |
| “Here is a GSC export—why did organic clicks drop over the last 28 days?” | GSC Growth Operator | Validates dates/freshness and filters; compares equal windows; returns an evidence-backed recovery queue. |
| “Why is https://example.com/pricing not indexed? Here is the URL Inspection result.” | GSC Growth Operator | Builds an indexing evidence record; requests Technical Website Soundness handoff for live header/robots/canonical/deploy proof if not supplied. |
| “Why is this landing page not ranking?” | GSC Growth Operator when GSC performance or indexation evidence is requested; otherwise clarify data scope | Never routes generically. Technical Website Soundness owns live headers/CWV; GSC owns property data and URL Inspection diagnosis. |
| “Create a monthly organic-search client report from this verified GSC analysis.” | Premium Report Craft, receiving GSC input | Formats the evidence and decision narrative without rerunning the analysis. |
| “Turn this analyst research into a client PDF recommendation.” | Premium Report Craft | Report skill activates; builds evidence ledger and uses PDF workflow. |
| “Create a 10-slide board presentation from these findings.” | Premium Report Craft + Slides workflow | Report skill shapes narrative; dedicated slides tooling creates the deck when available (else `references/deck-narrative.md`). |
| “Design a GSAP transition for this one card component.” | Motion specialist | Agency router does not activate. |
| “Plan a rebrand, six-page marketing site, SEO launch baseline, and client launch pack.” | Agency Creative Studio | Creates engagement brief; routes creative, GSC, technical, and report work by boundary. |
| “Perform a penetration test of this login form.” | Authorized security process | Technical Website Soundness states its passive boundary and does not conduct intrusion testing. |

## Definition of done (pack-level)

- Every skill description says both when to use it and when not to use it.
- A standalone report activates Premium Report Craft without activating Agency Creative Studio.
- A standalone GSC performance/indexing request activates GSC Growth Operator without rerunning production technical checks.
- A standalone PageSpeed/header/crawl audit activates Technical Website Soundness without loading GSC analysis or reporting procedures.
- A full brand/site/launch engagement activates Agency Creative Studio and produces one shared brief before specialist work starts.
- Premium Report Craft accepts verified GSC and Technical Website Soundness inputs without rerunning either analysis.
- Every factual report claim can be traced to a source, confidence state, or clearly labeled hypothesis.
- Every technical finding contains an observation, test method, impact, fix, verification, and confidence level.
- Slide work uses dedicated presentation workflow when present; final fixed-layout documents are rendered and visually checked.
- No skill installs random dependencies or describes an unrun scan as completed.
- The four skills share compatible terminology but do not duplicate each other’s long procedures.
