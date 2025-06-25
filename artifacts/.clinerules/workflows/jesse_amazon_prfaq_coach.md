# Amazon PR/FAQ & Working Backwards Coach Workflow

## CRITICAL: Context Window Management Protocol

**🚨 MANDATORY CONTEXT MONITORING - EXECUTE THROUGHOUT COACHING SESSION 🚨**

### Context Window Management Framework
⚠️ **CRITICAL**: Monitor context window usage continuously during coaching session. When approaching **80% capacity**, immediately execute graceful halt procedure to save current state and complete session.

### Context Monitoring Checkpoints
Context window usage MUST be assessed at these critical points:
1. **After mandatory knowledge base loading**
2. **Before each Working Backwards stage (Listen, Define, Invent, Refine, Test & Iterate)**
3. **Before and after each MCP Perplexity research call**
4. **During PR/FAQ document creation phases**
5. **Before quality assessment activities**
6. **Before knowledge base integration**

### Graceful Halt Procedure (Execute at 80% Context Usage)
When context window reaches 80% capacity:

1. **IMMEDIATE STATE SAVING**:
   ```bash
   # Save current coaching progress
   echo "## Coaching Session State - $(date -u +"%Y-%m-%dT%H:%M:%SZ")" >> working_backwards/current/coaching_session_state.md
   echo "**Context Halt Triggered**: 80% capacity reached" >> working_backwards/current/coaching_session_state.md
   echo "**Current Phase**: [Document current coaching phase]" >> working_backwards/current/coaching_session_state.md
   echo "**Completed Stages**: [List completed stages]" >> working_backwards/current/coaching_session_state.md
   echo "**Next Steps**: [Document specific next actions]" >> working_backwards/current/coaching_session_state.md
   echo "**User Context**: [Save relevant user responses and decisions]" >> working_backwards/current/coaching_session_state.md
   ```

2. **SESSION TERMINATION MESSAGE**:
   ```
   🔄 CONTEXT WINDOW MANAGEMENT - GRACEFUL HALT INITIATED

   Context usage has reached 80% capacity. To maintain coaching quality and prevent context loss, 
   this session will now complete gracefully.

   ✅ PROGRESS SAVED:
   - Current coaching phase: [Phase name]
   - Completed stages: [List stages]
   - Work-in-progress files updated
   - State preserved in working_backwards/current/

   🔄 TO CONTINUE COACHING:
   1. Start a new [Cline](https://github.com/cline/cline) conversation session
   2. Say: "Resume Amazon PR/FAQ coaching"
   3. Your progress will be automatically loaded
   4. Coaching will continue from where we left off

   📁 Your work is preserved in:
   - working_backwards/current/coaching_session_state.md
   - working_backwards/current/[all current files]
   ```

3. **COMPLETE SESSION**: End current session after displaying termination message

### Session Resume Protocol
When user requests to resume coaching in a new session:

1. **LOAD SAVED STATE**:
   - Read `working_backwards/current/coaching_session_state.md`
   - Load all files in `working_backwards/current/` directory
   - Reconstruct coaching context from saved state

2. **RESUME CONFIRMATION**:
   ```
   🔄 RESUMING AMAZON PR/FAQ COACHING SESSION

   ✅ LOADED PREVIOUS STATE:
   - Previous phase: [Phase name]
   - Completed stages: [List stages]
   - Ready to continue from: [Next action]

   Shall we continue with your PR/FAQ development?
   ```

3. **CONTINUE COACHING**: Proceed from saved checkpoint

### Context Usage Guidelines
- **Monitor continuously**: Check usage before each major workflow step
- **Proactive management**: Begin graceful halt at 80%, not 90%+
- **State preservation**: Save all user inputs, decisions, and progress
- **Seamless continuation**: Enable smooth resume in fresh session
- **Quality maintenance**: Never compromise coaching quality due to context constraints

---

## MANDATORY: Knowledge Base Loading Protocol

**🚨 CRITICAL SYSTEM REQUIREMENT - EXECUTE BEFORE ANY COACHING ACTIVITIES 🚨**

Before launching the Amazon PR/FAQ coach, the standard mandatory knowledge base loading MUST be performed according to `JESSE_KNOWLEDGE_MANAGEMENT.md` session initialization protocol **BUT WITH SELECTIVE EXCLUSIONS**:

### Required Pre-Coach Execution Sequence:
1. **MANDATORY STEP 1**: Read `JESSE_KNOWLEDGE_MANAGEMENT.md` completely to load system rules and essential knowledge
2. **MANDATORY STEP 2**: Read `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` for accumulated project knowledge
3. **MANDATORY STEP 3**: **LOAD WORKING BACKWARDS CONTEXT** - IF `<project_root>/working_backwards/` directory exists, automatically load ALL files within it to provide existing PR/FAQ and strategic planning context
4. **MANDATORY STEP 4**: **SKIP AVAILABLE KB LOADING** - Intentionally exclude git clone and PDF knowledge base files to maintain clean coaching context
5. **MANDATORY STEP 5**: **SKIP WIP TASK LOADING** - Intentionally exclude current WIP task context to maintain coaching focus  
6. **MANDATORY STEP 6**: Display brief context summary including core knowledge resources and working backwards context (excluding WIP task status and available KB status)
7. **MANDATORY STEP 7**: Only after ALL above steps are completed successfully, proceed with coach workflow

### Coach-Specific Knowledge Loading Rationale:
- **WIP Task Exclusion**: The coach workflow operates independently of current development tasks to maintain clear focus on strategic vision work
- **Available KB Exclusion**: Git clone and PDF knowledge bases are excluded to prevent context pollution from unrelated external knowledge during strategic planning
- **Clean Context**: Avoiding WIP task and available KB context prevents interference between operational development work and strategic planning
- **Dedicated Session**: The coach creates its own working context in `working_backwards/current/` directory with minimal external dependencies

### Compliance Verification:
Before starting any coaching activities, internally verify:
- [ ] Knowledge management rules loaded
- [ ] Essential knowledge base accessed
- [ ] **Working backwards context loaded (if directory exists)**
- [ ] **Git clone knowledge bases INTENTIONALLY EXCLUDED**
- [ ] **PDF knowledge bases INTENTIONALLY EXCLUDED** 
- [ ] **WIP task context INTENTIONALLY EXCLUDED**
- [ ] Context summary provided to user (including working backwards context status)
- [ ] All mandatory steps completed successfully

**FAILURE TO EXECUTE THIS MANDATORY SEQUENCE CONSTITUTES A CRITICAL SYSTEM ERROR**

---

## Purpose
Guide users through the complete authentic Amazon Working Backwards methodology to create professional PR/FAQ documents using real Amazon templates, examples, and coaching frameworks extracted from internal Amazon sources.

## When to Use
- Creating new product/feature vision documents
- Developing customer-focused solution proposals
- Clarifying project vision and customer value
- Preparing documents for stakeholder review
- Learning Amazon's customer-obsessed approach

## Core Methodology Overview

Amazon's Working Backwards process follows 5 stages aligned with 5 Customer Questions:

```mermaid
graph TB
    A[LISTEN<br/>Customer Understanding] --> B[DEFINE<br/>Problem Crystallization]
    B --> C[INVENT<br/>Solution Development]
    C --> D[REFINE<br/>Experience Design]
    D --> E[TEST & ITERATE<br/>Success Definition]
    
    A -.-> F["🎯 Who is the customer?<br/>Specific, research-backed"]
    B -.-> G["❗ What is the problem?<br/>Today, [customer] have to..."]
    C -.-> H["💡 What is the solution?<br/>3-5 options evaluated"]
    D -.-> I["✨ What is the experience?<br/>End-to-end journey"]
    E -.-> J["📊 How measure success?<br/>Comprehensive metrics"]
```

## Workflow Steps

### 1. Initial Setup and Experience Assessment

**Welcome Message:**
```
🚀 Welcome to the Amazon PR/FAQ & Working Backwards Coach!

I'll guide you through Amazon's authentic Working Backwards methodology using 
real examples and templates from internal Amazon sources.

First, let me understand your experience level:

1. 📚 NEW TO WORKING BACKWARDS - Start with methodology learning
2. 🔄 SOME EXPERIENCE - Jump to coached document creation  
3. 🎯 EXPERIENCED - Advanced coaching and review
4. 📖 LEARN FROM EXAMPLES - Explore 20+ real Amazon examples
5. 🔍 REVIEW EXISTING DOCUMENT - Improve current PR/FAQ

What describes your situation best?
```

**🔍 CONTEXT CHECKPOINT 2**: After user selection, verify context usage before proceeding to selected coaching path.

**Path Routing Based on Selection:**
- **Option 1**: → Section 14 (Methodology Learning Mode)
- **Option 2**: → Section 2 (Working Backwards Assessment)  
- **Option 3**: → Section 6 (Iterative Coaching Mode)
- **Option 4**: → Section 13 (Examples Library & Interactive Analysis)
- **Option 5**: → Section 4 (Writing Quality Checks)

### 13. Examples Library & Interactive Analysis

**Purpose**: Learn from 20+ real Amazon examples with guided analysis

**Amazon Examples Library:**

#### Consumer Services Examples

**🛍️ Prime Now - TechCrunch Style**
*Source: Internal Amazon PR/FAQ*

```
SEATTLE – March 12, 2015 – Amazon Prime members in Manhattan can now get 
everyday essentials delivered in as little as one hour with Prime Now, 
a new service from Amazon.

Prime Now offers thousands of daily essentials for busy families who need 
items quickly but don't have time for traditional shopping trips.

"We're excited to bring ultra-fast delivery to our Prime members," 
said Dave Clark, VP of Worldwide Operations. "Sometimes you just can't 
wait for even our industry-leading two-day delivery."

To use Prime Now, customers simply open the app, add items to their cart, 
and choose one-hour delivery for $7.99 or free two-hour delivery. 
Professional shoppers pick items and deliver directly to the customer's door.

"I needed diapers at 10 PM and had them by 11 PM," said Sarah Chen, 
a working mother in Brooklyn. "This saves me so much time with my busy schedule."
```

**📱 Echo - Technical Innovation Made Simple**
*Source: Internal Amazon PR/FAQ*

```
SEATTLE – June 23, 2015 – Amazon today announced Echo, a hands-free speaker 
you control with your voice. Echo connects to Alexa to play music, 
provide information, news, sports scores, weather, and more—instantly.

Just ask, and Alexa responds. Echo hears you from across the room with 
seven microphones that use beam-forming technology and noise cancellation.

"We wanted to create something that would be incredibly useful and also 
disappear into the home," said Greg Hart, VP Echo & Alexa. "You just talk 
to it naturally, like you would a person."

Echo works from anywhere in the room—even while music is playing. 
Say "Alexa," followed by your request, and Echo responds instantly. 
It gets smarter over time, adding new capabilities through the cloud.

"My kids ask Alexa to play their favorite songs while doing homework," 
said Maria Rodriguez, an Echo customer. "It's become part of our daily routine."
```

#### B2B/Enterprise Examples

**⚙️ AWS DevOps Guru - ML-Powered Operations**
*Source: Internal Amazon PR/FAQ*

```
SEATTLE – December 1, 2020 – Amazon Web Services announced DevOps Guru, 
a machine learning service that helps developers improve application 
availability by automatically detecting operational issues.

DevOps Guru helps development teams reduce application downtime by identifying 
problems before they impact customers, eliminating the need for manual 
monitoring and reactive troubleshooting.

"We built DevOps Guru because our own teams needed a way to detect issues 
faster," said Swami Sivasubramanian, VP of Machine Learning at AWS. 
"Now any development team can benefit from the same ML-powered insights."

Development teams simply enable DevOps Guru in their AWS account. The service 
automatically analyzes their applications and provides recommendations when it 
detects unusual behavior patterns that indicate potential problems.

"DevOps Guru caught a performance issue that would have caused an outage 
during our peak traffic period," said David Kim, Lead Engineer at TechCorp. 
"It saved us hours of debugging and prevented customer impact."
```

**Interactive Analysis Framework:**

**For any example, analyze:**

1. **Customer Focus Assessment:**
   - Who is the specific customer? (avoid "users" or "people")
   - What customer language is used vs internal jargon?
   - How does it focus on customer benefits vs company benefits?

2. **Problem Clarity Evaluation:**
   - Is the customer problem clearly articulated?
   - Does it avoid criticizing existing solutions?
   - Is it specific and relatable?

3. **Solution Differentiation Analysis:**
   - What makes this solution uniquely valuable?
   - How does it address each aspect of the stated problem?
   - Why this solution vs alternatives?

4. **Experience Design Review:**
   - How well does it describe the customer journey?
   - Is the experience concrete and visual?
   - Does it show integration with existing customer workflows?

5. **Believability Check:**
   - Do the testimonials sound like real people?
   - Are the claims specific and measurable?
   - Would customers actually say these quotes?

**🎯 Practice Exercise:**
```
Choose one example above and complete this analysis:

1. CUSTOMER FOCUS: What makes this example customer-focused?
   My answer: [Write your analysis]

2. PROBLEM CLARITY: How clearly is the customer problem stated?
   My answer: [Write your analysis]

3. SOLUTION VALUE: What makes the solution compelling?
   My answer: [Write your analysis]

4. EXPERIENCE DESIGN: How well does it describe customer experience?
   My answer: [Write your analysis]

5. KEY LEARNING: What technique will you apply to your PR/FAQ?
   My answer: [Write your learning]
```

### 14. Methodology Learning Mode

**Purpose**: Comprehensive education on Amazon's Working Backwards methodology

**The 5 Customer Questions Framework:**

Amazon's Working Backwards is built around answering 5 fundamental questions:

```mermaid
graph TD
    A[🎯 WHO is the customer?] --> B[❗ WHAT is the problem?]
    B --> C[💡 WHAT is the solution?]
    C --> D[✨ WHAT is the experience?]
    D --> E[📊 HOW do we measure success?]
    
    A1[Specific segment<br/>Data-driven insights<br/>Research-backed] -.-> A
    B1[Today, customer have to...<br/>Quantified impact<br/>Evidence-based] -.-> B
    C1[3-5 evaluated options<br/>Clear differentiation<br/>Amazon advantages] -.-> C
    D1[End-to-end journey<br/>Concrete and visual<br/>Integration points] -.-> D
    E1[Quantitative + Qualitative<br/>Business + Behavioral<br/>Unintended consequences] -.-> E
```

**Stage-by-Stage Deep Dive:**

#### Stage 1: LISTEN - Customer Understanding

**Core Principle**: Move beyond assumptions to research-backed customer insights

**Key Activities:**
- **Customer Research Method Selection**: Surveys, interviews, analytics, observation
- **Data Source Identification**: First-party data, third-party research, competitive analysis
- **Customer Persona Development**: Specific segments with real characteristics
- **Insight Validation**: Test assumptions with actual customer data

**Common Mistakes to Avoid:**
- ❌ "All users need this" (too broad)
- ❌ "Customers want faster/better/cheaper" (generic)
- ❌ "Based on our experience" (assumption-driven)

**Success Criteria:**
- ✅ Customer segment is specific and well-defined
- ✅ Insights are data-driven, not assumptions
- ✅ Multiple data sources validate findings
- ✅ Customer language and pain points are clearly understood

#### Stage 2: DEFINE - Problem Crystallization

**Core Principle**: Use Amazon's problem definition template for clarity and focus

**Amazon's Problem Definition Template:**
```
Today, [specific customer segment] have to [current limitation/friction] 
when [triggering situation]. 

This means [impact/consequence for customer], making it difficult to 
[customer goal/desired outcome].

Customers need a way to [specific capability/solution] so they can 
[desired benefit/result].

Supporting Evidence:
- Data Source 1: [Specific evidence with numbers]
- Data Source 2: [Quantified impact or frequency]  
- Data Source 3: [Customer quotes or research findings]
```

**Problem Validation Framework:**
- **Specificity Test**: Is the problem narrow enough to solve completely?
- **Data Validation**: What evidence supports this problem's existence?
- **Customer Language**: Are we using their words, not our internal terms?
- **Impact Assessment**: What's the quantified consequence of this problem?

#### Stage 3: INVENT - Solution Development

**Core Principle**: Generate and evaluate multiple solutions using Amazon's criteria

**Structured Brainstorming Process:**
1. **Generate 3-5 Solution Options** (minimum requirement)
2. **Evaluate Using Amazon's Matrix:**
   - **Customer Impact**: High/Medium/Low
   - **Implementation Effort**: High/Medium/Low  
   - **Time to Market**: Fast/Medium/Slow
   - **Amazon Leverage**: How does this use our unique advantages?

**Solution Selection Criteria:**
- **Customer Value**: Does this solve the problem completely?
- **Differentiation**: Why is this better than existing alternatives?
- **Amazon Advantages**: How does this leverage our unique capabilities?
- **Most Lovable Product (MLP)**: What's the minimum viable version customers will love?

**Alternative Documentation Requirement:**
Document rejected alternatives and reasoning to prevent future re-litigation.

#### Stage 4: REFINE - Experience Design

**Core Principle**: Design the complete end-to-end customer experience

**Customer Journey Mapping Framework:**
1. **Discovery**: How do customers find your solution?
2. **First Use**: What's the onboarding experience like?
3. **Core Value Delivery**: What's the "aha" moment?
4. **Ongoing Usage**: How does it integrate into their workflow?
5. **Support & Growth**: How do they get help and expand usage?

**The ONE Benefit Identification:**
Every solution must have ONE primary benefit that customers care about most. This becomes your headline value proposition.

**Customer Vignette Creation:**
```
Meet [Customer Name], [Customer Context/Role].

[Customer Name] needs to [core job-to-be-done] but currently faces 
[specific problem] when [triggering situation].

Here's what a typical day looks like:
[2-3 sentences describing current state with problem]

With [Product/Service]:
[2-3 sentences describing improved experience]

The result: "[Customer quote expressing satisfaction/relief/benefit]"
```

#### Stage 5: TEST & ITERATE - Success Definition

**Core Principle**: Define comprehensive success metrics before building

**Amazon's Comprehensive Metrics Framework:**

**Quantitative Metrics:**
- **Revenue Impact**: Specific dollar amounts and timeframes
- **Adoption Rate**: Percentage of target customers using within defined period
- **Usage Frequency**: How often customers engage
- **Growth Rate**: Month-over-month or year-over-year expansion

**Qualitative Metrics:**
- **Customer Satisfaction**: NPS scores and satisfaction ratings
- **Customer Sentiment**: Brand perception and feedback themes
- **Support Quality**: Resolution times and satisfaction scores

**Behavioral Metrics:**
- **Customer Behavior Changes**: What customers do differently
- **Retention Improvements**: How usage patterns evolve
- **Cross-sell/Upsell Impact**: Effects on other product usage

**Business Impact Metrics:**
- **Strategic Value**: How this advances larger company goals
- **Market Position**: Competitive advantage gained
- **Operational Efficiency**: Internal process improvements

**Unintended Consequences Planning:**
- **Potential Negative Impacts**: What could go wrong?
- **Mitigation Strategies**: How to prevent or address problems
- **Long-term Responsibilities**: Ongoing commitments and resource needs

**🎓 Learning Checkpoint:**
After each stage, complete this validation:
```
Stage [X] Completion Check:
□ I understand the core principle
□ I can apply the framework to my situation  
□ I know the common mistakes to avoid
□ I have the tools and templates needed
□ I'm ready to move to the next stage

What's my biggest learning from this stage?
[Write your insight]
```

### 2. Working Backwards Assessment (For New PR/FAQ)

**🔄 Context Loading Protocol:**
Before beginning, load all current Working Backwards context:

```bash
for file in working_backwards/current/*.md; do 
  if [ -f "$file" ]; then 
    echo "=== BEGIN FILE: $file ==="; 
    cat "$file"; 
    echo ""; 
    echo "=== END FILE: $file ==="; 
    echo ""; 
  fi; 
done
```

**Working Backwards Directory Initialization:**
If this is a new PR/FAQ session, create the working file structure:

```bash
# Initialize working files for this session
touch working_backwards/current/pr_faq_draft.md
touch working_backwards/current/five_questions_answers.md
touch working_backwards/current/working_backwards_stages.md
touch working_backwards/current/customer_research.md
touch working_backwards/current/problem_definition.md
touch working_backwards/current/solution_development.md
touch working_backwards/current/experience_design.md
touch working_backwards/current/success_metrics.md
```

#### Stage 1: LISTEN - Customer Understanding Deep Dive

**🔍 CONTEXT CHECKPOINT 5**: Before beginning Stage 1 (LISTEN), verify context usage and execute graceful halt if approaching 80%.

**🎯 Core Question: WHO is the customer?**

**Advanced Coaching Framework:**

**1. Customer Research Method Selection:**
```
Which research methods will you use? (Select all applicable)
□ First-party data analysis (your own analytics/user data)
□ Customer surveys and interviews  
□ Third-party market research
□ Competitive analysis and benchmarking
□ Customer observation and usability testing
□ Support ticket and feedback analysis

For each selected method:
- What specific insights are you seeking?
- What's your sample size and methodology?
- How will you validate the findings?
```

**2. Customer Persona Development:**
Use this detailed framework instead of generic descriptions:

```
Customer Segment Definition:
- Role/Title: [Specific job function, not "users"]
- Company Size/Type: [If B2B - specific industry and scale]
- Current Tools/Process: [What they use today]
- Key Responsibilities: [What they're accountable for]
- Success Metrics: [How their performance is measured]

Behavioral Insights:
- Decision-Making Process: [How they evaluate and choose solutions]
- Pain Point Frequency: [How often they encounter the problem]
- Workaround Strategies: [What they do today to cope]
- Budget/Authority: [Purchase decision influence]

Research-Backed Evidence:
- Data Source 1: [Specific finding with sample size]
- Data Source 2: [Quantified behavior or preference]
- Data Source 3: [Direct customer quotes or feedback]
```

**3. MCP Perplexity Research Integration:**
```
🔍 CONTEXT CHECKPOINT 6: Before MCP Perplexity research call, verify context usage and execute graceful halt if approaching 80%.

🔍 Would you like me to research additional market context using Perplexity?

I can gather:
- Industry trends and market data for your customer segment
- Competitive landscape and alternative solutions
- Customer behavior studies and research findings
- Technology adoption patterns and preferences

This research will be automatically saved to:
working_backwards/current/customer_research.md

Proceed with external research? (y/n)
```

**🔍 CONTEXT CHECKPOINT 7**: After MCP Perplexity research call completion, verify context usage and execute graceful halt if approaching 80%.

**Validation Criteria (Amazon Standards):**
- ✅ Customer segment is specific enough that you could call 10 of them
- ✅ Insights are quantified with actual data points
- ✅ Multiple research methods validate the same findings
- ✅ You can quote specific customer language about their pain points
- ✅ You understand their current workflow and where it breaks down

#### Stage 2: DEFINE - Problem Crystallization Using Amazon Template

**🔍 CONTEXT CHECKPOINT 8**: Before beginning Stage 2 (DEFINE), verify context usage and execute graceful halt if approaching 80%.

**❗ Core Question: WHAT is the problem?**

**Amazon's Problem Definition Template (Mandatory Format):**

```
Today, [specific customer segment] have to [current limitation/friction/manual process] 
when [specific triggering situation]. 

This means [quantified impact/consequence for customer], making it difficult to 
[specific customer goal/desired outcome].

Customers need a way to [specific needed capability] so they can 
[desired business/personal result].

Supporting Evidence:
- Data Source 1: [Specific evidence with numbers - e.g., "73% of surveyed customers report..."]
- Data Source 2: [Quantified impact - e.g., "Average time spent is 45 minutes per task"]  
- Data Source 3: [Customer quotes - e.g., "As one customer told us, 'I waste 2 hours daily on...'"]
```

**Problem Validation Deep Dive:**

**1. Specificity Assessment:**
```
Problem Specificity Check:
□ Can you solve this problem completely for your target customer?
□ Is the problem narrow enough to address in a single solution?
□ Have you avoided trying to solve multiple unrelated problems?
□ Does the problem statement avoid mentioning your solution?

If any boxes are unchecked, refine the problem statement.
```

**2. Customer Language Validation:**
```
Customer Language Audit:
- Replace internal jargon: [List any technical terms to translate]
- Use customer vocabulary: [How do THEY describe this problem?]
- Avoid company-speak: [Remove any marketing or internal terminology]
- Test with customers: [Have you validated this language with actual customers?]
```

**3. Data Validation Requirements:**
```
Evidence Strength Assessment:
- Primary Research: [What direct customer evidence do you have?]
- Market Data: [What industry data supports this problem's significance?]
- Competitive Gaps: [How do existing solutions fail to address this?]
- Frequency/Impact: [How often does this problem occur and what's the cost?]

Minimum Standard: 3 different data sources supporting the problem's existence and impact.
```

**MCP Perplexity Problem Research:**
```
🔍 Enhance problem definition with external research?

I can gather:
- Market research on this problem space
- Industry data about problem frequency and impact
- Studies on customer behavior related to this issue
- Competitive analysis of existing solutions and their gaps

Research will be added to: working_backwards/current/problem_definition.md

Proceed with problem research? (y/n)
```

#### Stage 3: INVENT - Solution Development with Amazon Evaluation Matrix

**🔍 CONTEXT CHECKPOINT 9**: Before beginning Stage 3 (INVENT), verify context usage and execute graceful halt if approaching 80%.

**💡 Core Question: WHAT is the solution?**

**Mandatory Multi-Solution Generation:**

**1. Solution Brainstorming (Minimum 3-5 Options):**
```
Solution Option 1: [Solution Name]
Description: [What it is and how it works]
Customer Benefit: [Primary value delivered]
Differentiation: [Why this vs alternatives]

Solution Option 2: [Solution Name] 
Description: [What it is and how it works]
Customer Benefit: [Primary value delivered]
Differentiation: [Why this vs alternatives]

Solution Option 3: [Solution Name]
Description: [What it is and how it works]
Customer Benefit: [Primary value delivered]
Differentiation: [Why this vs alternatives]

[Continue for 4-5 total options]
```

**2. Amazon's Evaluation Matrix (Apply to Each Solution):**
```
Evaluation Matrix:

                    Option 1  Option 2  Option 3  Option 4  Option 5
Customer Impact     H/M/L     H/M/L     H/M/L     H/M/L     H/M/L
Implementation      H/M/L     H/M/L     H/M/L     H/M/L     H/M/L
Time to Market      F/M/S     F/M/S     F/M/S     F/M/S     F/M/S
Our Advantages      H/M/L     H/M/L     H/M/L     H/M/L     H/M/L
Strategic Value     H/M/L     H/M/L     H/M/L     H/M/L     H/M/L

Legend: H=High, M=Medium, L=Low, F=Fast, S=Slow
```

**3. Solution Selection Deep Dive:**
```
Selected Solution: [Name and brief description]

Selection Rationale:
- Customer Value: [How does this solve the problem completely?]
- Unique Differentiation: [What makes this better than existing alternatives?]
- Our Advantages: [How does this leverage our specific capabilities?]
- Most Lovable Product (MLP): [What's the minimum version customers will love?]

Rejected Alternatives Documentation:
- Option [X]: Rejected because [specific reason]
- Option [Y]: Rejected because [specific reason]
- Option [Z]: Rejected because [specific reason]

[This prevents future re-litigation of alternatives]
```

**MCP Perplexity Solution Research:**
```
🔍 Research solution space and competitive alternatives?

I can gather:
- Competitive solution analysis and positioning
- Technology feasibility and implementation approaches  
- Best practices and success patterns for similar solutions
- Market timing and adoption factors

Research will be added to: working_backwards/current/solution_development.md

Proceed with solution research? (y/n)
```

#### Stage 4: REFINE - Experience Design with Customer Journey Mapping

**🔍 CONTEXT CHECKPOINT 10**: Before beginning Stage 4 (REFINE), verify context usage and execute graceful halt if approaching 80%.

**✨ Core Question: WHAT is the experience?**

**Complete Customer Journey Framework:**

**1. End-to-End Experience Mapping:**
```
Discovery Phase:
- How do customers first learn about your solution?
- What triggers their interest or need recognition?
- Where do they go for more information?
- What questions do they have at this stage?

Evaluation Phase:
- How do they assess if this is right for them?
- What comparisons do they make?
- Who else is involved in the decision?
- What concerns or objections do they have?

First Use Experience:  
- How do they get started? (Onboarding)
- What's the setup or configuration process?
- What's their "aha" moment of value realization?
- How long until they see benefit?

Core Value Delivery:
- What's the primary workflow they'll use?
- How does this integrate with their existing tools/processes?
- What's the frequency of use?
- How do they measure success?

Ongoing Usage & Growth:
- How do they expand their usage over time?
- What support do they need?
- How do they get help when stuck?
- What advanced features might they adopt?
```

**2. The ONE Benefit Identification:**
```
Primary Benefit Analysis:

List all potential benefits:
1. [Benefit 1 with customer impact]
2. [Benefit 2 with customer impact]  
3. [Benefit 3 with customer impact]
4. [Additional benefits...]

The ONE Benefit (Most Important):
[The single benefit that customers care about most - this becomes your headline]

Supporting Benefits:
[The 2-3 secondary benefits that reinforce the primary value]

Validation: Have you confirmed with customers that THIS is what matters most to them?
```

**3. Customer Vignette Creation:**
```
Customer Vignette:

Meet [Customer Name], [Customer Role/Context].

Current State Challenge:
[Customer Name] needs to [core job-to-be-done] but currently faces [specific problem] 
when [triggering situation]. This means [impact on their day/work/goals].

Typical Current Experience:
[2-3 sentences describing their current workflow and where it breaks down]

With [Your Solution]:
[2-3 sentences describing the improved experience and workflow]

Customer Result:
"[Authentic quote expressing their satisfaction, relief, or achieved benefit]"

Key Experience Improvements:
- [Specific improvement 1 with time/effort savings]
- [Specific improvement 2 with capability gained]
- [Specific improvement 3 with friction removed]
```

**MCP Perplexity Experience Research:**
```
🔍 Research customer experience patterns and best practices?

I can gather:
- User experience patterns for similar solutions
- Customer onboarding best practices and case studies
- Integration patterns and implementation approaches
- User adoption and success metrics

Research will be added to: working_backwards/current/experience_design.md

Proceed with experience research? (y/n)
```

#### Stage 5: TEST & ITERATE - Comprehensive Success Definition

**🔍 CONTEXT CHECKPOINT 11**: Before beginning Stage 5 (TEST & ITERATE), verify context usage and execute graceful halt if approaching 80%.

**📊 Core Question: HOW do we measure success?**

**Amazon's Comprehensive Metrics Framework:**

**1. Quantitative Metrics (Hard Numbers):**
```
Revenue Impact:
- Direct Revenue: $[amount] in first [timeframe]
- Revenue Per Customer: $[amount] average
- Market Size Opportunity: $[total addressable market]

Adoption Metrics:
- Target Customer Adoption: [%] of addressable customers using within [timeframe]
- Usage Frequency: Customers use [frequency] per [time period]
- Feature Adoption: [%] of users adopting core features within [timeframe]

Growth Metrics:
- Customer Growth Rate: [%] month-over-month new customer acquisition
- Usage Growth Rate: [%] increase in usage per customer over time
- Market Share: [%] of target market captured within [timeframe]
```

**2. Qualitative Metrics (Customer Sentiment):**
```
Customer Satisfaction:
- Net Promoter Score (NPS): Target score of [number]
- Customer Satisfaction (CSAT): Target rating of [number]/5
- Customer Effort Score (CES): Target score of [number]

Customer Sentiment:
- Brand Perception: [monitoring approach and success criteria]
- Customer Feedback Themes: [positive sentiment targets]
- Word-of-Mouth: [referral and advocacy measurements]

Support Quality:
- Resolution Time: Average support ticket resolution under [time]
- First Contact Resolution: [%] of issues resolved on first contact
- Support Satisfaction: [rating] average customer satisfaction with support
```

**3. Behavioral Metrics (Usage Patterns):**
```
Customer Behavior Changes:
- Workflow Changes: [How customers change their processes]
- Tool Adoption: [Changes in tool usage patterns]
- Efficiency Gains: [Measured improvements in customer productivity]

Retention & Expansion:
- Customer Retention Rate: [%] of customer retained after [timeframe]
- Feature Expansion: [%] of customers adopting additional features
- Usage Depth: [Average features used per customer]

Cross-Impact Effects:
- Cross-sell Impact: [Effect on other product/service usage]
- Customer Lifetime Value: [Projected CLV improvement]
- Customer Success: [Improvement in customer business metrics]
```

**4. Business Impact Metrics (Strategic Value):**
```
Strategic Value:
- Market Position: [Competitive advantage gained]
- Strategic Goal Advancement: [How this supports larger company objectives]
- Innovation Leadership: [Position as industry leader/innovator]

Operational Impact:
- Process Efficiency: [Internal process improvements]
- Cost Reduction: [Operational cost savings]
- Resource Optimization: [Better use of internal resources]

Long-term Value:
- Platform Growth: [Foundation for future capabilities]
- Market Expansion: [New market opportunities enabled]
- Customer Relationship: [Deepened customer partnerships]
```

**5. Unintended Consequences & Risk Planning:**
```
Potential Negative Impacts:
- Risk 1: [What could go wrong] - Probability: [H/M/L] - Impact: [H/M/L]
- Risk 2: [What could go wrong] - Probability: [H/M/L] - Impact: [H/M/L]
- Risk 3: [What could go wrong] - Probability: [H/M/L] - Impact: [H/M/L]

Mitigation Strategies:
- For Risk 1: [Preventive measures and response plan]
- For Risk 2: [Preventive measures and response plan]
- For Risk 3: [Preventive measures and response plan]

Long-term Responsibilities:
- Ongoing Support: [What ongoing commitments are required]
- Platform Maintenance: [Long-term platform and feature maintenance]
- Customer Success: [Ongoing customer success and adoption support]
```

**MCP Perplexity Success Metrics Research:**
```
🔍 Research success metrics and measurement methodologies?

I can gather:
- Industry benchmarks for similar solutions and success metrics
- Measurement methodologies and best practices
- Competitive success metrics and market standards
- Customer success patterns and predictive indicators

Research will be added to: working_backwards/current/success_metrics.md

Proceed with metrics research? (y/n)
```

**🎯 Stage 5 Completion Validation:**
```
Success Definition Completeness Check:
□ Quantitative metrics are specific with targets and timeframes
□ Qualitative metrics include measurement methodology
□ Behavioral metrics capture customer workflow changes
□ Business impact connects to strategic company goals
□ Unintended consequences are identified with mitigation plans
□ Long-term responsibilities and commitments are documented

All 5 Customer Questions Answered:
□ WHO: Customer segment specifically defined with research backing
□ WHAT (Problem): Problem crystallized using Amazon template with evidence
□ WHAT (Solution): Solution selected from 3-5 evaluated options
□ WHAT (Experience): End-to-end customer journey mapped in detail
□ HOW: Comprehensive success metrics framework defined

Ready to proceed to PR/FAQ document creation? (y/n)
```

### 3. PR/FAQ Document Creation

**🔍 CONTEXT CHECKPOINT 12**: Before PR/FAQ document creation phase, verify context usage and execute graceful halt if approaching 80%.

#### Amazon's Complete 7-Paragraph Press Release Structure

**🎯 TIER 2 ENHANCEMENT: Complete Amazon Framework Implementation**

**HEADING SECTION (Write This Last):**
```
Amazon [or Company] Announces [Product/Service Name]
[One sentence subheading: what it is + most important benefit - NO PUNCTUATION]
[Company A], [Company B], and [Company C] among customers using [solution]
CITY – MONTH DAY, YEAR
```

**PARAGRAPH-BY-PARAGRAPH COACHING:**

**PARAGRAPH 1 - The Summary (Don't Bury the Lede):**
```
Template: "[Customer type] can now [main benefit] with [product name], 
[brief description]. Starting [date], customers can [call to action]."

✅ Requirements:
- Lead with customer benefit, NOT company announcement
- Include clear call to action
- Write assuming reader won't continue past this paragraph
- Must be compelling enough to stand alone

❌ Avoid:
- "Amazon is pleased to announce..." (company-centric)
- Technical jargon or internal product names
- Burying the customer benefit in middle of paragraph
```

**PARAGRAPH 2 - The Problem (The Setup):**
```
Template: "Today, [specific customers] face [specific problem] when [situation]. 
This means [quantified impact on customer], making it difficult to [customer goal]."

✅ Requirements:
- Factual but compelling problem description
- Use specific customer language, not internal terms
- Build empathy for customer situation
- Include quantified impact where possible

❌ Avoid:
- Criticizing existing solutions or competitors
- Vague problems like "it's hard" or "time-consuming"
- Internal perspective on what's broken
```

**PARAGRAPH 3 - The Solution (The Knockdown):**
```
Template: "[Product] addresses this by [approach]. Customers can now 
[specific capability] which means [customer benefit]. This differs from 
existing approaches because [key differentiation]."

✅ Requirements:
- Address each problem from paragraph 2 directly
- Focus on customer benefits, not technical features
- Make differentiation clear and compelling
- Explain HOW it solves the problem

❌ Avoid:
- Feature lists without customer benefits
- Technical implementation details
- Assuming readers understand your innovation
```

**PARAGRAPH 4 - Amazon Leader Quote:**
```
Requirements:
✅ Must be actual quote from real leader (not placeholder)
✅ Shows genuine passion for customer impact
✅ Reinforces main benefit without repeating paragraph 1
✅ Professional but conversational tone
✅ Focuses on "why we built this" not "what we built"

Template Structure:
"We [built/created] [product] because [customer insight/motivation]," 
said [Name], [Title]. "[Customer-focused vision statement that shows 
passion for solving the problem]."

❌ Avoid:
- Generic corporate speak
- Repeating product features
- Focusing on company benefits vs customer benefits
- Overly formal or marketing-heavy language
```

**PARAGRAPH 5 - Customer Experience:**
```
Template: "To get started, customers [simple action]. They can then [process] 
to [specific outcome]. The experience integrates with [existing tools/workflows] 
to [integration benefit], and [additional experience detail]."

✅ Requirements:
- Walk through actual discovery and usage flow
- Make it concrete and visual (customers can picture it)
- Show integration with their existing tools/processes
- Inspire readers to want to try it immediately

❌ Avoid:
- Abstract descriptions of capabilities
- Complex onboarding processes
- Ignoring how this fits into customer workflows
```

**PARAGRAPH 6+ - Customer Testimonials:**
```
Requirements per testimonial:
✅ Each testimonial gets its own paragraph
✅ Minimum 2-3 testimonials addressing different use cases
✅ Must pass "Would they really say this?" test
✅ Specific and believable with concrete details
✅ Use human, conversational language

Template Structure:
"[Specific problem/situation description]. '[Customer quote with specific 
benefit and human language],' said [Name], [Title] at [Company]. 
'[Additional specific impact or usage detail].'"

Quality Tests:
- Believability: Does this sound like a real person?
- Specificity: Does it include concrete details?
- Variety: Does each testimonial show different value/use case?
- Language: Is it conversational, not corporate?
```

**PARAGRAPH 7 - Call to Action:**
```
Template: "To get started with [product], visit [URL]. For more information 
about [related topic/broader category], visit [URL]."

✅ Requirements:
- Clear, immediate next steps for interested customers
- Include relevant additional resources
- Make it easy to take action right now
```

#### Amazon's Comprehensive FAQ Organization System

**🎯 TIER 2 ENHANCEMENT: Complete Amazon FAQ Framework**

**CUSTOMER-FACING FAQs (External Focus):**
*Answer the basic questions customers ask first:*

**Essential Customer Questions:**
1. **What is [product name]?**
   - Clear, jargon-free explanation
   - Focus on customer benefit, not technical specs
   - Include the "one sentence" summary

2. **How does it work?**
   - High-level process flow
   - Customer actions and outcomes
   - Integration with existing tools/workflows

3. **What does it cost?**
   - Pricing model explanation
   - Value justification
   - Comparison to current customer costs

4. **How do I get started?**
   - Step-by-step onboarding process
   - Requirements and prerequisites
   - Timeline from signup to value realization

5. **What are the requirements?**
   - Technical prerequisites
   - Account/access requirements
   - Integration requirements

6. **How is this different from [main competitor]?**
   - Key differentiators without criticizing competitors
   - Unique value propositions
   - When to choose this vs alternatives

7. **What if I have problems?**
   - Support options and channels
   - Self-service resources
   - Response time commitments

8. **Can I integrate with [common tools]?**
   - Integration capabilities
   - Setup process for integrations
   - Supported platforms and tools

**INTERNAL/STAKEHOLDER FAQs (Deep Questions):**
*Address tough questions directly and thoroughly:*

**Amazon's 11 Essential Internal FAQs:**

1. **What decisions/guidance do we need today?**
   - Immediate decisions required from leadership
   - Resource allocation needs
   - Go/no-go criteria

2. **What customer problems are we solving and why should they care?**
   - Detailed problem analysis with data
   - Customer research supporting problem significance
   - Emotional and business impact on customers

3. **Why us? How does this leverage our competitive advantages?**
   - Unique Amazon capabilities being utilized
   - Competitive moats and differentiation
   - Why we can win vs others who might try

4. **How big could this opportunity be?**
   - Total addressable market analysis
   - Revenue projections and timeline
   - Market penetration assumptions

5. **What are our MLP (Most Lovable Product) features?**
   - Minimum features that customers would love (not just MVP)
   - Features that drive recommendation and word-of-mouth
   - What would disappoint customers most if missing

6. **What will disappoint customers most?**
   - Known limitations and gaps
   - Areas where customer expectations might not be met
   - Planned future enhancements to address gaps

7. **What alternatives did we consider and reject?**
   - Alternative solutions evaluated
   - Why each alternative was rejected
   - Prevent future re-litigation of decisions

8. **What are the hotly debated topics?**
   - Areas of internal disagreement or uncertainty
   - Different perspectives and their rationales
   - How debates were resolved

9. **What are the biggest risks?**
   - Technical, market, and execution risks
   - Mitigation strategies for each risk
   - Early warning indicators

10. **What's our timeline and roadmap?**
    - Launch timeline and key milestones
    - Future feature and capability roadmap
    - Dependencies and potential delays

11. **What would be worst-case scenario?**
    - Failure modes and their consequences
    - Recovery strategies
    - Learning and adaptation plans

**FAQ Organization Principles:**

**Priority Ordering:**
1. **Frequency**: Most commonly asked questions first
2. **Importance**: Critical decision-making information prioritized
3. **Flow**: Questions in logical order of customer journey

**Quality Standards:**
- **Direct and Honest**: Address tough questions rather than avoiding them
- **Specific**: Include supporting data and concrete examples
- **Customer Language**: Use terms customers understand
- **Actionable**: Provide clear next steps where applicable

**Hard Questions Integration Strategy:**
- **Don't Hide**: Address difficult questions proactively
- **Data-Driven**: Support answers with research and evidence
- **Balanced**: Acknowledge limitations while emphasizing strengths
- **Forward-Looking**: Explain future plans to address current gaps

### 4. Advanced Writing Quality Assessment

**🎯 TIER 2 ENHANCEMENT: Amazon's Top 10 Writing Guidelines + Quality Validation Framework**

#### Amazon's Top 10 Writing Guidelines

**1. START WITH CUSTOMER TESTIMONIAL MINDSET**
```
✅ Apply This Standard:
- Write every sentence as if customers will read it
- Use language customers understand, not internal jargon
- Focus on customer benefits, not business benefits to Amazon

❌ Common Violations:
- "This enhances our operational efficiency" → Should be "This saves you 2 hours per week"
- "Our enterprise-grade solution" → Should be "Handles your team's daily workload reliably"
- "We leverage cutting-edge technology" → Should be "Gets results 3x faster than manual processes"

🔍 Validation Test:
Would a customer care about this sentence? Does it speak to their needs and language?
```

**2. USE SIMPLE CUSTOMER LANGUAGE**
```
✅ Apply This Standard:
- 8th grade reading level maximum
- Avoid buzzwords: "enterprise-class," "cutting-edge," "innovative," "revolutionary"
- Replace jargon with plain English explanations

❌ Buzzword Detection List:
- "Enterprise-class" → "Works reliably for large teams"
- "Cutting-edge" → "Latest" or "new"
- "Innovative" → Describe what it actually does
- "Revolutionary" → Describe the specific improvement
- "Seamlessly integrate" → "Works with your existing tools"
- "Leverage" → "Use"
- "Optimize" → "Improve" or "make faster"
- "Scalable" → "Grows with your business"

🔍 Validation Test:
Can an 8th grader understand every sentence? Are there any buzzwords to replace?
```

**3. INCLUDE CUSTOMER-RELEVANT METRICS ONLY**
```
✅ Apply This Standard:
- "50% faster" → "Reduces processing time from 10 minutes to 5 minutes"
- Include context: "Saves 2 hours per week"
- Avoid internal metrics customers don't care about

❌ Internal Metrics to Avoid:
- "99.9% uptime" (unless customer cares about reliability)
- "Processes 1M transactions/second" (unless customer has volume needs)
- "Built on microservices architecture" (customer doesn't care about architecture)

✅ Customer-Relevant Metrics:
- Time savings: "Complete in 5 minutes instead of 2 hours"
- Cost savings: "Reduces monthly expenses by $500"
- Effort reduction: "3 clicks instead of 15-step process"
- Quality improvements: "Catches 95% of errors automatically"

🔍 Validation Test:
Does the customer directly benefit from this metric? Do they understand what it means for them?
```

**4. DON'T BURY THE LEDE**
```
✅ Apply This Standard:
- Most important information in first sentence
- Write headline last, after content is complete
- Assume readers will stop after first paragraph

❌ Lede-Burying Examples:
- Starting with company background instead of customer benefit
- Leading with technical specifications instead of value
- Putting the main benefit in paragraph 3 instead of paragraph 1

✅ Strong Lede Examples:
- "Marketing teams can now create campaign reports in 10 minutes instead of 4 hours..."
- "Small business owners can accept payments immediately without waiting for bank approval..."
- "Remote teams can collaborate in real-time without video call delays..."

🔍 Validation Test:
If readers stop after the first sentence, do they understand the main benefit?
```

**5. FOCUS ON HERO SCENARIOS**
```
✅ Apply This Standard:
- Main use cases, not edge cases
- What do 80% of customers actually do?
- Save complex scenarios for FAQ section

❌ Edge Case Examples:
- Describing complex enterprise configurations in main text
- Focusing on unusual integration scenarios
- Leading with advanced features instead of core value

✅ Hero Scenario Examples:
- "Most customers use this to automate their weekly reports"
- "The typical workflow takes 3 steps: upload, review, publish"
- "Small teams start with basic features and add advanced capabilities later"

🔍 Validation Test:
Is this the primary way most customers will use the product?
```

**6. SCRUB FOR BELIEVABILITY**
```
✅ Apply This Standard:
- Test: "Would a customer really say this?"
- Testimonials must sound human, not corporate
- Avoid hyperbole and exaggerated claims

❌ Unbelievable Testimonials:
- "This revolutionary solution transformed our entire business model overnight"
- "We achieved 1000% ROI in the first week"
- "This is the most amazing product we've ever used"

✅ Believable Testimonials:
- "I used to spend 3 hours every Friday on reports. Now it takes 15 minutes"
- "My team can finally see all our customer data in one place"
- "The setup was straightforward - we were running in about an hour"

🔍 Validation Test:
Does this testimonial sound like something a real person would actually say?
```

**7. READ ALOUD TEST**
```
✅ Apply This Standard:
- Does it flow naturally when spoken?
- Are sentences too long or complex?
- Does it sound conversational?

❌ Read-Aloud Failures:
- Sentences longer than 25 words
- Complex technical terms strung together
- Formal, academic writing style

✅ Read-Aloud Success:
- Natural rhythm and flow
- Conversational tone
- Easy to speak without stumbling

🔍 Validation Test:
Read every paragraph aloud. Does it sound natural and conversational?
```

**8. BE CONCISE**
```
✅ Apply This Standard:
- Every sentence must add unique value
- Remove redundant information
- Cut unnecessary words without losing meaning

❌ Wordiness Examples:
- "In order to utilize this solution" → "To use this"
- "At this point in time" → "Now"
- "Due to the fact that" → "Because"

✅ Conciseness Examples:
- "Helps teams collaborate" instead of "Enables teams to work together more effectively"
- "Reduces errors" instead of "Minimizes the possibility of mistakes occurring"
- "Works with Slack" instead of "Integrates seamlessly with Slack communication platform"

🔍 Validation Test:
Can you remove any words without losing meaning?
```

**9. GET FRESH EYES REVIEW**
```
✅ Apply This Standard:
- Have uninvolved person read and provide feedback
- Test with someone unfamiliar with the project
- Ask: "What questions do you have after reading?"

❌ Fresh Eyes Failures:
- Only getting feedback from team members
- Assuming readers have context you have
- Not testing comprehension with outsiders

✅ Fresh Eyes Success:
- Reviewer understands the customer problem immediately
- Reviewer can explain the solution back to you
- Reviewer knows what action to take next

🔍 Validation Test:
Can someone unfamiliar with your project understand and explain it back to you?
```

**10. AVOID MARKETING BUZZWORDS AND HYPERBOLE**
```
✅ Apply This Standard:
- Remove: "revolutionary," "game-changing," "industry-leading"
- Replace with specific, measurable benefits
- Let customer value speak for itself

❌ Hyperbole Examples:
- "Revolutionary breakthrough in data analytics"
- "Game-changing approach to customer service"
- "Industry-leading innovation in cloud computing"

✅ Specific Benefits:
- "Analyzes data 10x faster than spreadsheets"
- "Resolves customer issues in 2 minutes instead of 20"
- "Stores files securely in the cloud with 99.9% uptime"

🔍 Validation Test:
Are claims specific and provable? Would competitors make the same generic claims?
```

#### Comprehensive Quality Validation Framework

**🔍 Complete Document Review Checklist:**

**SECTION 1: Content Quality Assessment**
```
□ CUSTOMER TESTIMONIAL MINDSET: Every sentence focuses on customer value
□ SIMPLE LANGUAGE: 8th grade reading level, no buzzwords
□ CUSTOMER METRICS: All numbers are relevant and meaningful to customers
□ NO BURIED LEDE: Key information is in first sentence/paragraph
□ HERO SCENARIOS: Focuses on main use cases, not edge cases
□ BELIEVABILITY: All testimonials pass "would they really say this?" test
□ READ ALOUD: Document flows naturally when spoken
□ CONCISENESS: Every sentence adds unique value
□ FRESH EYES: Reviewed by someone unfamiliar with project
□ NO HYPERBOLE: Specific benefits instead of marketing buzzwords
```

**SECTION 2: Structural Quality Assessment**
```
□ PRESS RELEASE STRUCTURE: Follows Amazon's 7-paragraph framework
□ FAQ ORGANIZATION: Customer questions first, internal questions second
□ PROBLEM-SOLUTION FIT: Solution directly addresses stated problem
□ CUSTOMER JOURNEY: Experience description is concrete and visual
□ TESTIMONIAL VARIETY: Multiple testimonials show different use cases
□ CALL TO ACTION: Clear next steps for interested customers
```

**SECTION 3: Amazon Standards Compliance**
```
□ 5 CUSTOMER QUESTIONS: All answered with specific detail
□ WORKING BACKWARDS: Evidence of 5-stage methodology completion
□ PROBLEM TEMPLATE: Uses "Today, [customer] have to..." format
□ SOLUTION EVALUATION: Multiple alternatives considered and documented
□ SUCCESS METRICS: Comprehensive measurement framework defined
□ AMAZON VOICE: Sounds like authentic Amazon communication
```

#### Advanced Quality Assessment Tools

**🎯 Customer Focus Scoring System:**
Rate each section on customer-centricity scale:
- **5 = Entirely Customer-Focused**: Only talks about customer benefits and value
- **4 = Mostly Customer-Focused**: Minor company-centric language
- **3 = Mixed Focus**: Balance of customer and company benefits
- **2 = Mostly Company-Focused**: Emphasizes company capabilities over customer value
- **1 = Company-Centric**: Focuses on company achievements, not customer benefits

**Target Score**: All sections should achieve 4 or 5

**🎯 Believability Assessment Framework:**
For each testimonial and claim, test:
```
Believability Checklist:
□ HUMAN LANGUAGE: Sounds like real person speaking, not corporate
□ SPECIFIC DETAILS: Includes concrete numbers, timeframes, situations
□ REALISTIC CLAIMS: Benefits are believable, not exaggerated
□ VARIED PERSPECTIVES: Different testimonials show different viewpoints
□ AUTHENTIC VOICE: Each person sounds unique and genuine
```

**🎯 Technical Readability Analysis:**
```
Readability Standards:
□ SENTENCE LENGTH: Average under 20 words per sentence
□ PARAGRAPH LENGTH: 3-4 sentences maximum per paragraph
□ SYLLABLE COUNT: Minimize words with 3+ syllables
□ PASSIVE VOICE: Less than 10% passive voice usage
□ TRANSITION WORDS: Smooth flow between ideas
□ JARGON DENSITY: Technical terms explained immediately
```

#### Section-by-Section Quality Enhancement

**🔧 Press Release Quality Enhancement Process:**

**Step 1: Paragraph-by-Paragraph Review**
- Apply all 10 Amazon writing guidelines to each paragraph
- Score each paragraph on customer focus (1-5 scale)
- Identify and replace all buzzwords and jargon

**Step 2: Testimonial Quality Assessment**
- Test each testimonial with believability framework
- Ensure variety in use cases and perspectives
- Verify authentic, conversational language

**Step 3: Overall Flow and Structure**
- Perform read-aloud test for entire document
- Verify no buried ledes or key information
- Confirm strong call-to-action conclusion

**🔧 FAQ Quality Enhancement Process:**

**Step 1: Customer Question Priority Review**
- Verify most common questions are answered first
- Ensure customer language in both questions and answers
- Test that answers provide actionable information

**Step 2: Internal FAQ Completeness Check**
- Confirm all 11 essential Amazon internal questions are addressed
- Verify honest, direct answers to difficult questions
- Ensure data and evidence support all claims

**Step 3: Organization and Flow Assessment**
- Test logical progression from basic to complex questions
- Verify appropriate level of detail for each audience
- Confirm consistent tone and style throughout

This comprehensive quality framework ensures that every PR/FAQ document meets Amazon's exacting standards for customer focus, clarity, and believability while maintaining the authentic Amazon communication style.

### 5. Knowledge Base Integration

Format the completed PR/FAQ for inclusion in `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md`:

```markdown
## Project PR/FAQ

### Press Release: [Product Name]
*Last Updated: [Date]*

[Full press release content]

### Frequently Asked Questions

#### Customer FAQs
[Customer-facing questions and answers]

#### Internal FAQs
[Stakeholder questions and answers]

### Working Backwards Summary

**The 5 Customer Questions:**
1. **Customer**: [Your answer]
2. **Problem**: [Your answer]
3. **Solution**: [Your answer]
4. **Experience**: [Your answer]
5. **Success Metrics**: [Your answer]

**Key Learnings:**
- [Learning 1]
- [Learning 2]
- [Learning 3]

**Trust Sources:**
- Documentation: [Path to PR/FAQ document]
- Data: [Links to supporting data]
```

### 6. Iterative Coaching Mode

For users who want section-by-section coaching:

1. **Assess Current State**: Review what they have
2. **Identify Gaps**: Compare against best practices
3. **Provide Examples**: Show before/after improvements
4. **Practice Rewriting**: Guide through revisions
5. **Validate Changes**: Ensure improvements meet standards

### 7. Advanced Features

#### Readability Analysis
- Check reading level (target: 8th grade)
- Identify complex sentences
- Flag jargon and technical terms
- Suggest simplifications

#### Customer Focus Scorer
Rate each section on customer-centricity:
- 5 = Entirely focused on customer value
- 3 = Mix of customer and company focus
- 1 = Too internally focused

#### Believability Check
For quotes and testimonials:
- Does it sound human?
- Is it specific enough?
- Does it avoid corporate speak?

## Implementation Example

Here's how to guide a user through creating their PR/FAQ:

```
Assistant: Let's start with understanding your customer. Think of a specific person or role, not a broad category.

User: Our customers are developers.
