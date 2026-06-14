import json
import os
import sys
import requests
import datetime
from google import genai
import time

PREAMBLE = """
You are working for a website called "Parliament Simple"
which 'presents the most notable speeches of the House of Commons and the House of Lords every week, without spin, and without the boring bits.'.

Articles are almost entirely verbatim, but structured to highlight the key, most interesting points of debates.

Parliament Simple's motto is 'Know the debates of our time.'

Included below is an example article - all articles follow this format:

```
---
layout: post
title:  "Trump and Venezuela"
description: "Speeches following US military intervention in Venezuela and the capture of its President Nicolás Maduro."
author: Peter Warrington
---

> The US has attacked Venezuela and captured its President Nicolás Maduro, with Donald Trump vowing to "run the country" until there is a "proper" transition of power.
>
> <https://www.bbc.co.uk/news/articles/crmlz7r0zrxo> 3rd January 2026

---

**Key Quotes:**

> "We should be under no illusion as to the nature of the Maduro regime. A once functioning democracy has become a hub for very dangerous organised criminal gangs—corrupt links have involved Iran, with Hezbollah increasingly present in recent years, as well as malign support from Russia—and a regime that has facilitated illicit finance, sanctions evasion and organised criminal activity, including narcotics trafficking and illegal gold trading." - **Yvette Cooper (Labour)**

> "Oil companies are not state builders, nor are they capable of democratic capacity building or enabling political transitions." - **Alicia Kearns (Conservative)**

> "It would be hard to find an occasion on which a British Prime Minister has looked as irrelevant and spineless on an era-defining international issue as this one does on this occasion." - **Pete Wishart (SNP)**

> "The Prime Minister just looks ridiculous when he will not tell the truth: that Trump has broken international law." - **Ed Davey (Liberal Democrat)**

---

## House of Commons Venezuela Debate - January 5th 2026

<https://hansard.parliament.uk/commons/2026-01-05/debates/453C7107-419B-4AF7-8602-352E03B903AF/Venezuela>

The House of Commons met on Monday 5th January 2026 to hear a statement from the **Foreign secretary, Yvette Cooper (Labour)**:

>...
>
>Let me turn to Venezuela. Over the weekend, the United States conducted air strikes on a series of Venezuelan targets, and confirmed that it had captured Nicolás Maduro and his wife, Cilia Flores. They have been indicted on narcoterrorism, drug smuggling and weapons charges. I can confirm to the House that the United Kingdom was not involved in these operations.
>
> UK policy on Venezuela has long been to press for a peaceful transition from authoritarian rule to a democracy that reflects the will of the Venezuelan people, maintains security in the region and is in line with international law. That remains our position and our determined view about what must happen in Venezuela now. Over the weekend I discussed this with the US Secretary of State, Marco Rubio, and the UK Government are in close contact with our international partners on the issue.
>
>We should be under no illusion as to the nature of the Maduro regime. A once functioning democracy has become a hub for very dangerous organised criminal gangs—corrupt links have involved Iran, with Hezbollah increasingly present in recent years, as well as malign support from Russia—and a regime that has facilitated illicit finance, sanctions evasion and organised criminal activity, including narcotics trafficking and illegal gold trading. That undermines the security of the whole region, including UK overseas territories, as well as the United States and other regional partners. The country has been driven into economic ruin, with an 80% drop in its GDP in a decade. More than 8 million people have left, which has caused instability elsewhere in the region.
>
>We have seen Maduro’s regime systematically dismantle democratic institutions, silencing dissent and weaponising state resources to maintain power through fear and corruption. The International Criminal Court has opened an investigation into possible crimes against humanity, following reports of hundreds of extrajudicial killings, including at the hands of Venezuela’s security services and paramilitary groups under the regime’s command. UN investigators have repeatedly reported a pattern of arbitrary detentions, tortures and killings.
>
> In the July 2024 presidential election, millions of Venezuelans voted, but the official results have never been published. The opposition leader, María Corina Machado, was banned from standing by Maduro. International observers cited basic failures of election integrity. Independent tallies covering 80% of polling stations showed a clear victory for Edmundo González, yet Maduro claimed victory.
>
> Most recently, in October, the UN independent fact-finding mission reported on state security forces using firearms against protesters after the elections 18 months ago, where 25 people died. González has been forced to leave the country and claim political asylum in Spain. Machado was forced into hiding for her own safety and had to be spirited out of the country to receive her Nobel peace prize in Norway last month.
>
> These are the hallmarks of a regime that clings to power through fear, coercion and violence, not through democratic consent. That is why, as the Prime Minister said on Saturday, we can shed no tears for the end of Maduro’s rule.
>
> Let me turn to UK policy. The UK has long been an advocate for a democratic Venezuela and a vocal critic of the Maduro regime. Since 2019, successive UK Governments have refused to recognise the regime. Through the G7 and the UN, with partners and directly, we have continued to call out the Maduro regime and its appalling human rights violations.
>
> We have also, in some areas, taken a different policy approach from some of our allies. Our other Five Eyes partners have closed their embassies, but we have maintained our diplomatic mission in Caracas at a much more senior level than many of our partners and are seeking dialogue, sustaining direct contact with the opposition, supporting Venezuelan civil society and advocating for British interests.
>
> Of course, throughout we have promoted and maintained support for international law. The commitment to international law, as the Prime Minister set out on Saturday, is immensely important to this Government. Those principles guide the decisions that we make and the actions that we take as part of Britain’s foreign policy. That commitment to international law is part of our values; it is also strongly in the UK’s national interest. Our manifesto talked about a foreign policy that is progressive and is also realistic, engaging with the world as we find it, in the interests of UK security, prosperity and our values. That means upholding international law and defending democracy, and it means confronting the complex, evolving and hybrid threats that we and our allies face in the world today.
>
>Those principles and values also guide the conversations that we have with our allies across a range of issues where we agree and disagree. In my discussions with Secretary Rubio, I raised the importance of complying with international law, and we will continue to urge all partners to do so at every stage. It is, of course, for the US to set out the legal basis for its actions. The UN Security Council is discussing Venezuela this afternoon. These issues will continue to be matters for international discussion.
>
>I discussed with Secretary Rubio what should happen next and our continued commitment to a transition to a peaceful and stable democracy. Our collective immediate focus must be on avoiding any deterioration in Venezuela into further instability, criminality, repression or violence. That would be deeply damaging for the people of Venezuela, our own overseas territories, our allies in the US and other regional partners.
>
>The UK has long been clear that the leadership of Venezuela must reflect the will of the Venezuelan people, so the international community must come together to help achieve a peaceful transition to a democratic Government who respect the rights and will of their people. That must mean action on the economic crisis, the release of political prisoners, the return of opposition politicians, an end to political repression, respect for human rights, and plans for the holding of free and fair elections. I urge the acting President, Delcy Rodríguez, to take these steps forward, because the people of Venezuela have a right to decide their own future.
>
> ...
>

The **Leader of the Opposition, Kemi Badenoch (Conservative)** was the first to respond to the statement:

> ...
>
> Foreign policy should serve our national interest. It should be about keeping Britain safe. We should be clear-eyed. The United States is our closest security partner. We must work with it seriously, not snipe from the sidelines. The Opposition understand why the US has taken this action. As the Foreign Secretary said, UK policy has long been to press for a peaceful transition from authoritarian rule to a democracy. That never happened. Instead, Venezuelans have been living under Maduro’s brutal regime for many years.
>
>
> The US has made it clear that it is acting in its national interest against drug smuggling and other criminal activity, including potential terrorism. We understand that. However, we have concerns about what precedent this sets, especially when there are comments made about the future of Greenland. It is important that the United Kingdom supports its NATO ally Denmark, which has made it categorically clear that Greenland is not for sale, so I welcome the Foreign Secretary’s remarks in that regard.
>
> ...
>
> I am pleased to hear that the Foreign Secretary has spoken to María Corina Machado, but can she also update the House on whether the Prime Minister has spoken to President Trump? I ask that because the Government talk up their relationship with the US, but we keep finding that we are not in the room when big decisions are made.
>
> ...
>
> In a world changing as it is, we must be serious and responsible about our security and standing. We know what the strategy of the President of the United States is, because his Government set out their national security strategy last year. The US is acting in its national interests, and we need to do the same. We should be working to protect the rules-based order, and we should be standing up to hostile actors that want to undermine us, but what are our Government doing instead? They are giving away the Chagos islands, and paying £35 billion for the privilege, with no strong legal basis to justify doing so.
>
> ...
>
> It has never been more important for the UK to have a coherent foreign policy strategy. Right now, Labour does not have one. If it does, we would like the Foreign Secretary to tell us what it is, because I did not hear anything that sounded remotely like one in her statement. Let us be honest: old strategies will not work. We are living in an increasingly dangerous world, and the axis of authoritarian states seeking to undermine us respects just one thing: strength. Britain must be ready and willing to defend our own interests, to protect ourselves from those who would undermine us, to protect the unity of the western alliance, and to support democracy and freedom around the world.

**Yvette Cooper (Labour)** responded back:

> I must just say to the Leader of the Opposition that, while I obviously welcome her support on Switzerland, Greenland and Denmark and so on, it felt like the tone of her response was very poorly judged. It was really all over the place.
>
> ...
>
> In fact, on the different issues the Leader of the Opposition talked about, she seemed to agree with us. On Venezuela, she said that the Maduro regime has been deeply damaging, corrupt and deeply destructive, and therefore that no one should shed any tears for its going. She also—I think this was implicit when she talked about the rules-based order—recognised the importance of precedents, the importance of international law and the complexity of the world we face. She also said that she thought we should show support for Denmark and Greenland. In fact, I could not see in her response a single detailed thing that she disagreed with, except for the fact that she seemed to want to express opposition for opposition’s sake.
>
> Many times in the past we took a cross-party approach, and I would expect the Leader of the Opposition to do the same on what really matters for the future of this country. This Government will continue to stand up for Britain’s interests, our prosperity and our values.
>
> ...

---

As is custom in debates on foreign policy, the chair of the Foreign Affairs Select Committee, **Emily Thornberry (Labour)**, was called next to question the Foreign Secretary on their statement:

> If a large and powerful country abducts the leader of another, however abhorrent that leader is, and tries to intimidate the smaller country to, as it says itself, gain access to its resources, does the Foreign Secretary not agree that this should be called out not just by Britain, but by our western allies? We should be calling it out for what it is—a breach of international law. It is not for the country breaking the law to say whether or not it has broken the law; it is surely for the west to stand up and call it as it is. Does she not therefore share my concern that there may be a profound risk of international norms changing? If we do not call it out, this may become okay, and we risk living in a world where might is right, which is surely not in Britain’s interests.

**Yvette Cooper (Labour):**

> ... My right hon. Friend rightly referred to the issues of international law. I have set out our commitment to international law, and she will know that my predecessor as Foreign Secretary [David Lammy] talked about progressive realism. We have set out the progressive principles we follow—including how important international law is, because the framework it sets does not just reflect our values, but is in our interests—but also that we have to engage with the world the way it is. I can assure her that, as part of that, I have raised the issue of international law with Secretary of State Rubio and made it clear that we will continue to urge all countries to follow it.

---

As the 3rd largest party in the House of Commons, the **Leader of the Liberal Democrats, Ed Davey**, was next to question the Foreign Secretary:

> ...
>
> When President Reagan invaded Grenada, Margaret Thatcher said that
>
>*“we in…the Western democracies…use our force to defend our way of life, we do not use it to walk into other people’s countries... We try to extend our beliefs not by force but by persuasion.”*
>
> I am disappointed that we have heard nothing as clear and courageous from either the Prime Minister or the Foreign Secretary, or from today’s Conservative party.
>
> Maduro is a brutal, illegitimate dictator, but that does not give President Trump a free pass for illegal action. This was not about liberating the Venezuelan people. Trump’s refusal to back Nobel prize winner María Machado, Maduro’s brave liberal opponent, shows that Trump has no interest in Venezuelan democracy. This is about Trump believing he can grab anything he wants—this time, oil—and get away with it. We know what happens when an American President launches an illegal war under the pretext of an imminent threat. It is why we opposed the Iraq war, and why we condemn Trump today.
>
> National sovereignty matters and international law matters. Without them, the world is far more dangerous and we are all less safe. Anyone who thinks Trump’s actions will make China or Russia think twice is either hopelessly desperate or desperately naive. Putin and Xi will be using this precedent to strengthen their hands in Ukraine and Taiwan. Anyone who thinks Trump will stop with Venezuela has not read his new national security strategy. He is already threatening Colombia, Cuba and Greenland, and even democracies across Europe. Does the Foreign Secretary not realise how ridiculous it looks to refuse to call this what it is: a clear breach of international law? ...

**Yvette Cooper (Labour):**

> ... We have made very clear our commitment to international law and the way that it must guide our decisions and UK foreign policy. We will continue to raise it with our partners, both in public and in private. It is important that we do so. ...

---

Next to respond was **Diane Abbot (Labour)**, the longest continuously serving member of the House of Commons, often described as a "veteran left-winger" due to her prominent position in the Socialist Campaign Group caucus and her role in the Shadow Cabinet of Jeremy Corbyn:

> Nobody in this Chamber wants to defend the regime of Maduro, but what some of us want to do is to stand up for the importance of a rules-based international order. I might add that because my parents were born overseas, I take the question of national sovereignty extremely seriously. We cannot have a situation where a country, because it is bigger and stronger, walks into a smaller country, snatches its political leadership—whatever people think of that political leadership—helicopters it out and puts it on a show trial in an outside country. That cannot be something that this Government are prepared to support.
>
> ...
>
> I know that the Opposition are blithe about what Trump is doing, but let me say this: there will be countries that will look at Trump’s attitude and carelessness towards issues of sovereignty and think, “What happens if we have that threat? Who will be willing to stand up for us? Who will be willing to stand up for our national sovereignty?” As far as I have heard thus far, it will not necessarily be our Ministers.
>
> ...
>
> My question is: what would the Foreign Secretary say to British voters—ordinary British voters; not left-wing British voters in particular—who do not understand why a British Prime Minister is not willing to stand up for an international rules-based order and is not willing to defend national sovereignty?

**Yvette Cooper (Labour)**

> ... Support for a rules-based international order and for international law is a central part of our foreign policy and the decisions the UK Government make and the actions we take. There is an approach that says, “Look, this is a new world of great power politics and spheres of influence,” and rejects the role of international law. That is not our view not only because we believe it is right and part of our progressive values, but because it is in the UK’s interests. ...

---

**Richard Burgon (Labour)**, another member of the Socialist Campaign group:

> It was the Prime Minister who decided to disregard the United Nations charter when it came to Trump’s bombing and killing, and his kidnapping the Head of State. It speaks volumes that the Prime Minister has chosen not to come to this House to explain his decision. The reality is that if it were Putin doing this, the Prime Minister would not be saying, “It’s up to the Russians to decide whether or not this is legal,” but that is exactly what the Prime Minister has said in relation to Trump’s disgusting attack on Venezuela. Is not the reality that the Prime Minister is willing to ditch international law and side-step the United Nations charter in order to appease Donald Trump, and does not that cowardly, craven approach drag this country’s reputation through the dirt?

**Yvette Cooper (Labour):**

> I find it hard not to remember my hon. Friend’s support and welcome for the Maduro regime, a regime that is currently being investigated for crimes against humanity.

---

**Edward Morello (Liberal Democrat):**

> ... I will not mourn the passing of the Maduro regime, but I will mourn the passing of the rules-based international order. ...

---

Veteran, Former Minister of State for Security, and previous Conservative party leadership candidate (considered on the moderate wing of the party), **Tom Tugendhat**:

> ... As the Prime Minister revealed on Sunday, he has not even spoken to the American President. Does this not reveal the simple truth that the Americans did this without us because they do not give a damn what this House thinks?

**Yvette Cooper (Labour):**

> ... What has struck me since becoming Foreign Secretary, and having had discussions with Governments from across the world over the past few months, is how often those Governments say how welcome it is that Britain is back.

---

**Pete Wishart (SNP):**

> It would be hard to find an occasion on which a British Prime Minister has looked as irrelevant and spineless on an era-defining international issue as this one does on this occasion. We are witnessing an existential threat to the international rules-based order, and the Prime Minister cannot rouse himself to give it even the meekest of defences. France, Spain, Brazil, Mexico and the UN Secretary-General have all been clear that the Trump Administration have violated international law. When will the Prime Minister and the Foreign Secretary find their voices and join that chorus of condemnation?

**Yvette Cooper (Labour):**

> The Prime Minister’s response has been very much in line with the leaders of countries across not just Europe but the world. ...

---

**John McDonnell (Labour)**, who also is a member of the Socialist Campaign Group and is a close ally of Jeremy Corbyn:

> The Secretary of State has said that the role of the Government has been to uphold international law. Part of upholding international law is to call out crimes when they are witnessed. Article 2.4 of the United Nations charter is explicit about the illegality of entering into a foreign state with armed force. That is why I found it shameful, I have to say, that the Prime Minister and Ministers in the news rounds have refused to condemn this action. I think that Trump will interpret our not condemning this action as the green light to go in wherever to steal the national assets of those countries. As a result, we are all in a more dangerous place.

---

**Alicia Kearns (Conservative):**

> ... Oil companies are not state builders, nor are they capable of democratic capacity building or enabling political transitions. ...

---

**Simon Hoare (Conservative):**

> The essay question is not whether Mr Maduro was a good man, which is a clear no-brainer, but whether, as others have asked, the actions of the US President were legal. America cannot be expected to mark her own homework, so I have two questions for the Foreign Secretary. First, what body or bodies would she identify as being responsible to adjudicate on the legality of the American action? Secondly, as the vice-president of Venezuela, whose hands are as tainted with the previous regime as Maduro’s, has this afternoon been sworn in as the new President, what read-across should this House have from that incident?

**Yvette Cooper (Labour):**

> The UN Security Council has been discussing Venezuela today, and I am sure that those international discussions will continue. On the vice-president being sworn in, we continue not to recognise the legitimacy of the Venezuelan regime. ...

---

**Sir Bernard Jenkin (Conservative):**

> To those who still harbour illusions about an idealised world of international rules that will be abided by all, should we not just say, “Welcome to the real world, where might often proves to be right and we have to face the circumstances that we are in”? May I therefore give my support to the Government’s ambivalence, as supported by my right hon. Friend the Leader of the Opposition, who also rightly criticised—it was all she disagreed with the Government about—the slow pace of rearmament? Will the Foreign Secretary avoid blowing up the bridges we have with the United States and use that influence? Does she not agree it really would be stupid to slag off President Trump now when we want to have influence over what he does next?

**Yvette Cooper (Labour):**

> ... In terms of the UK’s approach, we continue to believe in the importance of a rules-based order and of such an international framework. We also engage with the world as it is—the world as we face it. ...

---

**Imran Hussain (Labour):**

> ... The reality is that we are sending a green light to say that international rules no longer apply. Let us call this what it is. Trump’s actions are not about democracy; they are about oil and old-fashioned colonialism. ...

---

**Dr Andrew Murrison (Conservative):**

> Will the Government use any influence that their silence on Venezuela is buying to impress on President Trump that ... hemispheric proto-colonialism that threatens UK interests or the integrity of any Commonwealth country or European neighbour would destroy the special relationship that has existed between our countries since the second world war?

---

**Paula Barker (Labour):**

> ... Trump’s rationale around stopping drug trafficking rings hollow following his pardon for ex-Honduran President Hernández. ...

---

**Tim Farron (Liberal Democrat)** and former leader of his party immediately following its coalition government with the Conservative Party:

> ... In 2003 in this House, a Labour Government voted, with Conservative support, to illegally invade Iraq. The consequences were the undermining of international law, the emboldening of despots around the world, and the massive degradation of Britain’s security, safety and significance. Have we learned nothing from that lesson of nearly 25 years ago? Have we not learned the one lesson above all of history—that those who appease bullies soon become their victims? ...

---

**Josh Babarinde (Liberal Democrat):**

> Throughout this statement the Foreign Secretary appears to have taken comfort from the UK not having been involved in the US’s illegal attack in Venezuela, but she cannot escape the reality that for as long as this Government fail to call out Trump for his actions, they are complicit in his demolition of the international rules-based order. ...

---

## Prime Minister's Questions - January 7th

<https://hansard.parliament.uk/commons/2026-01-07/debates/F2012EE8-5532-426B-8797-FA85B1832591/Engagements>

**Ed Davey (Liberal Democrat)**, Party leader:

> Geoffrey Robertson KC is a respected authority on international law. He is also the head of the Prime Minister’s barrister chambers and he could not be clearer: President Trump’s actions in Venezuela are illegal. He says the United States:
>
>“is in breach of the United Nations charter”
>
>and
>
>“has committed the crime of aggression, which the court at Nuremberg described as the supreme crime”.
>
> Does the Prime Minister agree with his old mentor, or has he got it wrong?

**Sir Keir Starmer (Labour)**, Prime Minister:

> There are plenty of things that Geoffrey and I have agreed on and disagreed on over the years, but let me set out our position. It is our long-standing position that Maduro was not a legitimate president in Venezuela, so nobody, I think, sheds any tears at his removal. What we were saying before the weekend, and we say again, is that there needs to be a peaceful transition to democracy in Venezuela. The benchmark of all actions of all countries is, of course, international law, and it is for the US to justify its actions accordingly. My focus is on the defence and security of the United Kingdom. ...

**Ed Davey (Liberal Democrat)**:

> The Prime Minister just looks ridiculous when he will not tell the truth: that Trump has broken international law.  ...

"""

client = genai.Client()

def prompt_ai(prompt):
    # url = "http://localhost:11434/api/chat"
    # data = {
    #     "model": "llama3.1",
    #     "messages": [
    #         {
    #             "role": "user",
    #             "content": f"{PREAMBLE}"
    #         },
    #         {
    #             "role": "user",
    #             "content": f"{prompt}"
    #         }
    #     ],
    #     "stream": False,
    #     "think": False,
    #     "options": {
    #         "num_ctx": 16384
    #     }
    # }
    # headers = {
    #     "Content-Type": "application/json"
    # }

    # response = requests.post(url, headers=headers, data=json.dumps(data))
    # try:
    #     return response.json()["message"]["content"]
    # except Exception as e:
    #     print(json.dumps(response.json(), indent=4))
    #     raise e

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=f"{PREAMBLE}\n\n{prompt}"
    )
    return response.text

def generate_key_quotes(transcript):
    key_quotes_prompt = f"""
    Here is the transcript of a parliamentary debate:

    ```
    {transcript}
    ```

    """ + """
    Output ONLY a JSON string array of up to ten of the most notable, memorable, rhetorically interesting, and/or entertaining quotes of the debate. Quotes should have adequate context and may be reasonably long.
    Quotes are preferably given in full.
    Quotes should be presented in descending order of notability, unless order is necessary for the context of the quote.

    This will be presented in the top of an article with the section title 'Key Quotes'.

    You may add information within square brackets to clarify the context of quotes for example to explain who/what a quote is in reply to, but you may not add any other editorialisation or commentary.

    Respond in the following format:

    [
        {
            "quote": "Quote 1",
            "speaker": "Speaker 1"
        },
        {
            "quote": "Quote 2",
            "speaker": "Speaker 2"
        },
        ...
    ]

    You should include some quotes from those leading the debate (e.g. Secretary of State).

    This should be the ENTIRETY of your response, and should be valid JSON. Do not include any other text or commentary. Do not enclose with ```json or any other code block markers.
    """

    key_quotes_response_str = prompt_ai(key_quotes_prompt)
    print("Raw key quotes response:")
    print(key_quotes_response_str)
    key_quotes_response = json.loads(key_quotes_response_str)

    return key_quotes_response

def generate_notable_speeches(transcript, key_quotes):
    notable_speeches_prompt = f"""
    Here is the transcript of a parliamentary debate:

    ```
    {transcript}
    ```

    Here are some selected key quotes:

    {key_quotes}

    """ + """
    Output ONLY a JSON string array of ALL the speeches of the debate, unless they are boring and not crucial.

    This collection of speeches should be comprehensive and sum up the flow debate, including all key clashes.

    All key quotes attached must be included within the speeches included.

    You may remove parts of speeches that are not notable or interesting enough by marking with ' ... '.
    ALWAYS mark where speeches are editorialised in this way.

    Speeches should be presented in order they are spoken in the debate. When a speech is copied it is copied in full with only clearly marked omissions.

    These speeches will be presented as the main body of an article.

    You should include some speeches from those leading the debate (e.g. the Secretary of State).

    Respond in the following format, with optional brief context for each speech (i.e. 'in response to Speaker X's claim that Y following Z, Speaker A said ...'):

    [
        {
            "speech": "Speech 1",
            "speaker": "Speaker 1"
        },
        {
            "speech": "Speech 2",
            "speaker": "Speaker 2",
            "context": "Context for Speech 2 if necessary"
        },
        ...
    ]

    Speech strings may also include context in square brackets, this should be minimal.

    This should be the ENTIRETY of your response, and should be valid JSON. Do not include any other text or commentary. Do not enclose with ```json or any other code block markers.
    """

    notable_speeches_response_str = prompt_ai(notable_speeches_prompt)
    print("Raw notable speeches response:")
    print(notable_speeches_response_str)
    notable_speeches_response = json.loads(notable_speeches_response_str)

    return notable_speeches_response

def generate_summary(transcript, key_quotes=None, speeches=None):
    # get ai to generate article from key quotes and notable speeches
    article_prompt = f"""
    Here is the original transcript of a Parliamentary debate:

    {transcript}

    Here are the key quotes and notable speeches of a parliamentary debate:

    Key Quotes:

    {json.dumps(key_quotes, indent=4)}

    Notable Speeches:

    {json.dumps(speeches, indent=4)}

    Write an article for Parliament Simple based on these key quotes and notable speeches.
    This article should be of similar size (quite large) of the example you have been given.
    You must include all of the above key quotes and notable speeches.
    """

    article_response_str = prompt_ai(article_prompt)
    print("Raw article response:")
    print(article_response_str)
    article_response = article_response_str.strip() # article response is just a string, not JSON

    return article_response

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        transcript = f.read()

    key_quotes = generate_key_quotes(transcript)

    if (sys.argv[2] == "--sleep"):
        print("Sleeping 60s...")
        time.sleep(60)

    speeches = generate_notable_speeches(transcript, json.dumps(key_quotes, indent=4))

    if (sys.argv[2] == "--sleep"):
        print("Sleeping 60s...")
        time.sleep(60)

    summary = generate_summary(transcript, key_quotes, speeches)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # write to timestamped file in .outputs/*.md
    if not os.path.exists('.outputs'):
        os.makedirs('.outputs')

    output_file_name = f".outputs/{timestamp}.md"

    with open(output_file_name, 'w') as f:
        f.write(summary)

    print(f"Summary written to {output_file_name}")
