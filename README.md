# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

UCI Data Science students face a unique recruiting landscape. It is a newer 
major with less established employer pipelines than CS, located in an Irvine 
tech corridor that is largely invisible in generic career advice. The UCI 
career center treats DS and CS recruiting as interchangeable, but students 
experience them very differently. This system makes student-generated knowledge 
about internships, professor recommendations, and what actually works for UCI 
DS students searchable and answerable.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | r/UCI Reddit | Forum thread | documents/reddit_uci_internship_hard.txt |
| 2 | r/UCI Reddit | Forum thread | documents/reddit_uci_internship_advice.txt |
| 3 | r/UCI Reddit | Forum thread | documents/reddit_uci_internship_tips.txt |
| 4 | r/UCI Reddit | Forum thread | documents/reddit_uci_cs_gpa_internship.txt |
| 5 | r/UCI Reddit | Forum thread | documents/reddit_uci_jobs_list_2026.txt |
| 6 | r/UCI Reddit | Forum thread | documents/reddit_uci_quarter_internship.txt |
| 7 | Rate My Professors | Student reviews | documents/rmp_uci_mandt_cs178.txt |
| 8 | Rate My Professors | Student reviews | documents/rmp_uci_dillencourt_cs161.txt |
| 9 | Rate My Professors | Student reviews | documents/rmp_uci_qian_stats120b.txt |
| 10 | Rate My Professors | Student reviews | documents/rmp_uci_yeh_ics46.txt |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 400 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** 
Most documents are short Reddit comments and Rate My Professor reviews, usually 2 to 5 sentences long. A 400 character chunk captures one complete thought or opinion without merging multiple unrelated reviews together. Overlap of 50 characters helps when a key fact like a professor name or company name falls near a chunk boundary, so retrieval can still find it from either side. Before chunking, documents were cleaned by removing blank lines, extra whitespace, and common Reddit UI elements like upvote counts, ad text, and navigation labels.


**Final chunk count:**
172
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers, running locally 
with no API key or rate limits.

**Production tradeoff reflection:** 
For a production system serving real UCI students I would consider text-embedding-3-small from OpenAI. It has higher accuracy on domain specific text and a longer context window, which would help with chunks that contain dense technical or career advice content. The tradeoff is cost and rate limits since it requires an API key and charges per token. all-MiniLM-L6-v2 runs locally for free which makes it practical for this project. If the system needed to support international students I would also evaluate paraphrase-multilingual-MiniLM-L12-v2, which handles multiple languages but sacrifices some accuracy on English-only text. Latency is another factor — a locally hosted model avoids network round trips, which matters for a real-time query interface.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
The system prompt instructs the model 
to answer using ONLY the information in the provided documents. The exact 
instruction is: "Answer the question using ONLY the information in the 
provided documents below. If the documents do not contain enough information 
to answer the question, say exactly: I don't have enough information in my 
documents to answer that." This forces the model to decline rather than 
generate a plausible-sounding answer from its training data when the 
documents don't cover the question.

**How source attribution is surfaced in the response:**
Retrieved chunks are 
passed to the model with numbered source labels in the format [Source 1: 
filename.txt]. The model is instructed to list which sources it used at the 
end of every response. Additionally, the Gradio interface displays a separate 
Retrieved from field that programmatically lists the unique source filenames 
from all retrieved chunks, independent of what the model writes, so 
attribution is guaranteed even if the model omits it.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which companies have actually hired UCI data science students recently? | Students mention Amazon, Blizzard, and local Irvine companies | Declined to answer — said not enough information in documents | Partially relevant | Inaccurate |
| 2 | Is the UCI career center worth using for data science internships? | Mixed reviews, Career Pathways mock interviews mentioned as useful | Declined to answer — said not enough information in documents | Partially relevant | Inaccurate |
| 3 | Does GPA matter when applying to internships as a UCI CS or DS student? | GPA matters less than experience, 3.0 cutoff common | GPA is not the only factor, anything above 3.0 is good, technical skills prioritized | Relevant | Accurate |
| 4 | What do students say about Stephan Mandt and CS 178 for ML preparation? | Generous grading, math heavy lectures, solid ML foundation | Mandt is caring, responsive, provides resources, highly recommended for ML | Relevant | Accurate |
| 5 | How does the UCI quarter system affect internship recruiting timelines? | Quarter system misaligns with recruiting cycles, finals conflict with start dates | Internships start in May/June aligning with semester system, UCI students still have coursework left 

**Retrieval quality:** Relevant 
**Response accuracy:** Accurate 

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
Which companies have actually hired UCI data science 
students recently?

**What the system returned:**
"I don't have enough information in my documents 
to answer that." The retrieved chunks came from reddit_uci_jobs_list_2026.txt 
and reddit_uci_internship_tips.txt, which are relevant sources but the model 
still declined.

**Root cause (tied to a specific pipeline stage):**
The failure happened at 
two stages. First, during document collection, the Reddit threads discuss 
internship strategies generally but rarely name specific companies that hired 
UCI DS students. The documents simply do not contain enough company-specific 
facts to answer the question. Second, during chunking, the 400 character 
chunks cut up the jobs list thread before any company names could appear in 
a single retrievable chunk, so the model received fragments without enough 
concrete information to form an answer.

**What you would change to fix it:**
Two fixes would help. First, collect more 
targeted documents — specifically Blind threads or Levels.fyi data that name 
companies and schools together. Second, increase chunk size for list-style 
documents like the jobs thread so that company names and context stay together 
in the same chunk instead of being split across boundaries.

---

## Spec Reflection

**One way the spec helped you during implementation:**
Writing the chunking 
strategy in planning.md before touching any code forced me to think about 
the structure of my documents first. Because I had already decided on 400 
character chunks with 50 character overlap and written down the reasoning, 
I could implement the chunk_text function directly without second-guessing 
the numbers mid-build. The spec also made it easy to prompt AI tools 
effectively since I could paste specific sections instead of explaining 
everything from scratch each time.


**One way your implementation diverged from the spec, and why:** 
The spec anticipated clean retrieval with distance scores below 0.5, but actual distances came back between 0.9 and 1.1. This happened because the Reddit documents were noisier than expected after manual copy-paste collection, containing leftover UI text and ad fragments that diluted the semantic signal. I addressed this by adding a skip_phrases filter to the clean_text function, which reduced noise but did not fully resolve the high distance scores. In a future iteration I would manually clean each document more thoroughly before chunking.

## AI Usage

**Instance 1**

- *What I gave the AI:* My Chunking Strategy and Documents sections from 
planning.md, along with the pipeline diagram showing the five stages of 
the system.
- *What it produced:* A complete ingest.py script with load_documents, 
clean_text, chunk_text, and process_documents functions using 400 character 
chunks and 50 character overlap as specified.
- *What I changed or overrode:* The original clean_text function only stripped 
whitespace and joined lines. After running it I found Reddit ad text and UI 
elements still appearing in chunks, so I overrode it with a skip_phrases 
filter that removes lines containing words like "promoted", "sign up", 
"upvote", and "downvote".


**Instance 2**

- *What I gave the AI:* My Retrieval Approach section from planning.md and 
the pipeline diagram, asking it to implement embedding with all-MiniLM-L6-v2 
and storage in ChromaDB with source metadata.
- *What it produced:* A complete embed.py script with embed_and_store and 
retrieve functions, storing chunks with source filename metadata and querying 
with top-k of 5.
- *What I changed or overrode:* The generated code did not handle the case 
where a ChromaDB collection already exists from a previous run, which caused 
an error on the second run. I added a try/except block to delete the existing 
collection before creating a new one so the script can be run repeatedly 
without errors.
