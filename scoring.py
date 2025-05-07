import re
import os
import google.generativeai as genai
from fastapi import HTTPException
from dotenv import load_dotenv
load_dotenv()

API_KEYS = []
for i in range(5):
    api_key = os.getenv(f"API_KEY_{i+1}")
    API_KEYS.append(api_key)
    
def grade_writing(essay_text, API_KEYS):
    prompt = f'''
    You are an expert VSTEP examiner grading a Writing Task 2 essay. Please score the essay based on the official VSTEP Writing rating scales, evaluating the following three criteria:
    ---
    1. **Organization (0-10)**:
        - **Band 10**: Organizes information and ideas logically; uses a variety as well as a range of cohesive devices; uses paragraphing sufficiently and appropriately.
        - **Band 9**: Organizes information and ideas coherently; uses a variety as well as a range of cohesive devices and organizational patterns effectively; uses paragraphing sufficiently and appropriately.
        - **Band 8**: Organizes information and ideas coherently; uses a range of linking words and cohesive devices appropriately, though there may be some under/overuse; uses paragraphing quite well.
        - **Band 7**: Organizes information and ideas coherently; uses a variety of linking words and a number of cohesive devices accurately within and across sentences, but there may be occasional inappropriacies; manages paragraphing well.
        - **Band 6**: Organizes information and ideas coherently; uses linking words and a limited number of cohesive devices within and across sentences accurately, but there are some inappropriacies; manages paragraphing relatively well.
        - **Band 5**: Organizes information and ideas fairly coherently; uses linking words and some familiar cohesive devices within and across sentences accurately, though there may be inaccuracies; may not write in paragraphs, or paragraphing is not adequate.
        - **Band 4**: Presents information and ideas with some organization; uses linking words accurately and attempts a few familiar cohesive devices within and across sentences, though there are repetitions and inaccuracies; may not write in paragraphs, or paragraphing is confusing.
        - **Band 3**: Presents information and ideas in a series of simple sentences linked by only basic, high-frequency linking words.
        - **Band 2**: Has very little control of organizational features.
        - **Band 1**: Has no organizational features.

    2. **Vocabulary (0-10)**:
        - **Band 10**: Uses a wide range of vocabulary including less common lexis precisely and flexibly; shows full control of style and collocation, but there may be occasional inappropriacies; errors are very rare with just one or two minor slips.
        - **Band 9**: Uses a wide range of vocabulary including less common lexis precisely; shows good control of style and collocation, but there may be some inaccuracies; errors, if present, are non-systematic and non-impeding.
        - **Band 8**: Uses a good range of vocabulary including some less common lexis appropriately; shows some control of style and collocation; errors, if present, are non-systematic and non-impeding.
        - **Band 7**: Uses a sufficient range of vocabulary; attempts less common lexis with occasional inappropriacies; errors do not impede communication.
        - **Band 6**: Uses a sufficient range of vocabulary; attempts less common lexis but most are faulty; errors do not impede communication.
        - **Band 5**: Uses an adequate range of vocabulary but tends to overuse certain lexical items; errors occur and may impede comprehension at times.
        - **Band 4**: Uses basic vocabulary with acceptable control; errors are noticeable and impede comprehension at times.
        - **Band 3**: Uses a limited range of basic vocabulary; errors are frequent and distort the meaning.
        - **Band 2**: Uses a very limited range of words and phrases; errors are dominant and distort the meaning.
        - **Band 1**: Uses only a few isolated words.
        - **Band 0:** does not write any words; writes only a memorized response

    3. **Grammar (0-10)**:
        - **Band 10**: Uses a wide range of structures precisely and flexibly; errors are very rare with just one or two minor slips.
        - **Band 9** Uses a wide range of simple and complex structures precisely; the vast majority of the sentences are error-free; errors, if present, are non-systematic and non-impeding.
        - **Band 8** Uses a variety of simple and complex structures with good control; the majority of the sentences are error-free; errors, if present, are non-systematic and non-impeding.
        - **Band 7** Uses both simple and complex structures in a relatively effective way; errors occur but they rarely lead to misunderstanding.
        - **Band 6** Uses both simple structures; errors occur but they rarely lead to misunderstanding.
        - **Band 5** Shows good control of simple structures; attempts complex structures but most are faulty; errors occur, but normally they do not impede comprehension.
        - **Band 4** Shows acceptable control of simple structures; attempts some complex structures, but unsuccessfully; errors occur frequently and impede comprehension at times.
        - **Band 3** Uses some simple structures correctly; frequently makes basic errors that distort the meaning.
        - **Band 2** Can only use some memorized structures; errors are dominant and distort the meaning.
        - **Band 1** Cannot use sentence forms at all.
        - **Band 0:** does not write any words; writes only a memorized respons
    ---
    ## **Instructions for Evaluation**
    - Carefully read the given essay and assess its **Organization, Vocabulary, and Grammar** using the detailed descriptors above.
    - Assign band ranges with 1-point intervals from **0 to 10** for each criterion based on the essay’s overall performance.
    - Ensure that your scoring aligns with the **VSTEP Writing rating scales** and reflects a **supportive and encouraging** evaluation approach.

    ### **Encouraging & Fair Assessment**
    - **Prioritize communicative effectiveness**: If errors in **Grammar** or **Vocabulary** do not significantly hinder understanding, **focus on the strengths** rather than the mistakes.
    - **Acknowledge effort and idea clarity**: Essays that demonstrate **clear idea development and coherence** should be **rewarded generously**, even if they contain frequent minor errors.
    - **Encourage risk-taking and complexity**: Essays that attempt **varied sentence structures and diverse vocabulary** should receive **higher scores**, even if occasional mistakes appear.
    - **Minimize penalties for minor mistakes**: **Common learner errors** should not drastically lower scores unless they severely affect readability.

    ### **Balanced & Flexible Scoring**
    - When in doubt, **opt for the higher band** if the essay shows **logical organization and idea progression**, despite some linguistic flaws.
    - **Balance accuracy with fluency**: If an essay **effectively conveys ideas**, do not overly penalize for minor grammatical or lexical issues.
    - If an essay contains **repetition, incoherence, or memorized responses**, reflect this in the **Organization** score, but still acknowledge any strengths.
    - **Reward range and effort**: Essays that showcase **a variety of vocabulary and grammatical structures** should receive **credit for ambition**, even if errors occur.
    - **Maintain flexibility and encouragement** in scoring to foster a **more human-like, fair, and motivating** evaluation process.

    ### **Handling Minimal, or Underdeveloped Essays**
    - If an essay is **under 60 words**, all three criteria (**Organization, Vocabulary, Grammar**) should receive **Band 0.5–1.0**, unless there is strong evidence to justify higher scores.
    - **Vocabulary must not be rewarded** simply for being "mostly understandable." If the essay uses **only basic vocabulary**, includes **wrong word forms or word misuse**, and shows **no variety**, score it as **Band 1.0–3.0 at most**.
    - **Grammar must not be given above Band 3.0** unless there are **multiple full, correctly structured sentences**. If only 1–2 correct sentences exist and the rest are flawed, treat the grammar ability as **extremely limited**.
    - **Do not average scores upward** just because part of the text is readable. Unless the essay shows **clear control, variety, and development**, do not award mid-range bands.
    - Remember: An essay is only meaningful for scoring if it shows **idea development, coherence, and evidence of language control**. Essays lacking these must be scored **harshly and consistently**.
    ---
    ### **Example 1**
    ### **Student's Essay:**
    *"there are many reasons i like this city. first, This is a beautiful city, have great beach in north city. it's a biggest city in area there. in the city, have many company, many buliding,..and we can coach jobs than earsy. with big city, it has many public transport. In here, people use public transport every day. city have ennergeer team, who alway fix teansport system when problem is bug. they are busy person, they spend most of time for computer, with key, with system problem. the second, city's people alway smile every time, every day so they love life here. Food in the city so great, also spycy but i like it and it very good with beer in city. sometime, I bought 1 ket beer for small party at house with may friends. I feel my life so preaty when i go to this city, every day when see in the sky with sea wind, i feel relax after tired day."*
    ---
    ### **Step-by-Step Evaluation**

    #### **1. Organization:**
    - The essay attempts to follow a general idea (why the writer likes the city), but the structure is **very weak and disorganized**.
    - There is **no clear paragraphing** or logical flow between ideas.
    - Linking devices are **limited or misused** (e.g., “the second” comes after no clear “first”), and transitions are awkward or missing.
    - Many ideas are just listed without development or cohesion.
    - **Score: 1.5**
    ---

    #### **2. Vocabulary:**
    - Uses a few descriptive words (e.g., *beautiful*, *great beach*, *public transport*, *spicy*, *sea wind*), but the range is **very limited**.
    - **Frequent spelling mistakes and word misuse**, such as:
      - *"ears y"* → *easily*
      - *"buliding"* → *building*
      - *"ennergeer"* → *engineer*
      - *"teansport"* → *transport*
      - *"spycy"* → *spicy*
      - *"ket beer"* → *keg of beer*
      - *"may friends"* → *my friends*
    - Some words are used **incorrectly or don't make sense** in context (e.g., *"coach jobs"*, *"problem is bug"*).
    - **Score: 1.5**
    ---

    #### **3. Grammar:**
    - The essay shows **very limited control** of grammar structures.
    - Most sentences are **simple and ungrammatical**, with frequent errors in:
      - Subject-verb agreement (e.g., *"city have"*, *"have beach"*)
      - Articles and comparatives (e.g., *"a biggest city"*)
      - Sentence construction (e.g., *"they are busy person"*)
    - Many sentences are **difficult to understand** due to grammar mistakes.
    - Almost no use of complex structures, and **numerous basic grammar errors** throughout.
    - **Score: 1**
    ---

    ### **Final Score:**
    - **Organization:** 1.5
    - **Vocabulary:** 1.5
    - **Grammar:** 1
    ---

    ### **Example 2**
      ### **Student's Essay:**
      *"In recent years, learning has become a broad issue to the general puplic. Some people think that learning only take place in a particular place and at particular period of time. On the other hand, others argue that learing should be a continous process rather than a stage in a person's life. In my onpion, I agree the latter point of view of this essay. I also believe that learning is never too late. We can learn at anywhere and anywhen in the life. Learning is process for long time, Learning life is the good way. Every people will experence for you outside book. Learning life will help us very much."*

      ---

      ### **Step-by-Step Evaluation**

      #### **1. Organization:**
      - The essay shows an **attempt at structure**, with an introduction, a point of view, and some supporting sentences.
      - Transitions such as *"On the other hand"* and *"In my opinion"* are used, though not always appropriately.
      - **Paragraphing is missing**, and ideas are **not clearly developed**.
      - The final part becomes a **list of vague generalizations**, lacking coherence.
      - **Score: 2.5**

      ---

      #### **2. Vocabulary:**
      - Vocabulary use is **very basic and repetitive** (*learning life*, *help us very much*, *every people*).
      - There are **some attempts** at less common expressions like *"learning is never too late"* and *"at anywhere and anywhen"*, though they are not used correctly.
      - Frequent **misspellings**: *puplic* → *public*, *learing* → *learning*, *onpion* → *opinion*, *experence* → *experience*.
      - Very **limited range**, with **inaccurate word forms** and **awkward phrasing**.
      - **Score: 2.5**

      ---

      #### **3. Grammar:**
      - Shows **some control of simple structures**, but grammar errors are frequent and often **impede clarity**.
      - Issues include:
        - Subject-verb agreement: *"learning only take place"*
        - Article misuse: *"a particular period of time"*, *"the life"*
        - Unclear phrases: *"Learning is process for long time"*, *"Every people will experence for you"*
      - **Sentence construction is awkward**, and few sentences are grammatically accurate.
      - **Score: 2.5**

      ---

      ### **Final Score:**
      - **Organization:** 2.5
      - **Vocabulary:** 2.5
      - **Grammar:** 2.5

        ---

    ### **Example 3:**
      ### **Student's Essay:**
      *"It is the fact that, education plays an important role in our life. At the present time, an increasing number of people are concerned about English language. Some people say that a good command of the English language can gain a great deal of information from internationla resources. I am one of those who strongly agree this idea because of the following reasons. Firstly, English is popular language, it easy to learn, easy to speaking and easy to listen. Anyone can use English language to communication. In development city, everyone learn English from young old. Moreover, they go to Musium or Park meet many England people that is improve communication skill. Secondly, All webside on internet have been writing by English language. When I excellent about English, you can gain a great deal of information from international resources. Therefore, you gain more knowlegde, improve many sortskill and chane take part in many necessry lesson. It is good for find and undertand about many cultural in the world. To sum up, I belived that a good command of the English language can gain a great deal of information from international resources. However, as fas as I am concerned people choose the most effective and suitable way for themselves and the Gorvernment should enact polices education to incearing knowledge."*

      ---

      ### **Step-by-Step Evaluation**

      #### **1. Organization:**
      - The essay has a **clear introduction, body, and conclusion**, showing an effort at structuring ideas.
      - Transition words like *"Firstly,"* *"Secondly,"* and *"To sum up,"* are used appropriately.
      - Some sentences are **disconnected or awkwardly linked**, reducing overall coherence.
      - Repetition of the main idea without deep development weakens impact.
      - **Score: 4.5**

      ---

      #### **2. Vocabulary:**
      - Uses some **topic-specific vocabulary** (*international resources*, *communication skills*, *knowledge*, *government*).
      - However, vocabulary range is **limited** and **repetitive** (*English language*, *gain a great deal of information* appears multiple times).
      - Multiple **spelling and word choice errors**:
        - *internationla* → *international*
        - *webside* → *website*
        - *sortskill* → likely meant *soft skills*
        - *chane* → unclear, perhaps *chance*?
        - *cultural* → should be *cultures*
        - *incearing knowledge* → *increasing knowledge*
      - **Score: 4**

      ---

      #### **3. Grammar:**
      - Demonstrates some **control of basic structures**, but numerous **errors reduce clarity**:
        - *"it easy to learn, easy to speaking"* → should be *it is easy to learn, speak and listen*
        - *"learn English from young old"* → unclear; perhaps *from a young age to old age*
        - *"have been writing by English language"* → should be *are written in English*
        - *"When I excellent about English"* → unclear meaning
      - Sentence structure is often **fragmented or incorrect**, though basic meaning is usually understandable.
      - **Score: 4**

      ---

      ### **Final Score:**
      - **Organization:** 4.5
      - **Vocabulary:** 4
      - **Grammar:** 4
        ---

    ### **Example 4**
      ### **Student's Essay:**
      *"It is more and more children are playing computer game. There's no denying this has a lot of positive and negative effects will give me point in this eassay are what are should do to mininmize the bad effects. On the one hand, playing computer games is very be beneficicalfor children. First, children will be sinnarter and more reponsive when playing games. Scientists have shown that when playing games, children will increase their problem solving abitity their eyes and hand will be faster. Second, playing game will help chidren gwt along with friends. After school. children playing game together will be full and reduce stress. On the other hand, playing computer game also has come negative effect on young children. If chidren play game for a long time, their eyesight will be reduced. For example, playing game that are not quailified, lack of light... all of the above factors will cause damege to the eyes. Second, they will become ibactive, not sitting in place playing game. Therefore, they will have a high risk of obesity. To minimize the negative effects, parent should pay attention to choosing healthy and safe game for children. Let your child play for up to 1 or 2 hours after completing the home work, this will hepl the chi;d to be happy and relax. Incluction, children."*

      ---

      ### **Step-by-Step Evaluation**

      #### **1. Organization:**
      - The essay attempts a **clear structure**: introduction, body (positive and negative effects), and a brief conclusion.
      - **Linking phrases** like *"On the one hand,"* and *"On the other hand,"* help organize ideas.
      - Some **sentence structures are awkward or confusing**, especially in the introduction and conclusion.
      - The final sentence is incomplete (*"Incluction, children"*), weakening the closing.
      - **Score: 5.5** – There is an effort to organize ideas, but paragraphing and transitions need refinement.

      ---

      #### **2. Vocabulary:**
      - Shows **some range** of vocabulary related to the topic (*problem solving ability*, *obesity*, *reduce stress*, *healthy and safe games*).
      - There are many **spelling mistakes and misused words**:
        - *sinnarter* → likely meant *smarter*
        - *abitity* → *ability*
        - *damege* → *damage*
        - *ibactive* → *inactive*
        - *quailified* → *qualified*
        - *incluction* → *in conclusion*
      - Despite the errors, most ideas are still **understandable**.
      - **Score: 5**

      ---

      #### **3. Grammar:**
      - Uses a mix of **simple and some complex sentences**.
      - There are **frequent grammatical errors**, such as:
        - *"children are playing computer game"* → should be *computer games*
        - *"this has a lot of positive and negative effects will give me point..."* → needs restructuring
        - *"playing game that are not quailified..."* → should be *games that are not qualified*
      - Errors **occasionally affect clarity**, but the message remains mostly **comprehensible**.
      - **Score: 5**

      ---

      ### **Final Score:**
      - **Organization:** 5.5
      - **Vocabulary:** 5
      - **Grammar:** 5

        ---

    ### **Example 5**
      ### **Student's Essay:**
      *"In recent years, Internet has become an integral part of rising debate in general public. Some people believe that Intenet has many advantages, others think it could also has negative effects. In my opinion, its cons could never overshadowing its pros. In the following essay, I will discuss the benefits as well as drawbacks of Internet. First and foremost, people should recognize that Internet has many advantages. Firstly, Internet makes great contribution to providing an unlimited sources of information, support for learning and researching. For instance, students can find out the information for essay, learning online or attend many online competition, meanwhile teacher can easily preprare our lesson plan. Another point I want to mention is that Internet is great way to entertain. For example, we can watch movie or playing game to reduce stress after a hard working or studying day. Moreover, Internet helps people easily connect with each other via many platforms like social media, email, video call and so on. On the other hand, in addition of important benefits of internet, it has many disadvantages. First of all is that there are many information posted online in Internet are inaccuracy. It lead to people could access with inaccuracy information. Moreover, there are numerous of violent and sex image or video in Internet, this can be badlly effect with people, specally children. In addition, nowaday, people spending much of time to use Internet to entertain, which can lead to neglect of other responsibilities such as study or work. In conclusion, the above-mentioned facts have outlined the benefits as well as the drawback of Internet. The its disadvantge should taken into account. People should have further consideration on this issue."*

      ---

      ### **Step-by-Step Evaluation**

      #### **1. Organization:**
      - The essay follows a **clear and logical structure**: introduction, body paragraphs (advantages and disadvantages), and conclusion.
      - Each paragraph is **clearly divided** and the points flow in a **coherent order**.
      - Linking phrases like *"First and foremost,"* *"On the other hand,"* and *"In conclusion"* are used effectively.
      - Some transitions could be improved for smoother flow (*"Another point I want to mention..."* could be more formal).
      - **Score: 7**

      ---

      #### **2. Vocabulary:**
      - Shows a **good range of topic-relevant vocabulary**: *integral part, unlimited sources of information, social media, online competition*.
      - Some **word choices are awkward or incorrect**:
        - *"overshadowing"* → should be *overshadow*
        - *"inaccuracy"* → should be *inaccurate*
        - *"badlly effect with people"* → *badly affect people*
        - *"numerous of violent and sex image"* → *numerous violent and sexual images*
      - However, meaning is **usually clear** despite errors.
      - **Score: 7**

      ---

      #### **3. Grammar:**
      - Uses a mix of **simple and complex sentence structures**, but often **with mistakes**:
        - *"Internet has become an integral part of rising debate..."* → awkward phrase
        - *"others think it could also has"* → should be *could also have*
        - *"teacher can easily preprare our lesson plan"* → *their lesson plans*
        - *"people spending much of time"* → *people spend much time*
      - Articles, subject-verb agreement, and sentence clarity need improvement.
      - **Frequent grammar errors**, but they don't fully obscure the meaning.
      - **Score: 6.5**

      ---

      ### **Final Score:**
      - **Organization:** 7
      - **Vocabulary:** 7
      - **Grammar:** 6.5

    ### **Example 6**
      ### **Student's Essay:**
      *"In recent years, brain drain has been getting more and more attention from the public due to its significant impacts on the developing countries. Rising demand of opportunities to improve the living standards make educated and talented experts move from developing countries to rich and developed countries. That leads to brain drain, which wastes a lot of national resources to raise such an educated person. This essay will explain why these people choose to leave their countries and give some possible solutions to deal with this problem. First of all, the reasons why the genius leave their country should be considered. They are grown and received support from authorities in numerous fields such as: education, health care and economy. Perhaps the policy to talented people in some developing countries is good, however, they are lack of opportunities for these experts to develop themselves. For example, in Vietnam, the technology is still not updated to the lastest version, is not matched with what these educated people learn. That results in the conflicts between what they has studied and what they do and then, these conflicts cause bad effects on their background knowledge. The another reason is the low salary. The income in developing countries is not enough for their desire of living although they need to work hard and contribute themselve to the economy. With the same job in developed countries, they can earn even two or three times higher than in developing countries. Therefore, it can be easy to see why they choose to work in developed countries. To minimize the number of talented experts leaving from developing countries to developed ones, there are some possible solutions for the government. The government should invest more to education and social policy. At the same time, they could hold some meetings with these educated people to listen their difficulties and desire to improve the issues. Cutting down finance on unneccessary fields is essential to spend money decreasing brain drain. In conclusion, brain drain now is still an urgent problem in developing countries. This must be solved as soon as possible."*

      ---

      ### **Step-by-Step Evaluation**

      #### **1. Organization:**
      - The essay is **well-organized**, with a **clear introduction, body, and conclusion**.
      - Logical flow of ideas: causes are followed by solutions.
      - Uses **cohesive devices effectively**: *"First of all,"* *"For example,"* *"Therefore,"* *"In conclusion."*
      - Paragraphing is mostly appropriate, though some transitions between ideas could be smoother.
      - **Score: 8.5**

      ---

      #### **2. Vocabulary:**
      - Demonstrates a **wide range of vocabulary** relevant to the topic: *"talented experts,"* *"national resources,"* *"updated technology,"* *"unnecessary fields."*
      - Minor lexical errors:
        - *"Rising demand of opportunities"* → should be *for opportunities*
        - *"lastest version"* → should be *latest version*
        - *"The another reason"* → should be *Another reason*
      - Despite small errors, word choice is generally precise and clear.
      - **Score: 8.5**

      ---

      #### **3. Grammar:**
      - Uses **a variety of sentence structures**, both simple and complex.
      - Some **minor grammar mistakes**, including:
        - *"They are grown and received support..."* → awkward phrasing
        - *"what they has studied"* → should be *have studied*
        - *"contribute themselve"* → should be *themselves*
        - *"invest more to education"* → should be *invest more in education*
      - These errors do not hinder comprehension but show room for improvement.
      - **Score: 8.5**

      ---

      ### **Final Score:**
      - **Organization:** 8.5
      - **Vocabulary:** 8.5
      - **Grammar:** 8.5
      ---

    Now let's think step by step to evaluate the student's essay:
    **Student's Essay:**
    {essay_text} </end of essay>
    '''
    
    for api_key in API_KEYS:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("models/gemini-2.0-pro-exp")
            response = model.generate_content(prompt, generation_config={"temperature": 0})

            if essay_text == "":
                response = """### **Final Score:**

*   **Organization:** 0
*   **Vocabulary:** 0
*   **Grammar:** 0
"""
                return response
            else:
                if response and response.text:
                    return response.text.strip()
                else:
                    return "Lỗi: API không trả về nội dung điểm số."

        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                # print(f"[CẢNH BÁO] API key {api_key} vượt quota, thử key tiếp theo...")
                continue
            else:
                # return f"[LỖI] Không xác định: {e}"
                raise HTTPException(status_code=500, detail=str(e))

    # return "[LỖI] Tất cả API Key đều vượt quota hoặc có lỗi."
    raise HTTPException(status_code=429, detail="Tất cả API Key đã hết quota.")
def extract_final_scores(text):
    scores = {}

    patterns = {
        "Organization": r"\*\*Organization:\*\*\s*(\d+(?:\.\d+)?)",
        "Vocabulary": r"\*\*Vocabulary:\*\*\s*(\d+(?:\.\d+)?)",
        "Grammar": r"\*\*Grammar:\*\*\s*(\d+(?:\.\d+)?)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            score = float(match.group(1))
            if key in ["Grammar", "Vocabulary"] and (score > 3.0 and score <= 7):
                score += 1
            # if key in ["Grammar", "Vocabulary"] and (score == 3):
            #     score += 0.5
            scores[key] = score

    return "\n".join([f"{key}: {value}" for key, value in scores.items()])
