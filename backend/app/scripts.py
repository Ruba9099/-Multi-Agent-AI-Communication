"""
Yahan har topic ke liye ek structured conversation "script" hai.
Har script ek list hai (speaker, text) tuples ki.
Speaker hamesha "innovator" ya "reviewer" hoga.

Ye design isliye rakha gaya hai taake:
1. Conversation coherent aur meaningful lage (random text nahi).
2. Aap chahen to future me is function ko replace kar ke
   Anthropic/OpenAI API se real LLM response generate kar saken
   (dekhein agents.py me `generate_reply` function - wahi single
   jagah hai jise replace karna hoga).
"""

TOPICS = {
    "agentic_ai": {
        "title": "Agentic AI & Multi-Agent Systems",
        "description": "AI agents jo khud decisions le kar tasks complete karte hain, aur ek dusre se collaborate karte hain.",
        "script": [
            ("innovator", "Aaj hum baat karte hain Agentic AI ki — yeh woh systems hain jo sirf answer nahi dete, balki khud steps plan karke, tools use karke, aur decisions le kar poora task complete karte hain."),
            ("reviewer", "Interesting start! Lekin mera pehla sawal yeh hai: agar agent khud decisions le raha hai, to accountability kiski hogi jab woh galat decision le?"),
            ("innovator", "Fair point. Lekin isi wajah se ab 'human-in-the-loop' pattern popular ho raha hai — agent critical steps par approval maangta hai, baaki routine kaam khud karta hai. Isse speed aur safety dono milte hain."),
            ("reviewer", "Theek hai, lekin real-world me agents ko multiple tools (email, database, payment systems) tak access dena bhi ek bada security risk hai. Ek prompt injection attack poora system compromise kar sakta hai."),
            ("innovator", "Bilkul sahi. Isliye sandboxing aur permission-scoping zaroori hai — agent ko sirf woh access do jo uske task ke liye chahiye, sab kuch nahi. Yeh 'principle of least privilege' hi hai."),
            ("reviewer", "Ek aur cheez — jab do agents aapas me baat karte hain (jaise hum abhi kar rahe hain!), to conversation kabhi kabhi loop me phas sakti hai, ya dono ek dusre se galat information confirm kar lete hain."),
            ("innovator", "Haan, isko 'hallucination amplification' kehte hain. Solution yeh hai ke ek third-party verifier ya grounding source (jaise database ya search) use kiya jaye taake conversation facts par based rahe, sirf agreement par nahi."),
            ("reviewer", "Overall main maanta hoon ke agentic workflows powerful hain — customer support, coding assistants, aur research automation me already dikh raha hai. Bas governance aur monitoring layer strong honi chahiye."),
            ("innovator", "Exactly. Mera conclusion yeh hai: Agentic AI ek bada shift hai 'AI as a tool' se 'AI as a collaborator' ki taraf — lekin isko responsibly design karna hi asli engineering challenge hai."),
            ("reviewer", "Well said. Main is discussion ko yahan close karta hoon — pros: automation, scalability, naye workflows. Cons: accountability, security, aur reliability. Dono balance karna hi sabse important hai."),
        ],
    },
    "rag": {
        "title": "Retrieval-Augmented Generation (RAG)",
        "description": "AI models ko live/external data se jodna taake woh outdated ya galat jawab na den.",
        "script": [
            ("innovator", "Chaliye baat karte hain RAG ki — Retrieval-Augmented Generation. Isme AI model apna jawab dene se pehle ek external database ya document store se relevant information nikalta hai."),
            ("reviewer", "Yeh to LLM ke 'knowledge cutoff' problem ka acha solution lagta hai. Lekin agar retrieval hi galat document laaye, to model bhi galat jawab dega — 'garbage in, garbage out'."),
            ("innovator", "Sahi kaha. Isliye retrieval quality (embeddings, chunking strategy, reranking) utni hi important hai jitna model khud. Achi RAG pipeline me hybrid search (keyword + semantic) use hota hai."),
            ("reviewer", "Cost aur latency ka bhi factor hai — har query par vector database search + LLM call, dono milakar response time badha dete hain. Real-time applications ke liye yeh challenge ban sakta hai."),
            ("innovator", "Yeh sach hai, lekin caching aur smaller/faster embedding models is problem ko kaafi had tak solve kar dete hain. Aur benefit itna bada hai — company apne private data par accurate answers de sakti hai — ke yeh trade-off worth it hai."),
            ("reviewer", "Ek aur concern: agar sensitive company data retrieval system me hai, to access control bahut zaroori hai, warna AI accidentally confidential info leak kar sakta hai."),
            ("innovator", "Bilkul, row-level security aur proper document permissions RAG pipeline ka hissa hona chahiye, na ke afterthought."),
            ("reviewer", "Mera final take: RAG un companies ke liye best hai jinke paas apna knowledge base hai — support docs, internal wikis, product manuals. General chit-chat ke liye zaroori nahi."),
            ("innovator", "Agreed. RAG ka sabse bada fayda hai 'grounded, up-to-date, aur verifiable' answers — jo trust badhata hai."),
            ("reviewer", "Discussion summary: Pros — accuracy, freshness, domain-specific knowledge. Cons — retrieval quality risk, latency, aur data security. Ek balanced tool, magic bullet nahi."),
        ],
    },
    "edge_ai": {
        "title": "On-Device / Edge AI",
        "description": "AI models jo cloud ke bajaye phone/laptop/IoT device par hi chalte hain.",
        "script": [
            ("innovator", "Aaj ka topic hai Edge AI — AI models jo device par hi (phone, laptop, camera) run hote hain, cloud server ki zaroorat nahi."),
            ("reviewer", "Privacy ke liye to yeh great hai — data device se bahar hi nahi jaata. Lekin mera sawal: chhote devices par bade models chalana technically possible hai?"),
            ("innovator", "Model quantization aur distillation techniques se ab 1-3 billion parameter models bhi phones par smoothly chal rahe hain — jaise on-device speech recognition aur photo enhancement."),
            ("reviewer", "Accha, lekin battery consumption aur heating ek real problem hai. Continuous AI processing device ki battery life kaafi kam kar sakti hai."),
            ("innovator", "Yeh valid hai, isliye dedicated NPUs (Neural Processing Units) ban rahe hain jo AI tasks ko efficiently, kam power me handle karte hain — jaise ab har naye phone chip me hota hai."),
            ("reviewer", "Cloud AI ke comparison me edge models kam powerful bhi hote hain — complex reasoning tasks abhi bhi cloud par better perform karte hain."),
            ("innovator", "Sahi, isliye hybrid approach best hai: simple/private tasks edge par, complex tasks cloud par — 'best of both worlds'."),
            ("reviewer", "Yeh design pattern makes sense. Especially healthcare aur finance jaise sensitive industries ke liye edge AI attractive hai kyunki data locally rehta hai."),
            ("innovator", "Bilkul — Edge AI privacy-first future ki taraf ek bada step hai."),
            ("reviewer", "Summary: Pros — privacy, low latency, offline capability. Cons — limited compute, battery drain, aur reasoning limitations. Use-case ke hisaab se decide karna chahiye."),
        ],
    },
}

DEFAULT_TOPIC = "agentic_ai"
